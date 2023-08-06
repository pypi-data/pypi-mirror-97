# Copyright 2011-2013 OpenStack Foundation
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

from unittest import mock

from oslo_config import cfg

import glance_store as store
from glance_store import backend
from glance_store import location
from glance_store import multi_backend
from glance_store.tests import base


class TestStoreBase(base.StoreBaseTest):

    def setUp(self):
        super(TestStoreBase, self).setUp()
        self.config(default_store='file', group='glance_store')

    @mock.patch.object(store.driver, 'LOG')
    def test_configure_does_not_raise_on_missing_driver_conf(self, mock_log):
        self.config(stores=['file'], group='glance_store')
        self.config(filesystem_store_datadir=None, group='glance_store')
        self.config(filesystem_store_datadirs=None, group='glance_store')
        for (__, store_instance) in backend._load_stores(self.conf):
            store_instance.configure()
            mock_log.warning.assert_called_once_with(
                "Failed to configure store correctly: Store filesystem "
                "could not be configured correctly. Reason: Specify "
                "at least 'filesystem_store_datadir' or "
                "'filesystem_store_datadirs' option Disabling add method.")


class TestMultiStoreBase(base.MultiStoreBaseTest):
    _CONF = multi_backend.CONF

    def setUp(self):
        super(TestMultiStoreBase, self).setUp()
        enabled_backends = {
            "fast": "file",
            "cheap": "file",
        }

        self.reserved_stores = {
            'consuming_service_reserved_store': 'file'
        }

        self.conf = self._CONF
        self.conf(args=[])
        self.conf.register_opt(cfg.DictOpt('enabled_backends'))
        self.config(enabled_backends=enabled_backends)

        store.register_store_opts(self.conf,
                                  reserved_stores=self.reserved_stores)
        self.config(default_backend='file1', group='glance_store')

        # Ensure stores + locations cleared
        location.SCHEME_TO_CLS_BACKEND_MAP = {}

        store.create_multi_stores(self.conf,
                                  reserved_stores=self.reserved_stores)
        self.addCleanup(setattr, location, 'SCHEME_TO_CLS_BACKEND_MAP',
                        dict())
        self.addCleanup(self.conf.reset)

    def test_reserved_stores_loaded(self):
        # assert global map has reserved stores registered
        store = multi_backend.get_store_from_store_identifier(
            'consuming_service_reserved_store')

        self.assertIsNotNone(store)
        self.assertEqual(self.reserved_stores, multi_backend._RESERVED_STORES)
        # verify that store config group in conf file is same as
        # reserved store name
        self.assertEqual('consuming_service_reserved_store',
                         store.backend_group)
