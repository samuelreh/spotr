import ami
import boto3
from botocore.configloader import raw_config_parse


class Config:
    def __init__(self, client, args):
        self._config = raw_config_parse("~/.spotr/config")['config']
        self._config.update({k: v for k, v in vars(args).iteritems() if v})

    def set_az(self, az):
        self._config['az'] = az

    @property
    def ami_tag(self):
        if 'ami_tag' in self._config:
            return self._config['ami_tag']
        else:
            return 'spotr'

    @property
    def instance_tag(self):
        if 'instance_tag' in self._config:
            return self._config['instance_tag']
        else:
            return 'spotr'

    @property
    def type(self):
        return self._config['type']

    @property
    def max_bid(self):
        return float(self._config['max_bid'])

    @property
    def ami(self):
        if 'ami' not in self._config:
            self._config['ami'] = ami.get_by_tag(client, self.ami_tag)
        return self._config['ami']

    @property
    def key_name(self):
        return self._config['key_name']

    @property
    def az(self):
        return self._config['az']
