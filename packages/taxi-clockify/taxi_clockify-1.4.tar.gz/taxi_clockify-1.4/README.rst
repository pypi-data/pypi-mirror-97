Clockify backend for Taxi
=========================

This is the Clockify backend for `Taxi <https://github.com/sephii/taxi>`_. It
exposes the ``clockify`` protocol to push entries and fetch projects and
activities from Clockify.

Installation
------------

    taxi plugin install clockify

Usage
-----

In your ``.taxirc`` file, use the ``clockify`` protocol for your backend and set
the `token` in the query string. For example::

    [backends]
    clockify = clockify://?token=abcdefghijklmnopqr

If you have multiple workspaces, add the workspace in the URL::

    [backends]
    clockify = clockify://?token=abcdefghijklmnopqr&workspace=ff00acab01

Contributing
------------

To setup a development environment, create a virtual environment and run the
following command in it::

    pip install -e .

To use a specific version of Taxi, eg. if you need to also make changes to Taxi,
install it in the virtual environment in editable mode::

    pip install -e /path/to/taxi
