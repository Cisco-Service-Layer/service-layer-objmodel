#------------------------------------------------------------------------------
# test_sl_global.py
#
# January 2020, Arshan Hashemi
#
# Copyright (c) 2019-2020 by Cisco Systems, Inc.
# All rights reserved.
#------------------------------------------------------------------------------
import unittest
import functools
import json
import os
import time

try:
    from base_ap import ApData
except ImportError:
    from .base_ap import ApData

try:
    from feature_lib.slapi.slapi_client import SLApiClient
    from feature_lib.slapi.sl_util import print_globals
except ImportError:
    from sl_api import SLApiClient
    from sl_api import print_globals


log = ApData.logger()

# Global variables
#------------------------------------------------------------------------------
client = None
json_params = None
#------------------------------------------------------------------------------

def setUpModule():
    global client, json_params

    json_params = ApData.json_params

    host, port = ApData.host, ApData.port
    client = SLApiClient(host, port, json_params["do_global_init"], json_params['global_init'])


def tearDownModule():
    client.cleanup()
    if ApData.sim_clean and ApData.vxr:
        ApData.vxr.clean()


class TestSuite_000_Global(unittest.TestCase):
    def test_001_get_globals(self):
        # Get Global info
        response = client.client.global_get()
        err = print_globals(response)
        self.assertTrue(err)


if __name__ == '__main__':
    unittest.main()

