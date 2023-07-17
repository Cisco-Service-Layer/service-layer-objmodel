# ------------------------------------------------------------------------------
# test_sl_mpls.py
#
# January 2020, Arshan Hashemi
#
# Copyright (c) 2019-2023 by Cisco Systems, Inc.
# All rights reserved.
# ------------------------------------------------------------------------------
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
    from feature_lib.slapi.sl_util import MplsUtil
    from feature_lib.slapi.genpy import sl_mpls_pb2
except ImportError:
    # Running outside of Cafy Env
    from sl_api import SLApiClient
    from sl_api import MplsUtil
    from genpy import sl_mpls_pb2

log = ApData.logger()
# Global variables
# ------------------------------------------------------------------------------
client = None
json_params = None
# ------------------------------------------------------------------------------


def setUpModule():
    global client, json_params

    json_params = ApData.json_params

    host, port = ApData.host, ApData.port

    client = SLApiClient(host, port, json_params["do_global_init"], json_params['global_init'])


def tearDownModule():
    client.cleanup()
    if ApData.sim_clean and ApData.vxr:
       ApData.vxr.clean()


class TestSuite_003_ILM_IPv4(unittest.TestCase):
    AF = 4
    STREAM = False
    validated_count = 0

    @classmethod
    def setUpClass(cls):
        super(TestSuite_003_ILM_IPv4, cls).setUpClass()
        cls.ilm_entry = json_params["batch_ilm"]
        cls.lbl_blk_params1 = json_params["batch_mpls_lbl_block"]
        cls.lbl_blk_params2 = json_params["mpls_lbl_block_srgb_3"]
        cls.ilm_get_info = json_params["ilm_get"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_00_blk_add(self):
        client.label_block_add(self.lbl_blk_params1)

    def test_002_01_blk_add(self):
        client.label_block_add(self.lbl_blk_params2)

    def test_003_ilm_add(self):
        client.ilm_add(self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info)

    def test_004_00_ilm_update(self, name=None):
        temp = None
        if name != None:
            temp = json_params["batch_ilm"]["label_path"]["path"]
            json_params["batch_ilm"]["label_path"]["path"] = name
        try:
            client.ilm_update(
                self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info
            )
        finally:
            if name != None:
                json_params["batch_ilm"]["label_path"]["path"] = temp

    def test_004_01_ilm_update_nhlfe_connected(self):
        self.test_004_00_ilm_update("path_nhlfe_connected")

    def test_004_02_ilm_update_nhlfe_ecmp(self):
        self.test_004_00_ilm_update("path_nhlfe_ecmp")

    # Turn off for now - Not supported
    # def test_004_03_ilm_update_nhlfe_non_connected(self):
    #    self.test_004_00_ilm_update("path_nhlfe_non_connected")

    def test_004_04_ilm_update_route_connected(self):
        self.test_004_00_ilm_update("path_route_connected")

    def test_004_05_ilm_update_route_ecmp(self):
        self.test_004_00_ilm_update("path_route_ecmp")

    # Turn off for now - Not supported
    # def test_004_06_ilm_update_route_non_connected(self):
    #    self.test_004_00_ilm_update("path_route_non_connected")

    def test_004_07_ilm_update_route_primary_with_labels_remote_pq_lfa(self):
        self.test_004_00_ilm_update("path_route_primary_with_labels_remote_pq_lfa")

    def test_004_08_ilm_update_route_primary_with_lfa(self):
        self.test_004_00_ilm_update("path_route_primary_with_lfa")

    def test_004_09_ilm_update_route_lookup(self):
        temp = json_params["paths"]["path_route_lookup"][0]["label_action"]
        if self.AF == 6:
            json_params["paths"]["path_route_lookup"][0][
                "label_action"
            ] = sl_mpls_pb2.SL_LABEL_ACTION_POP_AND_LOOKUP_IPV6
        self.test_004_00_ilm_update("path_route_lookup")
        # Restore
        if self.AF == 6:
            json_params["paths"]["path_route_lookup"][0]["label_action"] = temp

    def test_005_get_stats(self):
        # Get Global MPLS stats
        response = client.client.mpls_global_get_stats()
        err = MplsUtil.print_mpls_stats(response)
        self.assertTrue(err)

    def test_006_01_ilm_get_exact_match(self):
        get_info = self.ilm_get_info["get_exact_ilm"]
        client.ilm_get(get_info)

    def test_006_02_ilm_get_firstN(self):
        get_info = self.ilm_get_info["get_firstN_ilm"]
        client.ilm_get(get_info)

    def test_006_03_ilm_get_nextN_with_specified(self):
        get_info = self.ilm_get_info["get_nextN_include_ilm"]
        client.ilm_get(get_info)

    def test_006_04_ilm_get_nextN_after_specified(self):
        get_info = self.ilm_get_info["get_nextN_ilm"]
        client.ilm_get(get_info)

    def test_006_05_ilm_get_all(self):
        firstN = self.ilm_get_info["get_firstN_ilm"]
        client.ilm_get_all(firstN)

    def test_006_06_ilm_get_stream(self):
        # Pack 3 requests
        get_infos = (
            self.ilm_get_info[name]
            for name in ["get_firstN_ilm", "get_exact_ilm", "get_nextN_include_ilm"]
        )

        # Returns respons iterator
        responses = client.ilm_get(get_infos, stream=True)

        # Do not need to do extra verification
        for _ in responses:
            pass

    def test_007_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info
        )

    def test_008_01_lbl_blk_get_exact_match(self):
        get_info = self.lbl_blk_get["get_exact_lbl_blk"]
        client.label_block_get(get_info)

    def test_008_02_lbl_blk_get_exact_match(self):
        get_info = self.lbl_blk_get["get_exact_lbl_blk_client_name"]
        client.label_block_get(get_info)

    def test_008_03_lbl_blk_get_firstN(self):
        get_info = self.lbl_blk_get["get_firstN_lbl_blk"]
        client.label_block_get(get_info)

    def test_008_04_lbl_blk_get_nextN_with_specified(self):
        get_info = self.lbl_blk_get["get_nextN_include_lbl_blk"]
        client.label_block_get(get_info)

    def test_008_05_lbl_blk_get_nextN_after_specified(self):
        get_info = self.lbl_blk_get["get_nextN_lbl_blk"]
        client.label_block_get(get_info)

    def test_008_06_lbl_blk_get_all(self):
        get_info = self.lbl_blk_get["get_firstN_lbl_blk"]
        client.label_block_get_all(get_info)

    def test_009_00_blk_delete(self):
        client.label_block_delete(self.lbl_blk_params1)

    def test_009_01_blk_delete(self):
        client.label_block_delete(self.lbl_blk_params2)

    def test_010_mpls_eof(self):
        client.mpls_eof()

    def test_011_mpls_unregister(self):
        client.mpls_unregister()


#
# This class simply inherits the entire v4 class
#
class TestSuite_003_ILM_IPv4_Stream(TestSuite_003_ILM_IPv4):
    AF = 4
    STREAM = True
    # Inherit all v4 test cases


#
# This class simply inherits the entire v4 class
#
class TestSuite_004_ILM_IPv6(TestSuite_003_ILM_IPv4):
    AF = 6
    # Inherit all v4 test cases


#
# This class simply inherits the entire v4 class
#
class TestSuite_004_ILM_IPv6_Stream(TestSuite_003_ILM_IPv4):
    AF = 6
    STREAM = True
    # Inherit all v4 test cases


class TestSuite_014_MPLS_CoS_TC1(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_014_MPLS_CoS_TC1, cls).setUpClass()
        cls.ilm_entry = json_params["cos_ilm_tc1"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, default -> NH1
    def test_002_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # FIXME: REMOVE
    # add label 32220, default -> NH1
    def test_002b_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # add label 32220, exp 4 -> NH2
    def test_003_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 4 -> NH2 (fail)
    def test_004_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # update label 32220, exp 4 -> NH3
    def test_005_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 5 -> NH3
    def test_006_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220, default
    def test_007_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, default -> NH4
    def test_008_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 22220, default -> NH4 (fail)
    def test_009_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_6"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # delete label 32220 exp 4
    def test_010_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 4 (del of non-existent label is success)
    def test_011_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 5
    def test_012_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 default
    def test_013_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default_exp"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_014_mpls_eof(self):
        client.mpls_eof()

    def test_015_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_014_MPLS_CoS_TC1_v6(TestSuite_014_MPLS_CoS_TC1):
    AF = 6
    STREAM = False


class TestSuite_015_MPLS_CoS_TC2(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_015_MPLS_CoS_TC2, cls).setUpClass()
        cls.ilm_entry = json_params["cos_ilm_tc2"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params_2"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, exp 1 -> NH1,w2 NH2,w2
    def test_002_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 2 -> NH1,w4 NH3,w4
    def test_003_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 2
    def test_004_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, default -> NH1,w3
    def test_005_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, default -> NH1,w3 (fail)
    def test_006_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # update label 32220, exp 1 -> NH3,w3 NH4,w1
    def test_007_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 1
    def test_008_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 default
    def test_009_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 default (del of non-existent label is success)
    def test_010_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_011_mpls_eof(self):
        client.mpls_eof()

    def test_012_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_015_MPLS_CoS_TC2_v6(TestSuite_015_MPLS_CoS_TC2):
    AF = 6
    STREAM = False


class TestSuite_016_MPLS_CoS_TC3(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_016_MPLS_CoS_TC3, cls).setUpClass()
        cls.ilm_entry = json_params["cos_ilm_tc3"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, exp 0 -> NH1 NH2
    def test_002_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 1 -> NH2 NH3
    def test_003_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 1 -> NH2 NH3 (fail)
    def test_004_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # add label 32220, exp 2 -> NH3 NH4
    def test_005_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 3 -> NH4 NH5
    def test_006_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 3 -> NH2 NH4
    def test_007_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 4 -> NH1 NH4
    def test_008_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_6"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 5 -> NH1 NH3 NH5
    def test_009_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_7"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 5 -> NH2 NH4
    def test_010_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_8"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 6 -> NH6 NH7
    def test_011_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_9"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 7 -> NH5 NH8
    def test_012_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_10"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, default -> NH8, NH9 (Pop and lookup)
    # NOTE: Next hops are not required for pop and lookup and are just used
    #       to keep tests cases reusable
    def test_013_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_11"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, default -> NH8, NH9 (fail)
    def test_014_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_11"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # update label 32220, default -> NH7 NH9 (pop and lookup -> swap)
    def test_015_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_12"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 0
    def test_016_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_0"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 0 (del of non-existent label is success)
    def test_017_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_0"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 1
    def test_018_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 2
    def test_019_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 3
    def test_020_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 4
    def test_021_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 5
    def test_022_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 6
    def test_023_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_6"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 7
    def test_024_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_7"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 default
    def test_025_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 default (del of non-existent label is success)
    def test_026_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_027_mpls_eof(self):
        client.mpls_eof()

    def test_028_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_016_MPLS_CoS_TC3_v6(TestSuite_016_MPLS_CoS_TC3):
    AF = 6
    STREAM = False


class TestSuite_017_MPLS_CoS_TC4(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_017_MPLS_CoS_TC4, cls).setUpClass()
        cls.ilm_entry = json_params["cos_ilm_tc4"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # update label 32220, exp 0 -> NH1 NH2
    def test_002_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 1 -> NH2 NH3
    def test_003_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 1 -> NH2 NH3 (no op)
    def test_004_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 2 -> NH3 NH4
    def test_005_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 3 -> NH4 NH5
    def test_006_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 3 -> NH2 NH4
    def test_007_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 4 -> NH1 NH4
    def test_008_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_6"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 5 -> NH1 NH3 NH5
    def test_009_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_7"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 5 -> NH2 NH4
    def test_010_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_8"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 6 -> NH6 NH7
    def test_011_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_9"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 7 -> NH5 NH8
    def test_012_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_10"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, default -> NH8, NH9 (Pop and Lookup)
    # NOTE: Next hops are not required for pop and lookup and are just used
    #       to keep tests cases reusable
    def test_013_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_11"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, default -> NH8, NH9 (no op)
    def test_014_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_11"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, default -> NH7 NH9 (pop and lookup -> swap)
    def test_015_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_12"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 0
    def test_016_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_0"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 0 (del of non-existent label is success)
    def test_017_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_0"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 1
    def test_018_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 2
    def test_019_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 3
    def test_020_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 4
    def test_021_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 5
    def test_022_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 6
    def test_023_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_6"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 7
    def test_024_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_7"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 default
    def test_025_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 default (del of non-existent label is success)
    def test_026_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_027_mpls_eof(self):
        client.mpls_eof()

    def test_028_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_017_MPLS_CoS_TC4_v6(TestSuite_017_MPLS_CoS_TC4):
    AF = 6
    STREAM = False


class TestSuite_018_MPLS_CoS_TC5(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_018_MPLS_CoS_TC5, cls).setUpClass()
        cls.ilm_entry = json_params["cos_ilm_tc5"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }


    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, exp 0 -> NH1,w32
    def test_002_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 1 -> NH2,w32
    def test_003_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 2 -> NH3,w32
    def test_004_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 3 -> NH4,w32
    def test_005_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 4 -> NH5,w32
    def test_006_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 5 -> NH3,w32
    def test_007_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_7"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 6 -> NH3,w32
    def test_008_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_8"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 7 -> NH2,w32
    def test_009_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_9"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp default -> NH2,w32
    def test_010_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 2
    def test_011_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 2 -> NH3,w32
    def test_012_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_6"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 0
    def test_013_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_0"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 1
    def test_014_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 2
    def test_015_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 3
    def test_016_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 4
    def test_017_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 5
    def test_018_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 6
    def test_019_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_6"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 7
    def test_020_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_7"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp default
    def test_021_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_022_mpls_eof(self):
        client.mpls_eof()

    def test_023_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_018_MPLS_CoS_TC5_v6(TestSuite_018_MPLS_CoS_TC5):
    AF = 6
    STREAM = False


class TestSuite_019_MPLS_CoS_TC6(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_019_MPLS_CoS_TC6, cls).setUpClass()
        cls.ilm_entry = json_params["cos_ilm_tc6"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }


    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, exp 1 -> NH1,w1 NH2,w2
    def test_003_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 1 -> NH2,w3 NH3,w4
    def test_004_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, exp 1 -> NH5,w5 NH6,w6
    def test_005_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, default -> NH3,w3 NH4,w4 (pop and lookup)
    # NOTE: Next hops are not required for pop and lookup and are just used
    #       to keep tests cases reusable
    def test_006_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, default -> NH3,w3 NH4,w4 (fail)
    def test_007_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_4"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # update label 32220, default -> NH4,w4 NH5,w5 (pop and lookup -> swap)
    def test_008_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, default -> NH7,w7 NH8,w8
    def test_009_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_6"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 1
    def test_010_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 1 (del of non-existent label is success)
    def test_011_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 default
    def test_012_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 default (del of non-existent label is success)
    def test_013_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_014_mpls_eof(self):
        client.mpls_eof()

    def test_015_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_019_MPLS_CoS_TC6_v6(TestSuite_019_MPLS_CoS_TC6):
    AF = 6
    STREAM = False


class TestSuite_020_COS_ILM_IPv4_TC7(unittest.TestCase):
    AF = 4
    STREAM = False
    batch = "scale_cos_ilm_4"
    update_batch = "scale_cos_ilm_update_4"
    cos_block = "cos_mpls_lbl_block_2"
    srgb_batch = "scale_srgb_ilm_1"
    srgb_block = "mpls_lbl_block_srgb_1"
    get_ilm = "cos_ilm_get"

    @classmethod
    def setUpClass(cls):
        super(TestSuite_020_COS_ILM_IPv4_TC7, cls).setUpClass()
        cls.ilm_entry = json_params[cls.batch]
        cls.cos_lbl_blk_params = json_params[cls.cos_block]
        cls.srgb_lbl_blk_params = json_params[cls.srgb_block]
        cls.reg_params = json_params["reg_params"]
        cls.ilm_get_info = json_params[cls.get_ilm]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }


    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_00_blk_add(self):
        client.label_block_add(self.cos_lbl_blk_params)

    def test_002_01_blk_add(self):
        client.label_block_add(self.srgb_lbl_blk_params)

    def test_003_00_ilm_add(self):
        self.ilm_entry = json_params[self.batch]
        client.ilm_add(self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info)

    def test_003_01_ilm_add(self):
        self.ilm_entry = json_params[self.srgb_batch]
        client.ilm_add(self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info)

    def test_004_00_ilm_update(self):
        self.ilm_entry = json_params[self.update_batch]
        client.ilm_update(
            self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info
        )

    def test_006_01_ilm_get_exact_match(self):
        get_info = self.ilm_get_info["get_exact_ilm_default"]
        client.ilm_get(get_info)

    def test_006_02_ilm_get_exact_match(self):
        get_info = self.ilm_get_info["get_exact_ilm_exp"]
        client.ilm_get(get_info)

    def test_006_02_ilm_get_firstN(self):
        get_info = self.ilm_get_info["get_firstN_ilm"]
        client.ilm_get(get_info)

    def test_006_03_ilm_get_nextN_with_specified(self):
        get_info = self.ilm_get_info["get_nextN_include_ilm"]
        client.ilm_get(get_info)

    def test_006_04_ilm_get_nextN_after_specified(self):
        get_info = self.ilm_get_info["get_nextN_ilm"]
        client.ilm_get(get_info)

    def test_006_05_ilm_get_all(self):
        get_info = self.ilm_get_info["get_firstN_ilm"]

        xcount = MplsUtil.get_expected_ilm_count(json_params[self.update_batch])
        xcount += MplsUtil.get_expected_ilm_count(json_params[self.srgb_batch])

        client.ilm_get_all(get_info, xcount=xcount)

    def test_006_06_ilm_get_stream(self):
        # Pack 4 requests
        get_infos = (
            self.ilm_get_info[name]
            for name in [
                "get_firstN_ilm",
                "get_exact_ilm_exp",
                "get_exact_ilm_default",
                "get_nextN_include_ilm",
            ]
        )

        # Returns respons iterator
        responses = client.ilm_get(get_infos, stream=True)

        # Do not need to do extra verification
        for _ in responses:
            pass

    def test_007_00_ilm_delete(self):
        self.ilm_entry = json_params[self.srgb_batch]
        client.ilm_delete(
            self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info
        )

    def test_007_01_ilm_delete(self):
        self.ilm_entry = json_params[self.update_batch]
        client.ilm_delete(
            self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info
        )

    def test_009_00_blk_delete(self):
        client.label_block_delete(self.cos_lbl_blk_params)

    def test_009_01_blk_delete(self):
        client.label_block_delete(self.srgb_lbl_blk_params)

    def test_010_mpls_eof(self):
        client.mpls_eof()

    def test_011_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_020_COS_ILM_IPv6_TC7(TestSuite_020_COS_ILM_IPv4_TC7):
    AF = 6
    STREAM = False


class TestSuite_021_COS_ILM_IPv4_TC8(TestSuite_020_COS_ILM_IPv4_TC7):
    batch = "scale_cos_ilm_1"
    update_batch = "scale_cos_ilm_update_1"


class TestSuite_021_COS_ILM_IPv6_TC8(TestSuite_021_COS_ILM_IPv4_TC8):
    AF = 6
    STREAM = False


class TestSuite_022_COS_ILM_IPv4_TC9(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_022_COS_ILM_IPv4_TC9, cls).setUpClass()
        cls.ilm_entry = json_params["cos_ilm_tc9"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_invalid_client = json_params["cos_mpls_lbl_block_wrong_client_name"]
        cls.lbl_blk_duplicate_range = json_params["cos_mpls_lbl_block_duplicate_cbf"]
        cls.lbl_blk_srgb1 = json_params["mpls_lbl_block_srgb_1"]
        cls.lbl_blk_srgb2 = json_params["mpls_lbl_block_srgb_2"]
        cls.ilm_get_info = json_params["ilm_get"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }


    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    # Add blk with invalid client name (Negative)
    # @unittest.skip("This will only fail if LSD CLI is configured")
    # def test_002_blk_add(self):
    #     client.label_block_add(self.lbl_blk_invalid_client)

    # Add 25k-35k cbf block client name Service-layer (Positive)
    def test_003_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # Add 35k-40k duplicate cbf block client name Service-layer (Negative)
    def test_004_blk_add(self):
        client.label_block_add(self.lbl_blk_duplicate_range, xfail=True)

    # Add 35k-100k SRGB block (Positive)
    def test_005_blk_add(self):
        client.label_block_add(self.lbl_blk_srgb1)

    # Add 65k-75k SRGB block (Negative, context mismatch)
    def test_006_blk_add(self):
        client.label_block_add(self.lbl_blk_srgb2, xfail=True)

    # add label 32220, exp 4 -> NH1, remote label=Implicit Null
    def test_007_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 5 -> NH2, remote label=Explicit Null
    def test_008_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, non elsp to cbf block -> NH1 (fail)
    def test_009_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # delete label 32220 exp 4
    def test_010_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220 exp 5
    def test_011_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_5"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_014_mpls_eof(self):
        client.mpls_eof()

    def test_015_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_024_COS_ILM_IPv4_TC11(TestSuite_020_COS_ILM_IPv4_TC7):
    batch = "scale_cos_ilm_pop_and_lookup"
    batch_add = "scale_cos_ilm_5"
    update_batch = "scale_cos_ilm_update_pop_and_lookup"
    cos_block = "cos_mpls_lbl_block_2"
    srgb_block = "mpls_lbl_block_srgb_1"
    srgb_batch = "scale_srgb_ilm_1"

    # NOTE: These test add to TestSuite_020_COS_ILM_IPv4_TC7
    def test_005_00_ilm_add(self):
        self.ilm_entry = json_params[self.batch_add]
        client.ilm_add(self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info)

    def test_005_01_ilm_delete(self):
        self.ilm_entry = json_params[self.batch_add]
        client.ilm_delete(
            self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info
        )


class TestSuite_025_MPLS_CoS_TC12(unittest.TestCase):
    AF = 4
    STREAM = False
    tc_info = "cos_ilm_tc12"

    @classmethod
    def setUpClass(cls):
        super(TestSuite_025_MPLS_CoS_TC12, cls).setUpClass()
        cls.ilm_entry = json_params[cls.tc_info]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }


    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, default -> Pop and lookup
    def test_002_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, default -> NH1 swap
    def test_003_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_4"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 0 -> swap
    def test_004_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220, exp 1 -> swap
    def test_005_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220, exp 0
    def test_006_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220, exp 1
    def test_007_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # update label 32220, default -> Pop and Lookup
    def test_008_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # delete label 32220, default
    def test_009_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_010_mpls_eof(self):
        client.mpls_eof()

    def test_011_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_025_MPLS_CoS_TC12_v6(TestSuite_025_MPLS_CoS_TC12):
    AF = 6


# Skip as this is a duplicate TC as long as Pop and Lookup is mapped
# to Pop and Lookup v4
#
# class TestSuite_026_MPLS_CoS_TC13(TestSuite_025_MPLS_CoS_TC12):
#     tc_info = 'cos_ilm_tc13'

# class TestSuite_026_MPLS_CoS_TC13_v6(TestSuite_025_MPLS_CoS_TC12):
#     AF = 6


class TestSuite_027_MPLS_CoS_TC14(TestSuite_025_MPLS_CoS_TC12):
    tc_info = "cos_ilm_tc14"


class TestSuite_027_MPLS_CoS_TC14_v6(TestSuite_027_MPLS_CoS_TC14):
    AF = 6


class TestSuite_028_MPLS_CoS_TC15(unittest.TestCase):
    AF = 4
    STREAM = False
    tc_info = "cos_ilm_tc15"

    @classmethod
    def setUpClass(cls):
        super(TestSuite_028_MPLS_CoS_TC15, cls).setUpClass()
        cls.ilm_entry = json_params[cls.tc_info]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }


    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, default -> Pop and lookup
    def test_003_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_004_mpls_eof(self):
        client.mpls_eof()

    def test_005_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_006_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, default, exp0, exp1 -> swap
    def test_007_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_008_mpls_eof(self):
        client.mpls_eof()

    def test_009_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_010_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, default, exp1 -> swap
    def test_011_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_012_mpls_eof(self):
        client.mpls_eof()

    def test_013_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_014_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32220, default -> Pop and lookup
    def test_015_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_016_mpls_eof(self):
        client.mpls_eof()

    def test_017_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_028_MPLS_CoS_TC15_v6(TestSuite_028_MPLS_CoS_TC15):
    AF = 6


class TestSuite_029_MPLS_CoS_TC16_scale(unittest.TestCase):
    AF = 4  # AF is overwritten by scale tests
    STREAM = False
    pop_and_lookup_batch = "scale_cos_ilm_pop_and_lookup"
    swap_batch = "scale_cos_ilm_v4_v6"
    block = "cos_mpls_lbl_block_2"

    @classmethod
    def setUpClass(cls):
        super(TestSuite_029_MPLS_CoS_TC16_scale, cls).setUpClass()
        cls.ilm_entry = json_params[cls.pop_and_lookup_batch]
        cls.lbl_blk_params = json_params[cls.block]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }


    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32000-32999, default -> Pop and lookup
    def test_003_ilm_add(self):
        self.ilm_entry = json_params[self.pop_and_lookup_batch]
        client.ilm_add(self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info)

    def test_004_mpls_eof(self):
        client.mpls_eof()

    def test_005_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_006_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32000-32999, default, exp0, exp1 -> swap
    def test_007_ilm_add(self):
        self.ilm_entry = json_params[self.swap_batch]
        client.ilm_add(self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info)

    def test_008_mpls_eof(self):
        client.mpls_eof()

    def test_009_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_010_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label 32000-32999, default -> pop and lookup
    def test_011_ilm_add(self):
        self.ilm_entry = json_params[self.pop_and_lookup_batch]
        client.ilm_add(self.ilm_entry, stream=self.STREAM, af=self.AF, **self.path_info)

    def test_012_mpls_eof(self):
        client.mpls_eof()

    def test_013_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_031_MPLS_IPV4_PREFIX(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_031_MPLS_IPV4_PREFIX, cls).setUpClass()
        cls.ilm_entry = json_params['cos_ilm_ip_route_base']
        cls.ilm_entry_del = json_params['cos_ilm_del']
        cls.label_block = json_params['mpls_ip_route_label_block']
        cls.reg_params = json_params['reg_params']
        cls.path_info = {'paths': json_params['paths'], 'next_hops': json_params['next_hops']}

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_ilm_add(self):
        # Add single ilm entry with ipv4 prefix 10.1.1.1
        client.ilm_add(self.ilm_entry["cos_ilm_1"], stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_003_ilm_delete(self):
        # Remove the ilm entry with ipv4 prefix 10.1.1.1
        client.ilm_delete(self.ilm_entry_del["cos_del_prefix_1"],
                stream=self.STREAM, af=self.AF, **self.path_info)
    
    def test_004_ilm_add(self):
        # Add 5 ilm entries with ip prefix 10.1.1.2 to 10.1.1.6
        client.ilm_add(self.ilm_entry["cos_ilm_2"], stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_005_ilm_update(self):
        # Update the path entries for the above ip prefixes
        client.ilm_update(self.ilm_entry["cos_ilm_3"], stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_006_ilm_delete(self):
        # Remove the ilm entries
        client.ilm_delete(self.ilm_entry_del["cos_del_prefix_2"],
                stream=self.STREAM, af=self.AF, **self.path_info)

    def test_007_mpls_eof(self):
        client.mpls_eof()

    def test_008_mpls_unregister(self):
        client.mpls_unregister()

class TestSuite_032_MPLS_IPV6_PREFIX(unittest.TestCase):
    AF = 6
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_032_MPLS_IPV6_PREFIX, cls).setUpClass()
        cls.ilm_entry = json_params['cos_ilm_ip_route_base']
        cls.ilm_entry_del = json_params['cos_ilm_del']
        cls.label_block = json_params['mpls_ip_route_label_block']
        cls.reg_params = json_params['reg_params']
        cls.path_info = {'paths': json_params['paths'], 'next_hops': json_params['next_hops']}

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_ilm_add(self):
        # Add ilm with ipv6 prefix 10::1
        client.ilm_add(self.ilm_entry["cos_ilm_4"], stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_003_ilm_delete(self):
        # Delete the ilm with ipv6 prefix 10::1
        client.ilm_delete(self.ilm_entry_del["cos_del_prefix_3"],
                stream=self.STREAM, af=self.AF, **self.path_info)
    
    def test_004_ilm_add(self):
        # Add 5 ilm entries with ipv6 prefixes 10::2 - 10::6
        client.ilm_add(self.ilm_entry["cos_ilm_5"], stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_005_ilm_update(self):
        # Update the ilm entries with different path entries
        client.ilm_update(self.ilm_entry["cos_ilm_6"], stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_006_ilm_delete(self):
        # Remove the ilm entries. 
        client.ilm_delete(self.ilm_entry_del["cos_del_prefix_4"],
                stream=self.STREAM, af=self.AF, **self.path_info)

    def test_007_mpls_eof(self):
        client.mpls_eof()

    def test_008_mpls_unregister(self):
        client.mpls_unregister()

class TestSuite_033_MPLS_IPV4_IPV6_CBF_MIXED(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_033_MPLS_IPV4_IPV6_CBF_MIXED, cls).setUpClass()
        cls.ilm_entry = json_params['cos_ilm_tc17']
        cls.ilm_entry_del = json_params['cos_ilm_del']
        cls.label_block = json_params['mpls_ip_route_label_block']
        cls.reg_params = json_params['reg_params']
        cls.path_info = {'paths': json_params['paths'], 'next_hops': json_params['next_hops']}
        cls.get_ilm = json_params['cos_ilm_get']

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.label_block)

    def test_003_ilm_add(self):
        #add a mix of ilm entries with ipv4, ipv6 and cbf prefixes
        client.ilm_add(self.ilm_entry["cos_ilm_1"], stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_004_ilm_get_label(self):
        # Check that we are able to get a label ilm
        get_info = self.get_ilm["get_exact_match_ilm"]
        response = client.ilm_get(get_info)
        assert get_info["count"] == len(response.Entries)

    def test_005_ilm_get_label_exp(self):
        # Check that get works for ilm with label and exp as keys
        get_info = self.get_ilm["get_exact_match_ilm_exp"]
        response = client.ilm_get(get_info)
        assert get_info["count"] == len(response.Entries)

    def test_006_ilm_get_label_ipv4(self):
        #Check that get works for ilm with ipv4 prefix
        get_info = self.get_ilm["get_exact_match_ilm_ipv4"]
        response = client.ilm_get(get_info)
        assert get_info["count"] == len(response.Entries)

    def test_007_ilm_get_label_ipv6(self):
        # Check that get work for ilm with ipv6 prefix
        get_info = self.get_ilm["get_exact_match_ilm_ipv6"]
        response = client.ilm_get(get_info)
        assert get_info["count"] == len(response.Entries)

    def test_008_ilm_get_label_mixed(self):
        # Check that get works for ilm with mixed label, cbf, ipv4 and ipv6 prefixes
        get_info = self.get_ilm["get_mixed_ilm_ip_prefixes"]
        response = client.ilm_get(get_info)
        assert get_info["count"] == len(response.Entries)

    def test_009_mpls_eof(self):
        client.mpls_eof()

    def test_010_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_011_blk_add(self):
        client.label_block_add(self.label_block)

    def test_012_ilm_add(self):
        # Add half the number of entries, and check if previous entries are cleared
        client.ilm_add(self.ilm_entry["cos_ilm_2"], stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_013_mpls_eof(self):
        client.mpls_eof()

    def test_014_mpls_unregister(self):
        client.mpls_unregister()

class TestSuite_034_MPLS_IP_PREFIX_SCALE(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_034_MPLS_IP_PREFIX_SCALE, cls).setUpClass()
        cls.ilm_entry_1 = json_params['batch_ip_route_ilm']
        cls.ilm_entry_2 = json_params['batch_ip_route_ilm2']
        cls.reg_params = json_params['reg_params']
        cls.path_info = {'paths': json_params['paths'], 'next_hops': json_params['next_hops']}

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_003_ilm_add(self):
        # Generate and populate 50k ipv4 and ipv6 prefixes
        client.ilm_add(self.ilm_entry_1, stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_004_mpls_eof(self):
        client.mpls_eof()

    def test_005_mpls_register(self):
        client.mpls_register(self.reg_params)
    
    def test_006_ilm_add(self):
        # mark and sweep  testingwith half the number of prefixes
        client.ilm_add(self.ilm_entry_2, stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_007_mpls_eof(self):
        client.mpls_eof()

    def test_008_mpls_unregister(self):
        client.mpls_unregister()

class TestSuite_035_MPLS_IP_CBF_PREFIX_SCALE(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_035_MPLS_IP_CBF_PREFIX_SCALE, cls).setUpClass()
        cls.label_block = json_params['mpls_ip_route_label_block']
        cls.ilm_entry_1 = json_params['batch_ip_route_ilm3']
        cls.ilm_entry_2 = json_params['batch_ip_route_ilm4']
        cls.reg_params = json_params['reg_params']
        cls.path_info = {'paths': json_params['paths'], 'next_hops': json_params['next_hops']}

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)
    def test_002_blk_add(self):
        client.label_block_add(self.label_block)

    def test_003_ilm_add(self):
        # Generate and populate 12k mixed ipv4 ipv6 and cbf prefixes
        client.ilm_add(self.ilm_entry_1, stream=self.STREAM,
                af=self.AF, **self.path_info)


    def test_004_mpls_eof(self):
        client.mpls_eof()

    def test_005_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_006_blk_add(self):
        client.label_block_add(self.label_block)
    
    def test_007_ilm_add(self):
        # mark and sweep testing  with half the number of prefixes
        client.ilm_add(self.ilm_entry_2, stream=self.STREAM,
                af=self.AF, **self.path_info)

    def test_008_mpls_eof(self):
        client.mpls_eof()

    def test_009_mpls_unregister(self):
        client.mpls_unregister()

class TestSuite_030_MPLS_CoS_NHLFE_TC1(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_030_MPLS_CoS_NHLFE_TC1, cls).setUpClass()
        cls.ilm_entry = json_params["cos_nhlfe_tc1"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # # add label 32220 - 32224 - Pop and Lookup
    def test_003_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )
    
    #  # delete label 32220-32224
    def test_004_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_nhlfe_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # # add label 32220 -  Negative test, load metric non zero for down path
    def test_005_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_4"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # add label 32220 -  Negative test, Different priority for same setid
    def test_006_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_5"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # add label 32220 -  Negative test, Multiple primary setid
    def test_007_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_6"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )
    
     # # add label 32220 -  Negative test, Non contiguous setids
    def test_008_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_7"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

     # # add label 32220 -  Negative test, Non contiguous exps
    def test_009_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_8"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

      # # add label 32220 -  Negative test, inconsistent exp on path
    def test_010_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_9"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # # add label 32220 - 32224 - Pop and Lookup
    def test_011_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # # update label 32220-32224 - Swap/ Pop and Forward
    def test_012_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_nhlfe_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # # update label 32220 - 32224 - Pop and Lookup
    def test_013_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_nhlfe_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # # update label 32220-32224 - Swap/ Pop and Forward
    def test_012_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_nhlfe_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # # update label 32220-32224, change path priority
    def test_014_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_nhlfe_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # # update label 32220 - 32224 - Pop and Lookup
    def test_015_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_nhlfe_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    #  # delete label 32220-32224
    def test_016_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_nhlfe_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_017_mpls_eof(self):
        client.mpls_eof()

    def test_018_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_036_MPLS_PRIMARY_BACKUP_TC1(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_036_MPLS_PRIMARY_BACKUP_TC1, cls).setUpClass()
        cls.ilm_entry = json_params["cos_nhlfe_tc2"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # # add label 32220 - 32224 - Pop and Lookup
    def test_003_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )
    
    #  # delete label 32220-32224
    def test_004_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_nhlfe_del_default"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # # add label 32220 -  Negative test, load metric non zero for down path
    def test_005_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_4"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # delete label 32220
    def test_006_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_nhlfe_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220 -  Negative test, Different priority for same setid
    def test_007_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_5"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # delete label 32220
    def test_008_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_nhlfe_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220 -  Negative test, Multiple primary setid
    def test_009_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_6"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )
    
    # delete label 32220
    def test_010_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_nhlfe_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # add label 32220 -  Negative test, Non contiguous setids
    def test_011_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_7"],
            stream=self.STREAM,
            af=self.AF,
            xfail=True,
            **self.path_info
        )

    # delete label 32220
    def test_012_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_nhlfe_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )


    # # update label 32220
    def test_013_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    # # update label 32220 change path priority
    def test_014_ilm_update(self):
        client.ilm_update(
            self.ilm_entry["cos_nhlfe_3"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    #  # delete label 32220
    def test_016_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_nhlfe_del_2"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_016_mpls_eof(self):
        client.mpls_eof()

    def test_017_mpls_unregister(self):
        client.mpls_unregister()

        
class TestSuite_020_MPLS_CoS_TC7(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_020_MPLS_CoS_TC7, cls).setUpClass()
        cls.ilm_entry = json_params["cos_ilm_tc7"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }


    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)


    # add label 32220 - Push  
    def test_002_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_ilm_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )


    def test_003_ilm_delete(self):
        client.ilm_delete(
            self.ilm_entry_del["cos_ilm_del_default_exp"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_004_mpls_eof(self):
        client.mpls_eof()


    def test_005_mpls_unregister(self):
        client.mpls_unregister()


class TestSuite_020_MPLS_CoS_TC7_v6(TestSuite_020_MPLS_CoS_TC7):
    AF = 6
    STREAM = False

class TestSuite_031_MPLS_CoS_NHLFE_TC2(unittest.TestCase):
    AF = 4
    STREAM = False

    @classmethod
    def setUpClass(cls):
        super(TestSuite_031_MPLS_CoS_NHLFE_TC2, cls).setUpClass()
        cls.ilm_entry = json_params["cos_nhlfe_tc3"]
        cls.ilm_entry_del = json_params["cos_ilm_del"]
        cls.lbl_blk_params = json_params["cos_mpls_lbl_block_1"]
        cls.lbl_blk_get = json_params["lbl_blk_get"]
        cls.reg_params = json_params["reg_params"]
        cls.path_info = {
            "paths": json_params["paths"],
            "next_hops": json_params["next_hops"],
        }

    def test_000_get_globals(self):
        # Get Global MPLS info
        client.mpls_global_get()

    def test_001_mpls_register(self):
        client.mpls_register(self.reg_params)

    def test_002_blk_add(self):
        client.label_block_add(self.lbl_blk_params)

    # add label to multiple paths(inc > 1 remote labe) Push 
    def test_002_ilm_add(self):
        client.ilm_add(
            self.ilm_entry["cos_nhlfe_1"],
            stream=self.STREAM,
            af=self.AF,
            **self.path_info
        )

    def test_003_ilm_delete(self):
         client.ilm_delete(
             self.ilm_entry_del["cos_nhlfe_del_default"],
             stream=self.STREAM,
             af=self.AF,
             **self.path_info
         )

    def test_004_mpls_eof(self):
        client.mpls_eof()

    def test_005_mpls_unregister(self):
        client.mpls_unregister()
