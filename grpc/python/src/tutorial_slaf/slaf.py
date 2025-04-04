#
# Copyright (c) 2025 by cisco Systems, Inc. 
# All rights reserved.
#

# Standard python libs

import ipaddress
import os
import sys
import threading
import argparse
import time
import socket
import struct
import logging

# Add the generated python bindings directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# gRPC generated python bindings
from genpy import sl_af_pb2_grpc
from genpy import sl_af_pb2
from genpy import sl_route_common_pb2
from genpy import sl_common_types_pb2
from genpy import sl_global_pb2_grpc
from genpy import sl_global_pb2
from genpy import sl_version_pb2

# gRPC libs
import grpc

maxBatchSize = 1024
maxPrimaryPathPerEntry = 256
maxVrfNameLength = 33
maxInterfaceNameLength = 80

# Operation Id example
globalOperationID = 0

# Creating the logger object
name = 'SLAF'
logger = logging.getLogger(name)

#
# Helper Functions

def set_log_level(log_level=logging.WARNING):
    logging.basicConfig(level=log_level)

def network_addresses(start_ip, prefix, count):
    # Convert the IP address to an integer
    ip_int = struct.unpack('!I', socket.inet_aton(start_ip))[0]

    # Calculate the subnet mask from the prefix
    subnet_mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

    # Calculate the network address of the starting IP
    network_address_int = ip_int & subnet_mask

    # Generate the list of next network addresses
    network_list = []
    step = 1 << (32 - prefix)

    for i in range(0, count):
        next_network_int = network_address_int + (i * step)
        next_network_address = socket.inet_ntoa(struct.pack('!I', next_network_int))
        network_list.append(next_network_address)

    return network_list

# End of helper functions
#

#
# Client initialization functions
#
# Client Init: Initialize client session
#    stub: GRPC stub
#
def client_init(stub, event, metadata):

    #
    # Create SLInitMsg to handshake the version number with the server.
    # The Server will allow/deny access based on the version number.
    # The same RPC is used to setup a notification channel for global
    # events coming from the server.
    #
    # # Set the client version number based on the current proto files' version
    init_msg = sl_global_pb2.SLInitMsg()
    init_msg.MajorVer = sl_version_pb2.SL_MAJOR_VERSION
    init_msg.MinorVer = sl_version_pb2.SL_MINOR_VERSION
    init_msg.SubVer = sl_version_pb2.SL_SUB_VERSION

    # Set a very large timeout, as we will 'for ever' loop listening on
    # notifications from the server
    Timeout = 365*24*60*60 # Seconds

    # This for loop will never end unless the server closes the session
    try:
        for response in stub.SLGlobalInitNotif(init_msg, Timeout, metadata = metadata):
            if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_VERSION:
                if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                        response.ErrStatus.Status) or \
                    (sl_common_types_pb2.SLErrorStatus.SL_INIT_STATE_CLEAR ==
                        response.ErrStatus.Status) or \
                    (sl_common_types_pb2.SLErrorStatus.SL_INIT_STATE_READY ==
                        response.ErrStatus.Status):
                    print('Server Returned 0x%x, Version %d.%d.%d' %(
                        response.ErrStatus.Status,
                        response.InitRspMsg.MajorVer,
                        response.InitRspMsg.MinorVer,
                        response.InitRspMsg.SubVer))
                    print('Successfully Initialized, connection established!')
                    # Any thread waiting on this event can proceed
                    event.set()
                else:
                    print('client init error code 0x%x', response.ErrStatus.Status)
                    os._exit(0)
            elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_HEARTBEAT:
                print('Received HeartBeat')
            elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
                if (sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM ==
                        response.ErrStatus.Status):
                    print('Received notice to terminate. Client Takeover?')
                    os._exit(0)
                else:
                    print('Error not handled:', response)
            else:
                print('client init unrecognized response %d', response.EventType)
                os._exit(0)
    except grpc.RpcError as e:
        logging.error(f'Error: {e}')
        os._exit(0)

#
# Thread starting point
#
def global_thread(stub, event, metadata):
    print('Global thread spawned')

    # Initialize the GRPC session. This function should never return
    client_init(stub, event, metadata)

    print('global_thread: exiting unexpectedly')
    # If this session is lost, then most likely the server restarted
    # Typically this is handled by reconnecting to the server. For now, exit()
    os._exit(0)

#
# Spawn a thread for global events
#
def global_init(channel, username, password):
    # Create the gRPC stub.
    stub = sl_global_pb2_grpc.SLGlobalStub(channel)

    # Create the metadata object for the rpc
    metadata = [
                    ('username', username),
                    ('password', password)
                    ]

    # Create a thread sync event. This will be used to order thread execution
    event = threading.Event()

    # The main reason we spawn a thread here, is that we dedicate a GRPC
    # channel to listen on Global asynchronous events/notifications.
    # This thread will be handling these event notifications.
    t = threading.Thread(target = global_thread, args=(stub, event, metadata))
    t.start()

    # Wait for the spawned thread before proceeding
    event.wait()

    # Get the globals. Create a SLGlobalsGetMsg
    global_get = sl_global_pb2.SLGlobalsGetMsg()

    #
    # Make an RPC call to get global attributes
    #
    Timeout = 10 # Seconds
    try:
        response = stub.SLGlobalsGet(global_get, Timeout, metadata = metadata)

        # Check the received result from the Server
        if (response.ErrStatus.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            print('MaxVrfNameLength                 : %d' %(response.MaxVrfNameLength))
            print('MaxInterfaceNameLength           : %d' %(response.MaxInterfaceNameLength))
            print('MaxPathsPerEntry                 : %d' %(response.MaxPathsPerEntry))
            print('MaxPrimaryPathPerEntry           : %d' %(response.MaxPrimaryPathPerEntry))
            print('MaxBackupPathPerEntry            : %d' %(response.MaxBackupPathPerEntry))
            print('MaxMplsLabelsPerPath             : %d' %(response.MaxMplsLabelsPerPath))
            print('MinPrimaryPathIdNum              : %d' %(response.MinPrimaryPathIdNum))
            print('MaxPrimaryPathIdNum              : %d' %(response.MaxPrimaryPathIdNum))
            print('MinBackupPathIdNum               : %d' %(response.MinBackupPathIdNum))
            print('MaxBackupPathIdNum               : %d' %(response.MaxBackupPathIdNum))
            print('MaxRemoteAddressNum              : %d' %(response.MaxRemoteAddressNum))
            print('MaxL2BdNameLength                : %d' %(response.MaxL2BdNameLength))
            print('MaxL2PmsiTunnelIdLength          : %d' %(response.MaxL2PmsiTunnelIdLength))
            print('MaxLabelBlockClientNameLength    : %d' %(response.MaxLabelBlockClientNameLength))
            print('MaxPathsInNexthopNotif           : %d' %(response.MaxPathsInNexthopNotif))
            print('MaxVrfRegPerMsg                  : %d' %(response.MaxVrfRegPerMsg))
            print('MaxAFOpsPerMsg                   : %d' %(response.MaxAFOpsPerMsg))
            print('MaxNotifReqPerSLAFNotifReq       : %d' %(response.MaxNotifReqPerSLAFNotifReq))
            print('MaxMatchFilterInBgplsTopoNotif   : %d' %(response.MaxMatchFilterInBgplsTopoNotif))
        else:
            print('Globals response Error 0x%x' %(response.ErrStatus.Status))
            os._exit(0)

    except grpc.RpcError as e:
        logging.error(f'Error: {e}')
        os._exit(0)

    global maxBatchSize
    global maxPrimaryPathPerEntry
    global maxVrfNameLength
    global maxInterfaceNameLength
    maxBatchSize = response.MaxAFOpsPerMsg
    maxPrimaryPathPerEntry = response.MaxPrimaryPathPerEntry
    maxVrfNameLength = response.MaxVrfNameLength
    maxInterfaceNameLength = response.MaxInterfaceNameLength

# End of client initialization functions
#

#
# Performs the SLAFOp Unary rpc
#
def run_slaf_op_request (channel, metadata, messages, table_type):
    err = ''
    # Create the gRPC stub.
    stub = sl_af_pb2_grpc.SLAFStub(channel)

    Timeout = 60 # Seconds

    try:
        for x in range(len(messages)):

            # Issue the rpc for each message
            response = stub.SLAFOp(messages[x], timeout = Timeout, metadata = metadata)
            #
            # Check the received result from the Server
            #
            for result in response.Results:
                if result.Status.Status != sl_common_types_pb2.SLErrorStatus.SL_SUCCESS:
                    if table_type == sl_common_types_pb2.SL_IPv4_ROUTE_TABLE:
                        err = f'''route operation failed for: {result.Key.IPRoutePrefix.Prefix}/{result.Key.IPRoutePrefix.PrefixLen} 
                            ErrorStatus: {result.Status.Status} 
                            With OperationID: {result.OperationID}'''
                    if table_type == sl_common_types_pb2.SL_MPLS_LABEL_TABLE:
                        err = f'''route operation failed for: {result.Key.MplsLabel} 
                            ErrorStatus: {result.Status.Status} 
                            With OperationID: {result.OperationID}'''
                    if table_type == sl_common_types_pb2.SL_PATH_GROUP_TABLE:
                        err = f'''route operation failed for: {result.Key.PathGroupId} 
                            ErrorStatus: {result.Status.Status} 
                            With OperationID: {result.OperationID}'''
                else:
                    logging.info(f'Response: {result}')
    except grpc.RpcError as e:
        return e

    return err

#
# Performs the SLAFOpStream rpc
#
def run_slaf_op_stream_request (channel, metadata, messages, total_operations, fib_check, table_type):
    err = ''
    # Create the gRPC stub.
    stub = sl_af_pb2_grpc.SLAFStub(channel)

    # Create variables used in read Thread
    errMessage = []
    message_count = total_operations
    errorMessageLock = threading.Lock()
    fullErrMessage = ''
    Timeout = 60 # Seconds
    # Event object used by read thread to signal to write to finish
    event = threading.Event()

    def listen_for_responses(ev, response_iterator, addr_family, check_fib):
        responseCount = 0
        try:
            for response in response_iterator:
                for result in response.Results:
                    with errorMessageLock:
                        # Rib success check
                        if result.Status.Status != sl_common_types_pb2.SLErrorStatus.SL_SUCCESS:
                            # Based on address family check the specific sub-response
                            if addr_family == sl_common_types_pb2.SL_IPv4_ROUTE_TABLE:
                                errMessage.append(
                                    f'''route operation failed for: {result.Key.IPRoutePrefix.Prefix}/{result.Key.IPRoutePrefix.PrefixLen} 
                                    ErrorStatus: {result.Status.Status} 
                                    With OperationID: {result.OperationID}''')
                            if addr_family == sl_common_types_pb2.SL_MPLS_LABEL_TABLE:
                                errMessage.append(
                                    '''route operation failed for: {result.Key.MplsLabel} 
                                    ErrorStatus: {result.Status.Status} 
                                    With OperationID: {result.OperationID}''')
                            if addr_family == sl_common_types_pb2.SL_PATH_GROUP_TABLE:
                                errMessage.append(
                                    '''route operation failed for: {result.Key.PathGroupId} 
                                    ErrorStatus: {result.Status.Status} 
                                    With OperationID: {result.OperationID}''')
                        else:
                            # If ack type is set to rib ack, then print response
                            if check_fib == False:
                                logging.info(f'Response: {result}')

                        # Only care about fib response if set ack type to fib
                        if check_fib:
                            # Fib status of Unknown indicates the current response did not contain a fib response
                            if result.FIBStatus != sl_common_types_pb2.SL_FIB_UNKNOWN:
                                responseCount += 1

                                #Check for fib success
                                if result.FIBStatus != sl_common_types_pb2.SL_FIB_SUCCESS:
                                    if table_type == sl_common_types_pb2.SL_IPv4_ROUTE_TABLE:
                                        errMessage.append(
                                            f'''route operation failed for: {result.Key.IPRoutePrefix.Prefix}/{result.Key.IPRoutePrefix.PrefixLen} 
                                            FibErrorStatus: {result.FIBStatus} 
                                            With OperationID: {result.OperationID}''')
                                    if table_type == sl_common_types_pb2.SL_MPLS_LABEL_TABLE:
                                        errMessage.append(
                                            f'''route operation failed for: {result.Key.MplsLabel} 
                                            FibErrorStatus: {result.FIBStatus} 
                                            With OperationID: {result.OperationID}''')
                                    if table_type == sl_common_types_pb2.SL_PATH_GROUP_TABLE:
                                        errMessage.append(
                                            f'''route operation failed for: {result.Key.PathGroupId} 
                                            FibErrorStatus: {result.FIBStatus} 
                                            With OperationID: {result.OperationID}''')
                                else:
                                    logging.info(f'Response: {result}')
                        else:
                            # Counting response when expecting fib and received fib response, or expecting rib
                            responseCount += 1
                    # When expected number of responses has been reached, stop listening in stream
                    if responseCount >= message_count:
                        ev.set()
                        return
        except grpc.RpcError as e:
            with errorMessageLock:
                errMessage.append(f'RPC Error: {e}')
            ev.set()

    # Create a generator that yields messages
    def message_generator(ev):
        for message in messages:
            yield message
        # If we exit this function it will call a done write, which will result in stream closure
        ev.wait()

    # Start listening for responses before writing messages
    responseIterator = stub.SLAFOpStream(request_iterator = message_generator(event), timeout = Timeout, metadata = metadata)
    listenerThread = threading.Thread(target=listen_for_responses, args=(event,responseIterator,table_type,fib_check))
    listenerThread.start()

    # Wait for the listener thread to finish
    listenerThread.join()

    # Concatenate the error messages
    with errorMessageLock:
        fullErrMessage = '\n'.join(errMessage)
    if fullErrMessage:
        return fullErrMessage

    return err

#
# Performs the SLAFGet Unidirectional rpc
#
def run_slaf_get_request(channel, metadata, message):
    err = ''
    # Create variables used in read Thread
    errorMessageLock = threading.Lock()
    errMessage = []

    # Create the gRPC stub.
    stub = sl_af_pb2_grpc.SLAFStub(channel)
    Timeout = 10 # Seconds

    # Read stream
    def listen_for_get_responses(response_iterator):
        try:
            for response in response_iterator:
                status = response.ErrStatus.Status
                if status != sl_common_types_pb2.SLErrorStatus.SL_SUCCESS:
                    # Append error message to list of error messages
                    with errorMessageLock:
                        errMessage.append(
                            f'Get operation failed for VrfName {response.VrfName} and Client {response.ClientID} with ErrorStatus: {status}')
                else:
                    # Print out the response message
                    logging.info(f'Get operation Succeeded for VrfName: {response.VrfName}, and Client: {response.ClientID}')
                    afList = response.AFList
                    for entryIdx in range(len(afList)):
                        logging.info(f'Index: {entryIdx}, for Entry: {afList[entryIdx]}')

        except grpc.RpcError as e:
            with errorMessageLock:
                errMessage.append(f'RPC Error: {e}')

    # Start listening for responses before writing messages
    responseIterator = stub.SLAFGet(message, timeout = Timeout, metadata = metadata)
    listenerThread = threading.Thread(target=listen_for_get_responses, args=(responseIterator,))
    listenerThread.start()

    # Wait for the listener thread to finish
    listenerThread.join()

    with errorMessageLock:
        fullErrMessage = '\n'.join(errMessage)
        if fullErrMessage:
            return fullErrMessage

    return err

#
# Performs the SLAFVrfRegGet Unidirectional rpc
#
def run_slaf_vrf_reg_get_request(channel, metadata, message):
    err = ''
    # Create variables used in read Thread
    errorMessageLock = threading.Lock()
    errMessage = []

    # Create the gRPC stub.
    stub = sl_af_pb2_grpc.SLAFStub(channel)
    Timeout = 10 # Seconds

    # Read stream
    def listen_for_get_responses(response_iterator):
        try:
            for response in response_iterator:
                status = response.ErrStatus.Status
                if status != sl_common_types_pb2.SLErrorStatus.SL_SUCCESS:
                    # Append error message to list of error messages
                    with errorMessageLock:
                        errMessage.append(
                            f'vrfRegGet operation failed for Client {response.ClientID} with ErrorStatus: {status}')
                else:
                    # Print out the response message
                    logging.info(f'vrfRegGet operation Succeeded for Client: {response.ClientID} and Table Type: {response.Table}')
                    rspEntry = response.Entries
                    for entryIdx in range(len(rspEntry)):
                        logging.info(f'Index: {entryIdx}, for Entry: {rspEntry[entryIdx]}')

        except grpc.RpcError as e:
            with errorMessageLock:
                errMessage.append(f'RPC Error: {e}')

    # Start listening for responses before writing messages
    responseIterator = stub.SLAFVrfRegGet(message, timeout = Timeout, metadata = metadata)
    listenerThread = threading.Thread(target=listen_for_get_responses, args=(responseIterator,))
    listenerThread.start()

    # Wait for the listener thread to finish
    listenerThread.join()

    with errorMessageLock:
        fullErrMessage = '\n'.join(errMessage)
        if fullErrMessage:
            return fullErrMessage

    return err

#
# Performs the SLAFNotifStream rpc
#
def run_slaf_notif_stream_request (channel, metadata, messages, notif_duration):
    err = ''
    # Create the gRPC stub.
    stub = sl_af_pb2_grpc.SLAFStub(channel)

    # Create variables used in read Thread
    errMessage = []
    errorMessageLock = threading.Lock()
    fullErrMessage = ''
    Timeout = 60 # Seconds

    def listen_for_notif_responses(response_iterator):
        try:
            for response in response_iterator:
                for result in response.AFNotifs:
                    # Check the NotifStatus field exists
                    fieldName = result.WhichOneof("Event")
                    if fieldName == "NotifStatus":
                        status = result.NotifStatus
                        if status.NotifStatus.Status != sl_common_types_pb2.SLErrorStatus.SL_SUCCESS:
                            # If status is not success then append error message
                            with errorMessageLock:
                                errMessage.append(
                                    f'''Notification operation failed with
                                    VrfName: {esponse.VrfName},
                                    ErrorStatus: {status.NotifStatus.Status},
                                    for Request: {status.NotifReq}''')
                        else:
                            logging.info(f'Corresponding Request: {status.NotifReq}')
                    else:
                        # Print the information from the response if it does not indicate a status
                        logging.info(f'Response: {result}')

        except grpc.RpcError as e:
            # Append error message
            with errorMessageLock:
                errMessage.append(f'RPC Error: {e}')

    # Create a generator that yields messages
    def notif_message_generator(wait_seconds):
        for message in messages:
            yield message
        # If we exit this function it will call a done write, which will result in stream closure
        time.sleep(wait_seconds)

    # Start listening for responses before writing messages
    responseIterator = stub.SLAFNotifStream(request_iterator = notif_message_generator(notif_duration,), timeout = Timeout, metadata = metadata)
    listenerThread = threading.Thread(target=listen_for_notif_responses, args=(responseIterator,))
    listenerThread.start()

    # Wait for the listener thread to finish
    listenerThread.join()

    # Concatenate the error messages
    with errorMessageLock:
        fullErrMessage = '\n'.join(errMessage)
    if fullErrMessage:
        return fullErrMessage

    return err

#
# VRF operations
#    channel: GRPC channel
#    oper: sl_common_types_pb2.SL_REGOP_XXX
#    table_type: Vrf operation for specific table_type
#
def vrf_operation(channel, metadata, oper, table_type):
    # Create the gRPC stub.
    stub = sl_af_pb2_grpc.SLAFStub(channel)

    # Create the SLAFVrfRegMsg message used for VRF registrations
    vrfMsg = sl_af_pb2.SLAFVrfRegMsg()

    # Create a list to maintain the SLVrfReg objects (in case of batch VRF
    # registrations)
    # In this example, we fill in only a single SLVrfReg object
    vrfRegMsgs = []

    # Create an SLAFVrfReg object and set its attributes
    vrfRegMsg = sl_af_pb2.SLAFVrfReg()
    # Set table type
    vrfRegMsg.Table = table_type

    # Create an SLVrfReg object and set its attributes
    vrfReg = sl_route_common_pb2.SLVrfReg()
    # Set VRF name.
    vrfReg.VrfName = 'default'
    # Set Administrative distance
    vrfReg.AdminDistance = 99
    # Set VRF purge interval
    vrfReg.VrfPurgeIntervalSeconds = 500

    # Add the vrfReg object to the vrfRegMsg
    vrfRegMsg.VrfReg.CopyFrom(vrfReg)

    # Add the registration message to the list
    # In case of bulk, we can append other VRF objects to the list
    vrfRegMsgs.append(vrfRegMsg)

    # Now that the list is completed, assign it to the SLAFVrfRegMsg
    vrfMsg.VrfRegMsgs.extend(vrfRegMsgs)

    # Set the Operation
    vrfMsg.Oper = oper

    #
    # Make an RPC call
    #
    Timeout = 10 # Seconds

    try:
        response = stub.SLAFVrfRegOp(vrfMsg, Timeout, metadata = metadata)

        #
        # Check the received result from the Server
        #
        if (response.StatusSummary.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            logging.info('VRF %s Success!' %(
                list(sl_common_types_pb2.SLRegOp.keys())[oper]))
            for result in range(len(response.Results)):
                logging.info(f'Index: {result}, for Entry: {response.Results[result]}', )
        else:
            logging.error('Error code for VRF %s is 0x%x! Response:' % (
                list(sl_common_types_pb2.SLRegOp.keys())[oper],
                response.StatusSummary.Status
            ))
            # If we have partial failures within the batch, let's print them
            if (response.StatusSummary.Status == 
                sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR):
                for result in response.Results:
                    logging.error(f'Error code for {result.VrfName} with Table Type {results.Table} is 0x{result.ErrStatus.Status}')
            os._exit(0)
    except grpc.RpcError as e:
        status_code = e.code()
        logging.error(f'Error: {e}')
        os._exit(0)

#
# Route operation
# Sets up the SLAFMsg for ipv4 route programming
# Then calls appropriate function for issuing the rpc and collects the responses
#
def route_operation(channel, metadata, oper, route_flag,
                    admin_distance, ack_type, ack_permit, ack_cadence,
                    prefix, prefix_len, num_routes, use_pg_name,
                    batch_size, next_hop_ip, nexthop_interface, num_paths,
                    auto_inc_nhip, stream_case):
    # Initialize variables for message stats
    batchIndex = 0
    totalRoutes = 0
    setRoutes = 0
    routeCount = 0
    messages = []
    global globalOperationID

    if batch_size <= 0:
        logging.error(f'Invalid batch size: {batch_size}')
        os._exit(0)
    if num_routes <= 0:
        logging.error(f'Invalid number of routes: {num_routes}')
        os._exit(0)

    logging.debug(f'''Start Address: {prefix},
        Number of Routes: {num_routes},
        Number of Paths: {num_paths},
        Batch Size: {batch_size}''')

    # Set up the incrementing prefix list and next hop list
    prefixList = network_addresses(prefix, prefix_len, num_routes)
    nhList = network_addresses(next_hop_ip, 32, num_routes)

    # Let's keep track of the preparation time it takes to create the messages
    t0 = time.time()

    message = sl_af_pb2.SLAFMsg(
        Oper = oper,
        VrfName = 'default',
    )

    # Populate a batch with batch_size routes each
    while setRoutes < num_routes:

        # Populate the routes' attributes
        ipRoute = sl_af_pb2.SLAFIPRoute(
            IPRoutePrefix = sl_route_common_pb2.SLRoutePrefix(
                Prefix = sl_common_types_pb2.SLIpAddress(
                    V4Address = int(ipaddress.ip_address(prefixList[setRoutes]))),
                PrefixLen = prefix_len
            ),
            RouteCommon = sl_route_common_pb2.SLRouteCommon(
                AdminDistance=admin_distance,
                RouteFlags=[route_flag]
            )
        )

        # We don't need to setup the paths for DELETE
        if oper != sl_common_types_pb2.SL_OBJOP_DELETE:
            for pathIndex in range(num_paths):
                # Setup the route's Path 1
                p1 = sl_route_common_pb2.SLRoutePath(
                    VrfName = 'default',
                )
                if use_pg_name == 'none':
                    # Setup the route's Path 1
                    if auto_inc_nhip:
                        slipAddress = sl_common_types_pb2.SLIpAddress(
                            V4Address = int(ipaddress.ip_address(nhList[setRoutes]))
                        )
                        p1.NexthopAddress.CopyFrom(slipAddress)
                    else:
                        slipAddress = sl_common_types_pb2.SLIpAddress(
                            V4Address = int(ipaddress.ip_address(nhList[0]))
                        )
                        p1.NexthopAddress.CopyFrom(slipAddress)
                    if nexthop_interface:
                        nexthopInterface = sl_common_types_pb2.SLInterface(
                            Name = nexthop_interface
                        )
                        p1.NexthopInterface.CopyFrom(nexthopInterface)
                else:
                    # Use already existing path group
                    pathGroupKey = sl_common_types_pb2.SLPathGroupRefKey(
                            VrfName = 'default',
                            PathGroupId = sl_common_types_pb2.SLObjectId(
                                Name = use_pg_name
                            )
                    )
                    p1.PathGroupKey.CopyFrom(pathGroupKey)

                # Append to route
                ipRoute.PathList.append(p1)

        # Setup some SLAFOpMsg attributes
        af_object = sl_af_pb2.SLAFObject(
            IPRoute = ipRoute
        )

        # Add all objects to the opMsg
        op_msg = sl_af_pb2.SLAFOpMsg(
            AFObject = af_object,
            OperationID = globalOperationID,
            AckType = ack_type,
            AckPermits = [ack_permit],
            AckCadence = ack_cadence
        )
        globalOperationID += 1  # Update global operation ID

        logging.debug(f'For Prefix: {prefixList[setRoutes]}, The OpMsg: {op_msg}')

        # Append Route to batch
        message.OpList.append(op_msg)
        routeCount += 1
        totalRoutes += 1

        if routeCount == batch_size or setRoutes == num_routes - 1:
            routeCount = 0
            messages.append(message)

            # After appending clear the message
            message = sl_af_pb2.SLAFMsg(
                Oper = oper,
                VrfName = 'default'
            )
            batchIndex += 1

        # Increment the setRoutes
        setRoutes += 1

    t1 = time.time()

    print(f'{oper} Total Batches: {batchIndex}, Routes: {totalRoutes}, Preparation Time: {t1 - t0}')

    if totalRoutes > 0 and t1 != t0:
        rate = totalRoutes / (t1 - t0)
        print(f'Preparation Rate: {rate}')

    t0 = time.time()

    # Issue the rpc and handles the responses
    if stream_case:
        fibCheck = int(ack_type) != 0
        err = run_slaf_op_stream_request(channel, metadata, messages,
            totalRoutes, fibCheck, sl_common_types_pb2.SL_IPv4_ROUTE_TABLE)
    else:
        err = run_slaf_op_request(channel, metadata, messages,
            sl_common_types_pb2.SL_IPv4_ROUTE_TABLE)

    if err:
        logging.error(f'Error: {err}')
        os._exit(0)

    t1 = time.time()

    print(f'{oper} Total Batches: {batchIndex}, Routes: {totalRoutes}, ElapsedTime: {t1 - t0}')

    if totalRoutes > 0 and t1 != t0:
        rate = totalRoutes / (t1 - t0)
        print(f'Programming Rate: {rate}')
#
# Mpls operation
# Sets up the SLAFMsg for mpls label programming
# Then calls appropriate function for issuing the rpc and collects the responses
#
def mpls_operation(channel, metadata, oper, route_flag,
                    admin_distance, ack_type, ack_permit, ack_cadence,
                    start_label, out_label, num_labels, num_paths,
                    batch_size, next_hop_ip, nexthop_interface,
                    auto_inc_nhip, stream_case):
    # Initialize variables for message stats
    elspIdx, pathIdx, batchIndex = 0,0,0
    numElsps = 0
    sentIlms = 0
    totalIlms = 0
    numIlms = 0
    ilmsInBatch = 0
    messages = []
    global globalOperationID

    if batch_size <= 0:
        logging.error(f'Invalid batch size: {batch_size}')
        os._exit(0)
    if num_labels <= 0:
        logging.error(f'Invalid number of labels: {num_labels}')
        os._exit(0)

    logging.debug(f'''Start Label: {start_label},
        Number of Labels: {num_labels},
        Number of Paths: {num_paths},
        Batch Size: {batch_size}''')

    nhList = network_addresses(next_hop_ip, 32, num_labels)

    # Let's keep track of the preparation time it takes to create the messages
    t0 = time.time()

    # Set the initial variables
    label = start_label
    numIlms = 1
    totalIlms = num_labels * numIlms
    # batch_size used for appending last message
    if batch_size > totalIlms:
        batch_size = totalIlms

    message = sl_af_pb2.SLAFMsg(
        Oper = oper,
        VrfName = 'default',
    )

    #
    # Slaf protos currently do not allow elsps to be configured.
    # numElsps:  > 1 for ELSP, 0 otherwise (configured)
    # totalIlms: numLabels * numElsps (calculated)
    # batch_size: number of ilms per batch (configured)
    # numIlms: number of ilms (1 for non ELSP, numElsps otherwise)
    #
    while sentIlms < totalIlms:
        logging.debug(f'''
            sentIlms: {sentIlms},
            batchIndex: {batchIndex},
            ilmsInBatch: {ilmsInBatch},
            numIlms: {numIlms},
            batchSize: {batch_size},
            totalIlms: {totalIlms}''')

        if ilmsInBatch + numIlms > batch_size and sentIlms != 0:
            batchIndex += 1
            messages.append(message)
            ilmsInBatch = 0

        if ilmsInBatch == 0:
            # Create a new ILM batch
            message = sl_af_pb2.SLAFMsg(
                Oper=oper,
                VrfName="default"
            )
        #
        # If we are adding ELSP entries then loop and create as many
        # using the same label. If numElsps is set to 0 we just add
        # one ILM entry for that label.
        #
        for elspIdx in range(numIlms):
            logging.debug(f"label: {label}, numIlms: {numIlms}")

            logging.debug(f"Interface: {nexthop_interface}")

            # Setup message object attributes
            ilm = sl_af_pb2.SLMplsEntry(
                MplsKey = sl_af_pb2.SLMplsEntryKey(
                    Label = label
                ),
                AdminDistance = admin_distance,
                MplsFlags = [route_flag]
            )

            for pathIdx in range(num_paths):
                # Set the route path
                nhlfe = sl_route_common_pb2.SLRoutePath()
                if auto_inc_nhip:
                    slipAddress = sl_common_types_pb2.SLIpAddress(
                        V4Address = int(ipaddress.ip_address(nhList[sentIlms]))
                    )
                    nhlfe.NexthopAddress.CopyFrom(slipAddress)
                else:
                    slipAddress = sl_common_types_pb2.SLIpAddress(
                        V4Address = int(ipaddress.ip_address(nhList[0]))
                    )
                    nhlfe.NexthopAddress.CopyFrom(slipAddress)

                if nexthop_interface:
                    nexthopInterface = sl_common_types_pb2.SLInterface(
                            Name = nexthop_interface
                    )
                    nhlfe.NexthopInterface.CopyFrom(nexthopInterface)

                if out_label > 0:
                    outLabel = out_label + (label - start_label) * numElsps + elspIdx
                    nhlfe.LabelStack.append(outLabel)
                else:
                    logging.error("Invalid out label")
                    os._exit(0)

                # Append to route
                ilm.PathList.append(nhlfe)

            afObject = sl_af_pb2.SLAFObject(
                MplsLabel = ilm
            )

            # Add all objects to the opMsg
            opMsg = sl_af_pb2.SLAFOpMsg(
                AFObject = afObject,
                OperationID = globalOperationID,
                AckType = ack_type,
                AckPermits = [ack_permit],
                AckCadence = ack_cadence
            )

            globalOperationID += 1
            # Append Label to batch
            message.OpList.append(opMsg)

        sentIlms += numIlms
        # Append the last message
        if sentIlms >= totalIlms:
            batchIndex += 1
            logging.debug(f'Message: {message}')
            messages.append(message)
            ilmsInBatch = 0

        ilmsInBatch += numIlms
        label += 1


    t1 = time.time()

    print(f'{oper} Total Batches: {batchIndex}, Ilms: {sentIlms}, Preparation Time: {t1 - t0}')

    if sentIlms > 0 and t1 != t0:
        rate = sentIlms / (t1 - t0)
        print(f'Preparation Rate: {rate}')

    t0 = time.time()

    # Issue the rpc and handles the responses
    if stream_case:
        fibCheck = int(ack_type) != 0
        err = run_slaf_op_stream_request(channel, metadata, messages,
            sentIlms, fibCheck, sl_common_types_pb2.SL_MPLS_LABEL_TABLE)
    else:
        err = run_slaf_op_request(channel, metadata, messages,
            sl_common_types_pb2.SL_MPLS_LABEL_TABLE)

    if err:
        logging.error(f'Error: {err}')
        os._exit(0)

    t1 = time.time()

    print(f'{oper} Total Batches: {batchIndex}, Ilms: {sentIlms}, ElapsedTime: {t1 - t0}')

    if sentIlms > 0 and t1 != t0:
        rate = sentIlms / (t1 - t0)
        print(f'Programming Rate: {rate}')

#
# Pg operation
# Sets up the SLAFMsg for pg
# Then calls appropriate function for issuing the rpc and collects the responses
#
def pg_operation(channel, metadata, oper, route_flag,
                    admin_distance, ack_type, ack_permit, ack_cadence,
                    pg_name, pg_num_path, batch_size, next_hop_ip,
                    nexthop_interface, auto_inc_nhip, stream_case):
    # Initialize variables for message stats
    batchIndex = 0
    totalPG = 0
    messages = []
    global globalOperationID

    if batch_size <= 0:
        logging.error(f'Invalid batch size: {batch_size}')
        os._exit(0)
    if pg_num_path <= 0:
        logging.error(f'Invalid number of paths: {pg_num_path}')
        os._exit(0)

    logging.debug(f'''NH ip: {next_hop_ip},
        NH Interface: {nexthop_interface},
        Pg name: {pg_name},
        Number of Paths: {pg_num_path},
        Batch Size: {batch_size}''')

    nhList = network_addresses(next_hop_ip, 32, pg_num_path)

    # Let's keep track of the preparation time it takes to create the messages
    t0 = time.time()

    # Set up the message
    message = sl_af_pb2.SLAFMsg(
        Oper = oper,
        VrfName = 'default',
    )
    # Set the path list variables
    pathList = sl_af_pb2.SLPathGroup.SLPathList()

    # We don't need to setup the paths for DELETE
    if oper != sl_common_types_pb2.SL_OBJOP_DELETE:
        for count in range(1, pg_num_path + 1):
            # Populate the routes' attributes for the path group
            path = sl_route_common_pb2.SLRoutePath(
                VrfName = "default",
            )
            if auto_inc_nhip:
                slipAddress = sl_common_types_pb2.SLIpAddress(
                    V4Address = int(ipaddress.ip_address(nhList[count-1]))
                )
                path.NexthopAddress.CopyFrom(slipAddress)
            else:
                slipAddress = sl_common_types_pb2.SLIpAddress(
                    V4Address = int(ipaddress.ip_address(nhList[0]))
                )
                path.NexthopAddress.CopyFrom(slipAddress)

            if nexthop_interface:
                nexthopInterface = sl_common_types_pb2.SLInterface(
                        Name = nexthop_interface
                )
                path.NexthopInterface.CopyFrom(nexthopInterface)

            slPaths = sl_af_pb2.SLPathGroup.SLPath(
                Path = path
            )
            pathList.Paths.append(slPaths)

    # Populate the path group attributes
    pathGroup = sl_af_pb2.SLPathGroup(
        PathGroupId = sl_common_types_pb2.SLObjectId(
            Name = pg_name
        ),
        AdminDistance = admin_distance,
        PathList = pathList,
        PgFlags = [route_flag]
    )

    afObject = sl_af_pb2.SLAFObject(
        PathGroup = pathGroup
    )
    totalPG += 1

    # Add all objects to the opMsg
    opMsg = sl_af_pb2.SLAFOpMsg(
        AFObject = afObject,
        OperationID = globalOperationID,
        AckType = ack_type,
        AckPermits = [ack_permit],
        AckCadence = ack_cadence
    )

    globalOperationID += 1
    # Append Label to batch
    message.OpList.append(opMsg)
    messages.append(message)
    batchIndex += 1
    logging.debug(f'Message structure: {message}')

    t1 = time.time()
    print(f'{oper} Total Batches: {batchIndex}, Pgs: {totalPG}, Preparation Time: {t1 - t0}')

    if totalPG > 0 and t1 != t0:
        rate = totalPG / (t1 - t0)
        print(f'Preparation Rate: {rate}')

    t0 = time.time()

    # Issue the rpc and handles the responses
    if stream_case:
        fibCheck = int(ack_type) != 0
        err = run_slaf_op_stream_request(channel, metadata, messages,
            totalPG, fibCheck, sl_common_types_pb2.SL_PATH_GROUP_TABLE)
    else:
        err = run_slaf_op_request(channel, metadata, messages,
            sl_common_types_pb2.SL_PATH_GROUP_TABLE)

    if err:
        logging.error(f'Error: {err}')
        os._exit(0)

    t1 = time.time()

    print(f'{oper} Total Batches: {batchIndex}, Pgs: {totalPG}, ElapsedTime: {t1 - t0}')

    if totalPG > 0 and t1 != t0:
        rate = totalPG / (t1 - t0)
        print(f'Programming Rate: {rate}')

#
# Get operation
# Sets up the SLAFGetMsg for Get
# Then calls appropriate function for issuing the rpc and collects the responses
#
def get_operation(channel, metadata, vrf_name, client_id_all,
                    client_id, table_list, route_list, vx_lan_id,
                    pg_regex, ipv4_prefix, ipv4_prefix_len):
    # Initialize variables for message stats
    batchIndex = 0
    totalGet = 0

    logging.debug(f'''VrfName: {vrf_name},
        Client id all set: {client_id_all},
        client id: {client_id},
        Route list set: {route_list}''')

    # Let's keep track of the preparation time it takes to create the messages
    t0 = time.time()

    message = sl_af_pb2.SLAFGetMsg(
        VrfName = vrf_name
    )
    batchIndex += 1
    totalGet += 1

    # Set up the objects to be searched for by the client IDs
    if client_id_all:
        message.AllClients = client_id_all
    else:
        if client_id >= 0:
            clientIDList = sl_af_pb2.SLAFClientIDList(
                ClientIDList = [client_id]
            )
            message.ClientIDList.CopyFrom(clientIDList)

    # Set up the objects to search for based off match criteria
    if route_list:
        routeMatchList = sl_af_pb2.SLAFGetMatchList()

        # As these fields are optional, the user may want to set some and not others
        if vx_lan_id >= 0:
            # Populate vxLanId
            getMatch = sl_af_pb2.SLAFGetMatch()
            getMatch.VxlanVniId = vx_lan_id
            routeMatchList.Match.append(getMatch)

        if pg_regex:
            # Populate pg regex
            getMatch = sl_af_pb2.SLAFGetMatch()
            getMatch.PathGroupRegex = pg_regex
            routeMatchList.Match.append(getMatch)

        if ipv4_prefix:
            prefixList = network_addresses(ipv4_prefix, ipv4_prefix_len, 1)
            getMatch = sl_af_pb2.SLAFGetMatch()

            # Populate the ip routes' attributes
            ipRoutePrefix = sl_route_common_pb2.SLRoutePrefix(
                Prefix = sl_common_types_pb2.SLIpAddress(
                    V4Address = int(ipaddress.ip_address(prefixList[0]))),
                PrefixLen = ipv4_prefix_len
            )
            key = sl_af_pb2.SLAFObjectKey(
                IPRoutePrefix = ipRoutePrefix
            )
            getMatch.Key.CopyFrom(key)
            routeMatchList.Match.append(getMatch)
        message.RouteMatchList.CopyFrom(routeMatchList)
    else:
        # Set up only objects with specified table types
        if table_list != sl_common_types_pb2.SL_TABLE_TYPE_RESERVED:
            tableTypeList = sl_af_pb2.SLTableTypeList()
            tableTypeList.Table.append(table_list)
            message.TableList.CopyFrom(tableTypeList)
        else:
            logging.info('Table Type for get message is not set. If on purpose then ignore.')

    logging.debug(f'Message Structure: {message}')

    t1 = time.time()
    print(f'GET Total Batches: {batchIndex}, Requests: {totalGet}, Preparation Time: {t1 - t0}')

    if totalGet > 0 and t1 != t0:
        rate = totalGet / (t1 - t0)
        print(f'Preparation Rate: {rate}')

    t0 = time.time()

    # Issue the rpc and handles the responses
    err = run_slaf_get_request(channel, metadata, message)

    if err:
        logging.error(f'Error: {err}')
        os._exit(0)

    t1 = time.time()

    print(f'GET Total Batches: {batchIndex}, Requests: {totalGet}, ElapsedTime: {t1 - t0}')

    if totalGet > 0 and t1 != t0:
        rate = totalGet / (t1 - t0)
        print(f'Request Response Rate: {rate}')

#
# VrfRegGet operation
# Sets up the SLAFVrfRegGet
# Then calls appropriate function for issuing the rpc and collects the responses
#
def vrf_reg_get_operation(channel, metadata, get_vrf_all):
    # Initialize variables for message stats. Will always be 1 for this request
    batchIndex = 1
    totalVrfRegGet = 1

    logging.debug(f'Get all Vrf: {get_vrf_all}')

    # Let's keep track of the preparation time it takes to create the messages
    t0 = time.time()

    message = sl_af_pb2.SLAFVrfRegGetMsg(
        GetAll = get_vrf_all
    )

    logging.debug(f'Message Structure: {message}')

    t1 = time.time()
    print(f'VrfRegGet Total Batches: {batchIndex}, Requests: {totalVrfRegGet}, Preparation Time: {t1 - t0}')

    if totalVrfRegGet > 0 and t1 != t0:
        rate = totalVrfRegGet / (t1 - t0)
        print(f'Preparation Rate: {rate}')

    t0 = time.time()

    # Issue the rpc and handles the responses
    err = run_slaf_vrf_reg_get_request(channel, metadata, message)

    if err:
        logging.error(f'Error: {err}')
        os._exit(0)

    t1 = time.time()

    print(f'VrfRegGet Total Batches: {batchIndex}, Requests: {totalVrfRegGet}, ElapsedTime: {t1 - t0}')

    if totalVrfRegGet > 0 and t1 != t0:
        rate = totalVrfRegGet / (t1 - t0)
        print(f'Request Response Rate: {rate}')

#
# NotifStream operation
# Sets up the SLAFNotifStream
# Then calls appropriate function for issuing the rpc and collects the responses
#
def notif_stream_operation(channel, metadata, notif_duration,
                            oper, vrf_name, route_reg, route_src_proto,
                            route_src_proto_tag, route_table_type,
                            next_hop_reg, ipv4_prefix, ipv4_prefix_len,
                            exact_match, allow_default, recurse):
    # Initialize variables for message stats
    batchIndex = 0
    totalNotif = 0
    messages = []
    global globalOperationID

    logging.debug(f'''VrfName: {vrf_name},
        Oper: {oper},
        Duration: {notif_duration},
        Route redistribution registration Set: {route_reg},
        Next hop notification registration SetL {next_hop_reg}''')

    # Let's keep track of the preparation time it takes to create the messages
    t0 = time.time()

    # Create a message
    message = sl_af_pb2.SLAFNotifReq(
        Oper = oper,
        VrfName = vrf_name
    )
    batchIndex += 1

     # Fill in the Route redistribution registration fields
    if route_reg:
        notifReq = sl_af_pb2.SLAFNotifRegReq(
            RedistReq = sl_af_pb2.SLAFRedistRegMsg(
                SrcProto = route_src_proto,
                SrcProtoTag = route_src_proto_tag,
                Table = route_table_type
            ),
            OperationID = globalOperationID
        )
        globalOperationID += 1
        message.NotifReq.append(notifReq)

    # Fill in the Next hop registration notification fields
    if next_hop_reg:
        prefixList = network_addresses(ipv4_prefix, ipv4_prefix_len, 1)
        notifReq = sl_af_pb2.SLAFNotifRegReq(
            NextHopReq = sl_af_pb2.SLAFNextHopRegMsg(
                NextHopKey = sl_af_pb2.SLAFNextHopRegKey(
                    NextHop = sl_af_pb2.SLAFNextHopRegKey.SLNextHopKey(
                        NextHopIP = sl_route_common_pb2.SLRoutePrefix(
                            Prefix = sl_common_types_pb2.SLIpAddress(
                                V4Address = int(ipaddress.ip_address(prefixList[0]))),
                            PrefixLen = ipv4_prefix_len
                        ),
                        ExactMatch = exact_match,
                        AllowDefault = allow_default,
                        Recurse = recurse
                    )
                )
            ),
            OperationID = globalOperationID
        )
        globalOperationID += 1
        message.NotifReq.append(notifReq)

    messages.append(message)

    logging.debug(f'Message Structure: {message}')

    t1 = time.time()
    print(f'NotifStream Total Batches: {batchIndex}, Requests: {totalNotif}, Preparation Time: {t1 - t0}')

    if totalNotif > 0 and t1 != t0:
        rate = totalNotif / (t1 - t0)
        print(f'Preparation Rate: {rate}')

    t0 = time.time()

    # Issue the rpc and handles the responses
    err = run_slaf_notif_stream_request(channel, metadata, messages, notif_duration)

    if err:
        logging.error(f'ERROR: {err}')
        os._exit(0)

    t1 = time.time()

    print(f'NotifStream Total Batches: {batchIndex}, Requests: {totalNotif}, ElapsedTime: {t1 - t0}')

    if totalNotif > 0 and t1 != t0:
        rate = totalNotif / (t1 - t0)
        print(f'Request Response Rate: {rate}')
