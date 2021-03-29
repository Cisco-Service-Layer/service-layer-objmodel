#------------------------------------------------------------------------------
# test_sl_l2_route.py
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
    from feature_lib.slapi.slapi_client import SLApiClient
    from feature_lib.slapi.sl_util import L2RouteUtil
    from feature_lib.slapi.sl_util import BDUtil
    from feature_lib.slapi.genpy import sl_common_types_pb2
    from feature_lib.slapi.genpy import sl_l2_route_pb2
except ImportError:
    from sl_api import SLApiClient
    from sl_api import L2RouteUtil
    from sl_api import BDUtil
    from genpy import sl_common_types_pb2
    from genpy import sl_l2_route_pb2


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


class TestSuite_010_BD_reg(unittest.TestCase):
    bdAry = ["bd0", "bd1", "bd2"]

    def test_002_multiple_bd_reg(self):
        oper = 'SL_REGOP_REGISTER'
        count = 2
        bdRegOper = json_params["bdRegOper"]
        response = client.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  BDUtil.validate_bdreg_response(response)
        self.assertTrue(err)

    def test_003_stream_mac_add(self):
        oper = sl_common_types_pb2.SL_OBJOP_ADD
        count = 5
        rtype = sl_l2_route_pb2.SL_L2_ROUTE_MAC
        is_macip = False
        g_route_attrs = json_params["g_route_attrs"]

        client.l2_route_op_stream(oper, count, rtype, is_macip,
                                  self.bdAry, g_route_attrs)

    def test_004_stream_mac_del(self):
        oper = sl_common_types_pb2.SL_OBJOP_DELETE
        count = 5
        rtype = sl_l2_route_pb2.SL_L2_ROUTE_MAC
        is_macip = False
        g_route_attrs = json_params["g_route_attrs"]

        client.l2_route_op_stream(oper, count, rtype, is_macip,
                                  self.bdAry, g_route_attrs)



class TestSuite_011_L2Route_operation(unittest.TestCase):
    bdAry = ["bd0", "bd1", "bd2"]

    def test_000_global_reg(self):

        oper = 'SL_REGOP_REGISTER'
        g_route_attrs = json_params["g_route_attrs"]
        client.client.l2_global_reg_unreg_handler(oper, g_route_attrs)

    def test_001_global_unreg(self):
        oper = 'SL_REGOP_UNREGISTER'
        g_route_attrs = json_params["g_route_attrs"]
        client.client.l2_global_reg_unreg_handler(oper, g_route_attrs)

    def test_002_multiple_bd_reg(self):
        oper = 'SL_REGOP_REGISTER'
        count = 2

        bdRegOper = json_params["bdRegOper"]
        response = client.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  BDUtil.validate_bdreg_response(response)
        self.assertTrue(err)

    def test_003_l2route_notif_channel_setup(self):
        # If BdAll set to True, BdName is not assigned (oneof)
        BdAll, BdName = True, "bd0"
        g_oper = json_params["g_route_attrs"]["g_oper"]

        # Setup a grpc channel
        with client.notif_channel() as channel:
            notifs = channel.l2route_get_notif(g_oper, BdAll, BdName)
            for notif in notifs: 
                assert L2RouteUtil.validate_l2route_notif(notif)
                # TODO: Verify notifications follow semantics of RPC and then
                #       signal to request iterator to raise stop iteration
                print(notif)

    def test_004_global_eof(self):
        oper = 'SL_REGOP_EOF'
        g_route_attrs = json_params["g_route_attrs"]
        client.client.l2_global_reg_unreg_handler(oper, g_route_attrs)

    def test_005_multiple_mac_macip_route_add(self):
        oper = sl_common_types_pb2.SL_OBJOP_ADD
        count = 5
        rtype = sl_l2_route_pb2.SL_L2_ROUTE_MAC
        is_macip = False
        g_route_attrs = json_params["g_route_attrs"]

        for bd in self.bdAry:
            response = client.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  L2RouteUtil.validate_l2route_response(response)
            self.assertTrue(err)

        is_macip = True
        for bd in self.bdAry:
            response = client.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  L2RouteUtil.validate_l2route_response(response)
            self.assertTrue(err)

        rtype = sl_l2_route_pb2.SL_L2_ROUTE_IMET
        is_macip = False
        for bd in self.bdAry:
            response = client.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  L2RouteUtil.validate_l2route_response(response)
            self.assertTrue(err)
        time.sleep(3)

    def test_006_multiple_mac_macip_route_del(self):
        oper = sl_common_types_pb2.SL_OBJOP_DELETE
        count = 2
        rtype = sl_l2_route_pb2.SL_L2_ROUTE_MAC
        is_macip = False
        g_route_attrs = json_params["g_route_attrs"]

        for bd in self.bdAry:
            response = client.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  L2RouteUtil.validate_l2route_response(response)
            self.assertTrue(err)

        is_macip = True
        for bd in self.bdAry:
            response = client.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  L2RouteUtil.validate_l2route_response(response)
            self.assertTrue(err)

        rtype = sl_l2_route_pb2.SL_L2_ROUTE_IMET
        is_macip = False
        for bd in self.bdAry:
            response = client.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  L2RouteUtil.validate_l2route_response(response)
            self.assertTrue(err)

    def test_007_multiple_bd_unreg(self):
        oper = 'SL_REGOP_UNREGISTER'
        count = 2
        bdRegOper = json_params["bdRegOper"]
        response = client.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  BDUtil.validate_bdreg_response(response)
        self.assertTrue(err)

    def test_008_globals_get(self):
        response = client.client.l2_globals_get()
        err = response.ErrStatus
        self.assertTrue(err)

class TestSuite_012_BD_unreg(unittest.TestCase):

    def test_001_single_bd_unreg(self):
        oper = 'SL_REGOP_UNREGISTER'
        count = 0
        bdRegOper = json_params["bdRegOper"]
        response = client.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  BDUtil.validate_bdreg_response(response)
        self.assertTrue(err)

class TestSuite_013_BD_eof(unittest.TestCase):

    def test_000_bd_eof(self):
        oper = 'SL_REGOP_EOF'
        count = 1
        bdRegOper = json_params["bdRegOper"]
        response = client.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  BDUtil.validate_bdreg_response(response)
        self.assertTrue(err)

