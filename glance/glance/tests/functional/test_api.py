# Copyright 2012 OpenStack Foundation
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

"""Version-independent api tests"""


import httplib2
from oslo.serialization import jsonutils

from glance.tests import functional


class TestRootApi(functional.FunctionalTest):

    def test_version_configurations(self):
        """Test that versioning is handled properly through all channels"""

        # v1 and v2 api enabled
        self.cleanup()
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = {'versions': [
            {
                'id': 'v2.2',
                'status': 'CURRENT',
                'links': [{'rel': 'self', 'href': url % '2'}],
            },
            {
                'id': 'v2.1',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self', 'href': url % '2'}],
            },
            {
                'id': 'v2.0',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self', 'href': url % '2'}],
            },
            {
                'id': 'v1.1',
                'status': 'CURRENT',
                'links': [{'rel': 'self', 'href': url % '1'}],
            },
            {
                'id': 'v1.0',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self', 'href': url % '1'}],
            },
        ]}
        versions_json = jsonutils.dumps(versions)

        # Verify version choices returned.
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)
        self.stop_servers()

        # v2 api enabled
        self.cleanup()
        self.api_server.enable_v1_api = False
        self.api_server.enable_v2_api = True
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = {'versions': [
            {
                'id': 'v2.2',
                'status': 'CURRENT',
                'links': [{'rel': 'self', 'href': url % '2'}],
            },
            {
                'id': 'v2.1',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self', 'href': url % '2'}],
            },
            {
                'id': 'v2.0',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self', 'href': url % '2'}],
            },
        ]}
        versions_json = jsonutils.dumps(versions)

        # Verify version choices returned.
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)
        self.stop_servers()

        # v1 api enabled
        self.cleanup()
        self.api_server.enable_v1_api = True
        self.api_server.enable_v2_api = False
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = {'versions': [
            {
                'id': 'v1.1',
                'status': 'CURRENT',
                'links': [{'rel': 'self', 'href': url % '1'}],
            },
            {
                'id': 'v1.0',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self', 'href': url % '1'}],
            },
        ]}
        versions_json = jsonutils.dumps(versions)

        # Verify version choices returned.
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)
        self.stop_servers()

    def test_version_variations(self):
        """Test that versioning is handled properly through all channels"""

        self.cleanup()
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = {'versions': [
            {
                'id': 'v2.2',
                'status': 'CURRENT',
                'links': [{'rel': 'self', 'href': url % '2'}],
            },
            {
                'id': 'v2.1',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self', 'href': url % '2'}],
            },
            {
                'id': 'v2.0',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self', 'href': url % '2'}],
            },
            {
                'id': 'v1.1',
                'status': 'CURRENT',
                'links': [{'rel': 'self', 'href': url % '1'}],
            },
            {
                'id': 'v1.0',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self', 'href': url % '1'}],
            },
        ]}
        versions_json = jsonutils.dumps(versions)
        images = {'images': []}
        images_json = jsonutils.dumps(images)

        # 0. GET / with no Accept: header
        # Verify version choices returned.
        # Bug lp:803260  no Accept header causes a 500 in glance-api
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        # 1. GET /images with no Accept: header
        # Verify version choices returned.
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        # 2. GET /v1/images with no Accept: header
        # Verify empty images list returned.
        path = 'http://%s:%d/v1/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(200, response.status)
        self.assertEqual(images_json, content)

        # 3. GET / with Accept: unknown header
        # Verify version choices returned. Verify message in API log about
        # unknown accept header.
        path = 'http://%s:%d/' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'unknown'}
        response, content = http.request(path, 'GET', headers=headers)
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        # 4. GET / with an Accept: application/vnd.openstack.images-v1
        # Verify empty image list returned
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.images-v1'}
        response, content = http.request(path, 'GET', headers=headers)
        self.assertEqual(200, response.status)
        self.assertEqual(images_json, content)

        # 5. GET /images with a Accept: application/vnd.openstack.compute-v1
        # header. Verify version choices returned. Verify message in API log
        # about unknown accept header.
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.compute-v1'}
        response, content = http.request(path, 'GET', headers=headers)
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        # 6. GET /v1.0/images with no Accept: header
        # Verify version choices returned
        path = 'http://%s:%d/v1.a/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)

        # 7. GET /v1.a/images with no Accept: header
        # Verify version choices returned
        path = 'http://%s:%d/v1.a/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)

        # 8. GET /va.1/images with no Accept: header
        # Verify version choices returned
        path = 'http://%s:%d/va.1/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        # 9. GET /versions with no Accept: header
        # Verify version choices returned
        path = 'http://%s:%d/versions' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        # 10. GET /versions with a Accept: application/vnd.openstack.images-v1
        # header. Verify version choices returned.
        path = 'http://%s:%d/versions' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.images-v1'}
        response, content = http.request(path, 'GET', headers=headers)
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        # 11. GET /v1/versions with no Accept: header
        # Verify 404 returned
        path = 'http://%s:%d/v1/versions' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(404, response.status)

        # Verify version choices returned
        path = 'http://%s:%d/v10' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        # 13. GET /images with a Accept: application/vnd.openstack.compute-v2
        # header. Verify version choices returned. Verify message in API log
        # about unknown version in accept header.
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.images-v10'}
        response, content = http.request(path, 'GET', headers=headers)
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        # 14. GET /v1.2/images with no Accept: header
        # Verify version choices returned
        path = 'http://%s:%d/v1.2/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(300, response.status)
        self.assertEqual(versions_json, content)

        self.stop_servers()
