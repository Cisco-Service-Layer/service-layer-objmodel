#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#

# Standard python libs
import os
import sys
import argparse

# Add the generated python bindings to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# gRPC generated python bindings
from genpy import sl_route_ipv4_pb2_grpc
from genpy import sl_route_common_pb2
from genpy import sl_common_types_pb2

# gRPC libs
import grpc

# Utilities
from tutorial import client_init

#
# VRF operations
#    channel: GRPC channel
#    oper: sl_common_types_pb2.SL_REGOP_XXX
#
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

    server_ip, server_port = get_server_ip_port()
    parser = argparse.ArgumentParser(description ='Used to setup the Route vertical')
    parser.add_argument('-u', '--username', help='Specify username')
    parser.add_argument('-p', '--password', help='Specify password')
    args = parser.parse_args()

    metadata = [
                ("username", args.username),
                ("password", args.password)
                ]

    print("Using GRPC Server IP(%s) Port(%s)" %(server_ip, server_port))

    # Create the channel for Server notifications.
    channel = grpc.insecure_channel(str(server_ip)+":"+str(server_port))

    # Spawn a thread to Initialize the client and listen on notifications
    # The thread will run in the background
    client_init.global_init(channel, metadata)

    # Create another channel for gRPC requests.
    #channel = grpc.insecure_channel(str(server_ip)+":"+str(server_port))

    # Send an RPC for VRF registrations
    vrf_operation(channel, sl_common_types_pb2.SL_REGOP_REGISTER, metadata)

    # RPC EOF to cleanup any previous stale routes
    vrf_operation(channel, sl_common_types_pb2.SL_REGOP_EOF, metadata)

    # while ... add/update/delete routes

    # When done with the VRFs, RPC Delete Registration
    vrf_operation(channel, sl_common_types_pb2.SL_REGOP_UNREGISTER, metadata)

    # Exit and Kill any running GRPC threads.
    os._exit(0)
