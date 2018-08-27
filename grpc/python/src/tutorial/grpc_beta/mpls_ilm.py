#
# Copyright (c) 2016 by cisco Systems, Inc.
# All rights reserved.
#
import ipaddress
import os
import json
import sys

# Add the generated python bindings directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

# gRPC generated python bindings
from genpy import sl_global_pb2
from genpy import sl_common_types_pb2
from genpy import sl_mpls_pb2

# Utilities
import client_init

# gRPC libs
from grpc.beta import implementations


def mpls_register(stub, oper):

    if oper == sl_common_types_pb2.SL_REGOP_REGISTER:
        # Register the MPLS Client
        mplsReg = sl_mpls_pb2.SLMplsRegMsg()
        mplsReg.Oper = oper
        Timeout = 10
        response = stub.SLMplsRegOp(mplsReg, Timeout)

def mpls_operation(stub, oper):

    # MPLS Message
    mplsMsg = sl_mpls_pb2.SLMplsLabelBlockMsg()

    block = []

    for label in range(10):
        #Reserve the MPLS Space
        mplsBlock = sl_mpls_pb2.SLMplsLabelBlockKey()
        mplsBlock.StartLabel = 30000+1000*label
        mplsBlock.LabelBlockSize = 100
        block.append(mplsBlock)

    mplsMsg.MplsBlocks.extend(block)


    #Make an RPC Call
    Timeout = 10
    mplsMsg.Oper = oper
    response = stub.SLMplsLabelBlockOp(mplsMsg, Timeout)

    #
    # Check the received result from the Server
    #
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
        print "MPLS %s Success!" %(
            sl_common_types_pb2.SLObjectOp.keys()[oper])
    else:
        print "Error code for mpls %s is 0x%x" % (
            sl_common_types_pb2.SLObjectOp.keys()[oper],
            response.StatusSummary.Status)

def ilm_operation(stub, oper):

    # ilm Message
    ilmMsg = sl_mpls_pb2.SLMplsIlmMsg()

    # Create an empty ilm list
    ilm = []

    # Reserve ilm entry
    in_label_00 = sl_mpls_pb2.SLMplsIlmEntry()
    in_label_00.Key.LocalLabel = 34000

    # Create an empty Paths list
    paths = []

    if in_label_00:
    
        path = sl_mpls_pb2.SLMplsPath()
        path.NexthopAddress.V4Address = (
            int(ipaddress.ip_address('12.1.1.20'))
        )
        path.NexthopInterface.Name = 'GigabitEthernet0/0/0/1'
        path.Action = 1
        path.LoadMetric = 1
        path.VrfName = 'default'
        path.LabelStack.extend([10065])
        paths.append(path)
    in_label_00.Paths.extend(paths)
    ilm.append(in_label_00)
    
    ilmMsg.MplsIlms.extend(ilm)
    #else print "no ilm provided"

    #Make an RPC Call
    Timeout = 10
    ilmMsg.Oper = oper
    response = stub.SLMplsIlmOp(ilmMsg, Timeout)

    #
    # Check the received result from the Server
    #
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
        print "MPLS %s Success!" %(
            sl_common_types_pb2.SLObjectOp.keys()[oper])
    else:
        print "Error code for mpls %s is 0x%x" % (
            sl_common_types_pb2.SLObjectOp.keys()[oper],
            response.StatusSummary.Status)
#
# Setup the GRPC channel with the server, and issue RPCs
#
if __name__ == '__main__':


    from util import util
    server_ip, server_port = util.get_server_ip_port()

    print "Using GRPC Server IP(%s) Port(%s)" %(server_ip, server_port)


    # Create the channel for gRPC.
    channel = implementations.insecure_channel(server_ip, server_port)

    # Spawn a thread to Initialize the client and listen on notifications
    # The thread will run in the background
    client_init.global_init(channel)

    # Create another channel for gRPC requests.
    channel = implementations.insecure_channel(server_ip, server_port)

    # Create the gRPC stub.
    stub = sl_mpls_pb2.beta_create_SLMplsOper_stub(channel)

    # Send an RPC for LSD registration
    mpls_register(stub, sl_common_types_pb2.SL_REGOP_REGISTER)

    # RPC EOF to cleanup any previous stale entries
    mpls_register(stub, sl_common_types_pb2.SL_REGOP_EOF)


    # RPC MPLS block operations
    #    for add: sl_common_types_pb2.SL_OBJOP_ADD
    #    for update: sl_common_types_pb2.SL_OBJOP_UPDATE
    #    for delete: sl_common_types_pb2.SL_OBJOP_DELETE
    mpls_operation(stub, sl_common_types_pb2.SL_OBJOP_ADD)


    # RPC ILM operations
    #    for add: sl_common_types_pb2.SL_OBJOP_ADD
    #    for update: sl_common_types_pb2.SL_OBJOP_UPDATE
    #    for delete: sl_common_types_pb2.SL_OBJOP_DELETE
    ilm_operation(stub, sl_common_types_pb2.SL_OBJOP_UPDATE)
    # while ... add/update/delete routes



    # RPC ILM operations
    #    for add: sl_common_types_pb2.SL_OBJOP_ADD
    #    for update: sl_common_types_pb2.SL_OBJOP_UPDATE
    #    for delete: sl_common_types_pb2.SL_OBJOP_DELETE
    #ilm_operation(stub, sl_common_types_pb2.SL_OBJOP_DELETE)
    #mpls_operation(stub, sl_common_types_pb2.SL_OBJOP_DELETE)

    # Send an RPC to unregistration from LSD
    mpls_register(stub, sl_common_types_pb2.SL_REGOP_UNREGISTER)

    # Exit and Kill any running GRPC threads.
    os._exit(0)
