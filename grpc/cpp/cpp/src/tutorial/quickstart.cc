#include "quickstart.h"
#include <arpa/inet.h>
#include <google/protobuf/text_format.h>
#include <csignal>

using grpc::ClientContext;
using grpc::ClientReader;
using grpc::ClientReaderWriter;
using grpc::ClientWriter;
using grpc::CompletionQueue;
using grpc::Status;
using service_layer::SLInitMsg;
using service_layer::SLVersion;
using service_layer::SLGlobal;


std::mutex init_mutex;
std::condition_variable init_condVar;
bool init_success;


RShuttle::RShuttle(std::shared_ptr<grpc::Channel> Channel)
    : channel(Channel) {} 


uint32_t RShuttle::IPv4ToLong(const char* address)
{   
    struct sockaddr_in sa; 
    if (inet_pton(AF_INET, address, &(sa.sin_addr)) != 1) {
        std::cerr << "Invalid IPv4 address " << address << std::endl;
        return 0;
    }
    
    return ntohl(sa.sin_addr.s_addr);
}

std::string RShuttle::IPv6ToByteArrayString(const char* address)
{   
    //const char *ipv6str = address;
    struct in6_addr ipv6data;
    if (inet_pton(AF_INET6, address, &ipv6data) != 1 ) {
        std::cerr << "Invalid IPv6 address " << address << std::endl;
        return 0;
    }

    const char *ptr(reinterpret_cast<const char*>(&ipv6data.s6_addr));
    std::string ipv6_charstr(ptr, ptr+16);
    return ipv6_charstr;
}


service_layer::SLRoutev4* 
    RShuttle::routev4Add(std::string vrfName)
{
    routev4_msg.set_vrfname(vrfName);
    return routev4_msg.add_routes();
}


void RShuttle::routev4Set(service_layer::SLRoutev4* routev4Ptr,
                          uint32_t prefix,
                          uint32_t prefixLen,
                          uint32_t adminDistance)
{
    routev4Ptr->set_prefix(prefix);
    routev4Ptr->set_prefixlen(prefixLen);
    routev4Ptr->mutable_routecommon()->set_admindistance(adminDistance);
}

void RShuttle::routev4PathAdd(service_layer::SLRoutev4* routev4Ptr,
                              uint32_t nextHopAddress,
                              std::string nextHopIf)
{
    
    auto routev4PathPtr = routev4Ptr->add_pathlist();
    routev4PathPtr->mutable_nexthopaddress()->set_v4address(nextHopAddress);
    routev4PathPtr->mutable_nexthopinterface()->set_name(nextHopIf);
}

void RShuttle::routev4Op(service_layer::SLObjectOp routeOp,
                         unsigned int timeout)
{

    // Convert ADD to UPDATE automatically, it will solve both the 
    // conditions - add or update.

    if (routeOp == service_layer::SL_OBJOP_ADD) {
        routeOp = service_layer::SL_OBJOP_UPDATE;
    }

    route_op = routeOp;
    routev4_msg.set_oper(route_op);

    auto stub_ = service_layer::SLRoutev4Oper::NewStub(channel); 

    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    grpc::ClientContext context;

    // Storage for the status of the RPC upon completion.
    grpc::Status status;

    // Set timeout for RPC
    std::chrono::system_clock::time_point deadline =
        std::chrono::system_clock::now() + std::chrono::seconds(timeout);

    context.set_deadline(deadline);

    //Issue the RPC         
    std::string s;

    if (google::protobuf::TextFormat::PrintToString(routev4_msg, &s)) {
        std::cout << "\n\n###########################\n" ;
        std::cout << "Transmitted message: IOSXR-SL RouteV4 " << s;
        std::cout << "###########################\n\n\n" ;
    } else {
        std::cerr << "\n\n###########################\n" ;
        std::cerr << "Message not valid (partial content: "
                  << routev4_msg.ShortDebugString() << ")\n";
        std::cerr << "###########################\n\n\n" ;
    }

    status = stub_->SLRoutev4Op(&context, routev4_msg, &routev4_msg_resp);

    if (status.ok()) {
        std::cout << "RPC call was successful, checking response..." << std::endl;


        if (routev4_msg_resp.statussummary().status() ==
               service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {

            std::cout << "IPv4 Route Operation:"<< route_op << " Successful" << std::endl;
        } else {
            std::cerr << "Error code for IPv4 Route Operation:" << route_op << " is 0x" << std::hex << routev4_msg_resp.statussummary().status() << std::endl;

            // Print Partial failures within the batch if applicable
            if (routev4_msg_resp.statussummary().status() ==
                    service_layer::SLErrorStatus_SLErrno_SL_SOME_ERR) {
                for (int result = 0; result < routev4_msg_resp.results_size(); result++) {
                      auto slerr_status = static_cast<int>(routev4_msg_resp.results(result).errstatus().status());
                      std::cerr << "Error code for prefix: " << routev4_msg_resp.results(result).prefix() << " prefixlen: " << routev4_msg_resp.results(result).prefixlen()<<" is 0x"<< std::hex << slerr_status << std::endl;
                }
            }
        }
    } else {
        std::cerr << "RPC failed, error code is " << status.error_code() << std::endl;
    }
}



service_layer::SLRoutev6*
    RShuttle::routev6Add(std::string vrfName)
{
    routev6_msg.set_vrfname(vrfName);
    return routev6_msg.add_routes();
}


void RShuttle::routev6Set(service_layer::SLRoutev6* routev6Ptr,
                          std::string prefix,
                          uint32_t prefixLen,
                          uint32_t adminDistance)
{
    routev6Ptr->set_prefix(prefix);
    routev6Ptr->set_prefixlen(prefixLen);
    routev6Ptr->mutable_routecommon()->set_admindistance(adminDistance);
}

void RShuttle::routev6PathAdd(service_layer::SLRoutev6* routev6Ptr,
                              std::string nextHopAddress,
                              std::string nextHopIf)
{

    auto routev6PathPtr = routev6Ptr->add_pathlist();
    routev6PathPtr->mutable_nexthopaddress()->set_v6address(nextHopAddress);
    routev6PathPtr->mutable_nexthopinterface()->set_name(nextHopIf);
}

void RShuttle::routev6Op(service_layer::SLObjectOp routeOp,
                         unsigned int timeout)
{                      

    // Convert ADD to UPDATE automatically, it will solve both the 
    // conditions - add or update.
    
    if (routeOp == service_layer::SL_OBJOP_ADD) {
        routeOp = service_layer::SL_OBJOP_UPDATE;
    }
    
    route_op = routeOp;
    routev6_msg.set_oper(route_op);


    auto stub_ = service_layer::SLRoutev6Oper::NewStub(channel);

    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    grpc::ClientContext context;

    // Storage for the status of the RPC upon completion.
    grpc::Status status;

    // Set timeout for RPC
    std::chrono::system_clock::time_point deadline =
        std::chrono::system_clock::now() + std::chrono::seconds(timeout);

    context.set_deadline(deadline);


    //Issue the RPC         
    std::string s;

    if (google::protobuf::TextFormat::PrintToString(routev6_msg, &s)) {
        std::cout << "\n\n###########################\n" ;
        std::cout << "Transmitted message: IOSXR-SL RouteV6 " << s;
        std::cout << "###########################\n\n\n" ;
    } else {
        std::cerr << "\n\n###########################\n" ;
        std::cerr << "Message not valid (partial content: "
                  << routev6_msg.ShortDebugString() << ")\n";
        std::cerr << "###########################\n\n\n" ;
    }

    //Issue the RPC         

    status = stub_->SLRoutev6Op(&context, routev6_msg, &routev6_msg_resp);

    if (status.ok()) {
        std::cout << "RPC call was successful, checking response..." << std::endl;


        if (routev6_msg_resp.statussummary().status() ==
               service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {

            std::cout << "IPv6 Route Operation:"<< route_op << " Successful" << std::endl;
        } else {
            std::cerr << "Error code for IPv6 Route Operation:" << route_op << " is 0x" << std::hex << routev6_msg_resp.statussummary().status() << std::endl;

            // Print Partial failures within the batch if applicable
            if (routev6_msg_resp.statussummary().status() ==
                    service_layer::SLErrorStatus_SLErrno_SL_SOME_ERR) {
                for (int result = 0; result < routev6_msg_resp.results_size(); result++) {
                      auto slerr_status = static_cast<int>(routev6_msg_resp.results(result).errstatus().status());
                      std::cerr << "Error code for prefix: " << routev6_msg_resp.results(result).prefix() << " prefixlen: " << routev6_msg_resp.results(result).prefixlen()<<" is 0x"<< std::hex << slerr_status << std::endl;

                }
            }
        }
    } else {
        std::cerr << "RPC failed, error code is " << status.error_code() << std::endl;
    }
}




SLVrf::SLVrf(std::shared_ptr<grpc::Channel> Channel)
    : channel(Channel) {}

// Overloaded variant of vrfRegMsgAdd without adminDistance and Purgeinterval
// Suitable for VRF UNREGISTER and REGISTER operations

void SLVrf::vrfRegMsgAdd(std::string vrfName) {

    // Get a pointer to a new vrf_reg entry in vrf_msg
    service_layer::SLVrfReg* vrf_reg = vrf_msg.add_vrfregmsgs();

    // Populate the new vrf_reg entry
    vrf_reg->set_vrfname(vrfName);
}

// Overloaded variant of vrfRegMsgAdd with adminDistance and Purgeinterval
// Suitable for VRF REGISTER

void SLVrf::vrfRegMsgAdd(std::string vrfName,
                         unsigned int adminDistance,
                         unsigned int vrfPurgeIntervalSeconds) {

    // Get a pointer to a new vrf_reg entry in vrf_msg
    service_layer::SLVrfReg* vrf_reg = vrf_msg.add_vrfregmsgs();

    // Populate the new vrf_reg entry
    vrf_reg->set_vrfname(vrfName);
    vrf_reg->set_admindistance(adminDistance);
    vrf_reg->set_vrfpurgeintervalseconds(vrfPurgeIntervalSeconds);
}


void SLVrf::registerVrf(unsigned int addrFamily) {

    // Send an RPC for VRF registrations

    switch(addrFamily) {
    case AF_INET:
        vrf_op = service_layer::SL_REGOP_REGISTER;
        vrfOpv4();

        // RPC EOF to cleanup any previous stale routes
        vrf_op = service_layer::SL_REGOP_EOF;
        vrfOpv4();

        break;

    case AF_INET6:
        vrf_op = service_layer::SL_REGOP_REGISTER;
        vrfOpv6();

        // RPC EOF to cleanup any previous stale routes
        vrf_op = service_layer::SL_REGOP_EOF;
        vrfOpv6();

        break;            

    default:
        std::cout << "Invalid Address family, skipping.." << std::endl;
        break;
    }

}

void SLVrf::unregisterVrf(unsigned int addrFamily) {

    //  When done with the VRFs, RPC Delete Registration

    switch(addrFamily) {
    case AF_INET:
        std::cout << "IPv4 VRF Operation" << std::endl;

        vrf_op = service_layer::SL_REGOP_UNREGISTER;
        vrfOpv4();
            
        break;

    case AF_INET6:
        std::cout << "IPv6 VRF Operation" << std::endl;
        
        vrf_op = service_layer::SL_REGOP_UNREGISTER;
        vrfOpv6();
        
        break;

    default:
        std::cout << "Invalid Address family, skipping.." << std::endl;
        break;
    }
}

void SLVrf::vrfOpv4() {
    // Set up the RouteV4Oper Stub
    auto stub_ = service_layer::SLRoutev4Oper::NewStub(channel);

    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    grpc::ClientContext context;

    // Storage for the status of the RPC upon completion.
    grpc::Status status;        

    unsigned int timeout = 10;
        // Set timeout for API
    std::chrono::system_clock::time_point deadline =
        std::chrono::system_clock::now() + std::chrono::seconds(timeout);

    context.set_deadline(deadline);

    // Set up vrfRegMsg Operation

    vrf_msg.set_oper(vrf_op);

    std::string s;

    if (google::protobuf::TextFormat::PrintToString(vrf_msg, &s)) {
        std::cout << "\n\n###########################\n" ;
        std::cout << "Transmitted message: IOSXR-SL VRF " << s;
        std::cout << "###########################\n\n\n" ;
    } else {
        std::cerr << "\n\n###########################\n" ;
        std::cerr << "Message not valid (partial content: "
                  << vrf_msg.ShortDebugString() << ")\n";
        std::cerr << "###########################\n\n\n" ;
    }


    //Issue the RPC         

    status = stub_->SLRoutev4VrfRegOp(&context, vrf_msg, &vrf_msg_resp);

    if (status.ok()) {
        std::cout << "RPC call was successful, checking response..." << std::endl;


        if (vrf_msg_resp.statussummary().status() ==
               service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {

            std::cout << "IPv4 Vrf Operation:"<< vrf_op << " Successful" << std::endl;
        } else {
            std::cerr << "Error code for VRF Operation:" << vrf_op << " is 0x" << std::hex << vrf_msg_resp.statussummary().status() << std::endl;

            // Print Partial failures within the batch if applicable
            if (vrf_msg_resp.statussummary().status() ==
                    service_layer::SLErrorStatus_SLErrno_SL_SOME_ERR) {
                for (int result = 0; result < vrf_msg_resp.results_size(); result++) {
                      auto slerr_status = static_cast<int>(vrf_msg_resp.results(result).errstatus().status());
                      std::cerr << "Error code for vrf " << vrf_msg_resp.results(result).vrfname() << " is 0x" << std::hex << slerr_status << std::endl;
                }
            } 
        }
    } else {
        std::cerr << "RPC failed, error code is " << status.error_code() << std::endl;
    }
}
                    
void SLVrf::vrfOpv6() {

    // Set up the RouteV4Oper Stub
    auto stub_ = service_layer::SLRoutev6Oper::NewStub(channel);


    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    grpc::ClientContext context;
    
    // Storage for the status of the RPC upon completion.
    grpc::Status status;
    
    unsigned int timeout = 10;
    // Set timeout for API
    std::chrono::system_clock::time_point deadline =
        std::chrono::system_clock::now() + std::chrono::seconds(timeout);
     
    context.set_deadline(deadline);

    // Set up vrfRegMsg Operation

    vrf_msg.set_oper(vrf_op);

    std::string s;

    if (google::protobuf::TextFormat::PrintToString(vrf_msg, &s)) {
        std::cout << "\n\n###########################\n" ;
        std::cout << "Transmitted message: IOSXR-SL VRF " << s;
        std::cout << "###########################\n\n\n" ;
    } else {
        std::cerr << "\n\n###########################\n" ;
        std::cerr << "Message not valid (partial content: "
                  << vrf_msg.ShortDebugString() << ")\n";
        std::cerr << "###########################\n\n\n" ;
    }


    //Issue the RPC         

    status = stub_->SLRoutev6VrfRegOp(&context, vrf_msg, &vrf_msg_resp);

    if (status.ok()) {
        std::cout << "RPC call was successful, checking response..." << std::endl;
        if (vrf_msg_resp.statussummary().status() ==
               service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
            std::cout << "IPv6 Vrf Operation: "<< vrf_op << " successful" << std::endl;
        } else {
            std::cerr << "Error code for VRF Operation:" << vrf_op << " is 0x" << std::hex << vrf_msg_resp.statussummary().status() << std::endl;

            // Print Partial failures within the batch if applicable
            if (vrf_msg_resp.statussummary().status() ==
                    service_layer::SLErrorStatus_SLErrno_SL_SOME_ERR) {
                for (int result = 0; result < vrf_msg_resp.results_size(); result++) {
                    auto slerr_status = static_cast<int>(vrf_msg_resp.results(result).errstatus().status());
                    std::cerr << "Error code for vrf " << vrf_msg_resp.results(result).vrfname() << " is 0x" << std::hex << slerr_status << std::endl;
                }
            }
        }
    } else {
        std::cerr << "RPC failed, error code is " << status.error_code() << std::endl;
    }

}
 
AsyncNotifChannel::AsyncNotifChannel(std::shared_ptr<grpc::Channel> channel)
        : stub_(service_layer::SLGlobal::NewStub(channel)) {}


// Assembles the client's payload and sends it to the server.

void AsyncNotifChannel::SendInitMsg(const service_layer::SLInitMsg init_msg) {

    std::string s;

    if (google::protobuf::TextFormat::PrintToString(init_msg, &s)) {
        std::cout << "\n\n###########################\n" ;
        std::cout << "Transmitted message: IOSXR-SL INIT " << s;
        std::cout << "###########################\n\n\n" ;
    } else {
        std::cerr << "\n\n###########################\n" ;
        std::cerr << "Message not valid (partial content: "
                  << init_msg.ShortDebugString() << ")\n\n\n";
        std::cerr << "###########################\n" ;
    }

    // Typically when using the asynchronous API, we hold on to the 
    //"call" instance in order to get updates on the ongoing RPC.
    // In our case it isn't really necessary, since we operate within the
    // context of the same class, but anyway, we pass it in as the tag

    call.response_reader = stub_->AsyncSLGlobalInitNotif(&call.context, init_msg, &cq_, (void *)&call);
}

void AsyncNotifChannel::Shutdown() {

    tear_down = true;

    std::unique_lock<std::mutex> channel_lock(channel_mutex);

    while(!channel_closed) {
        channel_condVar.wait(channel_lock);
    }
}


void AsyncNotifChannel::Cleanup() {
    void* got_tag;
    bool ok = false;

    std::cout << "Asynchronous client shutdown requested\n"
              << "Let's clean up!\n";

    // Finish the Async session
    call.HandleResponse(false, &cq_);

    // Shutdown the completion queue
    call.HandleResponse(false, &cq_);

    std::cout << "Notifying channel close\n";
    channel_closed = true;
    // Notify the condition variable;
    channel_condVar.notify_one();
}


// Loop while listening for completed responses.
// Prints out the response from the server.
void AsyncNotifChannel::AsyncCompleteRpc() {
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
             std::cout << "Shutdown event received for completion queue" << std::endl;
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


AsyncNotifChannel::AsyncClientCall::AsyncClientCall(): callStatus_(CREATE) {}

void AsyncNotifChannel::AsyncClientCall::HandleResponse(bool responseStatus, grpc::CompletionQueue* pcq_) {
    //The First completion queue entry indicates session creation and shouldn't be processed - Check?
    switch (callStatus_) {
    case CREATE:
        if (responseStatus) {
            response_reader->Read(&notif, (void*)this);
            callStatus_ = PROCESS;
        } else {
            response_reader->Finish(&status, (void*)this);
            callStatus_ = FINISH;
        }
        break;
    case PROCESS:
        if (responseStatus) {
            response_reader->Read(&notif, (void *)this);
            auto slerrstatus = static_cast<int>(notif.errstatus().status());
            auto eventtype = static_cast<int>(notif.eventtype());

            if( eventtype == static_cast<int>(service_layer::SL_GLOBAL_EVENT_TYPE_VERSION) ) {
                if((slerrstatus == 
                       service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) ||
                   (slerrstatus == 
                       service_layer::SLErrorStatus_SLErrno_SL_INIT_STATE_READY) ||
                   (slerrstatus == 
                       service_layer::SLErrorStatus_SLErrno_SL_INIT_STATE_CLEAR)) {
                    std::cout << "Server returned " << std::endl; 
                    std::cout << "Successfully Initialized, connection Established!" << std::endl;
                            
                    // Lock the mutex before notifying using the conditional variable
                    std::lock_guard<std::mutex> guard(init_mutex);

                    // Set the initsuccess flag to indicate successful initialization
                    init_success = true;
       
                    // Notify the condition variable;
                    init_condVar.notify_one();

                } else {
                    std::cout << "client init error code " << slerrstatus << std::endl;
                }
            } else if (eventtype == static_cast<int>(service_layer::SL_GLOBAL_EVENT_TYPE_HEARTBEAT)) {
                std::cout << "Received Heartbeat" << std::endl; 
            } else if (eventtype == static_cast<int>(service_layer::SL_GLOBAL_EVENT_TYPE_ERROR)) {
                if (slerrstatus == service_layer::SLErrorStatus_SLErrno_SL_NOTIF_TERM) {
                    std::cerr << "Received notice to terminate. Client Takeover?" << std::endl;
                } else {
                    std::cerr << "Error Not Handled " << slerrstatus << std::endl;
                } 
            } else {
                std::cout << "client init unrecognized response " << eventtype << std::endl;
            }
        } else {
            response_reader->Finish(&status, (void*)this);
            callStatus_ = FINISH;
        }
        break;
    case FINISH:
        if (status.ok()) {
            std::cout << "Server Response Completed: " << this << " CallData: " << this << std::endl;
        }
        else {
            std::cerr << "RPC failed" << std::endl;
        }
        std::cout << "Shutting down the completion queue" << std::endl;
        pcq_->Shutdown();
    }
} 



std::string getEnvVar( std::string const & key )
{
    char * val = std::getenv( key.c_str() );
    return val == NULL ? std::string("") : std::string(val);
}


SLVrf* vrfhandler_signum;
AsyncNotifChannel* asynchandler_signum;

void signalHandler( int signum ) {
   std::cout << "Interrupt signal (" << signum << ") received.\n";

   // Clear out the last vrfRegMsg batch
   vrfhandler_signum->vrf_msg.clear_vrfregmsgs();

   // Create a fresh SLVrfRegMsg batch for cleanup
   vrfhandler_signum->vrfRegMsgAdd("default");

   vrfhandler_signum->unregisterVrf(AF_INET);
   vrfhandler_signum->unregisterVrf(AF_INET6);

 
   // Shutdown the Async Notification Channel  
   asynchandler_signum->Shutdown();

   // terminate program  

   exit(signum);  
}


int main(int argc, char** argv) {

    auto server_ip = getEnvVar("SERVER_IP");
    auto server_port = getEnvVar("SERVER_PORT");

    if (server_ip == "" || server_port == "") {
        if (server_ip == "") {
            std::cout << "SERVER_IP environment variable not set\n";
        }
        if (server_port == "") {
            std::cout << "SERVER_PORT environment variable not set\n";
        }
        return 1;

    }
    std::string grpc_server = server_ip + ":" + server_port;

    std::cout << "\n\nConnecting to grpc server at " << grpc_server << std::endl;

    AsyncNotifChannel asynchandler(grpc::CreateChannel(
                              grpc_server, grpc::InsecureChannelCredentials()));

    // Acquire the lock
    std::unique_lock<std::mutex> initlock(init_mutex);

    // Spawn reader thread that maintains our Notification Channel
    std::thread thread_ = std::thread(&AsyncNotifChannel::AsyncCompleteRpc, &asynchandler);


    service_layer::SLInitMsg init_msg;
    init_msg.set_majorver(service_layer::SL_MAJOR_VERSION);
    init_msg.set_minorver(service_layer::SL_MINOR_VERSION);
    init_msg.set_subver(service_layer::SL_SUB_VERSION);


    asynchandler.SendInitMsg(init_msg);  

    // Wait on the mutex lock
    while (!init_success) {
        init_condVar.wait(initlock);
    }

    // Set up a new channel for vrf/route messages

    SLVrf vrfhandler(grpc::CreateChannel(
                              grpc_server, grpc::InsecureChannelCredentials()));

    // Create a new SLVrfRegMsg batch
    vrfhandler.vrfRegMsgAdd("default", 10, 500);

    // Register the SLVrfRegMsg batch for v4 and v6
    vrfhandler.registerVrf(AF_INET);
    vrfhandler.registerVrf(AF_INET6);

   
    // Create an rshuttle object to send route batches 
    auto rshuttle = RShuttle(vrfhandler.channel);

    // Obtain pointer to a v4 route object within route batch
    auto routev4_ptr = rshuttle.routev4Add("default");

    // Set up the v4 route object
    rshuttle.routev4Set(routev4_ptr, rshuttle.IPv4ToLong("20.0.1.0") , 24, 120);

   
    // Obtain another pointer to a route object within route batch
    auto routev4_ptr2 = rshuttle.routev4Add("default");

    // Set up the new v4 route object
    rshuttle.routev4Set(routev4_ptr2, rshuttle.IPv4ToLong("23.0.1.0") , 24, 120);
 
    // Set up the paths for each v4 route object    
    rshuttle.routev4PathAdd(routev4_ptr, rshuttle.IPv4ToLong("14.1.1.10"), "GigabitEthernet0/0/0/0"); 
    rshuttle.routev4Op(service_layer::SL_OBJOP_ADD);
    rshuttle.routev4Op(service_layer::SL_OBJOP_ADD);


    rshuttle.routev4PathAdd(routev4_ptr2, rshuttle.IPv4ToLong("14.1.1.10"), "GigabitEthernet0/0/0/0");
    rshuttle.routev4Op(service_layer::SL_OBJOP_ADD);
    rshuttle.routev4Op(service_layer::SL_OBJOP_ADD);


    // Obtain pointer to a v6 route object within route batch

    auto routev6_ptr = rshuttle.routev6Add("default");

    // Set up the v6 route object 
    rshuttle.routev6Set(routev6_ptr, rshuttle.IPv6ToByteArrayString("2002:aa::0"), 64, 120);
  
    // Set up the path for v6 route object
    rshuttle.routev6PathAdd(routev6_ptr, rshuttle.IPv6ToByteArrayString("2002:ae::3"), "GigabitEthernet0/0/0/0");
    rshuttle.routev6Op(service_layer::SL_OBJOP_ADD);

    vrfhandler_signum = &vrfhandler;
    asynchandler_signum = &asynchandler;

    signal(SIGINT, signalHandler);  
    std::cout << "Press control-c to quit" << std::endl << std::endl;
    thread_.join();

    return 0;
}
