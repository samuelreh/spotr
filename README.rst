===============================
Spotter
===============================

Spotter simplifies launching and destroying an AWS spot instance.

Quick Start
-----------
First, install the library and set a default region:

.. code-block:: sh

    $ pip install spotter

Next, set up credentials (in e.g. ``~/.aws/credentials``):

.. code-block:: ini

    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET

Then, set up a default region (in e.g. ``~/.aws/config``):

.. code-block:: ini

    [default]
    region=us-east-1

Then, from a Python interpreter:

.. code-block:: sh

  $ spotter launch --type p2.xlarge --ami ami-4bf20033

When you're done with the instance, create a snapshot and detroy it with:

.. code-block:: sh

  $ spotter destroy
