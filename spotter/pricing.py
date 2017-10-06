import datetime
import boto3

from functools import partial

from availability_zone import AvailabilityZone


def get_az(client, config):
    zone_names = _get_zone_names(client)
    instance_type = config.type
    max_bid = config.max_bid

    azs = []
    for zone_name in zone_names:
        price_history = _get_price_history(client, zone_name, instance_type)
        az = AvailabilityZone(zone_name, price_history)
        azs.append(az)

    # Sort the AZs by score and return the best one
    score_for_az_func = partial(_score, max_bid)
    sorted_azs = sorted(azs, key=score_for_az_func)

    return sorted_azs[-1]


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


def _score(max_bid, az):
    if az.current_price is None or az.current_price > max_bid:
        return 0

    current_price_s = max_bid - az.current_price
    variance_s = -5 * (az.spot_price_variance * az.spot_price_mean)
    mean_s = 0.5 * (max_bid - az.spot_price_mean)

    return current_price_s + variance_s + mean_s
