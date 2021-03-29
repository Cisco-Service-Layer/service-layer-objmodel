#------------------------------------------------------------------------------
# test_sl_route.py
#
# January 2020, Arshan Hashemi
#
# Copyright (c) 2019-2020 by Cisco Systems, Inc.
# All rights reserved.
#------------------------------------------------------------------------------
import unittest
import os
import time

try:
    from base_ap import ApData
except ImportError:
    from .base_ap import ApData

try:
    # If running in Cafy Env
    from feature_lib.slapi.slapi_client import SLApiClient
    from feature_lib.slapi.sl_util import RouteUtil
except ImportError:
    # Running outside of Cafy Env
    from sl_api import SLApiClient
    from sl_api import RouteUtil

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


class TestSuite_001_Route_IPv4(unittest.TestCase):
    AF = 4
    STREAM = False

    def setUp(self):
        super(TestSuite_001_Route_IPv4, self).setUp()
        self.route_info = json_params['batch_v%d_route' % self.AF]
        self.route_label_info = json_params[
                'batch_v%d_route_label' % self.AF]
        self.vrf_batch = json_params['batch_v%d_vrf' % self.AF]
        self.route_get_info = json_params['route_get']
        self.vrf_get = json_params['vrf_get']
        self.path_info = {'paths': json_params['paths'], 'next_hops': json_params['next_hops']}

    def test_000_get_globals(self):
        client.route_global_get(self.AF)

    def test_001_vrf_register(self):
        client.vrf_register(self.vrf_batch)

    def test_002_00_route_add(self):
        for info in [self.route_info, self.route_label_info]:
            client.route_add(info, stream=self.STREAM, af=self.AF, **self.path_info)

    def test_002_01_l3route_notif_channel_setup(self):
        # Setup a grpc channel
        with client.notif_channel() as channel:
            for notif in channel.l3route_get_notif(self.AF):
                # TODO: Verify notifications follow semantics of RPC and then
                #       signal to request iterator to raise stop iteration 
                print(notif)

    def test_003_00_route_update(self, name = None):
        temp = None
        if name != None:
            # swap in new path
            temp = json_params['batch_v%d_route' % self.AF]['path']
            json_params['batch_v%d_route' % self.AF]['path'] = name

        try:
            for info in [self.route_info, self.route_label_info]:
                client.route_update(info, stream=self.STREAM, af=self.AF, **self.path_info)
        finally:
            # Ensure this is restored even if above fails
            if name != None:
                json_params['batch_v%d_route' % self.AF]['path'] = temp

    def test_003_01_route_update_nhlfe_connected(self):
        self.test_003_00_route_update("path_nhlfe_connected")

    def test_003_02_route_update_nhlfe_ecmp(self):
        self.test_003_00_route_update("path_nhlfe_ecmp")

    def test_003_03_route_update_nhlfe_non_connected(self):
        self.test_003_00_route_update("path_nhlfe_non_connected")

    def test_003_04_route_update_route_connected(self):
        self.test_003_00_route_update("path_route_connected")

    def test_003_05_route_update_route_ecmp(self):
        self.test_003_00_route_update("path_route_ecmp")

    def test_003_06_route_update_route_non_connected(self):
        self.test_003_00_route_update("path_route_non_connected")

    def test_003_07_route_update_route_primary_with_labels_remote_pq_lfa(self):
        self.test_003_00_route_update("path_route_primary_with_labels_remote_pq_lfa")

    def test_003_08_route_update_route_primary_with_lfa(self):
        self.test_003_00_route_update("path_route_primary_with_lfa")

    def test_004_01_route_get_exact_match(self):
        get_info = self.route_get_info["get_exact_route"]
        client.route_get(get_info, self.AF)

    def test_004_02_route_get_firstN(self):
        get_info = self.route_get_info["get_firstN_routes"]
        client.route_get(get_info, self.AF)

    def test_004_03_route_get_nextN_with_specified(self):
        get_info = self.route_get_info["get_nextN_include_route"]
        client.route_get(get_info, self.AF)

    def test_004_03_route_get_nextN_after_specified(self):
        get_info = self.route_get_info["get_nextN_route"]
        client.route_get(get_info, self.AF)

    def test_004_04_route_get_all(self):
        get_info = self.route_get_info["get_firstN_routes"]
        client.route_get_all(get_info, self.AF)

    def test_004_05_route_get_stream(self):
        get_infos = (self.route_get_info[name] for name in ["get_firstN_routes",
            "get_exact_route", "get_nextN_include_route"])
        
        # Returns response iterator
        responses = client.route_get(get_infos, self.AF, stream=True)

        # Consume the iterator
        for _ in responses:
            pass

    def test_005_route_stats_get(self):
        client.route_global_stats_get(self.AF)

    def test_006_01_vrf_get_exact_match(self):
        get_info = self.vrf_get["get_exact_vrf"]
        for stats in [False, True]:
            client.vrf_get(get_info, stats=stats, af=self.AF)

    def test_006_02_vrf_get_firstN(self):
        get_info = self.vrf_get["get_firstN_vrf"]
        for stats in [False, True]:
            client.vrf_get(get_info, stats=stats, af=self.AF)

    def test_006_03_vrf_get_nextN_with_specified(self):
        get_info = self.vrf_get["get_nextN_include_vrf"]
        for stats in [False, True]:
            client.vrf_get(get_info, stats=stats, af=self.AF)

    def test_006_04_vrf_get_nextN_after_specified(self):
        get_info = self.vrf_get["get_nextN_vrf"]
        for stats in [False, True]:
            client.vrf_get(get_info, stats=stats, af=self.AF)

    def test_006_05_vrf_get_all(self):
        get_info = self.vrf_get["get_firstN_vrf"]
        for stats in [False, True]:
            client.vrf_get_all(get_info, stats=stats, af=self.AF)

    def test_007_route_delete(self):
        for info in [self.route_info, self.route_label_info]:
            client.route_delete(info, stream=self.STREAM, af=self.AF, **self.path_info)

    def test_008_vrf_registration_eof(self):
        client.vrf_registration_eof(self.vrf_batch)

    def test_009_vrf_unregistration(self):
        client.vrf_unregister(self.vrf_batch)


class TestSuite_001_Route_IPv4_Stream(TestSuite_001_Route_IPv4):
    "This class simply inherits the entire v4 class"
    AF = 4
    STREAM = True


class TestSuite_002_Route_IPv6(TestSuite_001_Route_IPv4):
    "This class simply inherits the entire v4 class"
    AF = 6


class TestSuite_002_Route_IPv6_Stream(TestSuite_001_Route_IPv4):
    "This class simply inherits the entire v4 class"
    AF = 6
    STREAM = True

