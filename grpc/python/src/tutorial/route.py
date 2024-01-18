#
# Copyright (c) 2023 by cisco Systems, Inc.
# All rights reserved.
#

# Standard python libs
import ipaddress
import os
import sys
import threading
import socket
import struct
import argparse

# Add the generated python bindings directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# gRPC generated python bindings
from genpy import sl_global_pb2_grpc
from genpy import sl_global_pb2
from genpy import sl_common_types_pb2
from genpy import sl_version_pb2
from genpy import sl_route_ipv4_pb2_grpc
from genpy import sl_route_ipv4_pb2
from genpy import sl_route_common_pb2

# Utilities

# gRPC libs
import grpc

def network_addresses(start_ip, prefix, count):
    # Convert the IP address to an integer
    ip_int = struct.unpack("!I", socket.inet_aton(start_ip))[0]

    # Calculate the subnet mask from the prefix
    subnet_mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

    # Calculate the network address of the starting IP
    network_address_int = ip_int & subnet_mask

    # Generate the list of next network addresses
    network_list = []
    step = 1 << (32 - prefix)

    for i in range(0, count):
        next_network_int = network_address_int + (i * step)
        next_network_address = socket.inet_ntoa(struct.pack("!I", next_network_int))
        network_list.append(next_network_address)

    return network_list

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {iteration}/{total} ({percent}%) {suffix}')
    sys.stdout.flush()

#
# Get the GRPC Server IP address and port number
#
def get_server_ip_port():
    # Get GRPC Server's IP from the environment
    if 'SERVER_IP' not in os.environ.keys():
        print("Need to set the SERVER_IP env variable e.g.")
        print("export SERVER_IP='10.30.110.214'")
        os._exit(0)

    # Get GRPC Server's Port from the environment
    if 'SERVER_PORT' not in os.environ.keys():
        print("Need to set the SERVER_PORT env variable e.g.")
        print("export SERVER_PORT='57777'")
        os._exit(0)

    return (os.environ['SERVER_IP'], int(os.environ['SERVER_PORT']))


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

    # Set a very large timeout, as we will "for ever" loop listening on
    # notifications from the server
    Timeout = 365*24*60*60 # Seconds

    # This for loop will never end unless the server closes the session
    for response in stub.SLGlobalInitNotif(init_msg, Timeout, metadata = metadata):
        if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_VERSION:
            if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                    response.ErrStatus.Status) or \
                (sl_common_types_pb2.SLErrorStatus.SL_INIT_STATE_CLEAR ==
                    response.ErrStatus.Status) or \
                (sl_common_types_pb2.SLErrorStatus.SL_INIT_STATE_READY ==
                    response.ErrStatus.Status):
                print("Server Returned 0x%x, Version %d.%d.%d" %(
                    response.ErrStatus.Status,
                    response.InitRspMsg.MajorVer,
                    response.InitRspMsg.MinorVer,
                    response.InitRspMsg.SubVer))
                print("Successfully Initialized, connection established!")
                # Any thread waiting on this event can proceed
                event.set()
            else:
                print("client init error code 0x%x", response.ErrStatus.Status)
                os._exit(0)
        elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_HEARTBEAT:
            print("Received HeartBeat")
        elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
            if (sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM ==
                    response.ErrStatus.Status):
                print("Received notice to terminate. Client Takeover?")
                os._exit(0)
            else:
                print("Error not handled:", response)
        else:
            print("client init unrecognized response %d", response.EventType)
            os._exit(0)



#
# Thread starting point
#
def global_thread(stub, event, metadata):
    print("Global thread spawned")

    # Initialize the GRPC session. This function should never return
    client_init(stub, event, metadata)

    print("global_thread: exiting unexpectedly")
    # If this session is lost, then most likely the server restarted
    # Typically this is handled by reconnecting to the server. For now, exit()
    os._exit(0)

#
# Spawn a thread for global events
#
def global_init(channel, metadata):
    # Create the gRPC stub.
    stub = sl_global_pb2_grpc.SLGlobalStub(channel)

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
    response = stub.SLGlobalsGet(global_get, Timeout, metadata = metadata)

    # Check the received result from the Server
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
    else:
        print("Globals response Error 0x%x" %(response.ErrStatus.Status))
        os._exit(0)



def vrf_operation(channel, oper, metadata):
    # Create the gRPC stub.
    stub = sl_route_ipv4_pb2_grpc.SLRoutev4OperStub(channel)

    # Create the SLVrfRegMsg message used for VRF registrations
    vrfMsg = sl_route_common_pb2.SLVrfRegMsg()

    # Create a list to maintain the SLVrfReg objects (in case of batch VRF
    # registrations)
    # In this example, we fill in only a single SLVrfReg object
    vrfList = []

    # Create an SLVrfReg object and set its attributes
    vrfObj = sl_route_common_pb2.SLVrfReg()
    # Set VRF name.
    vrfObj.VrfName = 'default'
    # Set Administrative distance
    vrfObj.AdminDistance = 2
    # Set VRF purge interval
    vrfObj.VrfPurgeIntervalSeconds = 500

    #
    # Add the registration message to the list
    # In case of bulk, we can append other VRF objects to the list
    vrfList.append(vrfObj)

    # Now that the list is completed, assign it to the SLVrfRegMsg
    vrfMsg.VrfRegMsgs.extend(vrfList)

    # Set the Operation
    vrfMsg.Oper = oper

    #
    # Make an RPC call
    #
    Timeout = 10 # Seconds
    response = stub.SLRoutev4VrfRegOp(vrfMsg, Timeout, metadata = metadata)

    #
    # Check the received result from the Server
    # 
    if (response.StatusSummary.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print("VRF %s Success!" %(
            list(sl_common_types_pb2.SLRegOp.keys())[oper]))
    else:
        print("Error code for VRF %s is 0x%x! Response:" % (
            list(sl_common_types_pb2.SLRegOp.keys())[oper],
            response.StatusSummary.Status
        ))
        print(response)
        # If we have partial failures within the batch, let's print them
        if (response.StatusSummary.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR):
            for result in response.Results:
                print("Error code for %s is 0x%x" %(result.VrfName,
                    result.ErrStatus.Status
                ))
        os._exit(0)


#
# Route operations
#    channel: GRPC channel
#    oper: sl_common_types_pb2.SL_OBJOP_XXX
#
# A SLRoutev4Msg contains a list of SLRoutev4 (routes)
# Each SLRoutev4 (route) contains a list of SLRoutePath (paths)
#
def route_operation(channel, oper, p_begin, p_len, nh_begin, nh_intf, r_scale, metadata):
    # Create the gRPC stub.
    stub = sl_route_ipv4_pb2_grpc.SLRoutev4OperStub(channel)

    batchSize = 1024
    prefixList = network_addresses(p_begin, p_len, r_scale)
    nhList = network_addresses(nh_begin, 32, r_scale)
    r_index = 0

    # Fill in the routes
    for b in range((r_scale // batchSize)+1):
        # Create an empty list of routes.
        routeList = []

        # Create the SLRoutev4Msg message holding the SLRoutev4 object list
        rtMsg = sl_route_ipv4_pb2.SLRoutev4Msg()

        # Fill in the message attributes attributes.
        # VRF Name
        rtMsg.VrfName = 'default'
        if (((b + 1) * batchSize) <= r_scale):
            count = batchSize
        else:
            count = r_scale % batchSize
        for i in range(count):
            #
            # Create an SLRoutev4 object and set its attributes
            #
            route = sl_route_ipv4_pb2.SLRoutev4()
            # IP Prefix
            route.Prefix = (
                int(ipaddress.ip_address(prefixList[r_index]))
            )
            # Prefix Length
            route.PrefixLen = p_len

            # Administrative distance
            route.RouteCommon.AdminDistance = 2

            #
            # Set the route's paths.
            # A Route might have one or many paths
            #
            # Create an empty list of paths as a placeholder for these paths
            paths = []

            # Create an SLRoutePath path object.
            path = sl_route_common_pb2.SLRoutePath()
            # Fill in the path attributes.
            # Path next hop address
            path.NexthopAddress.V4Address = (
                int(ipaddress.ip_address(nhList[r_index]))
            )
            # Next hop interface name
            path.NexthopInterface.Name = nh_intf
            #
            # Add the path to the list
            #
            paths.append(path)

            # Let's create another path as equal cost multi-path (ECMP)
            path = sl_route_common_pb2.SLRoutePath()
            path.NexthopAddress.V4Address = (
                int(ipaddress.ip_address(nhList[(r_index + 1)%r_scale]))
            )
            path.NexthopInterface.Name = nh_intf

            #
            # Add the path to the list
            #
            paths.append(path)
            r_index += 1

            #
            # Assign the paths to the route object
            # Note: Route Delete operations do not require the paths
            #
            if oper != sl_common_types_pb2.SL_OBJOP_DELETE:
                route.PathList.extend(paths)

            #
            # Append the route to the route list (bulk routes)
            #
            routeList.append(route)

        #
        # Done building the routeList, assign it to the route message.
        #
        rtMsg.Routes.extend(routeList)

        #
        # Make an RPC call
        #
        Timeout = 10 # Seconds
        rtMsg.Oper = oper # Desired ADD, UPDATE, DELETE operation
        response = stub.SLRoutev4Op(rtMsg, Timeout, metadata = metadata)
        #
        # Check the received result from the Server
        #
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.StatusSummary.Status):
           #print("Route %s Success!" %(
           #    list(sl_common_types_pb2.SLObjectOp.keys())[oper]))
            print_progress_bar(r_index, r_scale, prefix='Routes:', suffix='Programmed', length=50)
        else:
            print("Error code for route %s is 0x%x" % (
                list(sl_common_types_pb2.SLObjectOp.keys())[oper],
                response.StatusSummary.Status
            ))
            # If we have partial failures within the batch, let's print them
            if (response.StatusSummary.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR):
                for result in response.Results:
                    print("Error code for %s/%d is 0x%x" %(
                        str(ipaddress.ip_address(result.Prefix)),
                        result.PrefixLen,
                        result.ErrStatus.Status
                    ))
            os._exit(0)
    print("\nSummary: \n prefixes:  [{} -> {}]\n next_hops: [{} -> {}]\n route_count: {}".format(
        prefixList[0], prefixList[r_index-1],
        nhList[0], nhList[r_index-1], r_scale))

#
# Setup the GRPC channel with the server, and issue RPCs
#
if __name__ == '__main__':
    server_ip, server_port = get_server_ip_port()

    parser = argparse.ArgumentParser(description="Example grpc route client")
    parser.add_argument("--p_start", type=str, default="20.0.0.0", help="starting ipv4 prefix (default: 20.0.0.0)")
    parser.add_argument("--p_len", type=int, default=24, help="ipv4 prefix len (default: 24")
    parser.add_argument("--nh_start", type=str, default="100.0.0.1", help="starting next hop address (default: 100.0.0.1)")
    parser.add_argument("--nh_intf", type=str, default="FourHundredGigE0/0/0/10", help="next hop interface (default: FourHundredGigE0/0/0/10)")
    parser.add_argument("--num_routes", type=int, default=100, help="number of routes (default: 100)")
    parser.add_argument('-u', '--username', help='Specify username', default="cisco")
    parser.add_argument('-p', '--password', help='Specify password', default="cisco123")
    args = parser.parse_args()
    global metadata 

    metadata = [
                    ("username", args.username),
                    ("password", args.password)
                    ]
    print (metadata)
    print("Using GRPC Server IP: {} Port: {}\n"
          "prefix_start: {}\n"
          "prefix_len: {}\n"
          "nexthop_start: {}\n"
          "nexthop_intf: {}\n"
          "num_routes: {}".format(server_ip, server_port, args.p_start, args.p_len, args.nh_start, args.nh_intf, args.num_routes))

    # Create the channel for gRPC.
    channel = grpc.insecure_channel(str(server_ip) + ":" + str(server_port))

    # Spawn a thread to Initialize the client and listen on notifications
    # The thread will run in the background
    global_init(channel,metadata)

    # Send an RPC for VRF registrations
    vrf_operation(channel, sl_common_types_pb2.SL_REGOP_REGISTER,metadata)

    # RPC EOF to cleanup any previous stale routes
    vrf_operation(channel, sl_common_types_pb2.SL_REGOP_EOF,metadata)

    # RPC route operations
    #    for add: sl_common_types_pb2.SL_OBJOP_ADD
    #    for update: sl_common_types_pb2.SL_OBJOP_UPDATE
    #    for delete: sl_common_types_pb2.SL_OBJOP_DELETE
    route_operation(channel, sl_common_types_pb2.SL_OBJOP_ADD, args.p_start, args.p_len, args.nh_start, args.nh_intf, args.num_routes,metadata)

    #route_operation(channel, sl_common_types_pb2.SL_OBJOP_DELETE)
    # while ... add/update/delete routes

    # When done with the VRFs, RPC Delete Registration
    #vrf_operation(channel, sl_common_types_pb2.SL_REGOP_UNREGISTER)

    # Exit and Kill any running GRPC threads.
    os._exit(0)
