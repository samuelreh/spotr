import ami
import boto3
from botocore.configloader import raw_config_parse


class Config:
    def __init__(self, client, args):
        self.client = client
        self._config = raw_config_parse("~/.spotr/config")['config']
        self._config.update({k: v for k, v in vars(args).iteritems() if v})

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
        return self._config.get('max_bid', None)

    @property
    def ami(self):
        if 'ami' not in self._config:
            self._config['ami'] = ami.get_by_tag(self.client, self.ami_tag)
        return self._config['ami']

    @property
    def key_name(self):
        return self._config['key_name']

    @property
    def az(self):
        return self._config['az']
