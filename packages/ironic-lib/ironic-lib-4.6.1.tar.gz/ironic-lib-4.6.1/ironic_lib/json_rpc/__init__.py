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

from oslo_config import cfg

from ironic_lib.common.i18n import _
from ironic_lib import keystone


CONF = cfg.CONF

opts = [
    cfg.StrOpt('auth_strategy',
               choices=[('noauth', _('no authentication')),
                        ('keystone', _('use the Identity service for '
                                       'authentication')),
                        ('http_basic', _('HTTP basic authentication'))],
               help=_('Authentication strategy used by JSON RPC. Defaults to '
                      'the global auth_strategy setting.')),
    cfg.StrOpt('http_basic_auth_user_file',
               default='/etc/ironic/htpasswd-json-rpc',
               help=_('Path to Apache format user authentication file used '
                      'when auth_strategy=http_basic')),
    cfg.HostAddressOpt('host_ip',
                       default='::',
                       help=_('The IP address or hostname on which JSON RPC '
                              'will listen.')),
    cfg.PortOpt('port',
                default=8089,
                help=_('The port to use for JSON RPC')),
    cfg.BoolOpt('use_ssl',
                default=False,
                help=_('Whether to use TLS for JSON RPC')),
    cfg.StrOpt('http_basic_username',
               deprecated_for_removal=True,
               deprecated_reason=_("Use username instead"),
               help=_("Name of the user to use for HTTP Basic authentication "
                      "client requests.")),
    cfg.StrOpt('http_basic_password',
               deprecated_for_removal=True,
               deprecated_reason=_("Use password instead"),
               secret=True,
               help=_("Password to use for HTTP Basic authentication "
                      "client requests.")),
]


def register_opts(conf):
    conf.register_opts(opts, group='json_rpc')
    keystone.register_auth_opts(conf, 'json_rpc')
    conf.set_default('timeout', 120, group='json_rpc')


register_opts(CONF)


def list_opts():
    return opts + keystone.add_auth_opts([])


def auth_strategy():
    # NOTE(dtantsur): this expects [DEFAULT]auth_strategy to be provided by the
    # service configuration.
    return CONF.json_rpc.auth_strategy or CONF.auth_strategy
