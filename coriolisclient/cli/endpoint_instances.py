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
"""
Command-line interface sub-commands related to endpoints.
"""
from cliff import lister

from coriolisclient.cli import formatter


# set of keys present by default in the resource info which may be ignored:
DEFAULT_KEYS = {"instance_name"}


class EndpointInstanceFormatter(formatter.EntityFormatter):

    def __init__(self, endpoint_instance):
        """ Sets the columns attribute after the keys in the info received
        as the given coriolisclient.base.Resource. """
        self._base_keys = []
        self._extra_keys = []
        if not endpoint_instance:
            return

        self._base_keys = endpoint_instance.attribute_mapping.keys()
        all_keys = set(sorted(endpoint_instance._info.keys()))
        self._extra_keys = list(
            all_keys - set(self._base_keys) - DEFAULT_KEYS)

        cols = [
            endpoint_instance.attribute_mapping[k] for k in self._base_keys]
        cols = cols + [self._format_column_name(k) for k in self._extra_keys]
        self.columns = cols

    def _format_column_name(self, attr_name):
        """ Replaces _ with spaces, capitalizes  first char and any 'id' """
        words = []
        for word in attr_name.split("_"):
            if word == "id":
                words.append("ID")
                continue
            words.append(word)
        return " ".join(words).capitalize()

    def _get_formatted_data(self, obj):
        data = [getattr(obj, k, None) for k in self._base_keys]
        data = data + [getattr(obj, k, None) for k in self._extra_keys]
        return tuple(data)


class ListEndpointInstance(lister.Lister):
    """List endpoint instances"""

    def get_parser(self, prog_name):
        parser = super(ListEndpointInstance, self).get_parser(prog_name)
        parser.add_argument('endpoint', help='The endpoint\'s id')
        parser.add_argument(
            '--marker',
            help='The id of the last instance on the previous page')
        parser.add_argument(
            '--limit', type=int, help='maximum number of instances per page')
        parser.add_argument(
            '--name',
            help='Filter results based on regular expression search')
        return parser

    def take_action(self, args):
        ei = self.app.client_manager.coriolis.endpoint_instances
        obj_list = ei.list(args.endpoint, args.marker, args.limit, args.name)
        sample_obj = None
        if obj_list:
            sample_obj = obj_list[0]
        return EndpointInstanceFormatter(sample_obj).list_objects(obj_list)
