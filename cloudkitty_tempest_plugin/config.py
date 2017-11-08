# Copyright 2017 Objectif Libre
# All Rights Reserved.
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

from oslo_config import cfg

rating_group = cfg.OptGroup(name='rating_plugin',
                            title='Rating Service Options')

RatingGroup = [
    cfg.StrOpt('service_name',
               default='rating',
               help="Service name of the Rating service."),
    cfg.StrOpt('user_name',
               default='cloudkitty',
               help="User name for the Rating service."),
    cfg.StrOpt('endpoint_type',
               default='publicURL',
               choices=['public', 'admin', 'internal',
                        'publicURL', 'adminURL', 'internalURL'],
               help="The endpoint type to use for the rating service."),
]
