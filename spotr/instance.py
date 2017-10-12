class Instance():
    def __init__(self, response):
        self.id = response['InstanceId']
        self.volume_id = response['BlockDeviceMappings'][0]['Ebs']['VolumeId']
        self.launch_time = response['LaunchTime']
        self.ip_address = response['PublicIpAddress']


class InstanceList():
    def __init__(self, response):
        self.instances = []
        for reservation in response['Reservations']:
            for insta in reservation['Instances']:
                self.instances.append(Instance(insta))

    def latest(self):
        return sorted(self.instances, key=lambda i: i.launch_time)[0]


def find_latest(client, config):
    instance_response = client.describe_instances(
        Filters=[{'Name': 'tag:project', 'Values': [config.instance_tag]}])
    return InstanceList(instance_response).latest()


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
