# Cpp Quick Tutorial

## Table of Contents
- [Server Setup](#server)
- [Running the tutorial](#quick)
- [Streaming vs Unary rpc implementation](#explain)
- [Generate gRPC Code](#gen)
- [Initialize the client server connection](#init)
- [Optional: Register the VRF](#vrf)

NOTE: If you only want to be able to run the code then you only need to follow the Server Setup and Running the tutorial sections.
#### <a name='server'></a>Server Setup

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

We also need to configure an any interface user wants to use for ipv4 and ipv6 tests.
For our tests the interface is Bunder-Ether (as this is the default):
    configure
    interface Bunder-Ether 1
    no shut
    commit
    end

We also need to configure an Interface (Or any interface user wants to use) for mpls tests
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

Go into the bash shell provided by running this command in the root of your service-layer-objmodel:

    make slapi-bash

Set the server address and port number as environment variables with the
following example command (this is assuming you are in bash shell):

    $ export SERVER_IP=192.168.122.192
    $ export SERVER_PORT=57344

The above assumes that the IP address of the node is 192.168.122.192.

This completes all the setup needed to start writing some code! Hop into
your cpp interpreter and try out some of the commands to get familiar
with the API.

## <a name='quick'></a>Running the tutorial

The following basic tutorial will walk you through getting started with the Service Layer API. The program can be used to test 
either IPV4, IPV6, or MPLS vertical through the unary rpc. Currently PG is not supported. This may require some initial cpp and GRPC setup, which will be explained below. 
For now, if you already have passed this setup step, follow this example:

| Required Argument | Description |
| --- | --- |
| -u/--username                                | Username (Required argument) |
| -p/--password                                | Password (Required argument) |
| -a/--route_oper                              | Route Operation: Add, Update, Delete (Required argument) |
| -w/--vrf_reg_oper                            | VRF registration Operation: Register, Unregister, EOF. When Unregister, all existing pushed routes will be deleted and route pushing will not be performed. Remember to specific correct table_type when Unregistering (Required argument) |

##### Optional arguments you can set in environment:

| Environment Variable | Description |
| --- | --- |
| -h/--help                       | Help |
| -v/--slaf                       | Specify if you want to use slaf proto RPCs to program objects or not. If false, no other configuration possible and will only run 100k ipv4 routes (default true) |
| -t/--table_type                 | Specify whether to do ipv4, ipv6 or mpls operation, PG is currently not supported (default ipv4) |
| -s/--global_init                | Enable our Async Global Init RPC to handshake the API version number with the server (default false) |
| -b/--num_operations             | Configure the number of ipv4 routes or MPLS entires to be added to a batch (default 1024) |
| -c/--batch_size                 | Configure the number of ipv4 routes or ILM entires for MPLS to be added to a batch (default 1024) |
| -x/--stream_case                | Want to use the streaming rpc or unary rpc (default true) |
##### IPv4 Testing

| Argument | Description |
| --- | --- |
| -d/--first_prefix_ipv4          | Configure the starting address for this test for IPV4 (default "40.0.0.0") |
| -e/--prefix_len_ipv4            | Configure the prefix length for this test for IPV4 address (default 24) |
| -f/--next_hop_interface_ipv4    | Configure the next hop interface for IPV4 (default "Bundle-Ether1") |
| -g/--next_hop_ip_ipv4           | Configure the next hop ip address for IPV4 (default "14.1.1.10") |

##### IPv6 Testing

| Argument | Description |
| --- | --- |
| -i/--first_prefix_ipv6          | Configure the starting address for this test for IPV6 (default "2002:aa::0") |
| -j/--prefix_len_ipv6            | Configure the prefix length for this test for IPV6 address (default 64) |
| -k/--next_hop_interface_ipv6    | Configure the next hop interface for IPV6 (default "Bundle-Ether1") |
| -l/--next_hop_ip_ipv6           | Configure the next hop ip address for IPV6 (default "2002:ae::3") |

##### MPLS Testing

| Argument | Description |
| --- | --- |
| -m/--first_mpls_path_nhip       | Configure the starting address for this test for MPLS (default "11.0.0.1") |
| -n/--next_hop_interface_mpls    | Configure the next hop interface for MPLS (default "FourHundredGigE0/0/0/0") |
| -o/--start_label                | Configure the starting label for this test for MPLS (default 20000) |
| -q/--num_label                  | Configure the number of labels to be allocated for MPLS (default 1000) |
| -r/--num_paths                  | Configure the number of paths for MPLS labels (default 1) |


##### How to Build

If you have a docker environment, you can run "make cpp-tutorial" from the service-layer-objmodel
top level directory where you see a Dockerfile and a Makefile. This will take some time to build
the first time, but once it completes you can run "make slapi-bash" to drop into bash, like so:

Bash-Prompt:sl$ make cpp-tutorial
Bash-Prompt:sl$ make slapi-bash

Once in bash, navigate to the tutorial directory:

root@f6179b5127f5:/slapi# cd grpc/cpp/src/tutorial/rshuttle

##### How to Run in Docker container (external client workflow)

Set SERVER_IP and SERVER_PORT Before Running:
    $ export SERVER_IP=111.111.111.111
    $ export SERVER_PORT=11111

Default Example (This runs ipv4 1):
    $ ./servicelayermain -u username -p password -a Add -w Register

Version 1 Default Example (This runs ipv4 only):
    $ ./servicelayermain -u username -p password -v false -a Add -w Register

IPV4 Examples:
    Adding 500 routes through stream:
    $ ./servicelayermain -u username -p password --table_type ipv4 -a Add -w Register -b 500
    Delete 20 routes using unary rpc with batch size at 10. Assuming vrf registration is handled automatically:
    $ ./servicelayermain -u username -p password --table_type ipv4 -a Delete -w EOF --num_operations 20 --batch_size 10 --stream_case false
    Delete 50 routes with streaming rpc with batch size at 30:
    $ ./servicelayermain -u username -p password --table_type ipv4 -a Delete -w Register --num_operations 50 --batch_size 30 --next_hop_ip_ipv4 14.1.1.21

IPV6 Example:
    Adding two routes:
    $ ./servicelayermain -u username -p password --table_type ipv6 -a Add -w Register
    Deleting All Routes and Unregister Vrf:
    $ ./servicelayermain -u username -p password --table_type ipv6 -w Unregister

MPLS Example:
    Adding 1000 Labels with streaming rpc:
    $ ./servicelayermain -u username -p password -a Add -w Register --table_type mpls -q 1000 --start_label 12000
    $ ./servicelayermain -u username -p password -a Add -w Register --table_type mpls --num_label 1000 -o 12000 --batch_size 1024 (same as above example)
    Deleting 35 labels with unary rpc:
    $ ./servicelayermain -u username -p password -a Delete -w Register --table_type mpls --num_label 35 --start_label 12010 -c false

Example using auto register (see section [Optional: Register the VRF](#vrf) for information on auto-register):
    $ ./servicelayermain -u username -p password -a Add (Same as above examples, just omit -w option)

The following sections explain the details of the above example tutorial.
The rest of these section is extra information and not required to run the tutorial above.

#### <a name='explain'></a>Streaming rpc vs Unary rpc implementation

Using a unary rpc, the client sends a single request and blocks for response to the request.
When invoked without --stream option, this program uses unary RPC. It invokes the unary RPC as many times needed to program the data set. Please follow through code for more information.

The streaming rpc implementation is a bit more complex.
A bi-directional stream is used, in which both the client and server have two independent streams. Both the client and server can read and write messages in any order.
Therefore, this section will explain a high level overview of how this program utilizes the streaming rpc.

Note: For more information on the differences/details of rpcs, refer to https://grpc.io/docs/what-is-grpc/core-concepts/#rpc-life-cycle.

Our code utilizes multithreading and locking to handle bidirectional streaming. The general life cycle looks like this:

    Main thread takes information given by user and creates a database. Each entry in the database corresponds to the information for one route/label.
    Main thread starts the stream and spawns a request queue, a writer thread and reader thread. At this point all three threads will operate concurrently and somewhat in parallel.

    Main thread acquires the lock for the database, combs through it, and creates service_layer::SLAFMsg objects. These are essentially batched databases route objects. We will refer to them as SLAPI objects. Main thread releases the lock for the database at the end of every batch, and then will reacquire it when trying the next batch. At the end of every batch, main thread will acquire the lock for the request queue, and enqueue these SLAPI object into it, then unlock.  
    Once done with the database, main thread will wait for a signal from the reader thread, which indicates to the main thread that all responses are received. Then, main thread enqueues poison pill into the request queue, then awaits for reader and writer thread to finish.

    Writer thread's only job is to acquire lock for the request queue, wait for it to be non empty, then pop the SLAPI object from it, and send the SLAPI object through the stream. When the object popped from request queue is the poison pill, writer thread will stops the entire stream and exit.

    Reader thread awaits for a response from the server, tries to obtain the lock for the database, and updates each associated database entry with the response information. It unlocks after every response, so that the main thread also has access to database. After all responses are given, it indicates to main thread that it received all responses through the use of a shared variable.

    After all of this is done, we print out any errors in the database.

We chose this design to allow ease of use and good performance. This design allows reusability for user specific code. The user just needs to hook up their own db and handle a few cases related to database information.

#### <a name='gen'></a>Generate gRPC Code (optional in this example)

If you are not familiar with gRPC, we recommend you refer to gRPC's
documentation before beginning with our tutorial: [gRPC Docs](http://www.grpc.io/docs/)

All SL-API protobuf files can be found in grpc/protos/
In order to generate the gRPC client side code stubs in cpp, run the following command (you may have to adjust the path to the proto files and the output according to your requirements):  

**For convenience, these files are also committed in this repo under cd grpc/cpp/src/gencpp (so you can skip this step).**

    $ protoc -I ../protos --grpc_out=./src/gencpp --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ../protos/*.proto
    $ protoc -I ../protos --cpp_out=./src/gencpp ../protos/*.proto

This generates the code stubs that we will now utilize to create a client.
The files are recognizable from the ".pb" and  ".grpc.pb" that is appended to the name of the
proto files they were generated from (example: sl_route_ipv4.pb.cc).

#### <a name='init'></a>Initialize the client server connection

In order to follow this quick tutorial, it is best to open the files in `grpc/cpp/src/tutorial/rshuttle/`

    ServiceLayerMain.cpp        : The full tutorial example using version 2 (SLAF protos) (Includes version 1 example too but only default ipv4 route case exists for version 1)
    ServiceLayerAsyncInit.cpp   : Used to help setup the client-server connection
    ServiceLayerRoutev2.cpp     : Used to setup the Route Operations using version 2 (SLAF protos)

As shown in ServiceLayerMain.cpp, the first thing to do is to setup the GRPC channel:

    auto server_ip = getEnvVar("SERVER_IP");
    auto server_port = getEnvVar("SERVER_PORT");
    auto channel = grpc::CreateChannel(grpc_server, grpc::InsecureChannelCredentials());

##### Optional: GlobalInit RPC
This represents the --global_init_rpc:

Once connected, client can choose to handshake the API version number with the server. This is optional step, not mandatory
The same RPC call also sets up an asynchronous stream of notifications from the server. The first notification would be the response to our version number message i.e. SLInitMsg, as a SLGlobalNotif event with type SL_GLOBAL_EVENT_TYPE_VERSION. This can be done by calling:

    call.response_reader = stub_->AsyncSLGlobalInitNotif(&call.context, init_msg, &cq_, (void *)&call);

The above function takes the client major, minor and sub version numbers and sends them to the Service Layer service to get a handshake on the API version number. More on this below.

    # Create SLInitMsg to handshake the version number with the server.
    # The Server will allow/deny access based on the version number.
    # The same RPC is used to setup a notification channel for global
    # events coming from the server.
    #
    # # Set the client version number based on the current proto files' version
    service_layer::SLInitMsg init_msg;
    init_msg.set_majorver(service_layer::SL_MAJOR_VERSION);
    init_msg.set_minorver(service_layer::SL_MINOR_VERSION);
    init_msg.set_subver(service_layer::SL_SUB_VERSION);

    if (username.length() > 0) {
        asynchandler.call.context.AddMetadata("username", username);
    }
    if (password.length() > 0) {
        asynchandler.call.context.AddMetadata("password", password);
    }

    asynchandler.SendInitMsg(init_msg);

Typically when using the asynchronous API, we hold on to the 
"call" instance in order to get updates on the ongoing RPC.
In our case it isn't really necessary, since we operate within the
context of the same class

The above cpp definition also handles other events such as errors and heartbeats.
Notice that the AsyncNotifChannel definition above creates a GRPC stub.
This is typically created through:

    AsyncNotifChannel asynchandler(channel);

Since the above SendInitMsg function would never return, it is best to spawn it as a thread, and run it in the background. In cpp, we do so by calling a threading event:

    // Spawn reader thread that maintains our Notification Channel
    std::thread thread_ = std::thread(&AsyncNotifChannel::AsyncCompleteRpc, &asynchandler);

    // Loop while listening for completed responses.
    // Prints out the response from the server.
    void
    AsyncNotifChannel::AsyncCompleteRpc()
    {
        void* got_tag;
        bool ok = false;
        // Storage for the status of the RPC upon completion.
        grpc::Status status;

        // Lock the mutex before notifying using the conditional variable
        std::lock_guard<std::mutex> guard(channel_mutex);


        unsigned int timeout = 5;

        // Set timeout for API
        std::chrono::system_clock::time_point deadline =
            std::chrono::system_clock::now() + std::chrono::seconds(timeout);

        while (!tear_down) {
            auto nextStatus = cq_.AsyncNext(&got_tag, &ok, deadline);

            switch(nextStatus) {
            case grpc::CompletionQueue::GOT_EVENT:
                // Verify that the request was completed successfully. Note that "ok"
                // corresponds solely to the request for updates introduced by Finish().
                call.HandleResponse(ok, &cq_);
                break;
            case grpc::CompletionQueue::SHUTDOWN:
                VLOG(1) << "Shutdown event received for completion queue";
                channel_closed = true;
                // Notify the condition variable;
                channel_condVar.notify_one();
                tear_down = true;
                break;
            case grpc::CompletionQueue::TIMEOUT:
                continue;
                break;
            }
        }

        if(!channel_closed) {
            Cleanup();
        }
    }

#### <a name='vrf'></a>Optional: Register the VRF

Registering the vrf is optional. User can configure "grpc service-layer auto-register" to avoid this registration requirement, and with auto-register, client owns the responsibility for reconciliation. Therefore, auto registration is preferred.
If using auto registration then user should not use -w/--vrf_reg_oper cli option.

In general, before we can use a vertical function like the route APIs, we have to register on that vertical. The SLAF API allows the user to register based on a per VRF basis.

We provide an optional class and function that handles VRF registration, and unregistration:
run_slaf(SLAFVrf* af_vrf_handler, unsigned int addr_family)
