from .pricing import get_az
from .spot_instance import request
from .instance import tag as tag_instance
from .instance import get_by_instance_id
from .client import build as build_client
from .config import Config


def launch(args):
    client = build_client(args)
    conf = Config(client, args)

    az = get_az(client, conf)
    _log_launching(az)
    conf.set_az(az.zone_name)

    inst = request(client, conf, tag_instance, get_by_instance_id)
    _log_instance_creation(inst, conf)


def _log_launching(az):
    print(">> Launching instance in:")
    print(str(az))


def _log_instance_creation(instance, conf):
    print(">> Instance launched, connect with:")
    ip = str(instance.ip_address)
    key_path = "~/.ssh/" + conf.key_name + ".pem"
    print("ssh -i " + key_path + " ubuntu@" + ip)
