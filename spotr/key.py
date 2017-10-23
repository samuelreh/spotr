import os

def find_or_create(client, conf_key_name):
    path = os.path.expanduser('~/.ssh/' + conf_key_name + '.pem')
    if not os.path.exists(path):
        response = client.create_key_pair(KeyName=conf_key_name)

        with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT, 0o400), 'w') as handle:
            handle.write(response['KeyMaterial'])

    return path
