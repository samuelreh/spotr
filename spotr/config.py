from .ami import get_by_tag
import six
import os.path
from botocore.configloader import raw_config_parse


class Config:
    def __init__(self, client, args, config_file_path="~/.spotr/config"):
        self.client = client
        config_file_path = os.path.expanduser(config_file_path)
        if os.path.isfile(config_file_path):
            self._config = raw_config_parse(config_file_path)['config']
        else:
            self._config = {}
        self._config.update({k: v for k, v in six.iteritems(vars(args)) if v})

    def map_subnet_id(self, az):
        subnet_var = az + "_subnet_id"
        subnet_id = self._config[subnet_var]
        return subnet_id

    def set_subnet_id(self, subnet_id):
        self._config['subnet_id'] = subnet_id

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
        if 'az' not in self._config:
            self._config['az'] = ''
        return self._config['az']

    @property
    def security_group_id(self):
        return self._config.get('security_group_id')

    @property
    def subnet_id(self):
        if 'subnet_id' not in self._config:
            self._config['subnet_id'] = ''
        return self._config.get('subnet_id')

    @property
    def ebs_optimized(self):
        return bool(self._config['ebs_optimized'])

    @property
    def iam_instance_profile_arn(self):
        return self._config.get('iam_instance_profile_arn')

    @property
    def user_data(self):
        return self._config.get('user_data')

    @property
    def hosted_zone_id(self):
        return self._config.get('hosted_zone_id')

    @property
    def record_name(self):
        return self._config.get('record_name')

    def _get_required(self, key):
        if not self._config.get(key):
            raise RuntimeError("Missing required parameter: {0}".format(key))
        return self._config.get(key)
