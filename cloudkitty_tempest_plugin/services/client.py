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

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient import client
from oslo_serialization import jsonutils as json
from tempest import clients as tempest_clients
from tempest import config
from tempest.lib.common import rest_client
from tempest.lib.services import clients

CONF = config.CONF


class BaseRatingClient(rest_client.RestClient):
    """Base class for cloudkittyclient implementations"""

    @staticmethod
    def deserialize(body):
        return json.loads(body.decode().replace("\n", ""))

    @staticmethod
    def serialize(body):
        return json.dumps(body)

    def _do_request(self, method, uri, body=None, expected_code=200):
        resp, body = self.request(method, uri, body=body)
        self.expected_success(expected_code, resp.status)
        body = self.deserialize(body) if body else dict()
        if not isinstance(body, dict) and not isinstance(body, list):
            body = dict()
        # ResponseBody inherits from dict, so lists must be converted
        body = dict(body=body) if isinstance(body, list) else body
        return rest_client.ResponseBody(resp, body)


class RatingClientV1(BaseRatingClient):
    """Implementation of cloudkittyclient for v1 endpoints"""

    api_version = 'v1'

    def get_collector_mappings(self, service=None):
        uri = '/collector/mappings/'
        if service:
            uri += service + '/'
        return self._do_request('GET', uri)

    def create_collector_mapping(self, collector='gnocchi', service='compute'):
        uri = '/collector/mappings/'
        request_body = {
            'collector': collector,
            'service': service,
        }
        return self._do_request('POST', uri, body=self.serialize(request_body))

    def delete_collector_mapping(self, service='compute'):
        uri = '/collector/mappings'
        request_body = {
            'service': service,
        }
        return self._do_request('DELETE', uri,
                                body=self.serialize(request_body),
                                expected_code=204)

    def get_collector_state(self, collector="gnocchi"):
        uri = '/collector/states/'
        request_body = {
            'name': collector,
        }
        return self._do_request('GET', uri, body=self.serialize(request_body))

    def set_collector_state(self, collector="gnocchi", enabled=True):
        uri = '/collector/states/'
        request_body = {
            'name': collector,
            'enabled': enabled,
        }
        return self._do_request('PUT', uri, body=self.serialize(request_body))

    def get_config(self):
        uri = '/info/config/'
        return self._do_request('GET', uri)

    def get_metric(self, metric_name=None):
        uri = '/info/metrics/'
        if metric_name:
            uri += metric_name + '/'
        return self._do_request('GET', uri)

    def get_rating_module(self, module_name=None):
        uri = '/rating/modules/'
        if module_name:
            uri += module_name + '/'
        return self._do_request('GET', uri)

    def update_rating_module(self, module_name, description='',
                             enabled=False, hot_config=True, priority=1):
        uri = '/rating/modules/' + module_name + '/'
        request_body = {
            'module_id': module_name,
            'description': description,
            'enabled': enabled,
            'hot-config': hot_config,
            'priority': priority,
        }
        return self._do_request('PUT', uri, body=self.serialize(request_body),
                                expected_code=302)

    def reload_rating_modules(self):
        uri = '/rating/reload_modules'
        return self._do_request('GET', uri, expected_code=204)

    def get_report_summary(self):
        uri = '/report/summary/'
        return self._do_request('GET', uri)

    def get_rated_tenants(self):
        uri = '/report/tenants/'
        return self._do_request('GET', uri)

    def get_report_total(self):
        uri = '/report/total/'
        return self._do_request('GET', uri)

    def get_storage_dataframes(self):
        uri = '/storage/dataframes/'
        return self._do_request('GET', uri)

    def get_hashmap_mapping_types(self):
        uri = '/rating/module_config/hashmap/types/'
        return self._do_request('GET', uri)

    def get_hashmap_service(self, service_id=None):
        uri = '/rating/module_config/hashmap/services/'
        if service_id:
            uri += service_id + '/'
        return self._do_request('GET', uri)

    def create_hashmap_service(self, name, service_id=None):
        uri = '/rating/module_config/hashmap/services/'
        request_body = {
            'name': name,
        }
        if service_id:
            request_body['service_id'] = service_id
        return self._do_request('POST', uri,
                                body=self.serialize(request_body),
                                expected_code=201)

    def delete_hashmap_service(self, service_id):
        uri = '/rating/module_config/hashmap/services/'
        request_body = {
            'service_id': service_id,
        }
        return self._do_request('DELETE', uri,
                                body=self.serialize(request_body),
                                expected_code=204)

    def get_hashmap_fields(self, service_id):
        uri = '/rating/module_config/hashmap/fields/'
        request_body = {
            'service_id': service_id,
        }
        return self._do_request('GET', uri,
                                body=self.serialize(request_body))

    def get_hashmap_field(self, field_id):
        uri = '/rating/module_config/hashmap/fields/' + field_id + '/'
        return self._do_request('GET', uri)

    def create_hashmap_field(self, field_name, service_id, field_id=None):
        uri = '/rating/module_config/hashmap/fields/'
        request_body = {
            'name': field_name,
            'service_id': service_id,
        }
        if field_id:
            request_body['field_id'] = field_id
        return self._do_request('POST', uri,
                                body=self.serialize(request_body),
                                expected_code=201)

    def delete_hashmap_field(self, field_id):
        uri = '/rating/module_config/hashmap/fields/'
        request_body = {
            'field_id': field_id,
        }
        return self._do_request('DELETE', uri,
                                body=self.serialize(request_body),
                                expected_code=204)

    def get_hashmap_mappings(self, service_id=None, field_id=None,
                             group_id=None, no_group=False, tenant_id=None,
                             filter_tenant=False):
        args = locals()
        args.pop('self')
        uri = '/rating/module_config/hashmap/mappings/'
        request_body = dict((k, v)
                            for k, v in six.iteritems(args) if v is not None)
        return self._do_request('GET', uri,
                                body=self.serialize(request_body))

    def get_hashmap_mapping(self, mapping_id):
        uri = '/rating/module_config/hashmap/mappings/' + mapping_id + '/'
        return self._do_request('GET', uri)

    def create_hashmap_mapping(self, cost=0, field_id=None, group_id=None,
                               map_type=None, mapping_id=None, service_id=None,
                               tenant_id=None, value=None):
        args = locals()
        args.pop('self')
        uri = '/rating/module_config/hashmap/mappings/'
        request_body = dict((k, v)
                            for k, v in six.iteritems(args) if v is not None)
        return self._do_request('POST', uri,
                                body=self.serialize(request_body),
                                expected_code=201)

    def delete_hashmap_mapping(self, mapping_id):
        uri = '/rating/module_config/hashmap/mappings/'
        request_body = {
            'mapping_id': mapping_id,
        }
        return self._do_request('DELETE', uri,
                                body=self.serialize(request_body),
                                expected_code=204)

    def update_hashmap_mapping(self, mapping_id, cost=0,
                               field_id=None, group_id=None, map_type=None,
                               service_id=None, tenant_id=None, value=None):
        args = locals()
        args.pop('self')
        uri = '/rating/module_config/hashmap/mappings/'
        request_body = dict((k, v)
                            for k, v in six.iteritems(args) if v is not None)
        return self._do_request('PUT', uri,
                                body=self.serialize(request_body),
                                expected_code=302)

    def get_hashmap_mapping_group(self, mapping_id):
        uri = '/rating/module_config/hashmap/mappings/group/'
        request_body = {
            'mapping_id': mapping_id,
        }
        return self._do_request('GET', uri,
                                body=self.serialize(request_body))

    def get_hashmap_group(self, group_id=None):
        uri = '/rating/module_config/hashmap/groups/'
        if group_id:
            uri += group_id + '/'
        return self._do_request('GET', uri)

    def create_hashmap_group(self, group_name, group_id=None):
        uri = '/rating/module_config/hashmap/groups'
        request_body = {
            'name': group_name,
        }
        if group_id:
            request_body['group_id'] = group_id
        return self._do_request('POST', uri,
                                body=self.serialize(request_body),
                                expected_code=201)

    def delete_hashmap_group(self, group_id):
        uri = '/rating/module_config/hashmap/groups'
        request_body = {
            'group_id': group_id,
        }
        return self._do_request('DELETE', uri,
                                body=self.serialize(request_body),
                                expected_code=204)

    def get_hashmap_group_mappings(self, group_id):
        uri = '/rating/module_config/hashmap/groups/mappings/'
        request_body = {
            'group_id': group_id,
        }
        return self._do_request('GET', uri,
                                body=self.serialize(request_body))

    def get_hashmap_group_threshold(self, group_id):
        uri = '/rating/module_config/hashmap/groups/thresholds/'
        request_body = {
            'group_id': group_id,
        }
        return self._do_request('GET', uri,
                                body=self.serialize(request_body))

    def get_hashmap_threshold(self, threshold_id):
        uri = '/rating/module_config/hashmap/thresholds/' + threshold_id + '/'
        return self._do_request('GET', uri)

    def get_hashmap_thresholds(self, service_id=None,
                               field_id=None, group_id=None):
        args = locals()
        args.pop('self')
        uri = '/rating/module_config/hashmap/thresholds/'
        request_body = dict((k, v)
                            for k, v in six.iteritems(args) if v is not None)
        return self._do_request('GET', uri,
                                body=self.serialize(request_body))

    def create_hashmap_threshold(self, field_id=None, group_id=None,
                                 threshold_id=None, map_type=None, cost=None,
                                 service_id=None, tenant_id=None, level=None):
        args = locals()
        args.pop('self')
        uri = '/rating/module_config/hashmap/thresholds/'
        request_body = dict((k, v)
                            for k, v in six.iteritems(args) if v is not None)
        return self._do_request('POST', uri,
                                body=self.serialize(request_body),
                                expected_code=201)

    def update_hashmap_threshold(self, threshold_id, field_id=None,
                                 group_id=None, map_type=None, cost=None,
                                 service_id=None, tenant_id=None, level=None):
        args = locals()
        args.pop('self')
        uri = '/rating/module_config/hashmap/thresholds/'
        request_body = dict((k, v)
                            for k, v in six.iteritems(args) if v is not None)
        return self._do_request('PUT', uri,
                                body=self.serialize(request_body),
                                expected_code=302)

    def delete_hashmap_threshold(self, threshold_id):
        uri = '/rating/module_config/hashmap/thresholds/'
        request_body = {
            'threshold_id': threshold_id,
        }
        return self._do_request('DELETE', uri,
                                body=self.serialize(request_body),
                                expected_code=204)

    def get_pyscripts(self, no_data=False):
        uri = '/rating/module_config/pyscripts/scripts/'
        request_body = {
            'no_data': no_data,
        }
        return self._do_request('GET', uri, body=self.serialize(request_body))

    def get_pyscript(self, script_id):
        uri = '/rating/module_config/pyscripts/scripts/' + script_id + '/'
        return self._do_request('GET', uri)

    @staticmethod
    def _get_pyscript_request_body(name, data, checksum, script_id):
        args = locals()
        request_body = dict((k, v)
                            for k, v in six.iteritems(args) if v is not None)
        return request_body

    def create_pyscript(self, name, data, checksum=None, script_id=None):
        uri = '/rating/module_config/pyscripts/scripts/'
        request_body = self._get_pyscript_request_body(name, data,
                                                       checksum, script_id)
        return self._do_request('POST', uri,
                                body=self.serialize(request_body),
                                expected_code=201)

    def update_pyscript(self, script_id, name=None, data=None, checksum=None):
        uri = '/rating/module_config/pyscripts/scripts/'
        request_body = self._get_pyscript_request_body(name, data,
                                                       checksum, script_id)
        return self._do_request('PUT', uri,
                                body=self.serialize(request_body),
                                expected_code=201)

    def delete_pyscript(self, script_id):
        uri = '/rating/module_config/pyscripts/scripts/'
        request_body = {
            'script_id': script_id,
        }
        return self._do_request('DELETE', uri,
                                body=self.serialize(request_body),
                                expected_code=204)


class RatingClientV2(RatingClientV1):
    """Implementation of cloudkittyclient for v2 endpoints"""

    api_version = 'v2'


class CustomIdentityClient(object):
    """Custom Keystone client

    Class used by the CK tempest plugin to add the 'rating' role to
    the dynamically allocated test tenant
    """

    def __init__(self):
        self.admin_auth = v3.Password(
            auth_url=CONF.identity.uri_v3,
            username=CONF.auth.admin_username,
            password=CONF.auth.admin_password,
            project_name=CONF.auth.admin_project_name,
            project_domain_name=CONF.auth.admin_domain_name,
            user_domain_name=CONF.auth.admin_domain_name,
        )
        self.admin_session = session.Session(auth=self.admin_auth)
        self.admin_client = client.Client(session=self.admin_session)
        self.ck_user_id = self._get_ck_user_id()
        self.rating_role_id = self._get_rating_role_id()

    def enable_rating(self, project_id):
        """Assigns the 'rating' role to ck user on the given project"""
        self.admin_client.roles.grant(self.rating_role_id,
                                      user=self.ck_user_id,
                                      project=project_id)

    @staticmethod
    def _find_item(iterable, key, value):
        item = None
        for elem in iterable:
            if getattr(elem, key, None) == value:
                item = elem
        return item

    def _get_ck_user_id(self):
        users = self.admin_client.users.list()
        return getattr(
            self._find_item(users, 'name', CONF.rating_plugin.user_name),
            'id', None,
        )

    def _get_rating_role_id(self):
        roles = self.admin_client.roles.list()
        return getattr(
            self._find_item(roles, 'name', 'rating'), 'id', None,
        )


class Manager(clients.ServiceClients):
    rating_params = {
        'service': CONF.rating_plugin.service_name,
        'region': CONF.identity.region,
        'endpoint_type': CONF.rating_plugin.endpoint_type,
    }

    def __init__(self, credentials=None, service=None):
        dscv = CONF.identity.disable_ssl_certificate_validation
        _, uri = tempest_clients.get_auth_provider_class(credentials)
        super(Manager, self).__init__(
            credentials=credentials,
            identity_uri=uri,
            scope='project',
            disable_ssl_certificate_validation=dscv,
            ca_certs=CONF.identity.ca_certificates_file,
            trace_requests=CONF.debug.trace_requests)
        self.rating_clients = {
            'v1': RatingClientV1(self.auth_provider, **self.rating_params),
            'v2': RatingClientV2(self.auth_provider, **self.rating_params),
        }

    def get_rating_client(self, api_version='v2'):
        if api_version not in self.rating_clients:
            raise ValueError('API version must be one of the following: {}',
                             list(self.rating_client.keys()))
        return self.rating_clients[api_version]
