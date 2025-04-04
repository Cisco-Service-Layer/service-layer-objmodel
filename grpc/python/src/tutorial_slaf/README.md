# SLAF Python Quick Tutorial

This tutorial goes over how to perform the SLAF RPC calls, setting up the message requests, and getting the responses. This tutorial does not claim to show how to fill every field for all SLAF RPC messages, nor does it allow the option to configure every field with the cli. The purpose of this tutorial is to showcase how the user can implement the SLAF RPC's, and provide examples on how to set/get most fields in the requests/responses for those RPCs. From there on, it is up to the user to figure out how to use said RPC's, and the associated requests and responses, to perform their intended actions. Obviously, a pre-requisite would be to learn what is an RPC. For more information detailing RPCs, refer to https://grpc.io/docs/what-is-grpc/core-concepts/#RPC-life-cycle.

## Table of Contents

- [Server Setup](#server-setup)

- [Python Setup](#python-setup)

- [Running the tutorial](#running-the-tutorial)

    1) [How to Build](#how-to-build)

    2) [Examples](#examples)

- [Optional Information](#optional-information)

    1) [Generate gRPC Code](#generate-grpc-code)

    2) [Initial Connection and Handshake](#initial-connection-and-handshake)

## Server Setup

On the server side, we need to configure GRPC and enable the service layer through the following CLI configuration:

    ! Configure GRPC
    configure
    grpc port 57344
    grpc no-tls
    grpc address-family ipv4
    commit
    end

    ! Configure Service layer
    configure
    grpc service-layer
    commit
    end

We also need to configure a server IP address. We will use our MgmtEth 0/RP0/CPU0/0. 
To configure an IP address on the management interface, one can use dhcp as follows:

    ! Configure the Mgmt Interface
    configure
    interface MgmtEth 0/RP0/CPU0/0
    ipv4 address dhcp
    no shut
    commit
    end

We also need to configure an any interface user wants to use for route programming.
For our tests the interface is FourHundredGigE0/0/0/0 (as this is the default):
    configure
    interface FourHundredGigE0/0/0/0
    no shut
    commit
    end

To check the IP address assigned:

    show ip interface brief

On the client side, the very first thing we need to do is set the server IP address and gRPC port.  
You can check your port number by running the following CLI command on the IOS-XR  
server box (should be the same as the one configured):  

    # show run grpc

## Python Setup

To install dependencies first create a virtual env:
    python3.11 -m venv sl-env
    source sl-env/bin/activate
    pip install -r grpc/python/requirements.txt

## Running the tutorial

First we will showcase the options the tutorial provides, and then show how to build and examples for each RPC:  

##### Arguments Required for Connection

| Argument | Description |
| --- | --- |
| -u/--username | Specify username (required) |
| -p/--password | Specify password (required) |
| -r/--rpc      | Specify what RPC user would like to test. SLAFOp/SLAFOpStream(1), SLAFGet(2), SLAFVrfRegGet(3), SLAFNotifStream(4) (default 0) |

##### Optional arguments

| Argument | Description |
| --- | --- |
| --debug           | Sets log level to debug. Will print Debug messages and levels above (default false) |
| --print_responses | Sets log level to Info. Will print Info messages and levels above (default false) |

##### Ipv4 Testing (when --rpc 1 option is used)

| Argument | Description |
| --- | --- |
| --ipv4            | Test IPv4 vertical |
| --first_prefix    | First Prefix to be used in the route operation (default 20.0.0.0) |
| --prefix_len      | Prefix Length to be used in the route operation (default 24) |
| --num_routes      | Number of routes used in the operation (default 100) |
| --use_pg_for_ipv4 | The path group to use for programming ipv4 routes (default none) |

##### MPLS Testing (when --rpc 1 option is used)

| Argument | Description |
| --- | --- |
| --mpls        | Test MPLS vertical |
| --start_label | Starting label (default 12000) |
| --out_label   | Out label (default 20000) |
| --num_labels  | Number of labels (default 1000) |
| --num_paths   | Number of paths (default 1) |

##### PG Testing (when --rpc 1 option is used)

| Argument | Description |
| --- | --- |
| --pg          | Test PG creation |
| --pg_name     | PathGroup Name (default default) |
| --pg_num_path | Number of Route paths to add into path group (default 1) |

##### General route programming fields in SLAF. When --rpc 1 option is used and one of the fields is set: -ipv4, -mpls, -pg

| Argument | Description |
| --- | --- |
| --route_oper      | Route Operation: Add(1), Update(2), Delete(3) (default 0) |
| --vrf_reg_oper    | VRF registration Operation: Reg(1), Unregister(2), EOF(3) (default 0) |
| --stream_case     | Use the streaming rpc for route programming in SLAF |
| --batch_size      | Number of entries per batch, used in the operation (default 1000) |
| --next_hop_intf   | Next hop interface name (default FourHundredGigE0/0/0/0) |
| --next_hop_ip     | Next Hop IP base address (default 10.0.0.1) |
| --auto_inc_nhip   | Auto Increment next hop IP |
| --admin_distance  | Admin Distance (default 99) |
| --ack_type        | Types of Acknowledgement agent expects: RIB_ACK(0), RIB_AND_FIB_ACK(1), RIB_FIB_INUSE_ACK(2) (default 0) |
| --ack_permit      | Response types permitted: SL_PERMIT_FIB_STATUS_ALL(0), SL_PERMIT_FIB_SUCCESS(1), SL_PERMIT_FIB_FAILED(2), SL_PERMIT_FIB_INELIGIBLE(3), SL_PERMIT_FIB_INUSE_SUCCESS(4) (default 0) |
| --ack_cadence     | Cadence of hw programming responses: SL_RSP_CONTINUOUS(0), SL_RSP_JUST_ONCE(1), SL_RSP_ONCE_EACH(2), SL_RSP_NONE(3) (default 0) |
| --route_flag      | Control programming of the route/PG to RIB: SL_ROUTE_FLAG_RESERVED(0), SL_ROUTE_FLAG_PREFER_OVER_LDP(1), SL_ROUTE_FLAG_DISABLE_LABEL_MERGE(2), SL_ROUTE_FLAG_VIABLE_PATHS_ONLY(3), SL_ROUTE_FLAG_ACTIVE_ON_VIABLE_PATH(4) (default 0) |

##### Get Testing. When --rpc 2 option is used

| Argument | Description |
| --- | --- |
| --get_vrf_name        | VrfName for object search (default default) |
| --get_client_id_all   | Indicates User wants to return objects produced by all client ids |
| --get_client_id       | Indicates User wants to return objects produced by specific client id (default 521) |
| --get_table_list      | Indicates the Table types the user wishes to search for Table type: SL_TABLE_TYPE_RESERVED(0), SL_IPv4_ROUTE_TABLE(1), SL_IPv6_ROUTE_TABLE(2), SL_MPLS_LABEL_TABLE(3), SL_PATH_GROUP_TABLE(4) (default 0) |
| --get_route_list      | Indicates user wishes to search based on any of the GetRouteList criteria below. If set, will override the table_list |
| --get_vxlanid         | This is a GetRouteList field. Using VxLanID for object search (default -1) |
| --get_pg_regex        | This is a GetRouteList field. Using Path Group Regex expression for object search (default "") |
| --get_ipv4_prefix     | This is a GetRouteList field and used in conjunction with get_ipv4_prefix_len. Using ipv4 prefix and prefix len for object search (default "") |
| --get_ipv4_prefix_len | This is a GetRouteList field and used in conjunction with get_ipv4_prefix. Using ipv4 prefix and len for object search (default 24) |

##### GetVrf Testing. When --rpc 3 option is used

| Argument | Description |
| --- | --- |
| --get_vrf_all | Test GetVrf Request for all clients, not just own client |

##### NotifStream Testing. When --rpc 4 option is used

| Argument | Description |
| --- | --- |
| --notif_duration              | Duration of time (seconds) that the user wants to keep the stream alive for (default 10) |
| --notif_oper                  | This is to enable or disable route notifications in a vrf or next hop change. The choices are: SL_NOTIFOP_RESERVED(0), SL_NOTIFOP_ENABLE(1) or SL_NOTIFOP_DISABLE(2) (default 0) |
| --notif_vrfname               | Vrf the client is interested in (default default) |
| --notif_route_reg             | This is to indicate the client wants to do Route redistribution registration. This option requires setting the NotifRouteReg fields below |
| --notif_route_src_proto       | This is a NotifRouteReg field. For route redistribution registration for routes with specified source protocol (default "") |
| --notif_route_src_proto_tag   | This is a NotifRouteReg field. For route redistribution registration for routes with specified source protocol tags (default "") |
| --notif_route_table_type      | This is a NotifRouteReg field. Indicate the Table types the user wishes to search for table type: SL_TABLE_TYPE_RESERVED(0), SL_IPv4_ROUTE_TABLE(1), SL_IPv6_ROUTE_TABLE(2), SL_MPLS_LABEL_TABLE(3), SL_PATH_GROUP_TABLE(4) (default 0) |
| --notif_next_hop_reg          | This is to indicate client wants to do next hop notification registration. For this tutorial we showcase how to do this for ipv4 routes. This option requires setting the NotifNextHopReg fields below |
| --notif_ipv4_prefix           | This is a NotifNextHopReg field (default 20.0.0.0) |
| --notif_ipv4_prefix_len       | This is a NotifNextHopReg field (default 24) |
| --notif_exact_match           | This is a NotifNextHopReg field. Choose to do exact match (true), or best match (false) |
| --notif_allow_default         | This is a NotifNextHopReg field. Allows default route to be returned |
| --notif_recurse               | This is a NotifNextHopReg field. Return all path list of nexthops (true) or immediately viable path list (false) |

### How to Build

All SL-API protobuf files can be found in the "grpc/protos/" directory  
>**Note:** User can find more information on generating the stubs from these proto files in the optional section: [Generate gRPC Code](#generate-grpc-code)

The user can run "make bindings" from the service-layer-objmodel top level directory. This will take some time to build
the first time, but once it completes you can run "make slapi-bash" to drop into bash, like so:

    Bash-Prompt:sl$ make bindings
    Bash-Prompt:sl$ make slapi-bash

Once in bash, you can navigate to the tutorial directory:

    root@f6179b5127f5:/slapi# cd grpc/python/src/tutorial_slaf/

### Examples

>**Note:** Before trying out the examples, make sure to setup and source the python environment [Python Setup](#python-setup), and the SERVER_IP and SERVER_PORT. Steps on how to get ip and port information from box are in [Server Setup](#server-setup):

Set the server address and port number as environment variables with the
following example command (this is assuming you are in bash shell):

    $ export SERVER_IP=111.111.111.111
    $ export SERVER_PORT=11111

IPV4 Examples:

    Adding 500 routes through stream RP while auto incrementing the nexthop ip:
    $ python3 quickstart.py -u username -p password --rpc 1 --ipv4 --route_oper 1 --vrf_reg_oper 1 --stream_case --num_routes 500 --auto_inc_nhip
    Delete 20 routes using unary RPC with batch size at 10. Assuming vrf registration is handled with auto-register. Print responses:
    $ python3 quickstart.py -u username -p password --rpc 1 --ipv4 --route_oper 3 --vrf_reg_oper 3 --num_routes 20 --batch_size 10 --print_responses
    Delete 50 routes with streaming RPC with batch size at 30 and with response ACK for FIB:
    $ python3 quickstart.py -u username -p password --rpc 1 --ipv4 --route_oper 3 --vrf_reg_oper 1 --num_routes 50 --batch_size 30 --ack_type 1
    Adding 100k routes with stream case with Ack type for RIB and FIB, but only permit a FIB success with cadence set to only once:
    $  python3 quickstart.py -u username -p password --rpc 1 --ipv4 --route_oper 1 --vrf_reg_oper 1 --stream_case --num_routes 100000 --ack_type 1 --ack_permit 1 --ack_cadence 1
    Deleting All Routes and Unregister Vrf:
    $ python3 quickstart.py -u username -p password --rpc 1 --ipv4 --vrf_reg_oper 2

MPLS Example:

    Adding 1000 Labels with incrementing nexthops whose starting address set as 11.0.0.0. Do this with streaming RPC and set response ack to RIB_AND_FIB_ACK:
    $ python3 quickstart.py -u username -p password --rpc 1 --mpls --route_oper 1 --vrf_reg_oper 1 --stream_case --next_hop_ip 11.0.0.0 --auto_inc_nhip --ack_type 1
    Deleting 35 labels with unary RPC. Print out any responses and debug messages:
    $ python3 quickstart.py -u username -p password --rpc 1 --mpls --route_oper 3 --vrf_reg_oper 1 --num_labels 35 --debug
    Adding 2 Label where the start label is 25000 and the out label is 26000:
    $ python3 quickstart.py -u username -p password --rpc 1 --mpls --route_oper 1 --vrf_reg_oper 1 --num_labels 2 --start_label 25000 --out_label 26000 --debug

Path Group Example:  
For purposes of this tutorial, we showcase how to create pg for ipv4 routes.  
When set, will use next_hop_ip and interface variables for information to create the pathgroup.  

    Create a path group named "temp" with 64 paths for ipv4 routes:
    $ python3 quickstart.py -u username -p password --rpc 1 --pg --route_oper 1 --vrf_reg_oper 1 --pg_name temp --pg_num_path 64
    Delete a path group named "temp":
    $ python3 quickstart.py -u username -p password --rpc 1 --pg --route_oper 3 --vrf_reg_oper 1 --pg_name temp
    Create a path group named "temp" with 64 paths for ipv4 routes with next_hop_ip address set to 11.0.0.1 and auto incrementing:
    $ python3 quickstart.py -u username -p password --rpc 1 --pg --route_oper 1 --vrf_reg_oper 1 --pg_name temp --pg_num_path 64 --next_hop_ip 11.0.0.1 --auto_inc_nhip
    Apply path group named "temp" for 1000 ipv4 routes with response ack set to RIB_ACK with stream case:
    $ python3 quickstart.py -u username -p password --rpc 1 --ipv4 --use_pg_for_ipv4 temp --route_oper 1 --vrf_reg_oper 1 --stream_case --num_routes 1000 --ack_type 0

Get Request Example:
For purposes of this tutorial, we showcase how to get route lists for only a ipv4 route.

    Get information for all routes based off of client id 521 with vrfname as 'default':
    $ python3 quickstart.py -u username -p password --rpc 2 --get_vrf_name default --get_client_id 521 --print_responses

    Get information for all routes based on all existing clients:
    $ python3 quickstart.py -u username -p password --rpc 2 --get_vrf_name default --get_client_id_all --print_responses

    Get information for all routes of a specific table type SL_IPv4_ROUTE_TABLE:
    $ python3 quickstart.py -u username -p password --rpc 2 --get_vrf_name default --get_client_id 521 --get_table_list 1 --print_responses

    Get information for an ipv4 route with address 20.0.0.0 with prefix length as 24:
    $ python3 quickstart.py -u username -p password --rpc 2 --get_vrf_name default --get_client_id 521 --get_route_list --get_ipv4_prefix 20.0.0.0 --get_ipv4_prefix_len 24 --print_responses

    Get information of all objects based on a regex expression for path group:
    $ python3 quickstart.py -u username -p password --rpc 2 --get_vrf_name default --get_client_id 521 --get_route_list --get_pg_regex te* --print_responses

    Get information of all objects based on regex expression for path group, and an ipv4 route from address 20.0.0.0 with prefix length as 24:
    $ python3 quickstart.py -u username -p password --rpc 2 --get_vrf_name default --get_client_id 521 --get_route_list --get_pg_regex te* --get_ipv4_prefix 20.0.0.0 --get_ipv4_prefix_len 24 --print_responses

GetVrf Request Example:

    Get information for all clients:
    $ python3 quickstart.py -u username -p password --rpc 3 --get_vrf_all --print_response
    Get Vrf Reg Information for own client 521:
    $ python3 quickstart.py -u username -p password --rpc 3 --print_responses

Notification Stream Example:
For purposes of this tutorial, we showcase how to enable route notifications for only a ipv4 route.

    Enabling route notification for routes with table type SL_IPv4_ROUTE_TABLE, and programmed from this tutorial (SrcProto as application, and SrcProtoTag as Service-layer) for 10 seconds:
    $ python3 quickstart.py -u username -p password --rpc 4 --notif_duration 10 --notif_oper 1 --notif_vrfname default --notif_route_reg --notif_route_src_proto application --notif_route_src_proto_tag Service-layer --notif_route_table_type 1 --print_responses

    Disabling next hop change notification for 15 seconds and for next hop ip ipv4 address as 20.0.0.0 with prefix length as 24. And with best match, allow default route to be returned, and return only for the immediate viable path list:
    $ python3 quickstart.py -u username -p password --rpc 4 --notif_duration 15 --notif_oper 2  --notif_vrfname default --notif_next_hop_reg --notif_ipv4_prefix 20.0.0.0 --notif_ipv4_prefix_len 24 --notif_allow_default --print_responses

    Enabling next hop change notification for 9 seconds and for next hop ip ipv4 address as 20.0.0.0 with prefix length as 24. And with exact match, allow default route to not be returned, and return all next hop's paths paths lists:
    $ python3 quickstart.py -u username -p password --rpc 4 --notif_duration 9 --notif_oper 1  --notif_vrfname default --notif_next_hop_reg --notif_ipv4_prefix 20.0.0.0 --notif_ipv4_prefix_len 24 --notif_exact_match --notif_recurse --print_responses

    Same as above example but also enable route notification for routes with table type as SL_IPv6_ROUTE_TABLE:
    $ python3 quickstart.py -u username -p password --rpc 4 --notif_duration 9 --notif_oper 1  --notif_vrfname default --notif_next_hop_reg --notif_ipv4_prefix 20.0.0.0 --notif_ipv4_prefix_len 24 --notif_exact_match --notif_recurse --print_responses --notif_route_reg --notif_route_src_proto application --notif_route_src_proto_tag Service-layer --notif_route_table_type 2

>**Note:** There are actually two optional RPC's which run before any test case.  
More information can be found in the [Initial Connection and Handshake](#initial-connection-and-handshake) section

### Optional Information

#### Generate gRPC Code

If you are not familiar with gRPC, we recommend you refer to gRPC's
documentation before beginning with our tutorial: [gRPC Docs](http://www.grpc.io/docs/)

You should have received all of the Protobuf files required to run the Cisco
Service Layer API. In order to generate the gRPC client side code stubs in python, run the following command (you may have to adjust the path to the proto files and the output according to your requirements):  

**For convenience, these files are also committed in this repo under grpc/python/src/genpy/ (so you can skip this step).**

    $ protoc -I ../../protos --python_out=. --grpc_out=./genpy/ --plugin=protoc-gen-grpc=`which grpc_python_plugin` ../../protos/*.proto

This generates the code stubs that we will now utilize to create a client.
The files are recognizable from the "_pb2" and  "_pb2_grpc" that is appended to the name of the proto files they were generated from.

#### Initial Connection and Handshake

The client sets up the connection with the server through insecure credentials.
Once connected, the client gets some information related to message restrictions (SLGlobalsGet) and handshakes the API version number with the server (SLGlobalInitNotif).

These are two RPC's performed before every other.  

    The first RPC receives one response with information related to message restrictions.
    Use this information when creating SLAF RPC message requests.  

    The second RPC mentioned also sets up an asynchronous stream of heartbeat notifications from the server.
    The first notification for this RPC would be the response to our version number message.
    This function takes the client major, minor and sub version numbers and sends them to the Service Layer service to get a handshake on the API version number.
