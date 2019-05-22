#
# Copyright (c) 2016-2018 by cisco Systems, Inc. 
# All rights reserved.
#
import json
import os
import unittest
import ipaddress
import threading
import time

from binascii import hexlify

from sl_api import GrpcClient
from genpy import sl_common_types_pb2
from genpy import sl_global_pb2
from genpy import sl_mpls_pb2
from genpy import sl_bfd_common_pb2
from genpy import sl_interface_pb2
from genpy import sl_l2_route_pb2
from util import util
from sl_api import serializers
from sl_api import BD_Util
from sl_api import Route_Util

#
#
#
class clientClass():
    json_params = None
    client = None
    global_notif = None
    is_ut_running = False

    ut_mutex = threading.Lock()

    def is_running():
        # if unit test is done return false
        # otherwise return true
        # release lock if it has been acquired
        if clientClass.ut_mutex.acquire(False):
            check_ut_status = clientClass.is_ut_running
            clientClass.ut_mutex.release()
            if check_ut_status == False:
                return False
            return True
        else:
            return True

    def set_ut_running(running):
        clientClass.ut_mutex.acquire()
        clientClass.is_ut_running = running
        clientClass.ut_mutex.release()

#
#
#
def setUpModule():
    clientClass.set_ut_running(True)

    # Read the .json template
    filepath = os.path.join(os.path.dirname(__file__), 'template.json')

    with open(filepath) as fp:
        clientClass.json_params = json.loads(fp.read())

    # Setup GRPC channel for RPC tests
    host, port = util.get_server_ip_port()
    clientClass.client = GrpcClient(host, port)

    # GRPC channel used for Global notifications
    # Setup a channel for the Global notification thread
    clientClass.global_notif = GrpcClient(host, port)

    # threading.Event() used to sync threads
    # Create a synchronization event
    global_event = threading.Event()
    # Spawn a thread to wait on notifications
    t = threading.Thread(target = global_init,
            args=(global_event,))
    t.start()
    #
    # Wait to hear from the server - Thread is blocked
    print("Waiting to hear from Global event...")
    global_event.wait()
    print("Global Event Notification Received! Waiting for events...")

#
#
#
def tearDownModule():
    clientClass.set_ut_running(False)

# Print Received Globals
def print_globals(response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print("Max VRF Name Len     : %d" %(response.MaxVrfNameLength))
        print("Max Iface Name Len   : %d" %(response.MaxInterfaceNameLength))
        print("Max Paths per Entry  : %d" %(response.MaxPathsPerEntry))
        print("Max Prim per Entry   : %d" %(response.MaxPrimaryPathPerEntry))
        print("Max Bckup per Entry  : %d" %(response.MaxBackupPathPerEntry))
        print("Max Labels per Entry : %d" %(response.MaxMplsLabelsPerPath))
        print("Min Prim Path-id     : %d" %(response.MinPrimaryPathIdNum))
        print("Max Prim Path-id     : %d" %(response.MaxPrimaryPathIdNum))
        print("Min Bckup Path-id    : %d" %(response.MinBackupPathIdNum))
        print("Max Bckup Path-id    : %d" %(response.MaxBackupPathIdNum))
        print("Max Remote Bckup Addr: %d" %(response.MaxRemoteAddressNum))
        print("Max L2 Bd Name Length: %d" %(response.MaxL2BdNameLength))
        print("Max L2 PMSI Tunnel Id Length %d" %(response.MaxL2PmsiTunnelIdLength))

    else:
        print("Globals response Error 0x%x" %(response.ErrStatus.Status))
        return False
    return True

# Print Received Route Globals
def print_route_globals(af, response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print("Max v%d VRF Reg Per VRF Msg : %d" %(af,
            response.MaxVrfregPerVrfregmsg))
        print("Max v%d Routes per Route Msg: %d" %(af,
            response.MaxRoutePerRoutemsg))
    else:
        print("Route Globals response Error 0x%x" %(response.ErrStatus.Status))
        return False
    return True

# Print Received Route Globals
def print_route_stats_globals(af, response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print("")
        print("VrfCount   v%d: %d" %(af, response.VrfCount))
        print("RouteCount v%d: %d" %(af, response.RouteCount))
    else:
        print("Route Get Stats response Error 0x%x" %(response.ErrStatus.Status))
        return False
    return True

# Print Received MPLS Globals
def print_mpls_globals(response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print("Max labels per label block            : %d" %(
            response.MaxLabelsPerBlock))
        print("Max label blocks per MplsLabelBlockMsg: %d" %(
            response.MaxLabelblocksPerLabelblockmsg))
        print("Min Start Label                       : %d" %(
            response.MinStartLabel))
        print("Label Table Size                      : %d" %(
            response.LabelTableSize))
        print("Max ILMs per IlmMsg                   : %d" %(
            response.MaxIlmPerIlmmsg))
        print("Max Paths per Ilm                     : %d" %(
            response.MaxPathsPerIlm))
    else:
        print("MPLS Globals response Error 0x%x" %(response.ErrStatus.Status))
        return False
    return True

# Print Received BFD Globals
def print_bfd_globals(af, response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print("Max v%d BFD Sess Per BFD Msg : %d" %(af,
            response.MaxBfdSessionCfgPerSLBfdMsg))
        print("Min v%d BFD Tx Interval Single hop  : %d" %(af,
            response.MinBfdTxIntervalSingleHop))
        print("Min v%d BFD Tx Interval Multi hop   : %d" %(af,
            response.MinBfdTxIntervalMultiHop))
        print("Min v%d BFD Detect Multi Single hop : %d" %(af,
            response.MinBfdDetectMultiplierSingleHop))
        print("Min v%d BFD Detect Multi Multi hop  : %d" %(af,
            response.MinBfdDetectMultiplierMultiHop))
    else:
        print("BFD Globals response Error 0x%x" %(response.ErrStatus.Status))
        return False
    return True

# Print Received BFD Stats
def print_bfd_stats(af, response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print(response)
    else:
        print("BFD Stats response Error 0x%x" %(response.ErrStatus.Status))
        return False
    return True

# Global notification Callback
# This function is called from the global_init thread context
# To break the stream recv(), return False
def global_init_cback(response, event):
    if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_VERSION:
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.ErrStatus.Status) or \
            (sl_common_types_pb2.SLErrorStatus.SL_INIT_STATE_CLEAR ==
                response.ErrStatus.Status) or \
            (sl_common_types_pb2.SLErrorStatus.SL_INIT_STATE_READY ==
                response.ErrStatus.Status):
            print("Server Returned 0x%x, Server's Version %d.%d.%d" %(
                response.ErrStatus.Status,
                response.InitRspMsg.MajorVer,
                response.InitRspMsg.MinorVer,
                response.InitRspMsg.SubVer))
            # Successfully Initialized
            # This would notify the main thread to proceed
            event.set()
        else:
            return False
    elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_HEARTBEAT:
        print("Received Event: Heartbeat")
        if not clientClass.is_running():
            os._exit(0)
        return True
    elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
        print("Received Global Error event:", response)
        return False
    else:
        print("Received unknown event:", response)
        return False

    # Continue looping on events
    return True

# Wait on Global notification events
def global_init(event):
    g_params = clientClass.json_params['global_init']

    try:
        response = clientClass.global_notif.global_init(g_params,
            global_init_cback, event)

        # Should return on errors
        if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
            if (response.ErrStatus.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
                print("Service Layer Session was taken over by another client")
        else:
            # If this session is lost, then most likely the server restarted
            print("global_init: exiting unexpectedly, Server Restart?")
            print("last response from server:", response)
    except Exception as e:
        print("Received exception:", e)
        print("Server died?")
    os._exit(0)

# BFD notification Callback
# This function is called from the BFD thread context
# To break the stream recv(), return False
def bfd_notif_cback(response, af):
    if response.EventType == sl_bfd_common_pb2.SL_BFD_EVENT_TYPE_ERROR:
        if (response.ErrStatus.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
            print("Received notification to Terminate, Stream taken over?")
        else:
            print("Received error 0x%x" %(response.ErrStatus.Status))
        return False
    elif response.EventType == sl_bfd_common_pb2.SL_BFD_EVENT_TYPE_SESSION_STATE:
        print("Received BFD Event:")
        if af == 4:
            print("Nbr : %s" %(
                str(ipaddress.ip_address(response.Session.Key.NbrAddr))))
        elif af == 6:
            print("Nbr : %s" %(
                str(ipaddress.IPv6Address(
                    int(hexlify(response.Session.Key.NbrAddr), 16)))))
        print(response)
    else:
        print("Received an unexpected event type %d" %(
            response.EventType))
        return False
    # Continue looping on events
    return True

# Wait on BFD notification events
def bfd_get_notif(event, af, thread_count):
    # This would notify the main thread to proceed
    event[af].set()
    # RPC to get Notifications
    response = TestSuite_005_BFD_IPv4.bfd_notif[af].bfd_get_notif(bfd_notif_cback, af)
    # Above, Should return on errors
    print("bfd_get_notif: thread %d exiting. response: %s" %(thread_count,
        response))
    # Do not exit the process, as other tests could be still going
#
#
#
def validate_vrf_response(response):
    if (response.StatusSummary.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        return True
    # Error cases
    print("Batch Error code 0x%x" %(response.StatusSummary.Status))
    # SOME ERROR
    if (response.StatusSummary.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR):
        for result in response.Results:
            print("Error code for %s is 0x%x" %(result.VrfName,
                result.ErrStatus.Status
            ))
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
    print("Batch Error code 0x%x" %(response.StatusSummary.Status))
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
            response.StatusSummary.Status):
        for result in response.Results:
            if AF == 4:
                print("Error code for %s/%d is 0x%x" %(
                    str(ipaddress.ip_address(result.Prefix)),
                    result.PrefixLen,
                    result.ErrStatus.Status
                ))
            elif AF == 6:
                print("Error code for %s/%d is 0x%x" %(
                    ipaddress.IPv6Address(
                        int(hexlify(result.Prefix), 16)
                    ),
                    result.PrefixLen,
                    result.ErrStatus.Status
                ))
            else:
                print("Unknown AF %d" %(AF))
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
        print("Route Get Msg Resp:")
        print("Corr:%d, Eof:%r, VRF:%s ErrStatus: 0x%x" %(
            response.Correlator, response.Eof,
            response.VrfName, response.ErrStatus.Status))
        for elem in response.Entries:
            if af == 4:
                addr = ipaddress.ip_address(elem.Prefix)
            elif af == 6:
                addr = ipaddress.IPv6Address(
                    int(hexlify(elem.Prefix),16))
            else:
                print("Unknown AF %d" %(af))
                return False
            print("  %s/%d" %(str(addr), elem.PrefixLen))
            for path in elem.PathList:
                if af == 4:
                    print("    via %s" %(
                      str(ipaddress.ip_address(path.NexthopAddress.V4Address))))
                elif af == 6:
                    print("    via %s" %(
                      str(ipaddress.IPv6Address(
                          int(hexlify(path.NexthopAddress.V6Address),
                          16)))))
                if af == 4:
                    for addr in path.RemoteAddress:
                        print("      Remote:%s" %(
                            str(ipaddress.ip_address(addr.V4Address))))
                elif af == 6:
                    for addr in path.RemoteAddress:
                        print("      Remote:%s" %(
                            str(ipaddress.IPv6Address(
                            int(hexlify(addr.V6Address), 16)))))
                else:
                    print("Unknown AF %d" %(af))
                    return False
            print("Details:")
            print(elem)
        return True
    print("Route Get Error code 0x%x" %(response.ErrStatus.Status))
    return False

#
#
#
def validate_vrf_get_response(response, af):
    print("VRF Get Attributes:")
    print(response)
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
            response.ErrStatus.Status):
        return False
    return True

#
#
#
def validate_vrf_stats_get_response(response, af):
    print("VRF Get Stats:")
    print(response)
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
            response.ErrStatus.Status):
        return False
    return True

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
    if 'local_label' in params[0]['routes'][0]:
        first_label = params[0]['routes'][0]['local_label']
    # Build the route (serializer)
    for b in range(batch_count):
        serializer, next, label = serializers.route_serializer(*params)
        serializer.Oper = oper
        yield serializer
        count = count + 1
        params[0]['routes'][0]['prefix'] = next
        if 'local_label' in params[0]['routes'][0]:
            params[0]['routes'][0]['local_label'] = label
    params[0]['routes'][0]['prefix'] = first_prefix
    if 'local_label' in params[0]['routes'][0]:
        params[0]['routes'][0]['local_label'] = first_label
    while (TestSuite_001_Route_IPv4.validated_count < count):
        time.sleep(0.1)
        time_limit = time_limit + 1
        if time_limit > 100:
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
        if time_limit > 100:
            return
    # A return would raise a stopIterator

#
#
#
def validate_mpls_regop_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.ErrStatus.Status):
        return True
    # Error cases
    print("Response Error code 0x%x" %(response.ErrStatus.Status))
    return False

#
#
# Print Received MPLS Stats
def print_mpls_stats(response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print("LabelBlockCount : %d" %(response.LabelBlockCount))
        print("IlmCount : %d" %(response.IlmCount))
    else:
        print("MPLS Stats response Error 0x%x" %(response.ErrStatus.Status))
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
    print("Batch Error code 0x%x" %(response.StatusSummary.Status))
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
            response.StatusSummary.Status):
        for result in response.Results:
            print("Error code for %d is 0x%x" %(
                result.Key.StartLabel,
                result.ErrStatus.Status
            ))
    return False

#
#
#
def validate_lbl_blk_get_response(response):
    # Increment the validated_count
    TestSuite_003_ILM_IPv4.validated_count =\
        TestSuite_001_Route_IPv4.validated_count + 1
    #
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.ErrStatus.Status):
        print(response)
        return True
    print("Label Block Get Error code 0x%x" %(response.ErrStatus.Status))
    return False

#
#
#
def validate_ilm_response(response):
    # Increment the validated_count
    TestSuite_003_ILM_IPv4.validated_count =\
        TestSuite_003_ILM_IPv4.validated_count + 1
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
        return True
    # Error cases
    print("Batch Error code 0x%x" %(response.StatusSummary.Status))
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
            response.StatusSummary.Status):
        for result in response.Results:
            print("Error code for %d is 0x%x" %(
                result.Key.LocalLabel,
                result.ErrStatus.Status
            ))
    return False

#
#
#
def ilm_op_iterator(params, oper):
    count = 0
    time_limit = 0
    batch_count = 1
    if 'batch_count' in params[0]:
        batch_count = params[0]['batch_count']
    first_label = params[0]['ilms'][0]['in_label']
    # Build the ilm (serializer)
    for b in range(batch_count):
        serializer, next = serializers.ilm_serializer(*params)
        serializer.Oper = oper
        yield serializer
        count = count + 1
        params[0]['ilms'][0]['in_label'] = next
    params[0]['ilms'][0]['in_label'] = first_label
    while (TestSuite_003_ILM_IPv4.validated_count < count):
        time.sleep(0.1)
        time_limit = time_limit + 1
        if time_limit > 100:
            return
    # A return would raise a stopIterator

#
#
#
def ilm_get_iterator(get_list):
    count = 0
    time_limit = 0
    for item in get_list:
        yield item
        count = count + 1
    while (TestSuite_003_ILM_IPv4.validated_count < count):
        time.sleep(0.1)
        time_limit = time_limit + 1
        if time_limit > 100:
            return
    # A return would raise a stopIterator

#
#
#
def validate_ilm_get_response(response):
    # Increment the validated_count
    TestSuite_003_ILM_IPv4.validated_count =\
        TestSuite_003_ILM_IPv4.validated_count + 1
    #
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.ErrStatus.Status):
        print(response)
        return True
    print("ILM Get Error code 0x%x" %(response.ErrStatus.Status))
    return False


#
#
#
def validate_bfd_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
        return True
    # Error cases
    print("Batch Error code 0x%x" %(response.StatusSummary.Status))
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
            response.StatusSummary.Status):
        for result in response.Results:
            print("Error code for %s is 0x%x" %(
                str(ipaddress.ip_address(result.Key.NbrAddr)),
                result.ErrStatus.Status
            ))
    return False

#
#
#
def validate_bfd_regop_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.ErrStatus.Status):
        return True
    # Error cases
    print("Response Error code 0x%x" %(response.ErrStatus.Status))
    return False

#
#
#
def validate_bfd_get_response(response, af):
    print("BFD Get Attributes:")
    print(response)
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
            response.ErrStatus.Status):
        return False
    return True

#
#
# Print Received Interface Globals
def print_intf_globals(response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print("Max Intf Per Msg : %d" %(response.MaxInterfacesPerBatch))
    else:
        print("Intf Globals response Error 0x%x" %(response.ErrStatus.Status))
        return False
    return True

# Interface notification Callback
# This function is called from the Interface thread context
# To break the stream recv(), return False
def intf_notif_cback(response):
    if response.EventType == sl_interface_pb2.SL_INTERFACE_EVENT_TYPE_ERROR:
        if (response.ErrStatus.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
            print("Received notification to Terminate, Stream taken over?")
        else:
            print("Received error 0x%x" %(response.ErrStatus.Status))
        return False
    elif response.EventType == sl_interface_pb2.SL_INTERFACE_EVENT_TYPE_INTERFACE_INFO:
        print("Received Interface Event:", response)
    else:
        print("Received an unexpected event type %d" %(
            response.EventType))
        return False
    # Continue looping on events
    return True

#
#
# Wait on Intf notification events
def intf_get_notif(event, thread_count):
    # This would notify the main thread to proceed
    event.set()
    # RPC to get Notifications
    response = TestSuite_009_INTERFACE.intf_notif.intf_get_notif(intf_notif_cback)
    # Above, Should return on errors
    print("intf_get_notif: thread %d exiting. response: %s" %(thread_count,
        response))
    # Do not exit the process, as other tests could be still going

#
#
#
def validate_intf_regop_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.ErrStatus.Status):
        return True
    # Error cases
    print("Response Error code 0x%x" %(response.ErrStatus.Status))
    return False

#
#
# Print Received BFD Stats
def print_intf_stats(response):
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print(response)
    else:
        print("Intf Stats response Error 0x%x" %(response.ErrStatus.Status))
        return False
    return True


#
#
#
def validate_intf_response(response):
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
        return True
    # Error cases
    print("Batch Error code 0x%x" %(response.StatusSummary.Status))
    # SOME ERROR
    if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
            response.StatusSummary.Status):
        print(response)
    return False

#
#
#
def validate_intf_get_response(response):
    print("Intf Get Attributes:")
    print(response)
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
            response.ErrStatus.Status):
        return False
    return True

#
# Alphabetical order makes this test runs first
#
class TestSuite_000_Global(unittest.TestCase):
    def test_001_get_globals(self):
        # Get Global info
        response = clientClass.client.global_get()
        err = print_globals(response)
        self.assertTrue(err)
#
#
#
class TestSuite_001_Route_IPv4(unittest.TestCase):
    AF = 4
    STREAM = False
    validated_count = 0
    # GRPC channel used for L3 Route notifications
    l3route_notif = None
    # threading.Event() used to sync threads
    l3route_event = None
    # thread count
    thread_count = 0

    def setUp(self):
        super(TestSuite_001_Route_IPv4, self).setUp()
        self.route_params = (
            clientClass.json_params['batch_v%d_route' % self.AF],
            clientClass.json_params['paths'],
            clientClass.json_params['nexthops'],
        )
        self.route_label_params = (
            clientClass.json_params['batch_v%d_route_label' % self.AF],
            clientClass.json_params['paths'],
            clientClass.json_params['nexthops'],
        )
        self.vrf_batch = clientClass.json_params['batch_v%d_vrf' % self.AF]
        self.route_get = clientClass.json_params['route_get']
        self.vrf_get = clientClass.json_params['vrf_get']

    def test_000_get_globals(self):
        # Get Global Route info
        response = clientClass.client.global_route_get(self.AF)
        err = print_route_globals(self.AF, response)
        self.assertTrue(err)

    def test_001_vrf_registration_add(self):
        response = clientClass.client.vrf_registration_add(self.vrf_batch)
        err = validate_vrf_response(response)
        self.assertTrue(err)

    # This is not a test
    def route_op(self, func, params):
        batch_count = 1
        if 'batch_count' in params[0]:
            batch_count = params[0]['batch_count']
        # We only use params[0]['routes'][0] in case of batch>0 and range>0
        first_prefix = params[0]['routes'][0]['prefix']
        if 'local_label' in params[0]['routes'][0]:
            first_label = params[0]['routes'][0]['local_label']
        for b in range(batch_count):
            response, next, label = func(*params)
            err = validate_route_response(response, self.AF)
            self.assertTrue(err)
            params[0]['routes'][0]['prefix'] = next
            if 'local_label' in params[0]['routes'][0]:
                params[0]['routes'][0]['local_label'] = label
        params[0]['routes'][0]['prefix'] = first_prefix
        if 'local_label' in params[0]['routes'][0]:
            params[0]['routes'][0]['local_label'] = first_label

    # This is not a test
    def route_op_stream(self, params, oper):
        iterator = route_op_iterator(params, oper)
        # Must reset this to sync the iterator with the responses
        TestSuite_001_Route_IPv4.validated_count = 0
        count, error = clientClass.client.route_op_stream(iterator,
                self.AF, validate_route_response)
        self.assertTrue(error)
        # This may fail if the server sends EOF prematurely
        # (or we did not wait for the last reply)
        self.assertTrue(count == TestSuite_001_Route_IPv4.validated_count)

    def test_002_route_add(self):
        params = [self.route_params, self.route_label_params]
        for p in params:
            if self.STREAM == False:
                self.route_op(clientClass.client.route_add, p)
            else:
                self.route_op_stream(p, sl_common_types_pb2.SL_OBJOP_ADD)

    def test_002_00_l3route_notif_channel_setup(self):
        # Setup a grpc channel
        host, port = util.get_server_ip_port()
        # Setup a channel and store info
        TestSuite_001_Route_IPv4.l3route_notif = GrpcClient(host, port)

        TestSuite_001_Route_IPv4.l3route_notif.l3route_get_notif(self.AF)
        time.sleep(3)

    def test_003_00_route_update(self, name = None):
        temp = None
        if name != None:
            temp = clientClass.json_params['batch_v%d_route' % self.AF]['routes'][0]['path']
            clientClass.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = name
        params = [self.route_params, self.route_label_params]
        for p in params:
            if self.STREAM == False:
                self.route_op(clientClass.client.route_update, p)
            else:
                self.route_op_stream(p, sl_common_types_pb2.SL_OBJOP_UPDATE)
        # NOTE: If the above fails, the following wont be restored
        if name != None:
            clientClass.json_params['batch_v%d_route' % self.AF]['routes'][0]['path'] = temp

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

    # Not a test case
    def route_get_info(self, get_info):
        print(get_info["_description"])
        response = clientClass.client.route_get(get_info, self.AF)
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
        response = clientClass.client.route_get(get_info, self.AF)
        err = validate_route_get_response(response, self.AF)
        self.assertTrue(err)
        total_routes = total_routes + len(response.Entries)
        get_info = self.route_get["get_nextN_route"]
        prefix_temp = get_info["v%d_prefix"  % self.AF]
        prefix_len_temp = get_info["prefix_len"]
        while (len(response.Entries)>0) and not response.Eof:
            if self.AF == 4:
                last_prefix = ipaddress.ip_address(response.Entries[len(response.Entries)-1].Prefix)
                get_info["v%d_prefix"  % self.AF] = str(last_prefix)
            elif self.AF == 6:
                last_prefix = ipaddress.IPv6Address(
                    int(hexlify(response.Entries[len(response.Entries)-1].Prefix), 16)
                )
                get_info["v%d_prefix"  % self.AF] = str(last_prefix)
            get_info["prefix_len"] = response.Entries[len(response.Entries)-1].PrefixLen
            response = clientClass.client.route_get(get_info, self.AF)
            err = validate_route_get_response(response, self.AF)
            total_routes = total_routes + len(response.Entries)
            self.assertTrue(err)
        get_info["v%d_prefix"  % self.AF] = prefix_temp
        get_info["prefix_len"] = prefix_len_temp
        print("Total Routes read: %d" %(total_routes))

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
        count, error = clientClass.client.route_get_stream(iterator,
            self.AF, validate_route_get_response)
        self.assertTrue(error)
        # This may fail if the server sends EOF prematurely
        if count != len(serialized_list):
            print("Count %d, Expecting:%d" %(count, len(serialized_list)))
        self.assertTrue(count == len(serialized_list))

    def test_005_route_stats_get(self):
        response = clientClass.client.global_route_stats_get(self.AF)
        err = print_route_stats_globals(self.AF, response)
        self.assertTrue(err)

    # Not a test case
    def vrf_get_info(self, get_info):
        print(get_info["_description"])
        response = clientClass.client.vrf_get(get_info, self.AF, False)
        err = validate_vrf_get_response(response, self.AF)
        self.assertTrue(err)
        response = clientClass.client.vrf_get(get_info, self.AF, True)
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
            response = clientClass.client.vrf_get(get_info, self.AF, stats)
            if not stats:
                err = validate_vrf_get_response(response, self.AF)
            else:
                err = validate_vrf_stats_get_response(response, self.AF)
            self.assertTrue(err)
            total_vrfs = total_vrfs + len(response.Entries)
            get_info = self.vrf_get["get_nextN_vrf"]
            vrf_name_temp = get_info["vrf_name"]
            while (len(response.Entries)>0) and not response.Eof:
                last_vrfName = response.Entries[len(response.Entries)-1].VrfName
                get_info["vrf_name"] = last_vrfName
                response = clientClass.client.vrf_get(get_info, self.AF, stats)
                if not stats:
                    err = validate_vrf_get_response(response, self.AF)
                else:
                    err = validate_vrf_stats_get_response(response, self.AF)
                total_vrfs = total_vrfs + len(response.Entries)
                self.assertTrue(err)
            get_info["vrf_name"] = vrf_name_temp
            print("Total VRFs read: %d" %(total_vrfs))

    def test_007_route_delete(self):
        params = [self.route_params, self.route_label_params]
        for p in params:
            if self.STREAM == False:
                self.route_op(clientClass.client.route_delete, p)
            else:
                self.route_op_stream(p, sl_common_types_pb2.SL_OBJOP_DELETE)

    def test_008_vrf_registration_eof(self):
        response = clientClass.client.vrf_registration_eof(self.vrf_batch)
        err = validate_vrf_response(response)
        self.assertTrue(err)

    def test_009_vrf_unregistration(self):
        response = clientClass.client.vrf_registration_delete(self.vrf_batch)
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
class TestSuite_003_ILM_IPv4(unittest.TestCase):
    AF = 4
    STREAM = False
    validated_count = 0

    def setUp(self):
        super(TestSuite_003_ILM_IPv4, self).setUp()
        self.ilm_params = (
            clientClass.json_params['batch_ilm'],
            self.AF,
            clientClass.json_params['paths'],
            clientClass.json_params['nexthops'],
        )
        self.lbl_blk_params = clientClass.json_params['batch_mpls_lbl_block']
        self.ilm_get = clientClass.json_params['ilm_get']
        self.lbl_blk_get = clientClass.json_params['lbl_blk_get']

    def test_000_get_globals(self):
        # Get Global MPLS info
        response = clientClass.client.mpls_global_get()
        err = print_mpls_globals(response)
        self.assertTrue(err)

    def test_001_mpls_register(self):
        response = clientClass.client.mpls_register_oper()
        err = validate_mpls_regop_response(response)
        self.assertTrue(err)

    def test_002_blk_add(self):
        response = clientClass.client.label_block_add(self.lbl_blk_params)
        err = validate_lbl_blk_response(response)
        self.assertTrue(err)

    # This is not a test
    def ilm_op(self, func, params):
        batch_count = 1
        if 'batch_count' in params[0]:
            batch_count = params[0]['batch_count']
        first_label = params[0]['ilms'][0]['in_label']
        for b in range(batch_count):
            response, next = func(*params)
            err = validate_ilm_response(response)
            self.assertTrue(err)
            params[0]['ilms'][0]['in_label'] = next
        params[0]['ilms'][0]['in_label'] = first_label

    # This is not a test
    def ilm_op_stream(self, params, oper):
        iterator = ilm_op_iterator(params, oper)
        # Must reset this to sync the iterator with the responses
        TestSuite_003_ILM_IPv4.validated_count = 0
        count, error = clientClass.client.ilm_op_stream(iterator,
                validate_ilm_response)
        self.assertTrue(error)
        # This may fail if the server sends EOF prematurely
        # (or we did not wait for the last reply)
        self.assertTrue(count == TestSuite_003_ILM_IPv4.validated_count)

    def test_003_ilm_add(self):
        if self.STREAM == False:
            self.ilm_op(clientClass.client.ilm_add,
                self.ilm_params)
        else:
            self.ilm_op_stream(self.ilm_params,
                sl_common_types_pb2.SL_OBJOP_ADD)

    def test_004_00_ilm_update(self, name = None):
        temp = None
        if name != None:
            temp = clientClass.json_params['batch_ilm']['ilms'][0]['path']
            clientClass.json_params['batch_ilm']['ilms'][0]['path'] = name
        if self.STREAM == False:
            self.ilm_op(clientClass.client.ilm_update,
                self.ilm_params)
        else:
            self.ilm_op_stream(self.ilm_params,
                sl_common_types_pb2.SL_OBJOP_UPDATE)
        # NOTE: If the above fails, the following wont be restored
        if name != None:
            clientClass.json_params['batch_ilm']['ilms'][0]['path'] = temp

    def test_004_01_ilm_update_nhlfe_connected(self):
        self.test_004_00_ilm_update("path_nhlfe_connected")

    def test_004_02_ilm_update_nhlfe_ecmp(self):
        self.test_004_00_ilm_update("path_nhlfe_ecmp")

    # Turn off for now - Not supported
    #def test_004_03_ilm_update_nhlfe_non_connected(self):
    #    self.test_004_00_ilm_update("path_nhlfe_non_connected")

    def test_004_04_ilm_update_route_connected(self):
        self.test_004_00_ilm_update("path_route_connected")

    def test_004_05_ilm_update_route_ecmp(self):
        self.test_004_00_ilm_update("path_route_ecmp")

    # Turn off for now - Not supported
    #def test_004_06_ilm_update_route_non_connected(self):
    #    self.test_004_00_ilm_update("path_route_non_connected")

    def test_004_07_ilm_update_route_primary_with_labels_remote_pq_lfa(self):
        self.test_004_00_ilm_update("path_route_primary_with_labels_remote_pq_lfa")

    def test_004_08_ilm_update_route_primary_with_lfa(self):
        self.test_004_00_ilm_update("path_route_primary_with_lfa")

    def test_004_09_ilm_update_route_lookup(self):
        temp = clientClass.json_params['paths']["path_route_lookup"][0]["label_action"]
        if self.AF == 6:
            clientClass.json_params['paths']["path_route_lookup"][0]["label_action"] = sl_mpls_pb2.SL_LABEL_ACTION_POP_AND_LOOKUP_IPV6
        self.test_004_00_ilm_update("path_route_lookup")
        # Restore
        if self.AF == 6:
            clientClass.json_params['paths']["path_route_lookup"][0]["label_action"] = temp

    def test_005_get_stats(self):
        # Get Global MPLS stats
        response = clientClass.client.mpls_global_get_stats()
        err = print_mpls_stats(response)
        self.assertTrue(err)

    # Not a test case
    def ilm_get_info(self, get_info):
        print(get_info["_description"])
        response = clientClass.client.ilm_get(get_info)
        err = validate_ilm_get_response(response)
        self.assertTrue(err)

    def test_006_01_ilm_get_exact_match(self):
        get_info = self.ilm_get["get_exact_ilm"]
        self.ilm_get_info(get_info)

    def test_006_02_ilm_get_firstN(self):
        get_info = self.ilm_get["get_firstN_ilm"]
        self.ilm_get_info(get_info)

    def test_006_03_ilm_get_nextN_with_specified(self):
        get_info = self.ilm_get["get_nextN_include_ilm"]
        self.ilm_get_info(get_info)

    def test_006_04_ilm_get_nextN_after_specified(self):
        get_info = self.ilm_get["get_nextN_ilm"]
        self.ilm_get_info(get_info)

    def test_006_05_ilm_get_all(self):
        total_ilms = 0
        get_info = self.ilm_get["get_firstN_ilm"]
        response = clientClass.client.ilm_get(get_info)
        err = validate_ilm_get_response(response)
        self.assertTrue(err)
        total_ilms = total_ilms + len(response.Entries)
        get_info = self.ilm_get["get_nextN_ilm"]
        label_temp = get_info["in_label"]
        while (len(response.Entries)>0) and not response.Eof:
            last_label = response.Entries[len(response.Entries)-1].Key.LocalLabel
            get_info["in_label"] = last_label
            response = clientClass.client.ilm_get(get_info)
            err = validate_ilm_get_response(response)
            total_ilms = total_ilms + len(response.Entries)
            self.assertTrue(err)
        get_info["in_label"] = label_temp
        print("Total ilms read: %d" %(total_ilms))

    def test_006_06_ilm_get_stream(self):
        serialized_list = []
        # Pack 3 requests
        get_info = self.ilm_get["get_firstN_ilm"]
        get_info["correlator"] = 1
        serializer = serializers.ilm_get_serializer(get_info)
        serialized_list.append(serializer)
        get_info = self.ilm_get["get_exact_ilm"]
        get_info["correlator"] = 2
        serializer = serializers.ilm_get_serializer(get_info)
        serialized_list.append(serializer)
        get_info = self.ilm_get["get_nextN_include_ilm"]
        get_info["correlator"] = 3
        serializer = serializers.ilm_get_serializer(get_info)
        serialized_list.append(serializer)
        # Call RPC
        iterator = ilm_get_iterator(serialized_list)
        # Must reset this to sync the iterator with the responses
        TestSuite_003_ILM_IPv4.validated_count = 0
        count, error = clientClass.client.ilm_get_stream(iterator,
            validate_ilm_get_response)
        self.assertTrue(error)
        # This may fail if the server sends EOF prematurely
        if count != len(serialized_list):
            print("Count %d, Expecting:%d" %(count, len(serialized_list)))
        self.assertTrue(count == len(serialized_list))

    def test_007_ilm_delete(self):
        if self.STREAM == False:
            self.ilm_op(clientClass.client.ilm_delete,
                self.ilm_params)
        else:
            self.ilm_op_stream(self.ilm_params,
                sl_common_types_pb2.SL_OBJOP_DELETE)

    # Not a test case
    def lbl_blk_get_info(self, get_info):
        print(get_info["_description"])
        response = clientClass.client.label_block_get(get_info)
        err = validate_lbl_blk_get_response(response)
        self.assertTrue(err)

    def test_008_01_lbl_blk_get_exact_match(self):
        get_info = self.lbl_blk_get["get_exact_lbl_blk"]
        self.lbl_blk_get_info(get_info)

    def test_008_02_lbl_blk_get_firstN(self):
        get_info = self.lbl_blk_get["get_firstN_lbl_blk"]
        self.lbl_blk_get_info(get_info)

    def test_008_03_lbl_blk_get_nextN_with_specified(self):
        get_info = self.lbl_blk_get["get_nextN_include_lbl_blk"]
        self.lbl_blk_get_info(get_info)

    def test_008_04_lbl_blk_get_nextN_after_specified(self):
        get_info = self.lbl_blk_get["get_nextN_lbl_blk"]
        self.lbl_blk_get_info(get_info)

    def test_008_05_lbl_blk_get_all(self):
        total_lbl_blks = 0
        get_info = self.lbl_blk_get["get_firstN_lbl_blk"]
        response = clientClass.client.label_block_get(get_info)
        err = validate_lbl_blk_get_response(response)
        self.assertTrue(err)
        total_lbl_blks = total_lbl_blks + len(response.Entries)
        get_info = self.lbl_blk_get["get_nextN_lbl_blk"]
        label_temp = get_info["start_label"]
        size_temp = get_info["block_size"]
        while (len(response.Entries)>0) and not response.Eof:
            last_label = response.Entries[len(response.Entries)-1].Key.StartLabel
            last_size = response.Entries[len(response.Entries)-1].Key.LabelBlockSize
            get_info["start_label"] = last_label
            get_info["block_size"] = last_size
            response = clientClass.client.label_block_get(get_info)
            err = validate_lbl_blk_get_response(response)
            total_lbl_blks = total_lbl_blks + len(response.Entries)
            self.assertTrue(err)
        get_info["start_label"] = label_temp
        get_info["block_size"] = size_temp
        print("Total lbl_blks read: %d" %(total_lbl_blks))

    def test_009_blk_delete(self):
        response = clientClass.client.label_block_delete(self.lbl_blk_params)
        err = validate_lbl_blk_response(response)
        self.assertTrue(err)

    def test_010_mpls_eof(self):
        response = clientClass.client.mpls_eof_oper()
        err = validate_mpls_regop_response(response)
        self.assertTrue(err)

    def test_011_mpls_unregister(self):
        response = clientClass.client.mpls_unregister_oper()
        err = validate_mpls_regop_response(response)
        self.assertTrue(err)


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

#
#
#
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
            clientClass.json_params[self.JSON_TEST],
            clientClass.json_params['nexthops'],
            self.AF,
        )
        self.bfd_get = clientClass.json_params['bfd_get']

    def test_000_get_globals(self):
        # Get Global BFD info
        response = clientClass.client.global_bfd_get(self.AF)
        err = print_bfd_globals(self.AF, response)
        self.assertTrue(err)

    def test_001_bfd_reg_notif(self):
        #
        # Setup a BFD notification channel
        #
        host, port = util.get_server_ip_port()
        # Setup a channel for the BFD notification thread
        TestSuite_005_BFD_IPv4.bfd_notif[self.AF] = GrpcClient(host, port)
        # Create a synchronization event
        TestSuite_005_BFD_IPv4.bfd_event[self.AF] = threading.Event()
        # Spawn a thread to wait on notifications
        TestSuite_005_BFD_IPv4.thread_count = TestSuite_005_BFD_IPv4.thread_count + 1
        t = threading.Thread(target = bfd_get_notif,
                args=(TestSuite_005_BFD_IPv4.bfd_event, self.AF,
                TestSuite_005_BFD_IPv4.thread_count))
        t.start()
        #
        # Wait to hear from the server - Thread is blocked
        print("Waiting to hear from BFD thread...")
        TestSuite_005_BFD_IPv4.bfd_event[self.AF].wait()
        print("BFD thread ok, proceeding")
        self.assertTrue(True)

    def test_002_bfd_register(self):
        response = clientClass.client.bfd_register_oper(self.AF)
        err = validate_bfd_regop_response(response)
        self.assertTrue(err)

    def test_003_bfd_add(self):
        response = clientClass.client.bfd_add(*self.bfd_params)
        err = validate_bfd_response(response)
        self.assertTrue(err)

    def test_004_bfd_update(self):
        # Can not change the key in updates. Change a non-key attribute:
        clientClass.json_params[self.JSON_TEST]['sessions'][0]['cfg_detect_multi'] = 10
        response = clientClass.client.bfd_update(*self.bfd_params)
        err = validate_bfd_response(response)
        self.assertTrue(err)

    def test_005_get_stats(self):
        # Get Global BFD stats
        response = clientClass.client.bfd_global_get_stats(self.AF)
        err = print_bfd_stats(self.AF, response)
        self.assertTrue(err)

        # Not a test case
    def bfd_get_info(self, get_info):
        print(get_info["_description"])
        response = clientClass.client.bfd_session_get(get_info, self.AF)
        err = validate_bfd_get_response(response, self.AF)
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
        response = clientClass.client.bfd_session_get(get_info, self.AF)
        err = validate_bfd_get_response(response, self.AF)
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
            get_info["if_name"] = response.Entries[len(response.Entries)-1].Key.Interface.Name
            get_info["type"] = response.Entries[len(response.Entries)-1].Key.Type
            get_info["v%d_nbr" % self.AF] = response.Entries[len(response.Entries)-1].Key.NbrAddr
            get_info["v%d_src" % self.AF] = response.Entries[len(response.Entries)-1].Key.SourceAddr
            get_info["vrf_name"] = response.Entries[len(response.Entries)-1].Key.VrfName
            # Resend the request
            response = clientClass.client.bfd_session_get(get_info, self.AF)
            err = validate_bfd_get_response(response, self.AF)
            total_bfds = total_bfds + len(response.Entries)
            self.assertTrue(err)
        get_info["if_name"] = if_name_temp
        get_info["type"] = type_temp
        get_info["v%d_nbr" % self.AF] = nbr_temp
        get_info["v%d_src" % self.AF] = src_temp
        get_info["vrf_name"] = vrf_name_temp
        print("Total VRFs read: %d" %(total_bfds))

    def test_007_bfd_delete(self):
        response = clientClass.client.bfd_delete(*self.bfd_params)
        err = validate_bfd_response(response)
        self.assertTrue(err)

    def test_008_bfd_eof(self):
        response = clientClass.client.bfd_eof_oper(self.AF)
        err = validate_bfd_regop_response(response)
        self.assertTrue(err)

    def test_009_bfd_unregister(self):
        response = clientClass.client.bfd_unregister_oper(self.AF)
        err = validate_bfd_regop_response(response)
        self.assertTrue(err)

#
#
#
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

#
#
#
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
        self.intf_params = clientClass.json_params['batch_interfaces']
        self.intf_get = clientClass.json_params['intf_get']
        self.intf_neg_get = clientClass.json_params['intf_neg_get']

    def test_000_get_globals(self):
        # Get Global Interface info
        response = clientClass.client.intf_global_get()
        err = print_intf_globals(response)
        self.assertTrue(err)

    def test_001_intf_reg_notif(self):
        #
        # Setup an Interface notification channel
        #
        host, port = util.get_server_ip_port()
        # Setup a channel for the Interface notification thread
        TestSuite_009_INTERFACE.intf_notif = GrpcClient(host, port)
        # Create a synchronization event
        TestSuite_009_INTERFACE.intf_event = threading.Event()
        # Spawn a thread to wait on notifications
        TestSuite_009_INTERFACE.thread_count = TestSuite_009_INTERFACE.thread_count + 1
        t = threading.Thread(target = intf_get_notif,
                args=(TestSuite_009_INTERFACE.intf_event,
                TestSuite_009_INTERFACE.thread_count))
        t.start()
        #
        # Wait to hear from the server - Thread is blocked
        print("Waiting to hear from Intf thread...")
        TestSuite_009_INTERFACE.intf_event.wait()
        print("Intf thread ok, proceeding")
        self.assertTrue(True)

    def test_002_intf_register(self):
        response = clientClass.client.intf_register_op()
        err = validate_intf_regop_response(response)
        self.assertTrue(err)

    def test_003_intf_subscribe(self):
        response = clientClass.client.intf_subscribe(self.intf_params)
        err = validate_intf_response(response)
        self.assertTrue(err)

    def test_005_get_stats(self):
        # Get Global Intf stats
        response = clientClass.client.intf_global_get_stats()
        err = print_intf_stats(response)
        self.assertTrue(err)

        # Not a test case
    def intf_get_info(self, get_info, positive=True):
        print(get_info["_description"])
        response = clientClass.client.intf_get(get_info)
        err = validate_intf_get_response(response)
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
        response = clientClass.client.intf_get(get_info)
        err = validate_intf_get_response(response)
        self.assertTrue(err)
        total_intfs = total_intfs + len(response.Entries)
        get_info = self.intf_get["get_nextN_intf"]
        if_name_temp = get_info["if_name"]
        while (len(response.Entries)>0) and not response.Eof:
            # Get key from last entry
            get_info["if_name"] = response.Entries[len(response.Entries)-1].Key.Interface.Name
            # Resend the request
            response = clientClass.client.intf_get(get_info)
            err = validate_intf_get_response(response)
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
        response = clientClass.client.intf_unsubscribe(self.intf_params)
        err = validate_intf_response(response)
        self.assertTrue(err)

    def test_008_intf_eof(self):
        response = clientClass.client.intf_eof_oper()
        err = validate_intf_regop_response(response)
        self.assertTrue(err)

    def test_009_intf_unregister(self):
        response = clientClass.client.intf_unregister_op()
        err = validate_intf_regop_response(response)
        self.assertTrue(err)

class TestSuite_010_BD_reg(unittest.TestCase):
    bdutil = BD_Util()
    route_util = Route_Util()
    bdAry = ["bd0", "bd1", "bd2"]

    def test_002_multiple_bd_reg(self):
        oper = 'SL_REGOP_REGISTER'
        count = 2
        bdRegOper = clientClass.json_params["bdRegOper"]
        response = clientClass.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  TestSuite_010_BD_reg.bdutil.validate_bdreg_response(response)
        self.assertTrue(err)

    def test_003_stream_mac_add(self):
        oper = sl_common_types_pb2.SL_OBJOP_ADD
        count = 5
        rtype = sl_l2_route_pb2.SL_L2_ROUTE_MAC
        is_macip = False
        g_route_attrs = clientClass.json_params["g_route_attrs"]

        count, err = clientClass.client.l2_route_op_stream(oper, count, rtype, is_macip,
                                                              self.bdAry, g_route_attrs)
        self.assertTrue(err)

    def test_004_stream_mac_del(self):
        oper = sl_common_types_pb2.SL_OBJOP_DELETE
        count = 5
        rtype = sl_l2_route_pb2.SL_L2_ROUTE_MAC
        is_macip = False
        g_route_attrs = clientClass.json_params["g_route_attrs"]

        count, err = clientClass.client.l2_route_op_stream(oper, count, rtype, is_macip,
                                                              self.bdAry, g_route_attrs)
        self.assertTrue(err)

def l2route_notif_cback(response):
    if response.EventType == sl_l2_route_pb2.SL_L2_EVENT_TYPE_ERROR:
        if (response.ErrStatus.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
            print("Received notification to Terminate, Stream taken over?")
        else:
            print("Received error 0x%x" % (response.ErrStatus.Status))
            return False
    else:
        print("Received L2route/Bd Notif Event Type: %d" %(response.EventType))

def l2route_get_notif(event, thread_count, BdAll, BdName):
    g_oper = clientClass.json_params["g_route_attrs"]["g_oper"]
    # This would notify the main thread to proceed
    event.set()
    # RPC to get Notifications
    response = TestSuite_011_L2Route_operation.l2route_notif.l2route_get_notif(l2route_notif_cback, g_oper, BdAll, BdName)
    # Above, should return on errors
    print("l2route_get_notif: thread %d exiting. response: %s" %(thread_count, response))


class TestSuite_011_L2Route_operation(unittest.TestCase):
    bdutil = BD_Util()
    route_util = Route_Util()
    bdAry = ["bd0", "bd1", "bd2"]

    # GRPC channel used for L2 Route notifications
    l2route_notif = None
    # threading.Event() used to sync threads
    l2route_event = None
    # thread count
    thread_count = 0

    def test_000_global_reg(self):

        oper = 'SL_REGOP_REGISTER'
        g_route_attrs = clientClass.json_params["g_route_attrs"]
        response = clientClass.client.l2_global_reg_unreg_handler(oper, g_route_attrs)

    def test_001_global_unreg(self):
        oper = 'SL_REGOP_UNREGISTER'
        g_route_attrs = clientClass.json_params["g_route_attrs"]
        response = clientClass.client.l2_global_reg_unreg_handler(oper, g_route_attrs)

    def test_002_multiple_bd_reg(self):
        oper = 'SL_REGOP_REGISTER'
        count = 2

        bdRegOper = clientClass.json_params["bdRegOper"]
        response = clientClass.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  TestSuite_011_L2Route_operation.bdutil.validate_bdreg_response(response)
        self.assertTrue(err)

    def test_003_l2route_notif_channel_setup(self):
        # Setup a grpc channel
        host, port = util.get_server_ip_port()
        # Setup a channel and store info
        TestSuite_011_L2Route_operation.l2route_notif = GrpcClient(host, port)
        # Create a synchronization event, update thread count
        TestSuite_011_L2Route_operation.l2route_event = threading.Event()
        TestSuite_011_L2Route_operation.thread_count = TestSuite_011_L2Route_operation.thread_count + 1

        # If BdAll set to True, BdName is not assigned (oneof)
        BdAll = True
        BdName = "bd0"
        t = threading.Thread(target = l2route_get_notif,
                        args =(TestSuite_011_L2Route_operation.l2route_event,
                            TestSuite_011_L2Route_operation.thread_count, BdAll, BdName))
        t.start()
        # Wait to hear from server - thread is blocked
        print ("Waiting to hear from l2 notif thread...")
        TestSuite_011_L2Route_operation.l2route_event.wait()
        print ("L2 notif thread ok, proceeding")
        self.assertTrue(True)

    def test_004_global_eof(self):
        oper = 'SL_REGOP_EOF'
        g_route_attrs = clientClass.json_params["g_route_attrs"]
        response = clientClass.client.l2_global_reg_unreg_handler(oper, g_route_attrs)

    def test_005_multiple_mac_macip_route_add(self):
        oper = sl_common_types_pb2.SL_OBJOP_ADD
        count = 5
        rtype = sl_l2_route_pb2.SL_L2_ROUTE_MAC
        is_macip = False
        g_route_attrs = clientClass.json_params["g_route_attrs"]

        for bd in self.bdAry:
            response = clientClass.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  TestSuite_011_L2Route_operation.route_util.validate_l2route_response(response)
            self.assertTrue(err)

        is_macip = True
        for bd in self.bdAry:
            response = clientClass.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  TestSuite_011_L2Route_operation.route_util.validate_l2route_response(response)
            self.assertTrue(err)

        rtype = sl_l2_route_pb2.SL_L2_ROUTE_IMET
        is_macip = False
        for bd in self.bdAry:
            response = clientClass.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  TestSuite_011_L2Route_operation.route_util.validate_l2route_response(response)
            self.assertTrue(err)
        time.sleep(30)

    def test_006_multiple_mac_macip_route_del(self):
        oper = sl_common_types_pb2.SL_OBJOP_DELETE
        count = 2
        rtype = sl_l2_route_pb2.SL_L2_ROUTE_MAC
        is_macip = False
        g_route_attrs = clientClass.json_params["g_route_attrs"]

        for bd in self.bdAry:
            response = clientClass.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  TestSuite_011_L2Route_operation.route_util.validate_l2route_response(response)
            self.assertTrue(err)

        is_macip = True
        for bd in self.bdAry:
            response = clientClass.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  TestSuite_011_L2Route_operation.route_util.validate_l2route_response(response)
            self.assertTrue(err)

        rtype = sl_l2_route_pb2.SL_L2_ROUTE_IMET
        is_macip = False
        for bd in self.bdAry:
            response = clientClass.client.l2_route_handle(oper, count, rtype, is_macip,
                                                                bd, g_route_attrs)
            err =  TestSuite_011_L2Route_operation.route_util.validate_l2route_response(response)
            self.assertTrue(err)

    def test_007_multiple_bd_unreg(self):
        oper = 'SL_REGOP_UNREGISTER'
        count = 2
        bdRegOper = clientClass.json_params["bdRegOper"]
        response = clientClass.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  TestSuite_011_L2Route_operation.bdutil.validate_bdreg_response(response)
        self.assertTrue(err)

    def test_008_globals_get(self):
        response = clientClass.client.l2_globals_get()
        err = response.ErrStatus
        self.assertTrue(err)

class TestSuite_012_BD_unreg(unittest.TestCase):
    bdutil = BD_Util()

    def test_001_single_bd_unreg(self):
        oper = 'SL_REGOP_UNREGISTER'
        count = 0
        bdRegOper = clientClass.json_params["bdRegOper"]
        response = clientClass.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  TestSuite_012_BD_unreg.bdutil.validate_bdreg_response(response)
        self.assertTrue(err)

class TestSuite_013_BD_eof(unittest.TestCase):
    bdutil = BD_Util()

    def test_000_bd_eof(self):
        oper = 'SL_REGOP_EOF'
        count = 1
        bdRegOper = clientClass.json_params["bdRegOper"]
        response = clientClass.client.bd_reg_unreg_handle(oper, count, bdRegOper)

        err =  TestSuite_013_BD_eof.bdutil.validate_bdreg_response(response)
        self.assertTrue(err)

if __name__ == '__main__':

    unittest.main()

