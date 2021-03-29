#------------------------------------------------------------------------------
# test_sl_intf.py
#
# January 2020, Arshan Hashemi
#
# Copyright (c) 2019-2020 by Cisco Systems, Inc.
# All rights reserved.
#------------------------------------------------------------------------------
import threading
import unittest
import os
import time

try:
    from base_ap import ApData
except ImportError:
    from .base_ap import ApData

try:
    from feature_lib.slapi.slapi_client import SLApiClient
    from feature_lib.slapi.sl_util import IntfUtil
except ImportError:
    from sl_api import SLApiClient
    from sl_api import IntfUtil

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
    client = SLApiClient(host, port, json_params['global_init'])


def tearDownModule():
    client.cleanup()
    if ApData.sim_clean and ApData.vxr:
        ApData.vxr.clean()


class TestSuite_009_INTERFACE(unittest.TestCase):
    # GRPC channel used for Interface notifications
    intf_notif = None
    # threading.Event() used to sync threads
    intf_event = None
    # thread count; increments every time we spawn a new Interface reg thread
    # Note: only one Interface Notif session is allowed at any time. Last one
    # takes over the previous session.
    thread_count = 0

    def setUp(self):
        super(TestSuite_009_INTERFACE, self).setUp()
        self.intf_params = json_params['batch_interfaces']
        self.intf_get = json_params['intf_get']
        self.intf_neg_get = json_params['intf_neg_get']

    def test_000_get_globals(self):
        # Get Global Interface info
        response = client.client.intf_global_get()
        err = IntfUtil.print_intf_globals(response)
        self.assertTrue(err)

    def test_001_intf_reg_notif(self):
        #
        # Setup an Interface notification channel
        #

        #
        # Setup a BFD notification channel
        #
        notif_stream = None
        event = threading.Event()
        def target():
            nonlocal notif_stream
            with client.notif_channel() as channel:
                notif_stream = channel.intf_get_notif()
                event.set()
                for notif in notif_stream:
                    assert IntfUtil.validate_intf_notif(notif)
                    print(notif)

        t = threading.Thread(target=target)
        t.start()
        # TODO: Since no intf notifications produced this test is pointless
        event.wait()
        notif_stream.cancel()

    def test_002_intf_register(self):
        response = client.client.intf_register_op()
        err = IntfUtil.validate_intf_regop_response(response)
        self.assertTrue(err)

    def test_003_intf_subscribe(self):
        response = client.client.intf_subscribe(self.intf_params)
        err = IntfUtil.validate_intf_response(response)
        self.assertTrue(err)

    def test_005_get_stats(self):
        # Get Global Intf stats
        response = client.client.intf_global_get_stats()
        err = IntfUtil.print_intf_stats(response)
        self.assertTrue(err)

        # Not a test case
    def intf_get_info(self, get_info, positive=True):
        print(get_info["_description"])
        response = client.client.intf_get(get_info)
        err = IntfUtil.validate_intf_get_response(response)
        if positive:
            self.assertTrue(err)
        else:
            self.assertFalse(err)

    def test_006_01_intf_get_exact_match(self):
        get_info = self.intf_get["get_exact_intf"]
        self.intf_get_info(get_info)

    def test_006_02_intf_get_firstN(self):
        get_info = self.intf_get["get_firstN_intf"]
        self.intf_get_info(get_info)

    def test_006_03_intf_get_nextN_with_specified(self):
        get_info = self.intf_get["get_nextN_include_intf"]
        self.intf_get_info(get_info)

    def test_006_04_intf_get_nextN_after_specified(self):
        get_info = self.intf_get["get_nextN_intf"]
        self.intf_get_info(get_info)

    def test_006_05_intf_get_all(self):
        total_intfs = 0
        get_info = self.intf_get["get_firstN_intf"]
        response = client.client.intf_get(get_info)
        err = IntfUtil.validate_intf_get_response(response)
        self.assertTrue(err)
        total_intfs = total_intfs + len(response.Entries)
        get_info = self.intf_get["get_nextN_intf"]
        if_name_temp = get_info["if_name"]
        while (len(response.Entries)>0) and not response.Eof:
            # Get key from last entry
            get_info["if_name"] = response.Entries[-1].Key.Interface.Name
            # Resend the request
            response = client.client.intf_get(get_info)
            err = IntfUtil.validate_intf_get_response(response)
            total_intfs = total_intfs + len(response.Entries)
            self.assertTrue(err)
        get_info["if_name"] = if_name_temp
        print("Total interfaces read: %d" %(total_intfs))

    # Non-existent interface
    def test_006_neg_01_intf_get_exact_match(self):
        get_info = self.intf_neg_get["get_exact_intf_neg1"]
        self.intf_get_info(get_info, False)

    # Non-subscribed interface
    def test_006_neg_02_intf_get_exact_match(self):
        get_info = self.intf_neg_get["get_exact_intf_neg2"]
        self.intf_get_info(get_info, False)

    def test_007_intf_unsubscribe(self):
        response = client.client.intf_unsubscribe(self.intf_params)
        err = IntfUtil.validate_intf_response(response)
        self.assertTrue(err)

    def test_008_intf_eof(self):
        response = client.client.intf_eof_oper()
        err = IntfUtil.validate_intf_regop_response(response)
        self.assertTrue(err)

    def test_009_intf_unregister(self):
        response = client.client.intf_unregister_op()
        err = IntfUtil.validate_intf_regop_response(response)
        self.assertTrue(err)
