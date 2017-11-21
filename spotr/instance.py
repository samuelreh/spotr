class Instance():
    def __init__(self, response):
        self.id = response['InstanceId']
        self.volume_id = response['BlockDeviceMappings'][0]['Ebs']['VolumeId']
        self.launch_time = response['LaunchTime']
        self.ip_address = response['PublicIpAddress']
        self.security_groups = response['SecurityGroups']

    @property
    def has_security_groups(self):
        return not len(self.security_groups) == 0


class InstanceList():
    def __init__(self, response):
        self.instances = []
        for reservation in response['Reservations']:
            for insta in reservation['Instances']:
                if 'PublicIpAddress' in insta:
                    self.instances.append(Instance(insta))

    def latest(self):
        return sorted(self.instances, key=lambda i: i.launch_time)[0]

    def __len__(self):
        return len(self.instances)


def find_latest(client, config):
    instance_response = client.describe_instances(
        Filters=[{'Name': 'tag:project', 'Values': [config.instance_tag]}])
    instance_list = InstanceList(instance_response)

    if len(instance_list) == 0:
        raise RuntimeError("No running spotr instances found")

    return instance_list.latest()


def destroy(client, instance_id):
    return client.terminate_instances(InstanceIds=[instance_id])


def tag(client, instance_id, config):
    return client.create_tags(
        Resources=[instance_id],
        Tags=[{'Key': 'project', 'Value': config.instance_tag, }]
    )


def get_by_instance_id(client, instance_id):
    response = client.describe_instances(InstanceIds=[instance_id])
    return Instance(response['Reservations'][0]['Instances'][0])

def open_port(client, instance, port):
    if len(instance.security_groups) == 0:
        raise RuntimeError("No security groups associated with instance")
    group_id = instance.security_groups[0].get('GroupId')
    group = client.describe_security_groups(GroupIds=[group_id])['SecurityGroups'][0]
    matching_rules = (x for x in group['IpPermissions'] if x.get('FromPort') == port and x.get('ToPort') == port)
    first_matching_rule = next(matching_rules, None)
    if not first_matching_rule:
        client.authorize_security_group_ingress(
            GroupId = group_id,
            IpPermissions=[
                {
                    'FromPort': port,
                    'IpProtocol': 'TCP',
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0',
                            'Description': 'Spotr Jupyter Port'
                        },
                    ],
                    'Ipv6Ranges': [
                        {
                            'CidrIpv6': '::/0',
                            'Description': 'Spotr Jupyter Port'
                        },
                    ],
                    'ToPort': port
                }
            ]
        )
    return True
