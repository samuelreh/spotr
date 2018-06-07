import argparse
import sys

from .launch import launch
from .destroy import destroy
from .snapshot import snapshot
from .version import VERSION


parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version=VERSION)
subparsers = parser.add_subparsers()

launch_parser = subparsers.add_parser('launch')
launch_parser.add_argument(
    '--type',
    help='the type of the instance to launch, eg p2.xlarge2')
launch_parser.add_argument(
    '--region',
    help='the region to launch the instance in')
launch_parser.add_argument(
    '--aws-access-key-id',
    help='the access key id to use')
launch_parser.add_argument(
    '--aws-secret-access-key',
    help='the secret access key to use')
launch_parser.add_argument(
    '--max-bid',
    help='the maximum bid price')
launch_parser.add_argument(
    '--ami',
    help='id of ami to use')
launch_parser.add_argument(
    '--ami-tag',
    help='the tag to search for the AMI by')
launch_parser.add_argument(
    '--key-name',
    help='name of the aws key pair to use')
launch_parser.add_argument(
    '--security-group-id',
    help='security group id for the security group to use')
launch_parser.add_argument(
    '--subnet-id',
    help='id of the subnet in which instance needs to be launched')
launch_parser.set_defaults(func=launch)

destroy_parser = subparsers.add_parser('snapshot')
destroy_parser.add_argument(
    '--region',
    help='the region of the launched spotr instance')
destroy_parser.add_argument(
    '--aws-access-key-id',
    help='the access key id to use')
destroy_parser.add_argument(
    '--aws-secret-access-key',
    help='the secret access key to use')
destroy_parser.set_defaults(func=snapshot)

destroy_parser = subparsers.add_parser('destroy')
destroy_parser.add_argument(
    '--region',
    help='the region of the launched spotr instance')
destroy_parser.add_argument(
    '--aws-access-key-id',
    help='the access key id to use')
destroy_parser.add_argument(
    '--aws-secret-access-key',
    help='the secret access key to use')
destroy_parser.set_defaults(func=destroy)


def main():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
