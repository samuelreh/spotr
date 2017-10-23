import time
from .snapshot import create_and_wait
from .instance import find_latest as find_latest_instance
from .instance import destroy as destroy_instance
from .client import build as build_client
from .config import Config
from .spin_cursor import spin


def destroy(args):
    client = build_client(args)
    conf = Config(client, args)
    instance = find_latest_instance(client, conf)

    with spin(">> Creating snapshot for instance: " + str(instance.ip_address)):
        snap = create_and_wait(client, instance.volume_id)
    with spin(">> Destroying instance."):
        destroyed = destroy_instance(client, instance.id)
    return destroyed
