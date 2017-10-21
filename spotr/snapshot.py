import boto3
import time


class Snapshot():
    def __init__(this, response):
        this.state = response['State']
        this.id = response['SnapshotId']


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
