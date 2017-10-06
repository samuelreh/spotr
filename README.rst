===============================
Spotr
===============================

Spotr simplifies launching and destroying an AWS spot instance.

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

Then, from a Python interpreter:

.. code-block:: sh

  $ spotr launch --type p2.xlarge --ami ami-4bf20033 --max-bid .030 --key-name aws-key-fast-ai

When you're done with the instance, create a snapshot and detroy it with:

.. code-block:: sh

  $ spotr destroy
