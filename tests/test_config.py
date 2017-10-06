import datetime
import unittest
import mock
import boto3
from mock import Mock, patch

from spotr.config import Config 


class TestConfig(unittest.TestCase):
    def test_ami_tag(self):
        args = mock_args({ 'ami_tag': 'my_tag', })
        conf = Config(mock_client(), args)
        self.assertEqual(conf.ami_tag, 'my_tag')

    def test_default_ami_tag(self):
        args = mock_args({})
        conf = Config(mock_client(), args)
        self.assertEqual(conf.ami_tag, 'spotr')


def mock_client():
    fake_client = Mock(boto3.client('ec2'))
    attrs = {}
    fake_client.configure_mock(**attrs)
    return fake_client


def mock_args(arg_dict):
    mock = Mock()
    attrs = {'__dict__': arg_dict}
    mock.configure_mock(**attrs)
    return mock
