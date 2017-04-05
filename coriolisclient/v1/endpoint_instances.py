# Copyright (c) 2017 Cloudbase Solutions Srl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections

from six.moves.urllib import parse as urlparse

from coriolisclient import base


class EndpointInstance(base.Resource):
    attribute_mapping = collections.OrderedDict([
        ("id", "Instance ID"),
        ("name", "Instance Name"),
        ("memory_mb", "Instance Memory (MB)"),
        ("num_cpu", "Cores"),
        ("num_cores_per_socket", "Cores per socket"),
        ("os_type", "OS Type")
    ])

    @property
    def id(self):
        return self._info.get("id")

    @property
    def name(self):
        return self._info.get("name")

    @property
    def memory_mb(self):
        return self._info.get("memory_mb")

    @property
    def num_cpu(self):
        return self._info.get("num_cpu")

    @property
    def os_type(self):
        return self._info.get("os_type")


class EndpointInstanceManager(base.BaseManager):
    resource_class = EndpointInstance

    def __init__(self, api):
        super(EndpointInstanceManager, self).__init__(api)

    def list(self, endpoint, marker=None, limit=None, name=None):

        query = {}
        if marker is not None:
            query['marker'] = marker
        if limit is not None:
            query['limit'] = limit
        if name is not None:
            query["name"] = name

        url = '/endpoints/%s/instances' % base.getid(endpoint)
        if query:
            url += "?" + urlparse.urlencode(query)

        return self._list(url, 'instances')
