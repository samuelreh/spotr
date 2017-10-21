from .ami import get_by_tag
import boto3
import six
from botocore.configloader import raw_config_parse


class Config:
    def __init__(self, client, args):
        self.client = client
        self._config = raw_config_parse("~/.spotr/config")['config']
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
        return self._config['type']

    @property
    def max_bid(self):
        return self._config.get('max_bid')

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
