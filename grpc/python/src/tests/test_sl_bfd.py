#------------------------------------------------------------------------------
# test_sl_bfd.py
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
    from feature_lib.slapi.sl_util import BfdUtil
except ImportError:
    from sl_api import SLApiClient
    from sl_api import BfdUtil

log = ApData.logger()

# Global variables
#------------------------------------------------------------------------------
client = None
json_params = None
#------------------------------------------------------------------------------

def setUpModule():
    global client, json_params

    json_params = ApData.json_params
    assert json_params

    host, port = ApData.host, ApData.port
    client = SLApiClient(host, port, json_params['global_init'])


def tearDownModule():
    client.cleanup()
    if ApData.sim_clean and ApData.vxr:
        ApData.vxr.clean()


class TestSuite_005_BFD_IPv4(unittest.TestCase):
    AF = 4
    JSON_TEST = 'batch_bfd_singlehop'
    # GRPC channel used for BFD notifications
    bfd_notif = {}
    # threading.Event() used to sync threads
    bfd_event = {}
    # thread count; increments every time we spawn a new BFD reg thread
    # Note: only one BFD Notif session is allowed at any time. Last one
    # takes over the previous session.
    thread_count = 0

    def setUp(self):
        super(TestSuite_005_BFD_IPv4, self).setUp()
        self.bfd_params = (
            json_params[self.JSON_TEST],
            json_params['next_hops'],
            self.AF,
        )
        self.bfd_get = json_params['bfd_get']

    def test_000_get_globals(self):
        # Get Global BFD info
        response = client.client.global_bfd_get(self.AF)
        err = BfdUtil.print_bfd_globals(self.AF, response)
        self.assertTrue(err)

    def test_001_bfd_reg_notif(self):
        #
        # Setup a BFD notification channel
        #
        def target():
            with client.notif_channel() as channel:
                for notif in channel.bfd_get_notif(self.AF):
                    assert BfdUtil.validate_bfd_notif(notif)
                    print(notif)

        # TODO: Since no BFD notifications produced this test is pointless
        # t = threading.Thread(target=target)
        # t.start()

    def test_002_bfd_register(self):
        response = client.client.bfd_register_oper(self.AF)
        err = BfdUtil.validate_bfd_regop_response(response)
        self.assertTrue(err)

    def test_003_bfd_add(self):
        response = client.client.bfd_add(*self.bfd_params)
        err = BfdUtil.validate_bfd_response(response)
        self.assertTrue(err)

    def test_004_bfd_update(self):
        # Can not change the key in updates. Change a non-key attribute:
        json_params[self.JSON_TEST]['sessions'][0]['cfg_detect_multi'] = 10
        response = client.client.bfd_update(*self.bfd_params)
        err = BfdUtil.validate_bfd_response(response)
        self.assertTrue(err)

    def test_005_get_stats(self):
        # Get Global BFD stats
        response = client.client.bfd_global_get_stats(self.AF)
        err = BfdUtil.print_bfd_stats(self.AF, response)
        self.assertTrue(err)

        # Not a test case
    def bfd_get_info(self, get_info):
        print(get_info["_description"])
        response = client.client.bfd_session_get(get_info, self.AF)
        err = BfdUtil.validate_bfd_get_response(response, self.AF)
        self.assertTrue(err)

    def test_006_01_bfd_get_exact_match(self):
        get_info = self.bfd_get["get_exact_bfd"]
        self.bfd_get_info(get_info)

    def test_006_02_bfd_get_firstN(self):
        get_info = self.bfd_get["get_firstN_bfd"]
        self.bfd_get_info(get_info)

    def test_006_03_bfd_get_nextN_with_specified(self):
        get_info = self.bfd_get["get_nextN_include_bfd"]
        self.bfd_get_info(get_info)

    def test_006_04_bfd_get_nextN_after_specified(self):
        get_info = self.bfd_get["get_nextN_bfd"]
        self.bfd_get_info(get_info)

    def test_006_05_bfd_get_all(self):
        total_bfds = 0
        get_info = self.bfd_get["get_firstN_bfd"]
        response = client.client.bfd_session_get(get_info, self.AF)
        err = BfdUtil.validate_bfd_get_response(response, self.AF)
        self.assertTrue(err)
        total_bfds = total_bfds + len(response.Entries)
        get_info = self.bfd_get["get_nextN_bfd"]
        if_name_temp = get_info["if_name"]
        type_temp = get_info["type"]
        nbr_temp = get_info["v%d_nbr" % self.AF]
        src_temp = get_info["v%d_src" % self.AF]
        vrf_name_temp = get_info["vrf_name"]
        while (len(response.Entries)>0) and not response.Eof:
            # Get key from last entry
            get_info["if_name"] = response.Entries[-1].Key.Interface.Name
            get_info["type"] = response.Entries[-1].Key.Type
            get_info["v%d_nbr" % self.AF] = response.Entries[-1].Key.NbrAddr
            get_info["v%d_src" % self.AF] = response.Entries[-1].Key.SourceAddr
            get_info["vrf_name"] = response.Entries[-1].Key.VrfName
            # Resend the request
            response = client.client.bfd_session_get(get_info, self.AF)
            err = BfdUtil.validate_bfd_get_response(response, self.AF)
            total_bfds = total_bfds + len(response.Entries)
            self.assertTrue(err)
        get_info["if_name"] = if_name_temp
        get_info["type"] = type_temp
        get_info["v%d_nbr" % self.AF] = nbr_temp
        get_info["v%d_src" % self.AF] = src_temp
        get_info["vrf_name"] = vrf_name_temp
        print("Total VRFs read: %d" %(total_bfds))

    def test_007_bfd_delete(self):
        response = client.client.bfd_delete(*self.bfd_params)
        err = BfdUtil.validate_bfd_response(response)
        self.assertTrue(err)

    def test_008_bfd_eof(self):
        response = client.client.bfd_eof_oper(self.AF)
        err = BfdUtil.validate_bfd_regop_response(response)
        self.assertTrue(err)

    def test_009_bfd_unregister(self):
        response = client.client.bfd_unregister_oper(self.AF)
        err = BfdUtil.validate_bfd_regop_response(response)
        self.assertTrue(err)

class TestSuite_006_BFD_IPv6(TestSuite_005_BFD_IPv4):
    AF = 6
    # Inherit all test cases

#
# Not Supported, turning off for now
#
#class TestSuite_007_BFD_IPv4_Multi_Hop(TestSuite_005_BFD_IPv4):
#    JSON_TEST = 'batch_bfd_multihop'
#    # Inherit all test cases

#
# Not Supported, turning off for now
#
#class TestSuite_008_BFD_IPv6(TestSuite_007_BFD_IPv4_Multi_Hop):
#    AF = 6
#    # Inherit all test cases
