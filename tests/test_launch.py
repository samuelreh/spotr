import unittest
import mock
import boto3
from mock import Mock, patch

from spotter.launch import launch


class TestLaunch(unittest.TestCase):
    @patch('spotter.spot_instance.request')
    @patch('spotter.pricing.get_az')
    @patch('spotter.client.build')
    def runTest(self, client_build, pricing_get_az, spot_request):
        attrs = {
            '__dict__': {
                'max_bid': 0.30,
                'ami': 'ami-1234',
                'ami_tag': 'spotter',
                'type': 'px-1-large',
                'security_group_id': 'sg-1234',
                'key_name': 'key-name',
            }
        }
        args = Mock()
        args.configure_mock(**attrs)

        client_build.return_value = Mock(boto3.client('ec2'))
        pricing_get_az.return_value = Mock(name='us-east-1a')
        spot_request.return_value = Mock(ip='10.0.0.1')
        response = launch(args)
