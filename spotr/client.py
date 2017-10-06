import boto3

from functools import partial


def build(args):
    if args.region:
        boto3.setup_default_session(region_name=args.region)

    client = partial(boto3.client, 'ec2')
    key_id = args.aws_access_key_id
    access_key = args.aws_secret_access_key

    if key_id and access_key:
        return client(
            aws_access_key_id=key_id,
            aws_secret_access_key=access_key)
    else:
        return client()
