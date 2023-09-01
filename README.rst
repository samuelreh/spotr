===============================
Spotr
===============================

Spotr simplifies launching, snapshotting and destroying AWS spot instances.

It's designed for users wanting to use a spot instance as a development box, and persist the state in between sessions.

Quick Start
-----------
First, install the library from pip or clone this git repository and install locally:

.. code-block:: sh

  $ pip install spotr

.. code-block:: sh

    $ pip install -e .

python -m build
Next, set up credentials and region (in ``~/.aws/config``):

.. code-block:: ini

    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET
    region=us-west-1

Then, launch an instance using:

.. code-block:: sh

  $ spotr launch --type p2.xlarge --max-bid .30 --ami ami-4bf20033

List your running spotr instances with:

.. code-block:: sh

  $ spotr list

When you're done working, you can save the current state (take a snapshot) using:

.. code-block:: sh

  $ spotr snapshot

And then to terminate the instance:

.. code-block:: sh

  $ spotr destroy
  
Next time you launch an instance, leave out the `--ami` tag and you'll restore the most recent snapshot taken with spotr.

.. code-block:: sh

  $ spotr launch --type p2.xlarge --max-bid .30

You can specify default configurations in ``~/.spotr/config``:

.. code-block:: ini

    [config]
    max_bid=.30
    type=p2.xlarge
    ebs_optimized=true
    security_group_id=sg-XXXXXXXXXXXXXXX
    ami=ami-XXXXXXXXXXXXXXXX
    us-west-2a_subnet_id=subnet-XXXXXXXX
    us-west-2b_subnet_id=subnet-XXXXXXXX
    us-west-2c_subnet_id=subnet-XXXXXXXX
    us-west-2d_subnet_id=subnet-XXXXXXXX
    iam_instance_profile_arn=arn:aws:iam::XXXXXXXX:instance-profile/instance-profile-role
    hosted_zone_id=XXXXXXXXXXX
    record_name=subdomain.example.com
    user_data=#cloud-config
        runcmd:
            - [ sh, -c, "/bin/bash /opt/dosomethinguseful.sh" ]         
