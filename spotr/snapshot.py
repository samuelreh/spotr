import boto3
import time
from .client import build as build_client
from .instance import find_latest as find_latest_instance
from .instance import tag
from .config import Config
from .spin_cursor import spin


def snapshot(args):
    client = build_client(args)
    conf = Config(client, args)
    instance = find_latest_instance(client, conf)

    with spin(">> Creating snapshot for instance: " + str(instance.ip_address)):
        snap = create_and_wait(client, instance, conf)

    return snap

def create_and_wait(client, instance, conf):
    image = create(client, instance)
    tag(client, image.id, conf)
    wait_for_completion(client, image)
    return image


def create(client, instance):
    now = time.strftime("%Y-%m-%d %H-%M")
    response = client.create_image(
        Name=("Spotr image {0}".format(now)),
        Description="Spotr image",
        InstanceId=instance.id)
    return Snapshot(response)


def wait_for_completion(client, image):
    waiter = client.get_waiter('image_available')
    waiter.wait(
        Filters=[
            {
                'Name': 'image-id',
                'Values': [image.id]
            },
        ]
    )

class Snapshot():
    def __init__(this, response):
        this.id = response['ImageId']
