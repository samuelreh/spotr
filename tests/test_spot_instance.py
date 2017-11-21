import unittest
import boto3
from six.moves import mock

from spotr.spot_instance import request

class TestSpotInstance(unittest.TestCase):
    def runTest(self):
        config = mock.Mock(
            max_bid=0.30,
            ami='1234',
            key_name='test_ssh_key',
            instance_type='p2.xlarge',
            az='us-west-2a',
        )
        fake_client = mock.Mock(boto3.client('ec2'))
        attrs = {
            'request_spot_instances.return_value': {
                'SpotInstanceRequests': [
                    {'SpotInstanceRequestId': '123456'}
                ]
            },
            'describe_spot_instance_requests.return_value': {
                'SpotInstanceRequests': [
                    {'InstanceId': '123456', 'Status': { 'Code': 'fulfilled' } }
                ]
            }

        }
        fake_client.configure_mock(**attrs)

        instance = mock.Mock(has_security_groups=True)
        tag = mock.Mock()
        get_by_instance_id = mock.Mock(return_value=instance)
        open_port = mock.Mock(return_value=True)
        response = request(fake_client, config, tag, get_by_instance_id, open_port)
        self.assertEqual(response, instance)
