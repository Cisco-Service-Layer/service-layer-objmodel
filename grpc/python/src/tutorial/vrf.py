#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#

# Standard python libs
import os
import sys

# Add the generated python bindings to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# gRPC generated python bindings
from genpy import sl_route_ipv4_pb2
from genpy import sl_route_common_pb2
from genpy import sl_common_types_pb2

# gRPC libs
from grpc.beta import implementations

# Utilities
from tutorial import client_init

#
# VRF operations
#    channel: GRPC channel
#    oper: sl_common_types_pb2.SL_REGOP_XXX
#
def vrf_operation(channel, oper):
    # Create the gRPC stub.
    stub = sl_route_ipv4_pb2.beta_create_SLRoutev4Oper_stub(channel)

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
    response = stub.SLRoutev4VrfRegOp(vrfMsg, Timeout)

    #
    # Check the received result from the Server
    # 
    if (response.StatusSummary.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        print "VRF %s Success!" %(
            sl_common_types_pb2.SLRegOp.keys()[oper])
    else:
        print "Error code for VRF %s is 0x%x! Response:" % (
            sl_common_types_pb2.SLRegOp.keys()[oper],
            response.StatusSummary.Status
        )
        print response
        # If we have partial failures within the batch, let's print them
        if (response.StatusSummary.Status == 
            sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR):
            for result in response.Results:
                print "Error code for %s is 0x%x" %(result.VrfName,
                    result.ErrStatus.Status
                )
        os._exit(0)


#
# Setup the GRPC channel with the server, and issue RPCs
#
if __name__ == '__main__':
    from util import util
    server_ip, server_port = util.get_server_ip_port()

    print "Using GRPC Server IP(%s) Port(%s)" %(server_ip, server_port)

    # Create the channel for Server notifications.
    channel = implementations.insecure_channel(server_ip, server_port)

    # Spawn a thread to Initialize the client and listen on notifications
    # The thread will run in the background
    client_init.global_init(channel)

    # Create another channel for gRPC requests.
    channel = implementations.insecure_channel(server_ip, server_port)

    # Send an RPC for VRF registrations
    vrf_operation(channel, sl_common_types_pb2.SL_REGOP_REGISTER)

    # RPC EOF to cleanup any previous stale routes
    vrf_operation(channel, sl_common_types_pb2.SL_REGOP_EOF)

    # while ... add/update/delete routes

    # When done with the VRFs, RPC Delete Registration
    vrf_operation(channel, sl_common_types_pb2.SL_REGOP_UNREGISTER)

    # Exit and Kill any running GRPC threads.
    os._exit(0)
