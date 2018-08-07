import random
import time


def request(client, config, tag, get_by_instance_id, open_port):
    request_id = _perform_request(client, config)
    time.sleep(2)

    request = _describe_request(client, request_id)
    if request.status_code == 'price-too-low':
        raise RuntimeError(request.status_message)

    _wait_until_completed(client, request_id)
    request = _describe_request(client, request_id)

    tag(client, request.instance_id, config)
    _wait_until_running(client, request.instance_id)

    instance = get_by_instance_id(client, request.instance_id)
    if instance.has_security_groups:
        open_port(client, instance, 8888)
    return instance


def _perform_request(client, config):
    random_id = str(random.random() * 1000)
    if config.security_group_id is None:
        security_group_ids = []
    else:
	security_group_ids = [config.security_group_id]
    response = client.request_spot_instances(
        SpotPrice=config.max_bid,
        ClientToken=random_id,
        InstanceCount=1,
        Type='one-time',
        LaunchSpecification={
            'ImageId': config.ami,
            'KeyName': config.key_name,
            'InstanceType': config.type,
            'Placement': {
                'AvailabilityZone': config.az,
            },
            'SecurityGroupIds': security_group_ids,
	    'SubnetId':config.subnet_id
        }
    )
    return response.get('SpotInstanceRequests')[0].get('SpotInstanceRequestId')


def _wait_until_completed(client, request_id):
    waiter = client.get_waiter('spot_instance_request_fulfilled')
    return waiter.wait(SpotInstanceRequestIds=[request_id])


def _describe_request(client, request_id):
    response = client.describe_spot_instance_requests(
        SpotInstanceRequestIds=[request_id],
    )
    return SpotInstanceRequest(response.get('SpotInstanceRequests')[0])


def _wait_until_running(client, instance_id):
    waiter = client.get_waiter('instance_running')
    return waiter.wait(InstanceIds=[instance_id])

class SpotInstanceRequest():
    def __init__(this, response):
        this.instance_id = response.get('InstanceId')
        this.status_code = response.get('Status').get('Code')
        this.status_message = response.get('Status').get('Message')
