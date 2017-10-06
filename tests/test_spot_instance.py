import unittest
import mock
import boto3
from mock import Mock, patch

from spotr.spot_instance import request


class TestSpotInstance(unittest.TestCase):
    @patch('spotr.instance.get_by_instance_id')
    def runTest(self, test_patch):
        mock = Mock()
        test_patch.return_value = mock
        config = Mock(
            max_bid=0.30,
            ami='1234',
            key_name='test_ssh_key',
            instance_type='p2.xlarge',
            az='us-west-2a',
        )
        fake_client = Mock(boto3.client('ec2'))
        attrs = {
            'request_spot_instances.return_value': {
                'SpotInstanceRequests': [
                    {'SpotInstanceRequestId': '123456'}
                ]
            },
            'describe_spot_instance_requests.return_value': {
                'SpotInstanceRequests': [
                    {'InstanceId': '123456'}
                ]
            }

        }
        fake_client.configure_mock(**attrs)
        response = request(fake_client, config)
        self.assertEqual(response, mock)
