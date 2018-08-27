# Copyright (c) 2016 by Cisco Systems, Inc.
# All rights reserved.
#

"""
This example explores the interface vertical of the IOS-XR SL-API.

A background thread will be launched by this example to listen to interface 
notification events for registered interfaces ( see intf_enable_notif() )

To test that the notification events get streamed to the client, issue a 'shut'
on one of the registered interfaces.

To terminate the program, issue a ^C in the running window.

"""

import pdb
import ipaddress
import os
import json
import sys,os
import threading
from functools import partial
import signal
from argparse import ArgumentParser
from google.protobuf import json_format


# Add the generated python bindings directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# gRPC generated python bindings

from genpy import sl_global_pb2_grpc
from genpy import sl_global_pb2
from genpy import sl_common_types_pb2
from genpy import sl_version_pb2
from genpy import sl_interface_pb2
from genpy import sl_interface_pb2_grpc

# gRPC libs
import grpc

class SLInterface(object):

    def __init__(self):

        self.path_event = {"path" : "active" , "status": True}

        grpc_server_ip, grpc_server_port = self.get_server_ip_port()

        print("Using GRPC Server IP(%s) Port(%s)" %(grpc_server_ip, grpc_server_port))
       
 
        # Create the channel for gRPC.
        channel = grpc.insecure_channel(str(grpc_server_ip)+":"+
                                                   str(grpc_server_port))

        # Spawn a thread to Initialize the client and listen on notifications
        # The thread will run in the background
        self.global_init(channel)

        self.stub = sl_interface_pb2_grpc.SLInterfaceOperStub(channel)


        # Send an RPC for VRF registrations
        self.intf_register(sl_common_types_pb2.SL_REGOP_REGISTER)

        self.intf_register(sl_common_types_pb2.SL_REGOP_EOF)

        self.intf_enable_notif()

        self.intf_get_globals()

        self.intf_get_msg()


    def intf_register(self,oper):

        #if oper == sl_common_types_pb2.SL_REGOP_REGISTER:
            # Register the interface Client
            intfReg = sl_interface_pb2.SLInterfaceGlobalsRegMsg()
            intfReg.Oper = oper
            Timeout = 10
            response = self.stub.SLInterfaceGlobalsRegOp(intfReg, Timeout)
            print(response)


    def process_message(self, message_dict):

        event_type = message_dict["EventType"] 

        if event_type == "SL_INTERFACE_EVENT_TYPE_INTERFACE_INFO":
            interface = message_dict["Info"]["SLIfInfo"]["Name"]
            state = message_dict["Info"]["IfState"]

            if interface == "GigabitEthernet0/0/0/0":
                if state == "SL_IF_STATE_DOWN":
                    print("Switching to backup path")
                    self.path_event["status"] = True
                    self.path_event["path"] = "backup"
                    print(self.path_event)
                elif state == "SL_IF_STATE_UP":
                    print("Switching to Active path")
                    self.path_event["status"] = True
                    self.path_event["path"] = "active"
                    print(self.path_event)

                elif statw == "SL_IF_STATE_UNKNOWN":
                    print("State Unknown, not taking any action")
                  

        
    def intf_listen_notifications(self):

        intf_getnotif_msg = sl_interface_pb2.SLInterfaceGetNotifMsg()

        Timeout = 3600*24*365

        try:
            while True:
                print("Starting listener for interface events")
                for response in self.stub.SLInterfaceGetNotifStream(intf_getnotif_msg, Timeout):
                    print(response)
                    response_dict = json_format.MessageToDict(response)
                    self.process_message(response_dict)                   
        except Exception as e:
            print("Exception occured while listening to Interface notifications")
            print(e)

    def intf_get_globals(self):
        intf_globalget = sl_interface_pb2.SLInterfaceGlobalsGetMsg()
   
        Timeout = 10 
        response = self.stub.SLInterfaceGlobalsGet(intf_globalget, Timeout)
        print(response)


    def intf_get_stats(self):
        intf_globalget = sl_interface_pb2.SLInterfaceGlobalsGetMsg()

        Timeout = 10
        response = self.stub.SLInterfaceGlobalsGetStats(intf_globalget, Timeout)
        print(response)

    def intf_enable_notif(self):

        intf_notif_op = sl_interface_pb2.SLInterfaceNotifMsg()

        intf_notif_op.Oper = sl_common_types_pb2.SL_NOTIFOP_ENABLE
        intf_name_list = []

        for intf_name in ['MgmtEth0/RP0/CPU0/0', 'GigabitEthernet0/0/0/0', 'GigabitEthernet0/0/0/1']:
            interface = sl_common_types_pb2.SLInterface()
            interface.Name = intf_name
            intf_name_list.append(interface)

        intf_notif_op.Entries.extend(intf_name_list)
          
        Timeout = 10
        response = self.stub.SLInterfaceNotifOp(intf_notif_op, Timeout)
        print(response)
    
    def intf_get_msg(self):
        intf_get = sl_interface_pb2.SLInterfaceGetMsg()

        intf_get.EntriesCount = 5
        intf_get.GetNext = 0
        Timeout = 10
        response = self.stub.SLInterfaceGet(intf_get, Timeout)
        print(response)



    def client_init(self, stub, event):
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
        #Timeout = 5

        while True:
            # This for loop will never end unless the server closes the session
            for response in stub.SLGlobalInitNotif(init_msg, Timeout):
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
                        sys.exit(0)
                elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_HEARTBEAT:
                    print("Received HeartBeat")
                elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
                    if (sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM ==
                            response.ErrStatus.Status):
                        print("Received notice to terminate. Client Takeover?")
                        sys.exit(0)
                    else:
                        print("Error not handled:", response)
                else:
                    print("client init unrecognized response %d", response.EventType)
                    sys.exit(0)



    def global_thread(self, stub, event):
        print("Global thread spawned")

        # Initialize the GRPC session. This function should never return
        self.client_init(stub, event)

        print("global_thread: exiting unexpectedly")
        # If this session is lost, then most likely the server restarted
        # Typically this is handled by reconnecting to the server. For now, exit()
        sys.exit(0)

    #
    # Spawn a thread for global events
    #
    def global_init(self,channel):
        # Create the gRPC stub.
        stub = sl_global_pb2_grpc.SLGlobalStub(channel)

        # Create a thread sync event. This will be used to order thread execution
        event = threading.Event()

        # The main reason we spawn a thread here, is that we dedicate a GRPC
        # channel to listen on Global asynchronous events/notifications.
        # This thread will be handling these event notifications.
        self.global_thread = threading.Thread(target = self.global_thread, args=(stub, event))
        self.global_thread.daemon = True
        self.global_thread.start()

        # Wait for the spawned thread before proceeding
        event.wait()

        # Get the globals. Create a SLGlobalsGetMsg
        global_get = sl_global_pb2.SLGlobalsGetMsg()

        #
        # Make an RPC call to get global attributes
        #
        Timeout = 10 # Seconds
        response = stub.SLGlobalsGet(global_get, Timeout)

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
            sys.exit(0)


    #
    # Get the GRPC Server IP address and port number
    #
    def get_server_ip_port(self):
        # Get GRPC Server's IP from the environment
        if 'SERVER_IP' not in list(os.environ.keys()):
            print("Need to set the SERVER_IP env variable e.g.")
            print("export SERVER_IP='10.30.110.214'")
            sys.exit(0)

        # Get GRPC Server's Port from the environment
        if 'SERVER_PORT' not in list(os.environ.keys()):
            print("Need to set the SERVER_PORT env variable e.g.")
            print("export SERVER_PORT='57777'")
            sys.exit(0)

        return (os.environ['SERVER_IP'], int(os.environ['SERVER_PORT']))

EXIT_FLAG = False
#POSIX signal handler to ensure we shutdown cleanly
def handler(sl_interface, signum, frame):
    global EXIT_FLAG

    if not EXIT_FLAG:
        EXIT_FLAG = True
        print("Unregistering...")
        sl_interface.intf_register(sl_common_types_pb2.SL_REGOP_UNREGISTER)
       # Exit and Kill any running GRPC threads.
        os._exit(0)


#
# Setup the GRPC channel with the server, and issue RPCs
#
if __name__ == '__main__':

    # Create SLInterface object to setup netconf and gRPC connections, and configure active path,
    # before listening for interface events

    sl_interface = SLInterface()


    sl_interface.intf_listen_notifications()
    # Register our handler for keyboard interrupt and termination signals
    signal.signal(signal.SIGINT, partial(handler, sl_interface))
    signal.signal(signal.SIGTERM, partial(handler, sl_interface))

    # The process main thread does nothing but wait for signals
    signal.pause()

