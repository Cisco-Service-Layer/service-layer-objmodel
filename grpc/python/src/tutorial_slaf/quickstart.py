#
# Copyright (c) 2025 by cisco Systems, Inc. 
# All rights reserved.
#

# Standard python libs
import ipaddress
import os
import sys
import argparse
import logging

# Add the generated python bindings directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# gRPC generated python bindings
from genpy import sl_route_ipv4_pb2_grpc
from genpy import sl_route_ipv4_pb2
from genpy import sl_route_common_pb2
from genpy import sl_common_types_pb2

#Utilities
from tutorial_slaf import slaf
# gRPC libs
import grpc

# Our Client ID
client_id = "521"

#
# Helper functions

#
# Verify the VRF Reg Oper is valid
#
def valid_vrf_reg(op):
    if op == int(sl_common_types_pb2.SL_REGOP_REGISTER) or \
       op == int(sl_common_types_pb2.SL_REGOP_UNREGISTER) or \
       op == int(sl_common_types_pb2.SL_REGOP_EOF):
       return True

    print('''Vrf Registration is not set to Reg(1), Unregister(2), EOF(3).
        Ignore if on purpose. User set this field to {}'''.format(op))
    return False

#
# Verify the Route Oper is valid
#
def valid_object_op(op):
    if op == int(sl_common_types_pb2.SL_OBJOP_ADD) or \
       op == int(sl_common_types_pb2.SL_OBJOP_UPDATE) or \
       op == int(sl_common_types_pb2.SL_OBJOP_DELETE):
       return True

    print('''Route operation is not set to Add(1), Update(2), nor Delete(3).
        Ignore if on purpose. User set this field to {}'''.format(op))
    return False

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

# End of helper functions
#

#
# Setup the GRPC channel with the server, and issue RPCs
#
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description ='The full tutorial example')
    parser.add_argument('-u', '--username', required=True, help='Specify username')
    parser.add_argument('-p', '--password', required=True, help='Specify password')
    parser.add_argument('-r', '--rpc', type=int, default=0, required=True, help='''Specify what RPC user would like to test.
                        SLAFOp/SLAFOpStream(1), SLAFGet(2), SLAFVrfRegGet(3), SLAFNotifStream(4)''')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable Debugging')
    parser.add_argument('-e', '--print_responses', action='store_true', help='Prints the responses')

    # Create the group for general fields in route programming
    rp_general = parser.add_argument_group(
        "General route programming fields in SLAF. When --rpc 1 option is used and one of the fields is set: -ipv4, -mpls, -pg"
    )

    # Common fields used for route programming. Set these arguments with the specific fields of ipv4, mpls, or pg.
    # Showcases how to set and perform SLAFOp and SLAFOpStream rpc's.
    rp_general.add_argument('--route_oper', type=int, default=0, help='Route Operation: Add(1), Update(2), Delete(3) (default 0)')
    rp_general.add_argument('--vrf_reg_oper', type=int, default=0, help='VRF registration Operation: Reg(1), Unregister(2), EOF(3) (default 0)')
    rp_general.add_argument('--stream_case', action='store_true', help='Use the streaming rpc for route programming in SLAF')
    rp_general.add_argument('--batch_size', type=int, default=1000, help='Number of entries per batch, used in the operation (default 1000)')
    rp_general.add_argument('--next_hop_intf', type=str, default='FourHundredGigE0/0/0/0', help='Next hop interface name (default FourHundredGigE0/0/0/0)')
    rp_general.add_argument('--next_hop_ip', type=str, default='10.0.0.1', help='Next Hop IP base address (default 10.0.0.1)')
    rp_general.add_argument('--auto_inc_nhip', action='store_true', help='Auto Increment next hop IP')
    rp_general.add_argument('--admin_distance', type=int, default=99, help='Admin Distance (default 99)')
    rp_general.add_argument('--ack_type', type=int, default=0, help='Types of Acknowledgement agent expects: RIB_ACK(0), RIB_AND_FIB_ACK(1), RIB_FIB_INUSE_ACK(2) (default 0)')
    rp_general.add_argument('--ack_permit', type=int, default=0, help='Response types permitted: SL_PERMIT_FIB_STATUS_ALL(0), SL_PERMIT_FIB_SUCCESS(1), SL_PERMIT_FIB_FAILED(2), SL_PERMIT_FIB_INELIGIBLE(3), SL_PERMIT_FIB_INUSE_SUCCESS(4) (default 0)')
    rp_general.add_argument('--ack_cadence', type=int, default=0, help='Cadence of hw programming responses: SL_RSP_CONTINUOUS(0), SL_RSP_JUST_ONCE(1), SL_RSP_ONCE_EACH(2), SL_RSP_NONE(3) (default 0)')
    rp_general.add_argument('--route_flag', type=int, default=0, help='Control programming of the route/PG to RIB: SL_ROUTE_FLAG_RESERVED(0), SL_ROUTE_FLAG_PREFER_OVER_LDP(1), SL_ROUTE_FLAG_DISABLE_LABEL_MERGE(2), SL_ROUTE_FLAG_VIABLE_PATHS_ONLY(3), SL_ROUTE_FLAG_ACTIVE_ON_VIABLE_PATH(4) (default 0)')

    # Create the group for specific table type in route programming
    rp_specific = parser.add_argument_group(
        "Route programming in SLAF. When --rpc 1 option is used"
    )

    # For Programming IPv4 routes:
    #   -ipv4:     Enable Ipv4 testing. Used in conjunction with the route programming fields.
    rp_specific.add_argument('--ipv4', action='store_true', help='Test IPv4 vertical')
    rp_specific.add_argument('--first_prefix', type=str, default='20.0.0.0', help='First Prefix to be used in the route operation (default 20.0.0.0)')
    rp_specific.add_argument('--prefix_len', type=int, default=24, help='Prefix Length to be used in the route operation (default 24)')
    rp_specific.add_argument('--num_routes', type=int, default=100, help='Number of routes used in the operation (default 100)')
    rp_specific.add_argument('--use_pg_for_ipv4', type=str, default='none', help='The path group to use for programming ipv4 routes (default none)')

    # For Programming MPLS labels:
    #   -mpls:      Enable MPLS testing. Used in conjunction with the route programming fields.
    rp_specific.add_argument('--mpls', action='store_true', help='Test MPLS vertical')
    rp_specific.add_argument('--start_label', type=int, default=12000, help='Starting label (default 12000)')
    rp_specific.add_argument('--out_label', type=int, default=20000, help='Out label (default 20000)')
    rp_specific.add_argument('--num_labels', type=int, default=1000, help='Number of labels (default 1000)')
    rp_specific.add_argument('--num_paths', type=int, default=1, help='Number of paths (default 1)')

    # For Programming PG:
    # -create_path_group:       Enable PG Testing and provide a name for the PG. For purposes of this tutorial, we showcase how to create pg for ipv4 routes.
    #                           When set, will use next_hop_ip and next_hop_intf variables for information to create the pathgroup
    rp_specific.add_argument('--pg', action='store_true', help='Test PG creation')
    rp_specific.add_argument('--pg_name', type=str, default='default', help='PathGroup Name (default default)')
    rp_specific.add_argument('--pg_num_path', type=int, default=1, help='Number of Route paths to add into path group (default 1)')

    # Create the group for get fields
    get = parser.add_argument_group(
        "Get fields in SLAF. When --rpc 2 option is used"
    )

    # For Get:
    #          Showcases how to set up and perform SLAFGet Rpc.
    #          The messaged request associated with this rpc can handle multiple different objects,
    #          but for this tutorial we showcase how to set one of each type in any repeated field of the request.
    get.add_argument('--get_vrf_name', type=str, default='default', help='VrfName for object search (default default)')
    get.add_argument('--get_client_id_all', action='store_true', help='Indicates User wants to return objects produced by all client ids')
    get.add_argument('--get_client_id', type=int, default=521, help='Indicates User wants to return objects produced by specific client id (default 521)')
    get.add_argument('--get_table_list', type=int, default=0, help='Indicates the Table types the user wishes to search for Table type: SL_TABLE_TYPE_RESERVED(0), SL_IPv4_ROUTE_TABLE(1), SL_IPv6_ROUTE_TABLE(2), SL_MPLS_LABEL_TABLE(3), SL_PATH_GROUP_TABLE(4) (default 0)')
    get.add_argument('--get_route_list', action='store_true', help='Indicates user wishes to search based on any of the GetRouteList criteria below. If set, will override the table_list')
    get.add_argument('--get_vxlanid', type=int, default=-1, help='This is a GetRouteList field. Using VxLanID for object search (default -1)')
    get.add_argument('--get_pg_regex', type=str, default='', help='This is a GetRouteList field. Using Path Group Regex expression for object search (default "")')
    get.add_argument('--get_ipv4_prefix', type=str, default='', help='This is a GetRouteList field and used in conjunction with get_ipv4_prefix_len. Using ipv4 prefix and prefix len for object search (default "")')
    get.add_argument('--get_ipv4_prefix_len', type=int, default=24, help='This is a GetRouteList field and used in conjunction with get_ipv4_prefix. Using ipv4 prefix and len for object search (default 24)')

    # Create the group for get fields
    get_vrf = parser.add_argument_group(
        "GetVrf fields in SLAF. When --rpc 3 option is used"
    )

    # For GetRegVrf:
    #           Showcases how to set up and perform SLAFNotifStream rpc.
    get_vrf.add_argument('--get_vrf_all', action='store_true', help='Test GetVrf Request for all clients, not just own client')

    # Create the group for notification fields
    notification = parser.add_argument_group('Notification Stream fields in SLAF. When --rpc 4 option is used')

    # For NotifStream:
    # -notif_stream:     Enable Notification Stream Testing. Showcases how to set up and perform SLAFGetVrf rpc.
    notification.add_argument('--notif_duration', type=int, default=10, help='Duration of time (seconds) that the user wants to keep the stream alive for (default 10)')
    notification.add_argument('--notif_oper', type=int, default=0, help='This is to enable or disable route notifications in a vrf or next hop change. The choices are: SL_NOTIFOP_RESERVED(0), SL_NOTIFOP_ENABLE(1) or SL_NOTIFOP_DISABLE(2) (default 0)')
    notification.add_argument('--notif_vrfname', type=str, default='default', help='Vrf the client is interested in (default default)')
    notification.add_argument('--notif_route_reg', action='store_true', help='This is to indicate the client wants to do Route redistribution registration. This option requires setting the NotifRouteReg fields below')
    notification.add_argument('--notif_route_src_proto', type=str, default='', help='This is a NotifRouteReg field. For route redistribution registration for routes with specified source protocol (default "")')
    notification.add_argument('--notif_route_src_proto_tag', type=str, default='', help='This is a NotifRouteReg field. For route redistribution registration for routes with specified source protocol tags (default "")')
    notification.add_argument('--notif_route_table_type', type=int, default=0, help='This is a NotifRouteReg field. Indicate the Table types the user wishes to search for table type: SL_TABLE_TYPE_RESERVED(0), SL_IPv4_ROUTE_TABLE(1), SL_IPv6_ROUTE_TABLE(2), SL_MPLS_LABEL_TABLE(3), SL_PATH_GROUP_TABLE(4) (default 0)')
    notification.add_argument('--notif_next_hop_reg', action='store_true', help='This is to indicate client wants to do next hop notification registration. For this tutorial we showcase how to do this for ipv4 routes. This option requires setting the NotifNextHopReg fields below')
    notification.add_argument('--notif_ipv4_prefix', type=str, default='20.0.0.0', help='This is a NotifNextHopReg field (default 20.0.0.0)')
    notification.add_argument('--notif_ipv4_prefix_len', type=int, default=24, help='This is a NotifNextHopReg field (default 24)')
    notification.add_argument('--notif_exact_match', action='store_true', help='This is a NotifNextHopReg field. Choose to do exact match (true), or best match (false)')
    notification.add_argument('--notif_allow_default', action='store_true', help='This is a NotifNextHopReg field. Allows default route to be returned')
    notification.add_argument('--notif_recurse', action='store_true', help='This is a NotifNextHopReg field. Return all path list of nexthops (true) or immediately viable path list (false)')

    args = parser.parse_args()
    server_ip, server_port = get_server_ip_port()

    # Set logging level
    if args.print_responses:
        slaf.set_log_level(logging.INFO)
    if args.debug:
        slaf.set_log_level(logging.DEBUG)

    print("Using GRPC Server IP(%s) Port(%s)" %(server_ip, server_port))

    # Create the channel for gRPC.
    channel = grpc.insecure_channel(str(server_ip) + ":" + str(server_port))
    global metadata

    metadata = [
                    ("username", args.username),
                    ("password", args.password),
                    ("iosxr-slapi-clientid", client_id)
                    ]
    if args.rpc <= 0 or args.rpc > 4:
        print("Invalid operation for rpc type. Please pick a valid operation.")
        os._exit(0)

    # Spawn a thread to Initialize the client and listen on notifications
    # The thread will run in the background
    slaf.global_init(channel, args.username, args.password)

    # Checks for some message restrictions
    if len(args.get_vrf_name) > slaf.maxVrfNameLength:
        print("get_vrf_name is too long! Exiting...")
        os._exit(0)
    if len(args.notif_vrfname) > slaf.maxVrfNameLength:
        print("notif_vrfname is too long! Exiting...")
        os._exit(0)
    if len(args.next_hop_intf) > slaf.maxInterfaceNameLength:
        print("Interface name is too long! Exiting...")
        os._exit(0)
    if args.batch_size > slaf.maxBatchSize:
        args.batch_size = slaf.maxBatchSize
        print("Batch size was above the max. It is now updated to the max batch size")
    if args.num_paths > slaf.maxPrimaryPathPerEntry:
        args.num_paths = slaf.maxPrimaryPathPerEntry
        print("Primary path per entry was above the max. It is now updated to the max amount")
    if args.pg_num_path > slaf.maxPrimaryPathPerEntry:
        args.pg_num_path = slaf.maxPrimaryPathPerEntry
        print("Primary path per entry was above the max. It is now updated to the max amount")

    if args.rpc == 1:
        # SLAFOp or SLAFOpStream case
        if args.ipv4:
            if valid_vrf_reg(args.vrf_reg_oper):
                # Send an RPC for VRF registrations
                print("Performing ipv4 vrf reg")
                slaf.vrf_operation(channel, metadata, args.vrf_reg_oper,
                    sl_common_types_pb2.SL_IPv4_ROUTE_TABLE)

            if valid_object_op(args.route_oper):
                # Send an RPC for ipv4 route programming
                print("Performing ipv4 route operation")
                slaf.route_operation(channel, metadata, args.route_oper, args.route_flag,
                    args.admin_distance, args.ack_type, args.ack_permit, args.ack_cadence,
                    args.first_prefix, args.prefix_len, args.num_routes, args.use_pg_for_ipv4,
                    args.batch_size, args.next_hop_ip, args.next_hop_intf, args.num_paths,
                    args.auto_inc_nhip, args.stream_case)
        if args.mpls:
            if valid_vrf_reg(args.vrf_reg_oper):
                # Send an RPC for VRF registrations
                print("Performing mpls vrf reg")
                slaf.vrf_operation(channel, metadata, args.vrf_reg_oper,
                    sl_common_types_pb2.SL_MPLS_LABEL_TABLE)

            if valid_object_op(args.route_oper):
                # Send an RPC for mpls programming
                print("Performing mpls operation")
                slaf.mpls_operation(channel, metadata, args.route_oper, args.route_flag,
                    args.admin_distance, args.ack_type, args.ack_permit, args.ack_cadence,
                    args.start_label, args.out_label, args.num_labels, args.num_paths,
                    args.batch_size, args.next_hop_ip, args.next_hop_intf,
                    args.auto_inc_nhip, args.stream_case)
        if args.pg:
            if valid_vrf_reg(args.vrf_reg_oper):
                # Send an RPC for VRF registrations
                print("Performing pg vrf reg")
                slaf.vrf_operation(channel, metadata, args.vrf_reg_oper,
                    sl_common_types_pb2.SL_PATH_GROUP_TABLE)

            if valid_object_op(args.route_oper):
                # Send an RPC for pg programming
                print("Performing pg operation")
                slaf.pg_operation(channel, metadata, args.route_oper, args.route_flag,
                    args.admin_distance, args.ack_type, args.ack_permit, args.ack_cadence,
                    args.pg_name, args.pg_num_path, args.batch_size, args.next_hop_ip, args.next_hop_intf,
                    args.auto_inc_nhip, args.stream_case)
    elif args.rpc == 2:
        # SLAFGet case
        # Send an rpc for get request
        print("Performing get operation")
        slaf.get_operation(channel, metadata, args.get_vrf_name,
            args.get_client_id_all, args.get_client_id, args.get_table_list,
            args.get_route_list, args.get_vxlanid, args.get_pg_regex,
            args.get_ipv4_prefix, args.get_ipv4_prefix_len)
    elif args.rpc == 3:
        # SLAFVrfRegGet case
        # Send an rpc for get vrf register request
        print("Performing vrf register get operation")
        slaf.vrf_reg_get_operation(channel, metadata, args.get_vrf_all)
    elif args.rpc == 4:
        # SLAFNotifStream case
        # Send an rpc for notification stream request
        print("Performing notificaiton stream operation")
        slaf.notif_stream_operation(channel, metadata, args.notif_duration,
            args.notif_oper, args.notif_vrfname, args.notif_route_reg, args.notif_route_src_proto,
            args.notif_route_src_proto_tag, args.notif_route_table_type,
            args.notif_next_hop_reg, args.notif_ipv4_prefix, args.notif_ipv4_prefix_len,
            args.notif_exact_match, args.notif_allow_default, args.notif_recurse)
    else:
        print("--rpc option is not valid")

    # Exit and Kill any running GRPC threads.
    os._exit(0)
