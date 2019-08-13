=================================
Tempest integration of CloudKitty
=================================

This project defines a tempest plugin containing tests used to verify the
functionality of a cloudkitty installation. The plugin will automatically load
these tests into tempest.

Dependencies
------------

This plugin tests the CloudKitty API. This supposes that the 'rating' role
exists in your OpenStack installation.

Developers
----------
For more information on cloudkitty, refer to:
https://docs.openstack.org/cloudkitty/latest/

For more information on tempest plugins, refer to:
https://docs.openstack.org/tempest/latest/#using-plugins

Bugs
----
Please report bugs to: https://storyboard.openstack.org/#!/project/890

Installing
----------

Clone this repository and call from the repo::

    $ pip install -e .

Running the tests
-----------------

To run all the tests from this plugin, call from the tempest repo::

    $ cd <Tempest Directory>
    $ tox -e all -- cloudkitty_tempest_plugin

To run a single test case, call with full path, for example::

    $ cd <Tempest Directory>
    $ tox -e all -- cloudkitty_tempest_plugin.tests.api.test_cloudkitty_api.CloudkittyAdminAPITest.test_get_collector_mappings

To retrieve a list of all tempest tests, run::

    $ cd <Tempest Directory>
    $ testr list-tests
