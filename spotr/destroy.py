from .snapshot import create_and_wait
from .instance import find_latest as find_latest_instance
from .instance import destroy as destroy_instance
from .client import build as build_client
from .config import Config


def destroy(args):
    client = build_client(args)
    conf = Config(client, args)
    instance = find_latest_instance(client, conf)
    _log_snapshot(instance)
    snap = create_and_wait(client, instance.volume_id)
    _log_destroying()
    return destroy_instance(client, instance.id)


def _log_snapshot(instance):
    print(">> Creating snapshot for instance:")
    print(str(instance.ip_address))


def _log_destroying():
    print(">> Destroying instance.")
