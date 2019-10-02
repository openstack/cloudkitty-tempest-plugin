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
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from cloudkitty_tempest_plugin.tests.api import base


class CloudkittyHashmapAPITest(base.BaseRatingTest):
    api_version = 'v1'
    credentials = ['admin']

    @decorators.idempotent_id('7037a3f8-b462-4243-a0bc-ffa3b4700397')
    def test_get_hashmap_rating_types(self):
        self.rating_client.get_hashmap_mapping_types()

    def _setup_dummy_service(self):
        service = self.rating_client.create_hashmap_service(
            data_utils.rand_name('service'),
        )
        self._created_resources['hashmap_service'].append(
            service['service_id'])
        return service['service_id']

    @decorators.idempotent_id('9e968284-7209-46e1-9742-4882b6e2cf2f')
    def test_create_delete_hashmap_service(self):
        service_id = self._setup_dummy_service()
        self.rating_client.delete_hashmap_service(service_id)

    @decorators.idempotent_id('9e9a67d1-e53d-46cf-8e13-8a332c40c32f')
    def test_get_hashmap_services(self):
        self.rating_client.get_hashmap_service()

    @decorators.idempotent_id('6c4260c0-8701-4959-b00e-4789d31715a7')
    def test_get_hashmap_service(self):
        service_id = self._setup_dummy_service()
        self.rating_client.get_hashmap_service(service_id=service_id)

    def _setup_dummy_fields(self, service_id):
        field_ids = list()
        for i in range(3):
            field = self.rating_client.create_hashmap_field(
                data_utils.rand_name('hashmap_field'),
                service_id,
            )
            field_ids.append(field['field_id'])
            self._created_resources['hashmap_field'].append(field['field_id'])
        return field_ids

    @decorators.idempotent_id('974669f9-392e-4aec-8e15-d24db23f08d4')
    def test_create_delete_hashmap_field(self):
        service_id = self._setup_dummy_service()
        field_ids = self._setup_dummy_fields(service_id)
        for field_id in field_ids:
            self.rating_client.delete_hashmap_field(field_id)
        self.rating_client.delete_hashmap_service(service_id)

    @decorators.idempotent_id('9ae98590-ff55-47f9-885e-baa4da1957d1')
    def test_get_hashmap_field(self):
        service_id = self._setup_dummy_service()
        self._setup_dummy_fields(service_id)
        fields = self.rating_client.get_hashmap_fields(service_id)
        for field in fields['fields']:
            field_info = self.rating_client.get_hashmap_field(
                field['field_id'],
            )
            self.assertEqual(field_info['field_id'], field['field_id'])
            self.assertEqual(field_info['service_id'], field['service_id'])
            self.assertEqual(field_info['name'], field['name'])

    def _find_item(self, haystack, needle, key):
        found = False
        for item in haystack:
            try:
                if item[key] == needle:
                    found = True
            except KeyError:
                continue
        self.assertTrue(found)

    @decorators.idempotent_id('4deb6914-7ba0-4219-a119-61b39bd58807')
    def test_get_hashmap_mappings(self):
        service_id = self._setup_dummy_service()
        field_ids = self._setup_dummy_fields(service_id)
        field_mapping = self.rating_client.create_hashmap_mapping(
            field_id=field_ids[0],
            value='dummy mapping',
        )
        service_mapping = self.rating_client.create_hashmap_mapping(
            service_id=service_id,
        )
        self._created_resources['hashmap_mapping'].append(
            field_mapping['mapping_id'],
        )
        self._created_resources['hashmap_mapping'].append(
            service_mapping['mapping_id'],
        )

        service_filtered_mappings = self.rating_client.get_hashmap_mappings(
            service_id=service_id,
        )
        field_filtered_mappings = self.rating_client.get_hashmap_mappings(
            field_id=field_ids[0],
        )
        self._find_item(service_filtered_mappings['mappings'],
                        service_mapping['mapping_id'],
                        'mapping_id')
        self._find_item(field_filtered_mappings['mappings'],
                        field_mapping['mapping_id'],
                        'mapping_id')

    @decorators.idempotent_id('b7ad24e5-c72c-469a-886b-db43aab8f328')
    def test_create_delete_hashmap_mapping(self):
        service_id = self._setup_dummy_service()
        field_ids = self._setup_dummy_fields(service_id)
        mapping_ids = list()
        for field_id in field_ids:
            mapping = self.rating_client.create_hashmap_mapping(
                field_id=field_id,
                value='dummy mapping',
            )
            self.assertEqual('dummy mapping', mapping['value'])
            mapping_ids.append(mapping['mapping_id'])
        mapping = self.rating_client.create_hashmap_mapping(
            service_id=service_id,
        )
        mapping_ids.append(mapping['mapping_id'])
        self._created_resources['hashmap_mapping'] += mapping_ids
        for mapping_id in mapping_ids:
            self.rating_client.delete_hashmap_mapping(mapping_id)

    @decorators.idempotent_id('6a04634d-2d3a-406e-980a-e7c7c9cc081b')
    def test_update_hashmap_mapping(self):
        service_id = self._setup_dummy_service()
        field_ids = self._setup_dummy_fields(service_id)
        mapping = self.rating_client.create_hashmap_mapping(
            field_id=field_ids[0],
            value='dummy field',
        )
        self._created_resources['hashmap_mapping'].append(
            mapping['mapping_id'],
        )
        self.assertEqual('dummy field', mapping['value'])
        self.rating_client.update_hashmap_mapping(
            mapping['mapping_id'],
            value='new value',
        )
        mapping = self.rating_client.get_hashmap_mapping(
            mapping['mapping_id']
        )
        self.assertEqual('new value', mapping['value'])

    @decorators.idempotent_id('0f9200ab-146b-4349-a579-ce12062f465b')
    def test_create_delete_hashmap_group(self):
        group = self.rating_client.create_hashmap_group(
            data_utils.rand_name('dummy_group'),
        )
        self._created_resources['hashmap_group'].append(group['group_id'])
        self.rating_client.delete_hashmap_group(group['group_id'])

    @decorators.idempotent_id('858a019a-fb64-4656-b7a6-c92917f641ab')
    def test_get_hashmap_group(self):
        group = self.rating_client.create_hashmap_group(
            data_utils.rand_name('dummy_group'),
        )
        self._created_resources['hashmap_group'].append(group['group_id'])
        group_name = group['name']
        groups = self.rating_client.get_hashmap_group()
        self._find_item(groups['groups'], group_name, 'name')
        group = self.rating_client.get_hashmap_group(group['group_id'])
        self.assertEqual(group['name'], group_name)

    @decorators.idempotent_id('98ca42dd-a9e2-477a-8e42-16389aed1f44')
    def test_get_hashmap_mapping_group(self):
        service_id = self._setup_dummy_service()
        field_ids = self._setup_dummy_fields(service_id)
        group = self.rating_client.create_hashmap_group(
            data_utils.rand_name('dummy_group'),
        )
        group_name = group['name']
        self._created_resources['hashmap_group'].append(group['group_id'])
        mapping = self.rating_client.create_hashmap_mapping(
            field_id=field_ids[0],
            group_id=group['group_id'],
            value='dummy mapping',
        )
        self._created_resources['hashmap_mapping'].append(
            mapping['mapping_id'],
        )
        group = self.rating_client.get_hashmap_mapping_group(
            mapping['mapping_id'],
        )
        self.assertEqual(group['name'], group_name)

    @decorators.idempotent_id('92860fc8-596a-42fd-b0d5-97e0f5a7bd2c')
    def test_get_hashmap_group_mappings(self):
        service_id = self._setup_dummy_service()
        field_ids = self._setup_dummy_fields(service_id)
        group = self.rating_client.create_hashmap_group(
            data_utils.rand_name('dummy_group'),
        )
        self._created_resources['hashmap_group'].append(group['group_id'])
        for i in range(3):
            mapping = self.rating_client.create_hashmap_mapping(
                field_id=field_ids[i],
                group_id=group['group_id'],
                value='dummy mapping {}'.format(i),
            )
            self._created_resources['hashmap_mapping'].append(
                mapping['mapping_id']
            )
        mappings = self.rating_client.get_hashmap_group_mappings(
            group['group_id'],
        )
        for i in range(3):
            self._find_item(mappings['mappings'],
                            'dummy mapping {}'.format(i),
                            'value')

    @decorators.idempotent_id('d2b3dba3-91df-4aa7-9ae2-96d971df2dbf')
    def test_create_delete_update_hashmap_threshold(self):
        service_id = self._setup_dummy_service()
        field_ids = self._setup_dummy_fields(service_id)
        thresholds = list()
        thresholds.append(self.rating_client.create_hashmap_threshold(
            service_id=service_id,
            level=0.95,
            cost=12,
        ))
        self._created_resources['hashmap_threshold'].append(
            thresholds[-1]['threshold_id']
        )
        for idx, field_id in enumerate(field_ids):
            thresholds.append(self.rating_client.create_hashmap_threshold(
                field_id=field_id,
                level=0.95 * (idx + 1),
                cost=12 * (idx + 1),
            ))
            self._created_resources['hashmap_threshold'].append(
                thresholds[-1]['threshold_id']
            )
        for threshold in thresholds:
            self.rating_client.update_hashmap_threshold(
                threshold['threshold_id'],
                cost=42,
                level=1.23,
            )
        for threshold in thresholds:
            self.rating_client.delete_hashmap_threshold(
                threshold['threshold_id'],
            )

    @decorators.idempotent_id('dc463432-3b92-44ac-8caf-b789857f9db7')
    def test_get_hashmap_threshold(self):
        service_id = self._setup_dummy_service()
        self._setup_dummy_fields(service_id)
        created_threshold = self.rating_client.create_hashmap_threshold(
            service_id=service_id,
            level=1.95,
            cost=42,
        )
        self._created_resources['hashmap_threshold'].append(
            created_threshold['threshold_id'],
        )
        threshold = self.rating_client.get_hashmap_threshold(
            created_threshold['threshold_id'],
        )
        self.assertEqual(threshold['level'], created_threshold['level'])
        self.rating_client.delete_hashmap_threshold(
            created_threshold['threshold_id'],
        )

    @decorators.idempotent_id('d04caad5-eb18-40ce-817e-13c257633cca')
    def test_get_hashmap_thresholds(self):
        service_id = self._setup_dummy_service()
        field_ids = self._setup_dummy_fields(service_id)
        group = self.rating_client.create_hashmap_group(
            data_utils.rand_name('dummy_group'),
        )
        self._created_resources['hashmap_group'].append(group['group_id'])
        field_threshold = self.rating_client.create_hashmap_threshold(
            group_id=group['group_id'],
            field_id=field_ids[0],
            level=1.95,
            cost=42,
        )
        self._created_resources['hashmap_threshold'].append(
            field_threshold['threshold_id'],
        )
        service_threshold = self.rating_client.create_hashmap_threshold(
            service_id=service_id,
            group_id=group['group_id'],
            level=1.95,
            cost=42,
        )
        self._created_resources['hashmap_threshold'].append(
            service_threshold['threshold_id'],
        )
        thresholds = self.rating_client.get_hashmap_thresholds(
            service_id=service_id,
        )
        self._find_item(thresholds['thresholds'],
                        group['group_id'],
                        'group_id')
        thresholds = self.rating_client.get_hashmap_thresholds(
            field_id=field_ids[0],
        )
        self._find_item(thresholds['thresholds'],
                        group['group_id'],
                        'group_id')
        thresholds = self.rating_client.get_hashmap_thresholds(
            group_id=group['group_id']
        )
        self._find_item(thresholds['thresholds'], service_id, 'service_id')
        self._find_item(thresholds['thresholds'], field_ids[0], 'field_id')
