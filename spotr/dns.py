import boto3
import functools


def build_client(args):
    if args.region:
        boto3.setup_default_session(region_name=args.region)

    client = functools.partial(boto3.client, 'route53')
    key_id = args.aws_access_key_id
    access_key = args.aws_secret_access_key

    if key_id and access_key:
        return client(
            aws_access_key_id=key_id,
            aws_secret_access_key=access_key)
    else:
        return client()


def set_record(client, instance, conf):
    print("Setting DNS record {} to point to IP address {}...".format(conf.record_name, instance.ip_address))
    client.change_resource_record_sets(
        HostedZoneId=conf.hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': conf.record_name,
                        'Type': 'A',  # We only support A records
                        'TTL': 300,
                        'ResourceRecords': [
                            {'Value': instance.ip_address},
                        ],
                    }
                },
            ]
        }
    )
    print('IP Address: {}'.format(instance.ip_address))

    return
