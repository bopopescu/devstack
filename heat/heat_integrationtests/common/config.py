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

import os
import sys

from oslo.config import cfg

import heat_integrationtests


IntegrationTestGroup = [

    cfg.StrOpt('username',
               default=os.environ.get('OS_USERNAME'),
               help="Username to use for API requests."),
    cfg.StrOpt('password',
               default=os.environ.get('OS_PASSWORD'),
               help="API key to use when authenticating.",
               secret=True),
    cfg.StrOpt('tenant_name',
               default=os.environ.get('OS_TENANT_NAME'),
               help="Tenant name to use for API requests."),
    cfg.StrOpt('auth_url',
               default=os.environ.get('OS_AUTH_URL'),
               help="Full URI of the OpenStack Identity API (Keystone), v2"),
    cfg.StrOpt('region',
               default=os.environ.get('OS_REGION_NAME'),
               help="The region name to us"),
    cfg.StrOpt('instance_type',
               default=os.environ.get('HEAT_TEST_INSTANCE_TYPE'),
               help="Instance type for tests. Needs to be big enough for a "
                    "full OS plus the test workload"),
    cfg.StrOpt('image_ref',
               default=os.environ.get('HEAT_TEST_IMAGE_REF'),
               help="Name of image to use for tests which boot servers."),
    cfg.StrOpt('keypair_name',
               default=None,
               help="Name of existing keypair to launch servers with."),
    cfg.StrOpt('minimal_image_ref',
               default=os.environ.get('HEAT_TEST_MINIMAL_IMAGE_REF'),
               help="Name of minimal (e.g cirros) image to use when "
                    "launching test instances."),
    cfg.StrOpt('auth_version',
               default='v2',
               help="Identity API version to be used for authentication "
                    "for API tests."),
    cfg.BoolOpt('disable_ssl_certificate_validation',
                default=False,
                help="Set to True if using self-signed SSL certificates."),
    cfg.IntOpt('build_interval',
               default=4,
               help="Time in seconds between build status checks."),
    cfg.IntOpt('build_timeout',
               default=1200,
               help="Timeout in seconds to wait for a stack to build."),
    cfg.StrOpt('network_for_ssh',
               default='private',
               help="Network used for SSH connections."),
    cfg.StrOpt('fixed_network_name',
               default='private',
               help="Visible fixed network name "),
    cfg.IntOpt('ssh_timeout',
               default=300,
               help="Timeout in seconds to wait for authentication to "
                    "succeed."),
    cfg.IntOpt('ip_version_for_ssh',
               default=4,
               help="IP version used for SSH connections."),
    cfg.IntOpt('ssh_channel_timeout',
               default=60,
               help="Timeout in seconds to wait for output from ssh "
                    "channel."),
    cfg.IntOpt('tenant_network_mask_bits',
               default=28,
               help="The mask bits for tenant ipv4 subnets"),
    cfg.IntOpt('volume_size',
               default=1,
               help='Default size in GB for volumes created by volumes tests'),
]


def init_conf(read_conf=True):

    default_config_files = None
    if read_conf:
        confpath = os.path.join(
            os.path.dirname(os.path.realpath(heat_integrationtests.__file__)),
            'heat_integrationtests.conf')
        if os.path.isfile(confpath):
            default_config_files = [confpath]

    conf = cfg.ConfigOpts()
    conf(args=[], project='heat_integrationtests',
         default_config_files=default_config_files)

    for opt in IntegrationTestGroup:
        conf.register_opt(opt)
    return conf


if __name__ == '__main__':
    cfg.CONF = init_conf(False)
    import heat.openstack.common.config.generator as generate
    generate.generate(sys.argv[1:])
