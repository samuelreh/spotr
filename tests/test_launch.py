import unittest
import boto3
from six.moves import mock
from mock import Mock, patch


class TestLaunch(unittest.TestCase):
    @mock.patch('spotr.spot_instance.request')
    @mock.patch('spotr.pricing.get_az')
    @mock.patch('spotr.client.build')
    def runTest(self, client_build, pricing_get_az, request):
        print(client_build)
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
        pricing_get_az.return_value = Mock(name='us-east-1a')
        spot_instance = Mock(ip_address='10.0.0.1')
        request.return_value = spot_instance
        from spotr import launch
        response = launch.launch(args)
        self.assertEqual(response, spot_instance)
