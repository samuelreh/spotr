def get_by_tag(client, tag):
    response = client.describe_images(
        Filters=[{'Name': 'tag:project', 'Values': [tag]}]
    )
    return response['Images'][0]['ImageId']
