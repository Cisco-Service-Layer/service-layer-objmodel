#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
import json
import os
import unittest
import ipaddress
import threading
import time

from lindt import GrpcClient
from genpy import sl_common_types_pb2
from genpy import sl_global_pb2
from genpy import sl_mpls_pb2
from genpy import sl_bfd_common_pb2
from util import util
from lindt import serializers

# Print Received Globals
def print_globals(response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print "Max VRF Name Len     : %d" %(response.MaxVrfNameLength)
        print "Max Iface Name Len   : %d" %(response.MaxInterfaceNameLength)
        print "Max Paths per Entry  : %d" %(response.MaxPathsPerEntry)
        print "Max Prim per Entry   : %d" %(response.MaxPrimaryPathPerEntry)
        print "Max Bckup per Entry  : %d" %(response.MaxBackupPathPerEntry)
        print "Max Labels per Entry : %d" %(response.MaxMplsLabelsPerPath)
        print "Min Prim Path-id     : %d" %(response.MinPrimaryPathIdNum)
        print "Max Prim Path-id     : %d" %(response.MaxPrimaryPathIdNum)
        print "Min Bckup Path-id    : %d" %(response.MinBackupPathIdNum)
        print "Max Bckup Path-id    : %d" %(response.MaxBackupPathIdNum)
        print "Max Remote Bckup Addr: %d" %(response.MaxRemoteAddressNum)
    else:
        print "Globals response Error 0x%x" %(response.ErrStatus.Status)
        return False
    return True

# Print Received Route Globals
def print_route_globals(af, response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print "Max v%d VRF Reg Per VRF Msg : %d" %(af,
            response.MaxVrfregPerVrfregmsg)
        print "Max v%d Routes per Route Msg: %d" %(af,
            response.MaxRoutePerRoutemsg)
    else:
        print "Route Globals response Error 0x%x" %(response.ErrStatus.Status)
        return False
    return True

# Print Received Route Globals
def print_route_stats_globals(af, response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print ""
        print "VrfCount   v%d: %d" %(af, response.VrfCount)
        print "RouteCount v%d: %d" %(af, response.RouteCount)
    else:
        print "Route Get Stats response Error 0x%x" %(response.ErrStatus.Status)
        return False
    return True

# Print Received MPLS Globals
def print_mpls_globals(response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print "Max labels per label block            : %d" %(
            response.MaxLabelsPerBlock)
        print "Max label blocks per MplsLabelBlockMsg: %d" %(
            response.MaxLabelblocksPerLabelblockmsg)
        print "Min Start Label                       : %d" %(
            response.MinStartLabel)
        print "Label Table Size                      : %d" %(
            response.LabelTableSize)
        print "Max ILMs per IlmMsg                   : %d" %(
            response.MaxIlmPerIlmmsg)
        print "Max Paths per Ilm                     : %d" %(
            response.MaxPathsPerIlm)
    else:
        print "MPLS Globals response Error 0x%x" %(response.ErrStatus.Status)
        return False
    return True

# Print Received BFD Globals
def print_bfd_globals(af, response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print "Max v%d BFD Sess Per BFD Msg : %d" %(af,
            response.MaxBfdSessionCfgPerSLBfdMsg)
        print "Min v%d BFD Tx Interval Single hop  : %d" %(af,
            response.MinBfdTxIntervalSingleHop)
        print "Min v%d BFD Tx Interval Multi hop   : %d" %(af,
            response.MinBfdTxIntervalMultiHop)
        print "Min v%d BFD Detect Multi Single hop : %d" %(af,
            response.MinBfdDetectMultiplierSingleHop)
        print "Min v%d BFD Detect Multi Multi hop  : %d" %(af,
            response.MinBfdDetectMultiplierMultiHop)
    else:
        print "BFD Globals response Error 0x%x" %(response.ErrStatus.Status)
        return False
    return True

# Global notification Callback
# This function is called from the global_init thread context
# To break the stream recv(), return False
def global_init_cback(response, event):
    if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_VERSION:
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.ErrStatus.Status):
            print "Server Version %d.%d.%d" %(
                response.InitRspMsg.MajorVer,
                response.InitRspMsg.MinorVer,
                response.InitRspMsg.SubVer)
            # Successfully Initialized
            # This would notify the main thread to proceed
            event.set()
        else:
            return False
    elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_HEARTBEAT:
        print "Received Event: Heartbeat"
        return True
    elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
        print "Received Global Error event:", response
        return False
    else:
        print "Received unknown event:", response
        return False

    # Continue looping on events
    return True

# Wait on Global notification events
def global_init(event):
    g_params = ClientTestCase.json_params['global_init']
    try:
        response = TestSuite_000_Global.global_notif.global_init(g_params, 
            global_init_cback, event)
        # Should return on errors
        if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
            if (response.ErrStatus.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
                print "Service Layer Session was taken over by another client"
        else:
            # If this session is lost, then most likely the server restarted
            print "global_init: exiting unexpectedly, Server Restart?"
            print "last response from server:", response
    except Exception as e:
        print "Received exception:", e
        print "Server died?"
    os._exit(0)

# BFD notification Callback
# This function is called from the BFD thread context
# To break the stream recv(), return False
def bfd_notif_cback(response):
    if response.EventType == sl_bfd_common_pb2.SL_BFD_EVENT_TYPE_ERROR:
        if (response.ErrStatus.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
            print "Received notification to Terminate, Stream taken over?"
        else:
            print "Received error 0x%x" %(response.ErrStatus.Status)
        return False
    elif response.EventType == sl_bfd_common_pb2.SL_BFD_EVENT_TYPE_SESSION_STATE:
        print "Received BFD Event:"
        print "    VrfName  : %s" %(response.Session.Key.VrfName)
        print "    Nbr      : %s" %(
            str(ipaddress.ip_address(response.Session.Key.Nbr.Addr)))
        print "    Interface: %s" %(
            response.Session.Key.Interface.InterfaceName)
        print "    Type     : %d" %(response.Session.Key.Type)
        # This would not print attributes with 0 value.
        print response.Session.State
    else:
        print "Received an unexpected event type %d" %(
            response.EventType)
        return False
    # Continue looping on events
    return True

# Wait on BFD notification events
def bfd_get_notif(event, thread_count):
    # This would notify the main thread to proceed
    event.set()
    # RPC to get Notifications
    response = TestSuite_005_BFD_IPv4.bfd_notif.bfd_get_notif(bfd_notif_cback)
    # Above, Should return on errors
    print "bfd_get_notif: thread %d exiting. response: %s" %(thread_count, 
        response)
    # Do not exit the process, as other tests could be still going
#
#
#
def validate_vrf_response(response):
    if (response.StatusSummary.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        return True
    # Error cases
    print "Batch Error code 0x%x" %(response.StatusSummary.Status)
    # SOME ERROR
    if (response.StatusSummary.Status == 
            sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR):
        for result in response.Results:
            print "Error code for %s is 0x%x" %(result.VrfName,
                result.ErrStatus.Status
            )
    return False

#
#
#
def validate_route_response(response, AF):
    # Increment the validated_count
    TestSuite_001_Route_IPv4.validated_count =\
        TestSuite_001_Route_IPv4.validated_count + 1
    #
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS == 
            response.StatusSummary.Status):
        return True
    # Error cases
    print "Batch Error code 0x%x" %(response.StatusSummary.Status)
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR == 
            response.StatusSummary.Status):
        for result in response.Results:
            if AF == 4:
                print "Error code for %s/%d is 0x%x" %(
                    str(ipaddress.ip_address(result.Prefix)),
                    result.PrefixLen,
                    result.ErrStatus.Status
                )
            elif AF == 6:
                print "Error code for %s/%d is 0x%x" %(
                    ipaddress.IPv6Address(
                        int((result.Prefix).encode('hex'), 16)
                    ),
                    result.PrefixLen,
                    result.ErrStatus.Status
                )
            else:
                print "Unknown AF %d" %(AF)
                return False
    return False

#
#
#
def validate_route_get_response(response, af):
    # Increment the validated_count
    TestSuite_001_Route_IPv4.validated_count =\
        TestSuite_001_Route_IPv4.validated_count + 1
    #
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS == 
            response.ErrStatus.Status):
        print ""
        print "Corr:%d, Eof:%r, VRF:%s ErrStatus: 0x%x" %(
            response.Correlator, response.Eof,
            response.VrfName, response.ErrStatus.Status)
        for elem in response.Entries:
            if af == 4:
                addr = ipaddress.ip_address(elem.Prefix)
            elif af == 6:
                addr = ipaddress.IPv6Address(
                    int((elem.Prefix).encode('hex'), 16))
            else:
                print "Unknown AF %d" %(af)
                return False
            print "  %s/%d admin:%d LocalLabel:%d" %(
                str(addr), elem.PrefixLen,
                elem.RouteCommon.AdminDistance, elem.RouteCommon.LocalLabel)
            for path in elem.PathList:
                if af == 4:
                    print "    via %s %s" %(
                      str(ipaddress.ip_address(path.NexthopAddress.V4Address)),
                      path.NexthopInterface.Name)
                elif af == 6:
                    print "    via %s %s" %(
                      str(ipaddress.IPv6Address(
                          int((path.NexthopAddress.V6Address).encode('hex'), 
                          16))),
                      path.NexthopInterface.Name)
                print "      Load:%d, Vrf:%s, PathId:%d, Bitmap:0x%x" %(
                    path.LoadMetric, path.VrfName,
                    path.PathId, path.ProtectedPathBitmap[0]) 
                for label in path.LabelStack:
                    print "      Label:%d" %(label)
                if af == 4:
                    for addr in path.RemoteAddress:
                        print "      Remote:%s" %(
                            str(ipaddress.ip_address(addr.V4Address)))
                elif af == 6:
                    for addr in path.RemoteAddress:
                        print "      Remote:%s" %(
                            str(ipaddress.IPv6Address(
                            int((addr.V6Address).encode('hex'), 16))))
                else:
                    print "Unknown AF %d" %(af)
                    return False
        return True
    print "Route Get Error code 0x%x" %(response.ErrStatus.Status)
    return False

#
#
#
def validate_vrf_get_response(response, af):
    print "VRF Get Attributes:"
    print response
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
            response.ErrStatus.Status):
        return False
    return True

#
#
#
def validate_vrf_stats_get_response(response, af):
    print "VRF Get Stats:"
    print response
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
            response.ErrStatus.Status):
        return False
    return True

#
#
#
def validate_lbl_blk_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS == 
            response.StatusSummary.Status):
        return True
    # Error cases
    print "Batch Error code 0x%x" %(response.StatusSummary.Status)
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR == 
            response.StatusSummary.Status):
        for result in response.Results:
            print "Error code for %d is 0x%x" %(
                result.Key.StartLabel,
                result.ErrStatus.Status
            )
    return False

#
#
#
def validate_ilmv4_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS == 
            response.StatusSummary.Status):
        return True
    # Error cases
    print "Batch Error code 0x%x" %(response.StatusSummary.Status)
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR == 
            response.StatusSummary.Status):
        for result in response.Results:
            print "Error code for %d is 0x%x" %(
                result.Key.LocalLabel,
                result.ErrStatus.Status
            )
    return False

#
#
#
def validate_ilmv6_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS == 
            response.StatusSummary.Status):
        return True
    # Error cases
    print "Batch Error code 0x%x" %(response.StatusSummary.Status)
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR == 
            response.StatusSummary.Status):
        for result in response.Results:
            print "Error code for %d is 0x%x" %(
                result.Key.LocalLabel,
                result.ErrStatus.Status
            )
    return False

#
#
#
def validate_bfdv4_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS == 
            response.StatusSummary.Status):
        return True
    # Error cases
    print "Batch Error code 0x%x" %(response.StatusSummary.Status)
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR == 
            response.StatusSummary.Status):
        for result in response.Results:
            print "Error code for %s is 0x%x" %(
                str(ipaddress.ip_address(result.Key.NbrAddr)),
                result.ErrStatus.Status
            )
    return False

#
#
#
def validate_bfd_regop_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.ErrStatus.Status):
        return True
    # Error cases
    print "Response Error code 0x%x" %(response.ErrStatus.Status)
    return False

#
#
#
class ClientTestCase(unittest.TestCase):
    # Class variables
    test_init = False
    # .json input variables to the test
    json_params = None
    # GRPC channel used for GRPC requests
    client = None

    def setUp(self):
        if not ClientTestCase.test_init:
            # Read the .json template
            filepath = os.path.join(os.path.dirname(__file__), 'template.json')
            with open(filepath) as fp:
                ClientTestCase.json_params = json.loads(fp.read())

            # Setup GRPC channel for RPC tests
            host, port = util.get_server_ip_port()
            ClientTestCase.client = GrpcClient(host, port)

            # Initialize only once
            ClientTestCase.test_init = True

#
# Alphabetical order makes this test runs first
#
class TestSuite_000_Global(ClientTestCase):
    # GRPC channel used for Global notifications
    global_notif = None
    # threading.Event() used to sync threads
    global_event = None

    def test_000_global_init(self):
        # Setup a channel for the Global notification thread
        host, port = util.get_server_ip_port()
        TestSuite_000_Global.global_notif = GrpcClient(host, port)

        # Create a synchronization event
        TestSuite_000_Global.global_event = threading.Event()
        # Spawn a thread to wait on notifications
        t = threading.Thread(target = global_init,
                args=(TestSuite_000_Global.global_event,))
        t.start()
        #
        # Wait to hear from the server - Thread is blocked
        print "Waiting to hear from Global event..."
        TestSuite_000_Global.global_event.wait()
        print "Global Event Notification Received! Waiting for events..."

    def test_001_get_globals(self):
        # Get Global info
        response = ClientTestCase.client.global_get()
        err = print_globals(response)
        self.assertTrue(err)

#
#
#
def route_op_iterator(params, oper):
    count = 0
    time_limit = 0
    batch_count = 1
    if 'batch_count' in params[0]:
        batch_count = params[0]['batch_count']
    first_prefix = params[0]['routes'][0]['prefix']
    # Build the route (serializer)
    for b in range(batch_count):
        serializer, next = serializers.route_serializer(*params)
        serializer.Oper = oper
        yield serializer
        count = count + 1
        params[0]['routes'][0]['prefix'] = next
    params[0]['routes'][0]['prefix'] = first_prefix
    while (TestSuite_001_Route_IPv4.validated_count < count):
        time.sleep(0.1)
        time_limit = time_limit + 1
        if time_limit > 30:
            return
    # A return would raise a stopIterator

#
#
#
def route_get_iterator(get_list):
    count = 0
    time_limit = 0
    for item in get_list:
        yield item
        count = count + 1
    while (TestSuite_001_Route_IPv4.validated_count < count):
        time.sleep(0.1)
        time_limit = time_limit + 1
        if time_limit > 30:
            return
    # A return would raise a stopIterator
#
#
#
class TestSuite_001_Route_IPv4(ClientTestCase):
    AF = 4
    STREAM = False
    validated_count = 0

    def setUp(self):
        super(TestSuite_001_Route_IPv4, self).setUp()
        self.route_params = (
            ClientTestCase.json_params['batch_v%d_route' % self.AF],
            ClientTestCase.json_params['paths'],
            ClientTestCase.json_params['nexthops'],
        )
        self.route_label_params = (
            ClientTestCase.json_params['batch_v%d_route_label' % self.AF],
            ClientTestCase.json_params['paths'],
            ClientTestCase.json_params['nexthops'],
        )
        self.vrf_batch = ClientTestCase.json_params['batch_v%d_vrf' % self.AF]
        self.route_get = ClientTestCase.json_params['route_get']
        self.vrf_get = ClientTestCase.json_params['vrf_get']

    def test_000_get_globals(self):
        # Get Global Route info
        response = ClientTestCase.client.global_route_get(self.AF)
        err = print_route_globals(self.AF, response)
        self.assertTrue(err)
    
    def test_001_vrf_registration_add(self):
        response = ClientTestCase.client.vrf_registration_add(self.vrf_batch)
        err = validate_vrf_response(response)
        self.assertTrue(err)

    # This is not a test
    def route_op(self, func, params):
        batch_count = 1
        if 'batch_count' in params[0]:
            batch_count = params[0]['batch_count']
        first_prefix = params[0]['routes'][0]['prefix']
        for b in range(batch_count):
            response, next = func(*params)
            err = validate_route_response(response, self.AF)
            self.assertTrue(err)
            params[0]['routes'][0]['prefix'] = next
        params[0]['routes'][0]['prefix'] = first_prefix

    # This is not a test
    def route_op_stream(self, params, oper):
        iterator = route_op_iterator(params, oper)
        # Must reset this to sync the iterator with the responses
        TestSuite_001_Route_IPv4.validated_count = 0
        count, error = ClientTestCase.client.route_op_stream(iterator,
                self.AF, validate_route_response)
        self.assertTrue(error)
        # This may fail if the server sends EOF prematurely
        # (or we did not wait for the last reply)
        self.assertTrue(count == TestSuite_001_Route_IPv4.validated_count)

    def test_002_route_add(self):
        params = [self.route_params, self.route_label_params]
        for p in params:
            if self.STREAM == False:
                self.route_op(ClientTestCase.client.route_add, p)
            else:
                self.route_op_stream(p, sl_common_types_pb2.SL_OBJOP_ADD)

    def test_003_00_route_update(self):
        params = [self.route_params, self.route_label_params]
        for p in params:
            if self.STREAM == False:
                self.route_op(ClientTestCase.client.route_update, p)
            else:
                self.route_op_stream(p, sl_common_types_pb2.SL_OBJOP_UPDATE)

    def test_003_01_route_update_nhlfe_connected(self):
        ClientTestCase.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = "path_nhlfe_connected"
        self.test_003_00_route_update()

    def test_003_02_route_update_nhlfe_ecmp(self):
        ClientTestCase.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = "path_nhlfe_ecmp"
        self.test_003_00_route_update()
    
    def test_003_03_route_update_nhlfe_non_connected(self):
        ClientTestCase.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = "path_nhlfe_non_connected"
        self.test_003_00_route_update()
    
    def test_003_04_route_update_route_connected(self):
        ClientTestCase.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = "path_route_connected"
        self.test_003_00_route_update()
    
    def test_003_05_route_update_route_ecmp(self):
        ClientTestCase.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = "path_route_ecmp"
        self.test_003_00_route_update()
    
    def test_003_06_route_update_route_non_connected(self):
        ClientTestCase.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = "path_route_non_connected"
        self.test_003_00_route_update()
    
    def test_003_07_route_update_route_primary_with_labels_remote_pq_lfa(self):
        ClientTestCase.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = "path_route_primary_with_labels_remote_pq_lfa"
        self.test_003_00_route_update()
    
    def test_003_08_route_update_route_primary_with_lfa(self):
        ClientTestCase.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = "path_route_primary_with_lfa"
        self.test_003_00_route_update()
    
    # Not a test case
    def route_get_info(self, get_info):
        print get_info["_description"]
        response = ClientTestCase.client.route_get(get_info, self.AF)
        err = validate_route_get_response(response, self.AF)
        self.assertTrue(err)

    def test_004_01_route_get_exact_match(self):
        get_info = self.route_get["get_exact_route"]
        self.route_get_info(get_info)

    def test_004_02_route_get_firstN(self):
        get_info = self.route_get["get_firstN_routes"]
        self.route_get_info(get_info)

    def test_004_03_route_get_nextN_with_specified(self):
        get_info = self.route_get["get_nextN_include_route"]
        self.route_get_info(get_info)
    
    def test_004_03_route_get_nextN_after_specified(self):
        get_info = self.route_get["get_nextN_route"]
        self.route_get_info(get_info)
    
    def test_004_04_route_get_all(self):
        total_routes = 0
        get_info = self.route_get["get_firstN_routes"]
        response = ClientTestCase.client.route_get(get_info, self.AF)
        err = validate_route_get_response(response, self.AF)
        self.assertTrue(err)
        total_routes = total_routes + len(response.Entries)
        get_info = self.route_get["get_nextN_route"]
        while (len(response.Entries)>0) and not response.Eof:
            if self.AF == 4:
                get_info["v%d_prefix"  % self.AF] = str(
                    ipaddress.ip_address(response.Entries[len(response.Entries)-1].Prefix))
            elif self.AF == 6:
                get_info["v%d_prefix"  % self.AF] = str(ipaddress.IPv6Address(
                    int((response.Entries[len(response.Entries)-1].Prefix).encode('hex'), 16)))
            get_info["prefix_len"] = response.Entries[len(response.Entries)-1].PrefixLen
            response = ClientTestCase.client.route_get(get_info, self.AF)
            err = validate_route_get_response(response, self.AF)
            total_routes = total_routes + len(response.Entries)
            self.assertTrue(err)
        print "Total Routes read: %d" %(total_routes)

    def test_004_05_route_get_stream(self):
        serialized_list = []
        # Pack 3 requests
        get_info = self.route_get["get_firstN_routes"]
        get_info["correlator"] = 1
        serializer = serializers.route_get_serializer(get_info, self.AF)
        serialized_list.append(serializer)
        get_info = self.route_get["get_exact_route"]
        get_info["correlator"] = 2
        serializer = serializers.route_get_serializer(get_info, self.AF)
        serialized_list.append(serializer)
        get_info = self.route_get["get_nextN_include_route"]
        get_info["correlator"] = 3
        serializer = serializers.route_get_serializer(get_info, self.AF)
        serialized_list.append(serializer)
        # Call RPC
        iterator = route_get_iterator(serialized_list)
        # Must reset this to sync the iterator with the responses
        TestSuite_001_Route_IPv4.validated_count = 0
        count, error = ClientTestCase.client.route_get_stream(iterator,
            self.AF, validate_route_get_response)
        self.assertTrue(error)
        # This may fail if the server sends EOF prematurely
        if count != len(serialized_list):
            print "Count %d, Expecting:%d" %(count, len(serialized_list))
        self.assertTrue(count == len(serialized_list))

    def test_005_route_stats_get(self):
        response = ClientTestCase.client.global_route_stats_get(self.AF)
        err = print_route_stats_globals(self.AF, response)
        self.assertTrue(err)

    # Not a test case
    def vrf_get_info(self, get_info):
        print get_info["_description"]
        response = ClientTestCase.client.vrf_get(get_info, self.AF, False)
        err = validate_vrf_get_response(response, self.AF)
        self.assertTrue(err)
        response = ClientTestCase.client.vrf_get(get_info, self.AF, True)
        err = validate_vrf_stats_get_response(response, self.AF)
        self.assertTrue(err)

    def test_006_01_vrf_get_exact_match(self):
        get_info = self.vrf_get["get_exact_vrf"]
        self.vrf_get_info(get_info)

    def test_006_02_vrf_get_firstN(self):
        get_info = self.vrf_get["get_firstN_vrf"]
        self.vrf_get_info(get_info)

    def test_006_03_vrf_get_nextN_with_specified(self):
        get_info = self.vrf_get["get_nextN_include_vrf"]
        self.vrf_get_info(get_info)

    def test_006_04_vrf_get_nextN_after_specified(self):
        get_info = self.vrf_get["get_nextN_vrf"]
        self.vrf_get_info(get_info)

    def test_006_05_vrf_get_all(self):
        for stats in [False, True]:
            total_vrfs = 0
            get_info = self.vrf_get["get_firstN_vrf"]
            response = ClientTestCase.client.vrf_get(get_info, self.AF, stats)
            if not stats:
                err = validate_vrf_get_response(response, self.AF)
            else:
                err = validate_vrf_stats_get_response(response, self.AF)
            self.assertTrue(err)
            total_vrfs = total_vrfs + len(response.Entries)
            get_info = self.vrf_get["get_nextN_vrf"]
            while (len(response.Entries)>0) and not response.Eof:
                get_info["vrf_name"] = response.Entries[len(response.Entries)-1].VrfName
                response = ClientTestCase.client.vrf_get(get_info, self.AF, stats)
                if not stats:
                    err = validate_vrf_get_response(response, self.AF)
                else:
                    err = validate_vrf_stats_get_response(response, self.AF)
                total_vrfs = total_vrfs + len(response.Entries)
                self.assertTrue(err)
            print "Total VRFs read: %d" %(total_vrfs)

    def test_007_route_delete(self):
        params = [self.route_params, self.route_label_params]
        for p in params:
            if self.STREAM == False:
                self.route_op(ClientTestCase.client.route_delete, p)
            else:
                self.route_op_stream(p, sl_common_types_pb2.SL_OBJOP_DELETE)

    def test_008_vrf_registration_eof(self):
        response = ClientTestCase.client.vrf_registration_eof(self.vrf_batch)
        err = validate_vrf_response(response)
        self.assertTrue(err)

#
# This class simply inherits the entire v4 class
#
class TestSuite_001_Route_IPv4_Stream(TestSuite_001_Route_IPv4):
    AF = 4
    STREAM = True
    # Inherit all v4 test cases

#
# This class simply inherits the entire v4 class
#
class TestSuite_002_Route_IPv6(TestSuite_001_Route_IPv4):
    AF = 6
    # Inherit all v4 test cases

#
# This class simply inherits the entire v4 class
#
class TestSuite_002_Route_IPv6_Stream(TestSuite_001_Route_IPv4):
    AF = 6
    STREAM = True
    # Inherit all v4 test cases

#
#
#
class TestSuite_003_ILM_IPv4(ClientTestCase):
    AF = 4

    def setUp(self):
        super(TestSuite_003_ILM_IPv4, self).setUp()
        self.ilm_params = (
            ClientTestCase.json_params['batch_ilm'],
            self.AF,
            ClientTestCase.json_params['paths'],
            ClientTestCase.json_params['nexthops'],
        )
        self.lbl_blk_params = ClientTestCase.json_params['batch_mpls_lbl_block']

    def test_000_get_globals(self):
        # Get Global MPLS info
        response = ClientTestCase.client.global_mpls_get()
        err = print_mpls_globals(response)
        self.assertTrue(err)
    
    def test_001_blk_add(self):
        response = ClientTestCase.client.block_label_add(self.lbl_blk_params)
        err = validate_lbl_blk_response(response)
        self.assertTrue(err)
    
    def test_002_ilm_add(self):
        ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_nhlfe_connected"
        response = ClientTestCase.client.ilm_add(*self.ilm_params)
        err = validate_ilmv4_response(response)
        self.assertTrue(err)

    def test_003_00_ilm_update(self):
        response = ClientTestCase.client.ilm_update(*self.ilm_params)
        err = validate_ilmv4_response(response)
        self.assertTrue(err)

    def test_003_01_ilm_update_nhlfe_connected(self):
        ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_nhlfe_connected"
        self.test_003_00_ilm_update()

    def test_003_02_ilm_update_nhlfe_ecmp(self):
        ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_nhlfe_ecmp"
        self.test_003_00_ilm_update()
    
    # Turn off for now
    #def test_003_03_ilm_update_nhlfe_non_connected(self):
    #    ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_nhlfe_non_connected"
    #    self.test_003_00_ilm_update()
    
    def test_003_04_ilm_update_route_connected(self):
        ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_route_connected"
        self.test_003_00_ilm_update()
    
    def test_003_05_ilm_update_route_ecmp(self):
        ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_route_ecmp"
        self.test_003_00_ilm_update()
    
    # Turn off for now
    #def test_003_06_ilm_update_route_non_connected(self):
    #    ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_route_non_connected"
    #    self.test_003_00_ilm_update()
    
    def test_003_07_ilm_update_route_primary_with_labels_remote_pq_lfa(self):
        ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_route_primary_with_labels_remote_pq_lfa"
        self.test_003_00_ilm_update()
    
    def test_003_08_ilm_update_route_primary_with_lfa(self):
        ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_route_primary_with_lfa"
        self.test_003_00_ilm_update()

    def test_003_09_ilm_update_route_lookup(self):
        if self.AF == 6:
            ClientTestCase.json_params['paths']["path_route_lookup"][0]["label_action"] = sl_mpls_pb2.SL_LABEL_ACTION_POP_AND_LOOKUP_IPV6
        ClientTestCase.json_params['batch_ilm']['ilms'][0]['path'] = "path_route_lookup"
        self.test_003_00_ilm_update()

    def test_004_ilm_delete(self):
        response = ClientTestCase.client.ilm_delete(*self.ilm_params)
        err = validate_ilmv4_response(response)
        self.assertTrue(err)

    def test_005_blk_delete(self):
        response = ClientTestCase.client.block_label_delete(self.lbl_blk_params)
        err = validate_lbl_blk_response(response)
        self.assertTrue(err)

#
# This class simply inherits the entire v4 class
#
class TestSuite_004_ILM_IPv6(TestSuite_003_ILM_IPv4):
    AF = 6
    # Inherit all v4 test cases

#
#
#
class TestSuite_005_BFD_IPv4(ClientTestCase):
    AF = 4
    # GRPC channel used for BFD notifications
    bfd_notif = None
    # threading.Event() used to sync threads
    bfd_event = None
    # thread count; increments every time we spawn a new BFD reg thread
    # Note: only one BFD Notif session is allowed at any time. Last one
    # takes over the previous session.
    thread_count = 0

    def setUp(self):
        super(TestSuite_005_BFD_IPv4, self).setUp()
        self.bfd_params = (
            ClientTestCase.json_params['batch_v%d_bfd_singlehop' % self.AF],
            ClientTestCase.json_params['nexthops'],
        )
        
    def test_000_get_globals(self):
        # Get Global BFDv4 info
        response = ClientTestCase.client.global_bfd_get(self.AF)
        err = print_bfd_globals(self.AF, response)
        self.assertTrue(err)
    
    def test_001_bfd_reg_notif(self):      
        #
        # Setup a BFD notification channel
        #
        host, port = util.get_server_ip_port()
        # Setup a channel for the BFD notification thread
        TestSuite_005_BFD_IPv4.bfd_notif = GrpcClient(host, port)
        # Create a synchronization event
        TestSuite_005_BFD_IPv4.bfd_event = threading.Event()
        # Spawn a thread to wait on notifications
        TestSuite_005_BFD_IPv4.thread_count = TestSuite_005_BFD_IPv4.thread_count + 1
        t = threading.Thread(target = bfd_get_notif,
                args=(TestSuite_005_BFD_IPv4.bfd_event,
                TestSuite_005_BFD_IPv4.thread_count))
        t.start()
        #
        # Wait to hear from the server - Thread is blocked
        print "Waiting to hear from BFD thread..."
        TestSuite_005_BFD_IPv4.bfd_event.wait()
        print "BFD thread ok, proceeding"
        self.assertTrue(True)

    def test_002_bfd_register(self):
        response = ClientTestCase.client.bfd_register_oper(self.AF)
        err = validate_bfd_regop_response(response)
        self.assertTrue(err)
        
    def test_003_bfd_add(self):
        response = ClientTestCase.client.bfd_add(*self.bfd_params)
        err = validate_bfdv4_response(response)
        self.assertTrue(err)

    def test_004_bfd_update(self):
        ClientTestCase.json_params['batch_v%d_bfd_singlehop' % self.AF]['sessions'][0]['nexthop'] = 'nh_r2_l2'
        response = ClientTestCase.client.bfd_update(*self.bfd_params)
        err = validate_bfdv4_response(response)
        self.assertTrue(err)

    def test_005_bfd_delete(self):
        response = ClientTestCase.client.bfd_delete(*self.bfd_params)
        err = validate_bfdv4_response(response)
        self.assertTrue(err)

    def test_006_bfd_eof(self):
        response = ClientTestCase.client.bfd_eof_oper(self.AF)
        err = validate_bfd_regop_response(response)
        self.assertTrue(err)

#
#
# Turn off for now
#class TestSuite_006_BFD_IPv4_Multi_Hop(TestSuite_005_BFD_IPv4):
#    def setUp(self):
#        super(TestSuite_005_BFD_IPv4, self).setUp()
#        self.bfd_params = (
#            ClientTestCase.json_params['batch_v%d_bfd_multihop' % self.AF],
#            ClientTestCase.json_params['nexthops'],
#        )
#    # Inherit all TestSuite_005_BFD_IPv4 test cases

if __name__ == '__main__':
    unittest.main()
