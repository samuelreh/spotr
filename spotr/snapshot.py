import boto3
import time
from .client import build as build_client
from .instance import find_latest as find_latest_instance
from .config import Config
from .spin_cursor import spin


def snapshot(args):
    client = build_client(args)
    conf = Config(client, args)
    instance = find_latest_instance(client, conf)

    with spin(">> Creating snapshot for instance: " + str(instance.ip_address)):
        snap = create_and_wait(client, instance.volume_id)
    return snap

def create_and_wait(client, volume_id):
    snapshot = create(client, volume_id)
    wait_for_completion(client, snapshot)
    return snapshot


def create(client, volume_id):
    response = client.create_snapshot(
        Description="Spotr snapshot",
        VolumeId=volume_id)
    return Snapshot(response)


def wait_for_completion(client, snapshot):
    waiter = client.get_waiter('snapshot_completed')
    waiter.wait(
        Filters=[
            {
                'Name': 'snapshot-id',
                'Values': [snapshot.id]
            },
        ]
    )

class Snapshot():
    def __init__(this, response):
        this.state = response['State']
        this.id = response['SnapshotId']

