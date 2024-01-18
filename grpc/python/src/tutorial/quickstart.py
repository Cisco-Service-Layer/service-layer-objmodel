#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#

# Standard python libs
import ipaddress
import os
import sys
import argparse

# Add the generated python bindings directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# gRPC generated python bindings
from genpy import sl_route_ipv4_pb2_grpc
from genpy import sl_route_ipv4_pb2
from genpy import sl_route_common_pb2
from genpy import sl_common_types_pb2

# Utilities
from tutorial import vrf
from tutorial import client_init

# gRPC libs
import grpc

#
# Route operations
#    channel: GRPC channel
#    oper: sl_common_types_pb2.SL_OBJOP_XXX
#
# A SLRoutev4Msg contains a list of SLRoutev4 (routes)
# Each SLRoutev4 (route) contains a list of SLRoutePath (paths)
#
def route_operation(channel, oper):
    # Create the gRPC stub.
    stub = sl_route_ipv4_pb2_grpc.SLRoutev4OperStub(channel)

    # Create an empty list of routes.
    routeList = []

    # Create the SLRoutev4Msg message holding the SLRoutev4 object list
    rtMsg = sl_route_ipv4_pb2.SLRoutev4Msg()

    # Fill in the message attributes attributes.
    # VRF Name
    rtMsg.VrfName = 'default'

    # Fill in the routes
    for i in range(10):
        #
        # Create an SLRoutev4 object and set its attributes
        #
        route = sl_route_ipv4_pb2.SLRoutev4()
        # IP Prefix
        route.Prefix = (
            int(ipaddress.ip_address('20.0.'+ str(i) + '.0'))
        )
        # Prefix Length
        route.PrefixLen = 24

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
            int(ipaddress.ip_address('10.10.10.1'))
        )
        # Next hop interface name
        path.NexthopInterface.Name = 'GigabitEthernet0/0/0/0'

        #
        # Add the path to the list
        #
        paths.append(path)

        # Let's create another path as equal cost multi-path (ECMP)
        path = sl_route_common_pb2.SLRoutePath()
        path.NexthopAddress.V4Address = (
            int(ipaddress.ip_address('10.10.10.2'))
        )
        path.NexthopInterface.Name = 'GigabitEthernet0/0/0/0'

        #
        # Add the path to the list
        #
        paths.append(path)

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
        print("Route %s Success!" %(
            list(sl_common_types_pb2.SLObjectOp.keys())[oper]))
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
# Setup the GRPC channel with the server, and issue RPCs
#
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description ='Basic test')
    parser.add_argument('-u', '--username', help='Specify username', default="cisco")
    parser.add_argument('-p', '--password', help='Specify password', default="cisco123")
    args = parser.parse_args()

    server_ip, server_port = get_server_ip_port()

    print("Using GRPC Server IP(%s) Port(%s)" %(server_ip, server_port))

    # Create the channel for gRPC.
    channel = grpc.insecure_channel(str(server_ip) + ":" + str(server_port))
    global metadata 

    metadata = [
                    ("username", args.username),
                    ("password", args.password)
                    ]

    # Spawn a thread to Initialize the client and listen on notifications
    # The thread will run in the background
    client_init.global_init(channel, metadata)

    # Send an RPC for VRF registrations
    vrf.vrf_operation(channel, sl_common_types_pb2.SL_REGOP_REGISTER, metadata)

    # RPC EOF to cleanup any previous stale routes
    vrf.vrf_operation(channel, sl_common_types_pb2.SL_REGOP_EOF, metadata)

    # RPC route operations
    #    for add: sl_common_types_pb2.SL_OBJOP_ADD
    #    for update: sl_common_types_pb2.SL_OBJOP_UPDATE
    #    for delete: sl_common_types_pb2.SL_OBJOP_DELETE
    route_operation(channel, sl_common_types_pb2.SL_OBJOP_ADD)

    #route_operation(channel, sl_common_types_pb2.SL_OBJOP_DELETE)
    # while ... add/update/delete routes

    # When done with the VRFs, RPC Delete Registration
    #vrf.vrf_operation(channel, sl_common_types_pb2.SL_REGOP_UNREGISTER)

    # Exit and Kill any running GRPC threads.
    os._exit(0)
