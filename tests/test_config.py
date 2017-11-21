import datetime
import unittest
import boto3

from six.moves import mock

from spotr.config import Config


class TestConfig(unittest.TestCase):
    def test_ami_tag(self):
        args = mock_args({'ami_tag': 'my_tag'})
        conf = Config(mock_client(), args)
        self.assertEqual(conf.ami_tag, 'my_tag')

    def test_default_ami_tag(self):
        args = mock_args({})
        conf = Config(mock_client(), args)
        self.assertEqual(conf.ami_tag, 'spotr')

    def test_no_config_file(self):
        args = mock_args({})
        conf = Config(mock_client(), args, "./non-existent-config")
        self.assertEqual(conf.key_name, 'spotr')

    def test_config_file(self):
        args = mock_args({})
        conf = Config(mock_client(), args, "./tests/fixtures/config")
        self.assertEqual(conf.key_name, 'test_key_name')


def mock_client():
    fake_client = mock.Mock(boto3.client('ec2'))
    attrs = {}
    fake_client.configure_mock(**attrs)
    return fake_client


def mock_args(arg_dict):
    config_mock = mock.Mock()
    attrs = {'__dict__': arg_dict}
    config_mock.configure_mock(**attrs)
    return config_mock
