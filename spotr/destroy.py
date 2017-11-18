import time
from .instance import find_latest as find_latest_instance
from .instance import destroy as destroy_instance
from .client import build as build_client
from .config import Config
from .spin_cursor import spin


def destroy(args):
    client = build_client(args)
    conf = Config(client, args)
    instance = find_latest_instance(client, conf)

    with spin(">> Destroying instance."):
        destroyed = destroy_instance(client, instance.id)

    _log_instance_destroyed(instance)

    return destroyed

def _log_instance_destroyed(instance):
    print(">> Instance {0} destroyed".format(instance.id))
