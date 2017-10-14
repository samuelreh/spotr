===============================
Spotr
===============================

Spotr simplifies launching, snapshotting and destroying AWS spot instances.

It's designed for users wanting to use a spot instance as a development box, and persist the state in between sessions.

Quick Start
-----------
First, install the library and set a default region:

.. code-block:: sh

    $ pip install spotr

Next, set up credentials and region (in e.g. ``~/.aws/config``):

.. code-block:: ini

    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET
    region=us-west-1

Then, launch an instance using:

.. code-block:: sh

  $ spotr launch --type p2.xlarge --ami ami-4bf20033 --max-bid .30 --key-name aws-key-fast-ai

When you're done with the instance, use the destroy command to create a snapshot and destroy the instance:

.. code-block:: sh

  $ spotr destroy

You can specify default configurations in ``~/.spotr/config``:

.. code-block:: ini

    [config]
    key_name=aws-key-fast-ai
    max_bid=.030
    ami-tag=spotr
    type=p2.xlarge
