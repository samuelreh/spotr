import datetime
import unittest
import mock
import boto3
from mock import Mock, patch

import spotr.instance as instance


class TestInstanceFindLatest(unittest.TestCase):
    def runTest(self):
        mock_config = Mock(ami_tag='spotr')
        fake_client, config = mock_client()
        latest_instance = instance.find_latest(fake_client, mock_config)
        self.assertEqual(latest_instance.id, config['instance_id'])
        self.assertEqual(latest_instance.volume_id, config['volume_id'])
        self.assertEqual(latest_instance.launch_time, config['launch_time'])
        self.assertEqual(latest_instance.ip_address, config['ip_address'])


class TestInstanceGetByInstanceId(unittest.TestCase):
    def runTest(self):
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
    fake_client = Mock(boto3.client('ec2'))
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
