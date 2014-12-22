#
# Copyright 2014 Red Hat
#
# Author: Chris Dent <chdent@redhat.com>
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


from tempest import config
from tempest.openstack.common import log as logging
from tempest.scenario import manager
from tempest import test

CONF = config.CONF

LOG = logging.getLogger(__name__)

# Loop for up to 120 seconds waiting on notifications
# NOTE(chdent): The choice of 120 seconds is fairly
# arbitrary: Long enough to give the notifications the
# chance to travel across a highly latent bus but not
# so long as to allow excessive latency to never be visible.
# TODO(chdent): Ideally this value would come from configuration.
NOTIFICATIONS_WAIT = 120
NOTIFICATIONS_SLEEP = 1


class TestSwiftTelemetry(manager.SwiftScenarioTest):
    """
    Test that swift uses the ceilometer middleware.
     * create container.
     * upload a file to the created container.
     * retrieve the file from the created container.
     * wait for notifications from ceilometer.
    """

    @classmethod
    def resource_setup(cls):
        if not CONF.service_available.ceilometer:
            skip_msg = ("%s skipped as ceilometer is not available" %
                        cls.__name__)
            raise cls.skipException(skip_msg)
        elif CONF.telemetry.too_slow_to_test:
            skip_msg = "Ceilometer feature for fast work mysql is disabled"
            raise cls.skipException(skip_msg)
        super(TestSwiftTelemetry, cls).resource_setup()
        cls.telemetry_client = cls.manager.telemetry_client

    def _confirm_notifications(self, container_name, obj_name):
        """
        Loop seeking for appropriate notifications about the containers
        and objects sent to swift.
        """

        def _check_samples():
            """
            Return True only if we have notifications about some
            containers and some objects and the notifications are about
            the expected containers and objects.
            Otherwise returning False will case _check_samples to be
            called again.
            """
            _, results = self.telemetry_client.list_samples(
                'storage.api.request')
            LOG.debug('got samples %s', results)

            # Extract container info from samples.
            containers = [sample['resource_metadata']['container']
                          for sample in results
                          if sample['resource_metadata']['container']
                          != 'None']
            # Extract object info from samples.
            objects = [sample['resource_metadata']['object']
                       for sample in results
                       if sample['resource_metadata']['object'] != 'None']

            return (containers
                    and objects
                    and container_name in containers
                    and obj_name in objects)

        self.assertTrue(test.call_until_true(_check_samples,
                                             NOTIFICATIONS_WAIT,
                                             NOTIFICATIONS_SLEEP),
                        'Correct notifications were not received after '
                        '%s seconds.' % NOTIFICATIONS_WAIT)

    @test.services('object_storage', 'telemetry')
    def test_swift_middleware_notifies(self):
        container_name = self.create_container()
        obj_name, _ = self.upload_object_to_container(container_name)
        self._confirm_notifications(container_name, obj_name)
