# -*- coding: utf-8 -*-
# Copyright 2017 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
import six

from tempest import config
from tempest.lib import exceptions
import tempest.test

from cloudkitty_tempest_plugin.services import client

CONF = config.CONF


def skipIf(flag, reason):
    def decorator(f):
        def wrapper(self, *args, **kwargs):
            if getattr(self, flag):
                self.skipTest(reason)
            else:
                f(self, *args, **kwargs)
        return wrapper
    return decorator


class BaseRatingTest(tempest.test.BaseTestCase):
    """Base test class for all Rating API tests."""
    client_manager = client.Manager

    @classmethod
    def setup_clients(cls):
        super(BaseRatingTest, cls).setup_clients()
        os_var = 'os_{}'.format(cls.credentials[0])
        cls.rating_client = getattr(cls, os_var).get_rating_client(
            getattr(cls, 'api_version'))

    @classmethod
    def setup_credentials(cls):
        super(BaseRatingTest, cls).setup_credentials()
        os_var = 'os_{}'.format(cls.credentials[0])
        project_id = getattr(cls, os_var).credentials.project_id
        cls.skip_rating_tests = False
        try:
            cls.custom_identity_client = client.CustomIdentityClient()
            cls.custom_identity_client.enable_rating(project_id)
        except Exception:
            cls.skip_rating_tests = True

    @classmethod
    def resource_setup(cls):
        super(BaseRatingTest, cls).resource_setup()
        cls._created_resources = {
            'collector_mapping': list(),
            'hashmap_service': list(),
            'hashmap_field': list(),
            'hashmap_mapping': list(),
            'hashmap_group': list(),
            'hashmap_threshold': list(),
            'pyscript': list(),
        }

    @classmethod
    def resource_cleanup(cls):
        super(BaseRatingTest, cls).resource_cleanup()
        for method, item_ids in six.iteritems(cls._created_resources):
            delete_method = 'delete_' + method
            delete_method = getattr(cls.rating_client, delete_method)
            for item_id in item_ids:
                try:
                    delete_method(item_id)
                except (exceptions.NotFound,
                        exceptions.UnexpectedResponseCode):
                    pass
