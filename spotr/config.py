from .ami import get_by_tag
import boto3
import six
import os.path
from botocore.configloader import raw_config_parse


class Config:
    def __init__(self, client, args, config_file_path = "~/.spotr/config"):
        self.client = client
        config_file_path = os.path.expanduser(config_file_path)
        if os.path.isfile(config_file_path):
            self._config = raw_config_parse(config_file_path)['config']
        else:
            self._config = {}
        self._config.update({k: v for k, v in six.iteritems(vars(args)) if v})

    def set_az(self, az):
        self._config['az'] = az

    @property
    def ami_tag(self):
        return self._config.get('ami_tag', 'spotr')

    @property
    def instance_tag(self):
        return self._config.get('instance_tag', 'spotr')

    @property
    def type(self):
        return self._get_required('type')

    @property
    def max_bid(self):
        return self._get_required('max_bid')

    @property
    def ami(self):
        if 'ami' not in self._config:
            self._config['ami'] = get_by_tag(self.client, self.ami_tag)
        return self._config['ami']

    @property
    def key_name(self):
        return self._config.get('key_name', 'spotr')

    @property
    def az(self):
        return self._config['az']

    @property
    def security_group_id(self):
        return self._config.get('security_group_id')

    @property
    def subnet_id(self):
        return self._config.get('subnet_id')

    def _get_required(self, key):
        if not self._config.get(key):
            raise RuntimeError("Missing required parameter: {0}".format(key))
        return self._config.get(key)
