import unittest
import mock
import boto3
from mock import Mock, patch

from spotr.launch import launch


class TestLaunch(unittest.TestCase):
    @patch('spotr.spot_instance.request')
    @patch('spotr.pricing.get_az')
    @patch('spotr.client.build')
    def runTest(self, client_build, pricing_get_az, spot_request):
        attrs = {
            '__dict__': {
                'max_bid': 0.30,
                'ami': 'ami-1234',
                'ami_tag': 'spotr',
                'type': 'px-1-large',
                'key_name': 'key-name',
            }
        }
        args = Mock()
        args.configure_mock(**attrs)

        client_build.return_value = Mock(boto3.client('ec2'))
        pricing_get_az.return_value = Mock(name='us-east-1a')
        spot_request.return_value = Mock(ip='10.0.0.1')
        response = launch(args)
