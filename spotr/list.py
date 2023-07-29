from .instance import find_instances
from .client import build as build_client
from .config import Config
from .spin_cursor import spin


def list_instances(args):
    client = build_client(args)
    conf = Config(client, args)
    with spin("Searching for instances..."):
        instances = find_instances(client, conf)
    print('\nFound {} instances'.format(len(instances)))
    if instances:
        for instance in instances:
            print('Instance ID: {}'.format(instance.id))
            print('IP Address: {}'.format(instance.ip_address))
            print('Launch Time: {}'.format(instance.launch_time))
            print('Security Groups: {}'.format(instance.security_groups))
    if not instances:
        print('No instances found')

    return
