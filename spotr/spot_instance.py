import time
import random

import instance


def request(client, config):
    request_id = _perform_request(client, config)
    _wait_until_completed(client, request_id)
    instance_id = _get_status(client, request_id)
    instance.tag(client, instance_id, config)
    return instance.get_by_instance_id(client, instance_id)


def _perform_request(client, config):
    random_id = str(random.random() * 1000)
    response = client.request_spot_instances(
        SpotPrice=str(config.max_bid),
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
            'EbsOptimized': False
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
