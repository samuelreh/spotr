import pricing
import spot_instance
import client as boto_client
from config import Config


def launch(args):
    client = boto_client.build(args)
    conf = Config(client, args)

    az = pricing.get_az(client, conf)
    _log_launching(az)
    conf.set_az(az.zone_name)

    instance = spot_instance.request(client, conf)
    _log_instance_creation(instance, conf)


def _log_launching(az):
    print(">> Launching instance in:")
    print(str(az))


def _log_instance_creation(instance, conf):
    print(">> Instance launched, connect with:")
    ip = str(instance.ip_address)
    key_path = "~/.ssh/" + conf.key_name + ".pem"
    print("ssh -i " + key_path + " ubuntu@" + ip)
