import unittest
import boto3
from six.moves import mock
from mock import Mock, patch


class TestSnapshot(unittest.TestCase):
    @mock.patch('spotr.instance.find_latest')
    @mock.patch('spotr.client.build')
    def test_snapshot(self, build_client, find_latest_instance):
        attrs = {
            '__dict__': {
                'max_bid': 0.30,
                'ami': 'ami-1234',
                'type': 'px-1-large',
                'key_name': 'key-name',
            }
        }
        args = Mock()
        args.configure_mock(**attrs)

        fake_client = mock.Mock(boto3.client('ec2'))
        attrs = {
            'create_image.return_value': {
                'ImageId': '1234'
            },
            'get_waiter.return_value': mock.Mock(wait=mock.Mock())
        }
        fake_client.configure_mock(**attrs)
        build_client.return_value = fake_client
        find_latest_instance.return_value = Mock(volume_id='123')

        from spotr import snapshot
        response = snapshot.snapshot(args)
        self.assertEqual(response.id, '1234')
