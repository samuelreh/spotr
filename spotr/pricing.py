import datetime
import sys
import boto3

from .availability_zone import AvailabilityZone


def get_az(client, config):
    zone_names = _get_zone_names(client)
    instance_type = config.type

    azs = []
    for zone_name in zone_names:
        price_history = _get_price_history(client, zone_name, instance_type)
        az = AvailabilityZone(zone_name, price_history)
        azs.append(az)

    return sorted(azs, key=_score)[0]


def _get_zone_names(client):
    zone_names = []
    for zone in client.describe_availability_zones()['AvailabilityZones']:
        if zone['State'] == 'available':
            zone_names.append(zone['ZoneName'])
    return zone_names


def _get_price_history(client, zone_name, instance_type):
    response = client.describe_spot_price_history(
        DryRun=False,
        StartTime=datetime.datetime.now() - datetime.timedelta(days=7),
        EndTime=datetime.datetime.now(),
        InstanceTypes=[instance_type],
        AvailabilityZone=zone_name,
        ProductDescriptions=['Linux/UNIX'])
    return response.get('SpotPriceHistory', [])


def _score(az):
    return az.current_price or sys.maxsize
