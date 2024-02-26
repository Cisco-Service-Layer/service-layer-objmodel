# Cpp Quick Tutorial

## Table of Contents
- [Server Setup](#server)\
- [Running the tutorial](#quick)
- [Generate gRPC Code](#gen)
- [Initialize the client server connection](#init)
- [Register the VRF](#vrf)
- [Add a Batch of Routes](#route)

NOTE: If you only want to be able to run the code then you only need to follow the Server Setup and Running the tutorial sections.
#### <a name='server'></a>Server Setup

On the server side, we need to configure GRPC and enable the service layer through the following CLI configuration:

    ! Configure GRPC
    configure
    grpc port 57344
    grpc address-family ipv4
    commit
    end

    ! Configure Service layer
    configure
    grpc service-layer
    commit
    end

We also need to configure a server IP address. To configure an IP address on the management interface, one can use dhcp as follows:

    ! Configure the Mgmt Interface
    configure
    interface MgmtEth 0/RP0/CPU0/0
    ipv4 address dhcp
    no shut
    commit
    end

We also need to configure a Bunder-Ether Interface for ipv4 and ipv6 tests:
    configure
    interface Bunder-Ether 1
    no shut
    commit
    end

We also need to configure a FourHundredGigE0/0/0/0 Interface for mpls tests:
    configure
    interface FourHundredGigE0/0/0/0
    mpls mtu 68
    commit
    end

To check the IP address assigned:

    show ip interface brief

On the client side, the very first thing we need to do is set the server IP address and gRPC port. 
You can check your port number by running the following CLI command on the IOS-XR 
server box (should be the same as the one configured):

    # show run grpc

Go into the bash shell provided by running this command in the ../service-
layer-objmodel path:

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
either IPV4, IPV6, or MPLS vertical. This may require some initial cpp and GRPC setup, which will be explained below. 
For now, if you already have passed this setup step, follow this example:

| Required Argument | Description |
| --- | --- |
| -u                                | Username |
| -p                                | Password |

##### Optional arguments you can set in environment:

| Environment Variable | Description |
| --- | --- |
| export table_type                 | Specify whether to do ipv4(value = 0), ipv6(value = 1) or mpls(value = 2) operation (default 0) |
| export batch_size                 | Configure the number of ipv4 routes or ILM entires for MPLS to be added to a batch (default 1024) |
| export batch_num                  | Configure the number of batches (default 98) |

##### IPv4 Testing

| Argument | Description |
| --- | --- |
| export first_prefix_ipv4          | Configure the starting address for this test for IPV4 (default "40.0.0.0") |
| export prefix_len_ipv4            | Configure the prefix length for this test for IPV4 address (default 24) |
| export next_hop_interface_ipv4    | Configure the next hop interface for IPV4 (default "Bundle-Ether1") |
| export next_hop_ip_ipv4           | Configure the next hop ip address for IPV4 (default "14.1.1.10") |

##### IPv6 Testing

| Argument | Description |
| --- | --- |
| export first_prefix_ipv6          | Configure the starting address for this test for IPV6 (default "2002:aa::0") |
| export prefix_len_ipv6            | Configure the prefix length for this test for IPV6 address (default 64) |
| export next_hop_interface_ipv6    | Configure the next hop interface for IPV6 (default "Bundle-Ether1") |
| export next_hop_ip_ipv6           | Configure the next hop ip address for IPV6 (default "2002:ae::3") |

##### MPLS Testing

| Argument | Description |
| --- | --- |
| export first_prefix_mpls          | Configure the starting address for this test for MPLS (default "11.0.0.1") |
| export next_hop_interface_mpls    | Configure the next hop interface for MPLS (default "FourHundredGigE0/0/0/0") |
| export start_label                | Configure the starting label for this test for MPLS (default 20000) |
| export num_label                  | Configure the number of labels to be allocated for MPLS (default 1000) |
| export num_paths                  | Configure the number of paths for MPLS labels (default 1) |


##### How to Build

If you have a docker environment, you can run "make cpp-tutorial" from the service-layer-objmodel
top level directory where you see a Dockerfile and a Makefile. This will take some time
the first time but once it completes it should drop you into bash, like so:

Bash-Prompt:sl$ make cpp-tutorial

Once in bash, navigate to the tutorial directory:

root@f6179b5127f5:/slapi# cd grpc/cpp/src/tutorial/rshuttle

#### How to Run in container (normal)

Default Example (This runs ipv4):
    $ ./servicelayermain -u cisco -p cisco123

IPV4 Example:
    $ export route_op=0
    $ ./servicelayermain -u cisco -p cisco123

IPV6 Example:
    $ export route_op=1
    $ ./servicelayermain -u cisco -p cisco123

MPLS Example:
    $ export route_op=2
    $ export start_label=12000
    $ ./servicelayermain -u cisco -p cisco123


#### How to Run if using Sandbox on Server

Once you follow the How to Build section, you need to exit the container:

root@f6179b5127f5:/slapi# exit

Navigate to rshuttle directory:

Bash-Prompt:sl$ cd grpc/cpp/src/tutorial/rshuttle

From here you need to run the create_giso.sh script into to create a giso image. Each argument requires full path.
Example:

Bash-Prompt:sl$ ./create_giso.sh -p /nobackup/habassi/rpmtest/
 -b /nobackup/habassi/service-layer-objmodel/grpc/cpp/src/tutorial/rshuttle/servicelayermain -v 1.0.0
 -n servicelayermain -x 1 -i /auto/prod_weekly_archive2/bin/24.2.1.21I.DT_IMAGE/8000/8000-x64-24.2.1.21I.iso 
 -s /auto/prod_weekly_archive2/bin/24.2.1.21I.DT_IMAGE/8000/optional-rpms/sandbox/

This will create a folder output_gisobuild/giso which contains the giso image. You need to get it onto your server and store it under /misc/disk1:

Example:
EX: scp -P PORT_NUMBER 8000-golden-x86_64-24.2.1.21I-sandbox.iso USERNAME@IP_ADDRESS:/misc/disk1/

You now need to log-on to the server. Once there you will need to perform install replace. 
Replace usually takes a couple of minutes to finish. To check of the status, use 'show install log' command. 
Then Sandbox and a local-connection needs to be enabled. Before committing, test if sandbox is ready. 
You can do this with 'bash sandbox'. Then you need to install commit. Commit takes about a minute. 
Use 'show install log' to see when the commit is done. After that a reload needs to be performed.

Example:

    ! Replacing with your giso image
    install replace /misc/disk1/8000-golden-x86_64-24.2.1.21I-sandbox.iso

    ! Configure Sandbox
    configure
    sandbox
    enable
    commit
    end

    ! Configure GRPC local-connection
    configure
    grpc
    local-conection
    commit
    end

    ! Commit and Perform reload
    install commit
    reload

Once the reload is finished you can check if your rpms are installed on the server

Example:

    show sandbox rpms install
LIST OF INSTALLED RPMs
----------------------------------------------------------------------------------
1  servicelayermain.x86_64                 1.0.0-1.el8                             
----------------------------------------------------------------------------------

Note: If you do not see your rpm's installed here when running the "show sandbox rpms install" 
then you might need to do the install replace, commit and reload again.

Now to get into run sandbox on server:
    bash sandbox

You need to specify the variables SERVER_IP and SERVER_PORT on Sandbox. 
We are using unix sockets here so you and that is what the local-connection was for. 
Set SERVER_IP=unix and SERVER_PORT=/ems/grpc.sock:

    [root@ios /]# export SERVER_IP=unix
    [root@ios /]# export SERVER_PORT=/ems/grpc.sock

All that is left is to run the application:
Default Example (This runs ipv4):
    $ ./servicelayermain

Note: you don't need to give username or password since grpc is established to unix sockets, unlike running in container


The following sections explain the details of the above example tutorial and are similar to the Python quick start tutorial.
The rest of these section is extra information and not required to run the tutorial above.

#### <a name='gen'></a>Generate gRPC Code (optional in this example)

If you are not familiar with gRPC, we recommend you refer to gRPC's
documentation before beginning with our tutorial: [gRPC Docs](http://www.grpc.io/docs/)

You should have received all of the Protobuf files required to run the Cisco
Service Laye API. In order to generate the gRPC client side code stubs in cpp, run the following command (you may have to adjust the path to the proto files and the output according to your requirements):  

**For convenience, these files are also committed in this repo under cd grpc/cpp/src/gencpp (so you can skip this step).**

    $ protoc -I ../protos --grpc_out=./src/gencpp --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ../protos/*.proto
    $ protoc -I ../protos --cpp_out=./src/gencpp ../protos/*.proto

This generates the code stubs that we will now utilize to create a client.
The files are recognizable from the ".pb" and  ".grpc.pb" that is appended to the name of the
proto files they were generated from (example: sl_route_ipv4.pb.cc).

#### <a name='init'></a>Initialize the client server connection

In order to follow this quick tutorial, it is best to open the files in `grpc/cpp/src/tutorial/rshuttle/`

    ServiceLayerMain.cpp        : The full tutorial example using version 2 (SLAF protos)
    ServiceLayerAsyncInit.cpp   : Used to help setup the client-server connection
    ServiceLayerRoutev2.cpp     : Used to setup the Route Operations using version 2 (SLAF protos)

As shown in ServiceLayerMain.cpp, the first thing to do is to setup the GRPC channel:

    auto server_ip = getEnvVar("SERVER_IP");
    auto server_port = getEnvVar("SERVER_PORT");
    auto channel = grpc::CreateChannel(
                              grpc_server, grpc::InsecureChannelCredentials());

Once connected, we need to handshake the API version number with the server.
The same RPC call also sets up an asynchronous stream of notifications from the server. The first notification would be the response to our version number message i.e. SLInitMsg, as a SLGlobalNotif event with type SL_GLOBAL_EVENT_TYPE_VERSION. This can be done by calling:

    call.response_reader = stub_->AsyncSLGlobalInitNotif(&call.context, init_msg, &cq_, (void *)&call);

The above function takes the client major, minor and sub version numbers and sends them to the Service Layer service to get a handshake on the API version number. More on this below.

The following code snippets are copied from file ServiceLayerMain.cpp and ServiceLayerAsyncInit.cpp

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

#### <a name='vrf'></a>Register the VRF

In general, before we can use a vertical function like the route APIs, we have to register on that vertical. The SLAF API allows the user to register based on a per VRF basis.
So, before any additions or modification of routes can be made we need to register with the proper VRF, which requires sending a VRF registration message and then an EOF message to clean up any stale routes that may be there from an older configuration (this will become handy on restart or recovery scenarios).

The following snippets are copied from file ServiceLayerMain.cpp

Time to fill in some variables! We first create a vrf handler which has appropriate functions
for creating necessary objects.

    auto af_vrf_handler = SLAFVrf(channel,username,password);

The next steps are a rundown of what the runv2 and supporting functions called in
runv2 do.

    // Need to specify ipv4 (default), ipv6(value = 1) or mpls(value = 2)
    if (env_data.route_op == 1) {
        route_operation = AF_INET6;
    } else if (env_data.route_op == 2) {
        route_operation = AF_MPLS;
    } else {
        route_operation = AF_INET;
    }
    run_v2(&af_vrf_handler,route_operation);

The following snippets are copied from file ServiceLayerRoutev2.cpp

Create the `SLAFVrfReg` object. Generating a `SLAFVrfReg` object allows us to
access and set it's variables. The `SLAFVrfReg` object requires it's table to be set
indicating which route operations are to be performed. Ipv4, Ipv6 or mpls.

    #include <iosxrsl/sl_af.grpc.pb.h>
    #include <iosxrsl/sl_af.pb.h>
    service_layer::SLAFVrfReg* af_vrf_reg = af_vrf_msg.add_vrfregmsgs();
    af_vrf_reg->set_table(service_layer::SL_IPv4_ROUTE_TABLE);

The VRF registration message contains a set of VRF registration objects.

Create an `SLVrfReg` object.

    service_layer::SLVrfReg* vrf_reg = af_vrf_reg->mutable_vrfreg();

Set the VRF registration object attributes:

VRF name. The default VRF in IOS-XR is called "default":

    vrf_reg->set_vrfname(vrfName);

Administrative distance. The admin distance is used by RIB to make best path decisions.

    vrf_reg->set_admindistance(adminDistance);

VRF purge interval. This is useful on restart scenarios.

    vrf_reg->set_vrfpurgeintervalseconds(vrfPurgeIntervalSeconds);

Next up, create the stub instance using the channel. This stub will
have the exact same methods that are available on the server. To do this,
we need to import the stub code generated from our ProtoBuf files. Depending on
what calls you want to make, different stubs will be used. We are going to be
making changes to our IPv4 routes, but for all routes we use the SLAF stub.

    #include <iosxrsl/sl_af.grpc.pb.h>
    #include <iosxrsl/sl_af.pb.h>
    auto stub_ = service_layer::SLAF::NewStub(channel);

Make the RPC call.

We are ready to make our call to the API. We'll send the
`SLAFVrfRegMsg af_vrf_msg` and a timeout interval (in seconds) and any other context information for the gRPC
server.

    grpc::ClientContext context;
    unsigned int timeout = 10;
        // Set timeout for API
    std::chrono::system_clock::time_point deadline =
        std::chrono::system_clock::now() + std::chrono::seconds(timeout);

    context.set_deadline(deadline);
    if (username.length() > 0) {
        context.AddMetadata("username", username);
    }
    if (password.length() > 0) {
        context.AddMetadata("password", password);
    }

    // Set up afVrfRegMsg Operation
    af_vrf_msg.set_oper(vrfOp);
    if (google::protobuf::TextFormat::PrintToString(af_vrf_msg, &s)) {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Transmitted message: IOSXR-SL VRF " << s;
        VLOG(2) << "###########################" ;
    } else {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Message not valid (partial content: "
                << af_vrf_msg.ShortDebugString() << ")";
        VLOG(2) << "###########################" ;
        return false;
    }


    //Issue the RPC

    status = stub_->SLAFVrfRegOp(&context, af_vrf_msg, &af_vrf_msg_resp);

Note that the af_vrf_msg has an Oper field that determines the operation type:

    SL_REGOP_REGISTER  : used for registrations
    SL_REGOP_EOF       : used for EOF signaling. Useful for restart scenarios
    SL_REGOP_UNREGISTER: used to unregister, which would clean all previous roues added in that VRF.

Finally, we can print our response from the server. Notice that, since we can add a batch of VRF registrations, we want to print a result code for each individual response.
To do this, we check if the response is an error, and if it is we print the
name of the vrf that caused the error as well as the hexadecimal error
code.

    if (af_vrf_msg_resp.statussummary().status() ==
        service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {

        VLOG(1) << "Vrf Operation:"<< vrfOp << " Successful";
        return true;
    } else {
        LOG(ERROR) << "Error code for VRF Operation:" 
                    << vrfOp 
                    << " is 0x" << std::hex 
                    << af_vrf_msg_resp.statussummary().status();

        // Print Partial failures within the batch if applicable
        if (af_vrf_msg_resp.statussummary().status() ==
                service_layer::SLErrorStatus_SLErrno_SL_SOME_ERR) {
            for (int result = 0; result < af_vrf_msg_resp.results_size(); result++) {
                    auto slerr_status = 
                    static_cast<int>(af_vrf_msg_resp.results(result).errstatus().status());
                    LOG(ERROR) << "Error code for vrf " 
                                << af_vrf_msg_resp.results(result).vrfname() 
                                << " is 0x" << std::hex 
                                << slerr_status;
            }
        }
        return false;
    }

#### <a name='route'></a>Add a Batch of Routes

Now that we have registered the VRF, we can start adding routes. We will show
adding a batch of 100k routes to the RIB.

In our implementation you can call this function and provide the batch size and number of batches
to indicate how many routes you want to push. We also create a RShuttlev2 struct
which simplifies the setting of route attributes. The route_operation is used
to specify ipv4, ipv6 or mpls operation

The following code snippets are copied from file ServiceLayerMain.cpp

    route_shuttlev2 = new RShuttlev2(af_vrf_handler.channel, username, password);
    routepushv2(route_shuttlev2, batch_size, batch_num,route_operation);

This creates a `SLAFMsg` message.

Fill in the route attributes.

VRF Name

    route_shuttlev2->setVrfV4("default");

What this actually does is this:

    route_msg.set_vrfname(vrfName);

Add a loop that will add 100k incrementing routes to the RIB table since batchSize passed is 1024
and batchNum is 98.

    for (int batchindex = 0; batchindex < batchNum; batchindex++) {
            for (int routeindex = 0; routeindex < batchSize; routeindex++, prefix=incrementIpv4Pfx(prefix,prefix_len)) {
            }
        }

We use a helper function called insertAddBatchv4 to set all attributes for the `SLAFMsg` Object:

    route_shuttlev2->insertAddBatchV4(route_shuttlev2->longToIpv4(prefix), prefix_len, 99, "14.1.1.10", "Bundle-Ether1");

The following code snippets are copied from file ServiceLayerRoutev2.cpp
We will be following insertAddBatchV4 and helper functions, but only show the setting of the `SLAFMsg` attributes

Obtain pointer to a new route object within route batch, by creating a `SLAFOp` , `SLAFObject` ,and `SLRoutev4` object.

    service_layer::SLAFOp* operation = route_msg.add_oplist();
    service_layer::SLAFObject* af_object = operation->mutable_afobject();
    service_layer::SLRoutev4* routev4Ptr = af_object->mutable_ipv4route();
    return routev4Ptr;

IP address we already passed in above, but we must set it now
along with the Prefix Length

    routev4Ptr->set_prefix(prefix);
    routev4Ptr->set_prefixlen(prefixLen);

Administrative distance (this can override the VRF registration admin distance)

    routev4Ptr->mutable_routecommon()->set_admindistance(adminDistance);

Set the route's paths.

A route may have one or many paths.
Create an `SLRoutePath` object.

    auto routev4PathPtr = routev4Ptr->add_pathlist();

Path next hop address

    routev4PathPtr->mutable_nexthopaddress()->set_v4address(nextHopAddress);

Next hop interface name

    routev4PathPtr->mutable_nexthopinterface()->set_name(nextHopIf);

We have finished the for loop and now need to make the RPC call. We do this with
routev4Op() function called in routepushv2 in ServiceLayerMain.cpp

    route_shuttlev2->routev4Op(service_layer::SL_OBJOP_UPDATE);

The following code snippets are copied from function route_shuttlev2->routev4Op from file ServiceLayerRoutev2.cpp
similar to when we register the vrf message in earlier steps

    route_op = routeOp;
    route_msg.set_oper(route_op); // Desired ADD, UPDATE, DELETE operation
    auto stub_ = service_layer::SLAF::NewStub(channel);

Again, there are other route calls beyond just adding bulk routes.

    # RPC route operations
    #    for add: service_layer::SL_OBJOP_ADD
    #    for update: service_layer::SL_OBJOP_UPDATE
    #    for delete: service_layer::SL_OBJOP_DELETE
    routev4Op(service_layer::SLObjectOp routeOp,
                    unsigned int timeout)

These calls show examples of bulk additions, updates, and deletes. Also Updates handle
add operations as well

We are ready to make our call to the API. We'll send then `SLAFMsg route_msg` and a
timeout interval (in seconds) and any other context information for the gRPC server.

    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    grpc::ClientContext context;

    // Storage for the status of the RPC upon completion.
    grpc::Status status;

    // Set timeout for RPC
    std::chrono::system_clock::time_point deadline =
        std::chrono::system_clock::now() + std::chrono::seconds(timeout);

    context.set_deadline(deadline);
    if (username.length() > 0) {
        context.AddMetadata("username", username);
    }
    if (password.length() > 0) {
        context.AddMetadata("password", password);
    }

    //Issue the RPC
    std::string s;

    if (google::protobuf::TextFormat::PrintToString(route_msg, &s)) {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Transmitted message: IOSXR-SL Routev4 " << s;
        VLOG(2) << "###########################" ;
    } else {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Message not valid (partial content: "
                  << route_msg.ShortDebugString() << ")";
        VLOG(2) << "###########################" ;
        return false;
    }

    status = stub_->SLAFOp(&context, route_msg, &route_msg_resp);

Check the server's response. Here again we can check each individual route that
was added for an error message.

    for (int result = 0; result < route_msg_resp.results_size(); result++) {
                auto slerr_status = 
                static_cast<int>(route_msg_resp.results(result).errstatus().status());
                if(slerr_status != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS){
                    LOG(ERROR) << "Error code for prefix: " 
                            << route_msg_resp.results(result).operation().afobject().ipv4route().prefix()
                            << " prefixlen: " 
                            << route_msg_resp.results(result).operation().afobject().ipv4route().prefixlen()
                            <<" is 0x"<< std::hex << slerr_status;
                    ipv4_error = true;
                }
        }

That's all for now! Remember some key takeaways:

1. The VRF must be registered before adding, updating, or removing routes 
from the RIB.

2. All API operations are CRUD based (Create, Read, Update, Delete), and the initial setup of all calls to the same object will be (about) the same. 
Note that in our implementation no delete is required. As soon as a signal interrupt is given, we delete anything we created or updated by sending a delete request to the server.
