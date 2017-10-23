import random


def request(client, config, tag, get_by_instance_id):
    request_id = _perform_request(client, config)
    _wait_until_completed(client, request_id)
    instance_id = _get_status(client, request_id)
    tag(client, instance_id, config)
    _wait_until_running(client, instance_id)
    return get_by_instance_id(client, instance_id)


def _perform_request(client, config):
    random_id = str(random.random() * 1000)
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
            }
        }
    )
    return response.get('SpotInstanceRequests')[0].get('SpotInstanceRequestId')


def _wait_until_completed(client, request_id):
    waiter = client.get_waiter('spot_instance_request_fulfilled')
    return waiter.wait(SpotInstanceRequestIds=[request_id])


def _get_status(client, request_id):
    response = client.describe_spot_instance_requests(
        SpotInstanceRequestIds=[request_id],
    )
    return response.get('SpotInstanceRequests')[0].get('InstanceId')


def _wait_until_running(client, instance_id):
    waiter = client.get_waiter('instance_running')
    return waiter.wait(InstanceIds=[instance_id])
