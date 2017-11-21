def get_by_tag(client, tag):
    response = client.describe_images(
        Filters=[{'Name': 'tag:project', 'Values': [tag]}]
    )
    images = response['Images']
    if len(images) == 0:
        raise RuntimeError("No saved images with tag: '{0}'".format(tag))
    return images[0]['ImageId']
