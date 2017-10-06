import launch
import snapshot
import instance as ec2_instance
import client as boto_client
from config import Config


def destroy(args):
    client = boto_client.build(args)
    conf = Config(client, args)
    instance = ec2_instance.find_latest(client, conf)
    _log_snapshot(instance)
    snap = snapshot.create_and_wait(client, instance.volume_id)
    _log_destroying()
    ec2_instance.destroy(client, instance.id)


def _log_snapshot(instance):
    print(">> Creating snapshot for instance:")
    print(str(instance.ip_address))


def _log_destroying():
    print(">> Destroying instance.")
