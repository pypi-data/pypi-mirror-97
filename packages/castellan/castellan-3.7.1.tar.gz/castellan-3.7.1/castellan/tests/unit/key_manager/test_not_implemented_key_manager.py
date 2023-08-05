# Copyright (c) 2015 The Johns Hopkins University/Applied Physics Laboratory
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

"""
Test cases for the not implemented key manager.
"""

from castellan.key_manager import not_implemented_key_manager
from castellan.tests.unit.key_manager import test_key_manager


class NotImplementedKeyManagerTestCase(test_key_manager.KeyManagerTestCase):

    def _create_key_manager(self):
        return not_implemented_key_manager.NotImplementedKeyManager()

    def test_create_key(self):
        self.assertRaises(NotImplementedError,
                          self.key_mgr.create_key, None)

    def test_create_key_pair(self):
        self.assertRaises(NotImplementedError,
                          self.key_mgr.create_key_pair, None, None, None)

    def test_store(self):
        self.assertRaises(NotImplementedError,
                          self.key_mgr.store, None, None)

    def test_copy(self):
        self.assertRaises(NotImplementedError,
                          self.key_mgr.copy, None, None)

    def test_get(self):
        self.assertRaises(NotImplementedError,
                          self.key_mgr.get, None, None)

    def test_list(self):
        self.assertRaises(NotImplementedError,
                          self.key_mgr.list, None)

    def test_delete(self):
        self.assertRaises(NotImplementedError,
                          self.key_mgr.delete, None, None)
