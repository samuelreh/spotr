import unittest
import boto3
from six.moves import mock
from mock import Mock, patch


class TestDestroy(unittest.TestCase):
    @mock.patch('spotr.instance.destroy')
    @mock.patch('spotr.instance.find_latest')
    @mock.patch('spotr.client.build')
    def runTest(self, client_build, find_latest_instance, destroy_instance):
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

        client_build.return_value = Mock(boto3.client('ec2'))
        find_latest_instance.return_value = Mock(volume_id='123')
        destroy_instance.return_value = True
        from spotr import destroy
        response = destroy.destroy(args)
        self.assertEqual(response, True)
