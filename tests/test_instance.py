import datetime
import unittest
import boto3

from six.moves import mock

import spotr.instance as instance


class TestInstance(unittest.TestCase):
    def test_find_latest(self):
        mock_config = mock.Mock(instance_tag='spotr')
        fake_client, config = mock_client()
        latest_instance = instance.find_latest(fake_client, mock_config)
        self.assertEqual(latest_instance.id, config['instance_id'])
        self.assertEqual(latest_instance.volume_id, config['volume_id'])
        self.assertEqual(latest_instance.launch_time, config['launch_time'])
        self.assertEqual(latest_instance.ip_address, config['ip_address'])

    def test_find_latest_none_found(self):
        mock_config = mock.Mock(instance_tag='spotr')
        fake_client = mock_client_no_reservations()
        with self.assertRaises(RuntimeError) as context:
            instance.find_latest(fake_client, mock_config)
        self.assertTrue('No running spotr instances found' in repr(context.exception))

    def test_get_by_instance_id(self):
        fake_client, config = mock_client()
        insta = instance.get_by_instance_id(fake_client, config['instance_id'])
        self.assertEqual(insta.id, config['instance_id'])


def mock_client():
    config = {
        'instance_id': 'inst-1234556',
        'volume_id': 'vol-1234556',
        'ip_address': '10.0.0.1',
        'launch_time': datetime.datetime.today()
    }
    fake_client = mock.Mock(boto3.client('ec2'))
    attrs = {
        'describe_instances.return_value': {
            'Reservations': [
                {
                    'Instances': [{
                        'InstanceId': config['instance_id'],
                        'LaunchTime': config['launch_time'],
                        'PublicIpAddress': config['ip_address'],
                        'BlockDeviceMappings': [{
                            'Ebs': {
                                'VolumeId': config['volume_id'],
                            }
                        }]
                    }]
                }
            ]
        }

    }
    fake_client.configure_mock(**attrs)
    return fake_client, config

def mock_client_no_reservations():
    fake_client = mock.Mock(boto3.client('ec2'))
    attrs = {
        'describe_instances.return_value': {
            'Reservations': []
        }

    }
    fake_client.configure_mock(**attrs)
    return fake_client
