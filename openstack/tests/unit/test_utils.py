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

import logging
import mock
import sys
import testtools

import fixtures

from openstack import utils


class Test_enable_logging(testtools.TestCase):

    def setUp(self):
        super(Test_enable_logging, self).setUp()
        self.openstack_logger = mock.Mock()
        self.openstack_logger.handlers = []
        self.ksa_logger_1 = mock.Mock()
        self.ksa_logger_1.handlers = []
        self.ksa_logger_2 = mock.Mock()
        self.ksa_logger_2.handlers = []
        self.ksa_logger_3 = mock.Mock()
        self.ksa_logger_3.handlers = []
        self.fake_get_logger = mock.Mock()
        self.fake_get_logger.side_effect = [
            self.openstack_logger,
            self.ksa_logger_1,
            self.ksa_logger_2,
            self.ksa_logger_3
        ]
        self.useFixture(
            fixtures.MonkeyPatch('logging.getLogger', self.fake_get_logger))

    def _console_tests(self, level, debug, stream):

        utils.enable_logging(debug=debug, stream=stream)

        self.assertEqual(self.openstack_logger.addHandler.call_count, 1)
        self.openstack_logger.setLevel.assert_called_with(level)

    def _file_tests(self, level, debug):
        file_handler = mock.Mock()
        self.useFixture(
            fixtures.MonkeyPatch('logging.FileHandler', file_handler))
        fake_path = "fake/path.log"

        utils.enable_logging(debug=debug, path=fake_path)

        file_handler.assert_called_with(fake_path)
        self.assertEqual(self.openstack_logger.addHandler.call_count, 1)
        self.openstack_logger.setLevel.assert_called_with(level)

    def test_none(self):
        utils.enable_logging(debug=True)
        self.fake_get_logger.assert_has_calls([])
        self.openstack_logger.setLevel.assert_called_with(logging.DEBUG)
        self.assertEqual(self.openstack_logger.addHandler.call_count, 1)
        self.assertIsInstance(
            self.openstack_logger.addHandler.call_args_list[0][0][0],
            logging.StreamHandler)

    def test_debug_console_stderr(self):
        self._console_tests(logging.DEBUG, True, sys.stderr)

    def test_warning_console_stderr(self):
        self._console_tests(logging.INFO, False, sys.stderr)

    def test_debug_console_stdout(self):
        self._console_tests(logging.DEBUG, True, sys.stdout)

    def test_warning_console_stdout(self):
        self._console_tests(logging.INFO, False, sys.stdout)

    def test_debug_file(self):
        self._file_tests(logging.DEBUG, True)

    def test_warning_file(self):
        self._file_tests(logging.INFO, False)


class Test_urljoin(testtools.TestCase):

    def test_strings(self):
        root = "http://www.example.com"
        leaves = "foo", "bar"

        result = utils.urljoin(root, *leaves)
        self.assertEqual(result, "http://www.example.com/foo/bar")

    def test_with_none(self):
        root = "http://www.example.com"
        leaves = "foo", None

        result = utils.urljoin(root, *leaves)
        self.assertEqual(result, "http://www.example.com/foo/")
