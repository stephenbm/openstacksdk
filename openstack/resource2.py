# Copyright 2018 Red Hat, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import resource
from openstack import utils


class Resource(resource.Resource):

    @utils.deprecated(deprecated_in="0.10.0", removed_in="1.0",
                      details="openstack.resource2 is now openstack.resource")
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)
