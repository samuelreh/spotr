import time
import pprint
from .instance import find_latest_list as find_latest_instances
from .client import build as build_client
from .config import Config
from .spin_cursor import spin


def list(args):
    client = build_client(args)
    conf = Config(client, args)
    instances = find_latest_instances(client, conf)

    print(instances.toString())

    return
