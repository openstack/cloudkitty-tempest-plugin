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
from tempest.lib import exceptions as lib_exc

from cloudkitty_tempest_plugin.tests.api import base

SCRIPT_DATA_ONE = """
def dumbfunc():
    return 0

data = dumbfunc()
"""

SCRIPT_DATA_TWO = """
def dumbfunc():
    return 0

data = dumbfunc() + 2
"""


class CloudkittyPyscriptAPITest(base.BaseRatingTest):
    api_version = 'v1'
    credentials = ['admin']

    @decorators.idempotent_id('2015c966-b707-40f7-b84d-9aa6550b9e41')
    def test_get_pyscripts(self):
        self.rating_client.get_pyscripts()

    @decorators.idempotent_id('9e78cccc-ca85-42ce-8648-4cd9682375df')
    def test_create_update_delete_pyscript(self):
        pyscript = self.rating_client.create_pyscript(
            data_utils.rand_name('dummy_script'),
            SCRIPT_DATA_ONE,
        )
        self._created_resources['pyscript'].append(pyscript['script_id'])
        self.assertEqual(pyscript['data'], SCRIPT_DATA_ONE)
        # We are creating this flag to allow the test to work for
        # both old and new API version. We can remove this validation
        # in the end of life of version 2024.1.
        old_version = True
        try:
            self.rating_client.update_pyscript(pyscript['script_id'],
                                               data=SCRIPT_DATA_TWO,
                                               name=pyscript['name'])
        except lib_exc.BadRequest as e:
            old_version = False
            self.assertTrue("You are allowed to update only the attribute "
                            "[end] as this rule is already running as it "
                            "started on " in e.resp_body['faultstring'])

        if old_version:
            pyscript = self.rating_client.get_pyscript(pyscript['script_id'])
            self.assertEqual(pyscript['data'], SCRIPT_DATA_TWO)
            self.rating_client.delete_pyscript(pyscript['script_id'])
            return

        end_date = '3000-01-01T23:59:59'

        self.rating_client.update_pyscript(pyscript['script_id'],
                                           name=pyscript['name'],
                                           end=end_date)
        try:
            self.rating_client.update_pyscript(pyscript['script_id'],
                                               name=pyscript['name'],
                                               end=end_date)
        except lib_exc.BadRequest as e:
            self.assertTrue("Cannot update a rule that was already "
                            "processed and has a defined end date."
                            in e.resp_body['faultstring'])

        pyscript = self.rating_client.get_pyscript(pyscript['script_id'])
        self.assertEqual(pyscript['data'], SCRIPT_DATA_ONE)
        self.assertEqual(pyscript['end'], end_date)
        self.rating_client.delete_pyscript(pyscript['script_id'])

    @decorators.idempotent_id('3fbaf8b4-c472-4509-8d73-55dc4a87a442')
    def test_get_pyscript(self):
        pyscript = self.rating_client.create_pyscript(
            data_utils.rand_name('dummy_script'),
            SCRIPT_DATA_ONE,
        )
        self.assertEqual(pyscript['data'], SCRIPT_DATA_ONE)
        self._created_resources['pyscript'].append(pyscript['script_id'])
        pyscript = self.rating_client.get_pyscript(pyscript['script_id'])


class CloudkittyPyscriptAPITestNegative(base.BaseRatingTest):
    api_version = 'v1'
    credentials = ['admin']

    @decorators.idempotent_id('999c97cc-1d71-43b8-988f-d89b8fac4040')
    @decorators.attr(type=['negative'])
    def test_update_script_negative(self):
        pyscript = self.rating_client.create_pyscript(
            data_utils.rand_name('dummy_script'),
            SCRIPT_DATA_ONE,
        )
        self._created_resources['pyscript'].append(pyscript['script_id'])
        fake_id = data_utils.rand_uuid()
        self.assertRaises(lib_exc.NotFound,
                          self.rating_client.get_pyscript,
                          fake_id)
