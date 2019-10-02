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
import testtools

from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from cloudkitty_tempest_plugin.tests.api import base


class CloudkittyAdminAPITest(base.BaseRatingTest):
    api_version = 'v1'
    credentials = ['admin']

    @decorators.idempotent_id('9c1d4c27-6e7c-42d7-b663-d88f097b7131')
    def test_get_collector_mappings(self):
        self.rating_client.get_collector_mappings()

    def _find_item(self, haystack, needle, key, assert_method):
        found = False
        for item in haystack:
            try:
                if item[key] == needle:
                    found = True
            except KeyError:
                continue
        assert_method(found)

    @decorators.idempotent_id('af902c86-6022-4b94-a716-ec7932d5ae78')
    def test_create_get_delete_collector_mapping(self):
        mapping = self.rating_client.create_collector_mapping(
            collector=data_utils.rand_name('gnocchi'),
            service=data_utils.rand_name('compute'),
        )
        self._created_resources['collector_mapping'].append(
            mapping['service'],
        )
        mappings = self.rating_client.get_collector_mappings()
        self._find_item(mappings['mappings'],
                        mapping['service'],
                        'service',
                        self.assertTrue)
        self.rating_client.delete_collector_mapping(mapping['service'])
        mappings = self.rating_client.get_collector_mappings()
        self._find_item(mappings['mappings'],
                        mapping['service'],
                        'service',
                        self.assertFalse)

    @decorators.idempotent_id('3fd83647-3058-4450-9588-a528557585c5')
    def test_get_collector_state(self):
        collector = self.rating_client.get_collector_state(
            collector=data_utils.rand_name('gnocchi'),
        )
        self.assertFalse(collector['enabled'])

    @decorators.idempotent_id('71131104-fdae-43ec-9bed-c8d1d5ba7eb0')
    def test_set_collector_state(self):
        collector_name = data_utils.rand_name('gnocchi')
        self.rating_client.set_collector_state(
            collector=collector_name,
            enabled=True,
        )
        collector = self.rating_client.get_collector_state(collector_name)
        self.assertTrue(collector['enabled'])
        self.rating_client.set_collector_state(
            collector=collector_name,
            enabled=False,
        )
        collector = self.rating_client.get_collector_state(collector_name)
        self.assertFalse(collector['enabled'])

    @decorators.idempotent_id('fba44b6a-6ca4-4155-b5c6-c4eb2465e4fb')
    def test_get_rating_modules(self):
        modules = self.rating_client.get_rating_module()
        self._find_item(modules['modules'],
                        'hashmap',
                        'module_id',
                        self.assertTrue)
        self._find_item(modules['modules'],
                        'pyscripts',
                        'module_id',
                        self.assertTrue)
        self._find_item(modules['modules'],
                        'noop',
                        'module_id',
                        self.assertTrue)
        self.assertEqual(
            'hashmap',
            self.rating_client.get_rating_module('hashmap')['module_id'],
        )
        self.assertEqual(
            'pyscripts',
            self.rating_client.get_rating_module('pyscripts')['module_id'],
        )

    @decorators.idempotent_id('7fc9e020-9547-4a66-a691-94cab7181358')
    def test_update_rating_module(self):
        self.rating_client.update_rating_module('hashmap', enabled=True)
        module = self.rating_client.get_rating_module('hashmap')
        self.assertTrue(module['enabled'])
        self.rating_client.update_rating_module('hashmap', enabled=False)
        module = self.rating_client.get_rating_module('hashmap')
        self.assertFalse(module['enabled'])

    @decorators.idempotent_id('daeef22b-d52d-4e89-abb0-ae492e4648d4')
    def test_reload_rating_modules(self):
        self.rating_client.reload_rating_modules()

    @decorators.idempotent_id('e439019e-9e8a-4bcd-aa83-95bdba6e6115')
    def test_get_rated_tenants(self):
        raise testtools.TestCase.skipException('No data pushed to backend.')
        rated_tenants = self.rating_client.get_rated_tenants()['body']
        self.assertGreater(len(rated_tenants), 0)


class CloudkittyPrimaryAPITest(base.BaseRatingTest):
    api_version = 'v1'
    credentials = ['primary']

    @decorators.idempotent_id('3285bccf-d043-4ad1-b64f-af4db8317cf9')
    def test_get_config(self):
        self.rating_client.get_config()

    @decorators.idempotent_id('43b03099-0493-4291-9749-85cd8d512811')
    def test_get_metrics(self):
        self.rating_client.get_metric()

    @decorators.idempotent_id('64ecae87-0138-41bd-829f-91302dae7802')
    def test_get_metric(self):
        self.rating_client.get_metric('instance')

    @decorators.idempotent_id('cccbff8a-24b2-4251-8f7b-ea941d048b9d')
    def test_report_summary(self):
        self.rating_client.get_report_summary()

    @decorators.idempotent_id('2492dfd7-0688-4957-93ac-8c91933c28f5')
    def test_report_total(self):
        self.rating_client.get_report_total()

    @decorators.idempotent_id('e233139b-3c75-4b70-b1f5-0776ef32c916')
    def test_get_storage_dataframes(self):
        self.rating_client.get_storage_dataframes()
