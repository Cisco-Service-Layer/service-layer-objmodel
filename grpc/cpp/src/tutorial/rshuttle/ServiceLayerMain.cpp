// #include "ServiceLayerRoute.h"
#include "ServiceLayerRoutev2.h"
#include <string>
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

std::string username = "";
std::string password = "";

class testingData
{
public:
    // route_op is used to determine if we are doing ipv4(value = 0) ipv6(value = 1), or mpls(value = 2)
    unsigned int route_op;
    unsigned int batch_size;
    unsigned int batch_num;

    // For Ipv4
    std::string first_prefix_ipv4;
    unsigned int prefix_len_ipv4;
    std::string next_hop_interface_ipv4;
    std::string next_hop_ip_ipv4;

    // For Ipv6
    std::string first_prefix_ipv6;
    unsigned int prefix_len_ipv6;
    std::string next_hop_interface_ipv6;
    std::string next_hop_ip_ipv6;

    // For MPLS
    std::string first_prefix_mpls;
    std::string next_hop_interface_mpls;
    unsigned int start_label;
    unsigned int num_label;
    unsigned int num_paths;
};
int route_operation;

class Timer
{
public:
    Timer() : beg_(clock_::now()) {}
    void reset() { beg_ = clock_::now(); }
    double elapsed() const {
        return std::chrono::duration_cast<second_>
            (clock_::now() - beg_).count(); }

private:
    typedef std::chrono::high_resolution_clock clock_;
    typedef std::chrono::duration<double, std::ratio<1> > second_;
    std::chrono::time_point<clock_> beg_;
};


uint32_t incrementIpv4Pfx(uint32_t prefix, uint32_t prefixLen) {
    if (prefixLen > 32) {
        LOG(ERROR) << "PrefixLen > 32";
    }

    auto offset = 1 << 32 - prefixLen;

    return prefix + offset;
}

std::string 
getEnvVar(std::string const & key)
{
    char * val = std::getenv( key.c_str() );
    return val == NULL ? std::string("") : std::string(val);
}


// SLVrf* vrfhandler_signum;
// RShuttle* rshuttle_signum;
SLAFVrf* afvrfhandler_signum;
SLAFRShuttle* slaf_rshuttle_signum;
AsyncNotifChannel* asynchandler_signum;
bool sighandle_initiated = false;

void 
signalHandler(int signum)
{

   if (!sighandle_initiated) {
       sighandle_initiated = true;
       VLOG(1) << "Interrupt signal (" << signum << ") received.";

       // Clear out the last vrfRegMsg batch
       afvrfhandler_signum->af_vrf_msg.clear_vrfregmsgs();

        // Create a fresh SLVrfRegMsg batch for cleanup
        if(route_operation == AF_INET){
            afvrfhandler_signum->afVrfRegMsgAdd("default",AF_INET);
            afvrfhandler_signum->unregisterAfVrf(AF_INET);
        } else if (route_operation == AF_INET6){
            afvrfhandler_signum->afVrfRegMsgAdd("default",AF_INET6);
            afvrfhandler_signum->unregisterAfVrf(AF_INET6);
        } else if(route_operation == AF_MPLS){
            afvrfhandler_signum->afVrfRegMsgAdd("default",AF_MPLS);
            afvrfhandler_signum->unregisterAfVrf(AF_MPLS);
        }

       delete slaf_rshuttle_signum;

       // Shutdown the Async Notification Channel  
       asynchandler_signum->Shutdown();

       //terminate program  
       exit(signum);  
    } 
}


// void routepush(RShuttle* route_shuttle,
//                unsigned int batchSize,
//                unsigned int batchNum)

// {

//     route_shuttle->setVrfV4("default");

//     LOG(INFO) << "Starting Route batch";

//     std::string prefix_str = "40.0.0.0";
//     auto prefix = route_shuttle->ipv4ToLong(prefix_str.c_str());
//     uint8_t prefix_len = 24;

//     Timer tmr;
//     unsigned int totalroutes = 0;

//     for (int batchindex = 0; batchindex < batchNum; batchindex++) {
//         VLOG(1) << "Batch: " << (batchindex + 1) << "\n";
//         VLOG(1) << tmr.elapsed();
//         for (int routeindex = 0; routeindex < batchSize; routeindex++, prefix=incrementIpv4Pfx(prefix, prefix_len)) {
//             route_shuttle->insertAddBatchV4(route_shuttle->longToIpv4(prefix), prefix_len, 99, "14.1.1.10", "Bundle-Ether1");
//             totalroutes++;
//         }
//         route_shuttle->routev4Op(service_layer::SL_OBJOP_UPDATE);
//     }

//     auto time_taken = tmr.elapsed();

//     LOG(INFO) << "\nTime taken to program "<< totalroutes << " routes\n " 
//               << time_taken
//               << "\nRoute programming rate\n"
//               << float(totalroutes)/time_taken << " routes/sec\n";

// }

void routepushv2(SLAFRShuttle* slaf_route_shuttle,
               testingData env_data,
               unsigned int addr_family)

{
    Timer tmr;
    unsigned int totalroutes = 0;

    if (addr_family == AF_INET) {
        slaf_route_shuttle->setVrfV4("default");
        LOG(INFO) << "Starting IPV4 Route batch";

        if (env_data.batch_num == 0) {
            LOG(ERROR) << "batch_num needs to be higher than 0";
            return;
        }

        if (env_data.batch_num == 0) {
            LOG(ERROR) << "batch_num needs to be higher than 0";
            return;
        }
        auto prefix = slaf_route_shuttle->ipv4ToLong(env_data.first_prefix_ipv4.c_str());
        uint8_t prefix_len = env_data.prefix_len_ipv4;

        for (int batchindex = 0; batchindex < env_data.batch_num; batchindex++) {
            VLOG(1) << "Batch: " << (batchindex + 1) << "\n";
            VLOG(1) << tmr.elapsed();
            for (int routeindex = 0; routeindex < env_data.batch_size; routeindex++, prefix=incrementIpv4Pfx(prefix,prefix_len)) {
                slaf_route_shuttle->insertAddBatchV4(slaf_route_shuttle->longToIpv4(prefix),
                                                  prefix_len,
                                                  99,
                                                  env_data.next_hop_ip_ipv4,
                                                  env_data.next_hop_interface_ipv4);
                totalroutes++;
            }
            slaf_route_shuttle->routeSLAFOp(service_layer::SL_OBJOP_UPDATE, addr_family);
        }

    } else if (addr_family == AF_INET6) {
        slaf_route_shuttle->setVrfV6("default");
        LOG(INFO) << "Starting IPV6 Route batch";

        std::string prefix_str = env_data.first_prefix_ipv6;
        auto prefix = slaf_route_shuttle->ipv6ToByteArrayString(prefix_str.c_str());
        uint8_t prefix_len = env_data.prefix_len_ipv6;
        slaf_route_shuttle->insertAddBatchV6(slaf_route_shuttle->ByteArrayStringtoIpv6(prefix),
                                          prefix_len,
                                          99,
                                          env_data.next_hop_ip_ipv6,
                                          env_data.next_hop_interface_ipv6);
        totalroutes++;

        prefix_str = "2003:aa::0";
        prefix = slaf_route_shuttle->ipv6ToByteArrayString(prefix_str.c_str());
        slaf_route_shuttle->insertAddBatchV6(slaf_route_shuttle->ByteArrayStringtoIpv6(prefix),
                                          prefix_len,
                                          99,
                                          env_data.next_hop_ip_ipv6,
                                          env_data.next_hop_interface_ipv6);
        totalroutes++;
        slaf_route_shuttle->routeSLAFOp(service_layer::SL_OBJOP_UPDATE, addr_family);

    } else if (addr_family == AF_MPLS) {
        // Do not need to setvrf name as not needed for 
        slaf_route_shuttle->setVrfV4("default");
        LOG(INFO) << "Starting MPLS";
        if (env_data.batch_size == 0) {
            LOG(ERROR) << "batch_size needs to be higher than 0";
            return;
        }
        auto next_hop_address = slaf_route_shuttle->ipv4ToLong(env_data.first_prefix_mpls.c_str());
        totalroutes = slaf_route_shuttle->insertAddBatchMPLS(env_data.start_label,
                                                          env_data.num_label,
                                                          env_data.num_paths, env_data.batch_size,
                                                          next_hop_address,
                                                          env_data.next_hop_interface_mpls);
    }

    auto time_taken = tmr.elapsed();
    LOG(INFO) << "\nTime taken to program "<< totalroutes << " routes\n " 
              << time_taken
              << "\nRoute programming rate\n"
              << float(totalroutes)/time_taken << " routes/sec\n";

}
void run_v2(SLAFVrf* af_vrf_handler, unsigned int addr_family){

    switch(addr_family){
        // Create a new SLAFVrfRegMsg batch and Register it
        case AF_INET:
            af_vrf_handler->afVrfRegMsgAdd("default", 10, 500, AF_INET);
            af_vrf_handler->registerAfVrf(AF_INET);
            break;
        case AF_INET6:
            af_vrf_handler->afVrfRegMsgAdd("default", 10, 500, AF_INET6);
            af_vrf_handler->registerAfVrf(AF_INET6);
            break;
        case AF_MPLS:
            af_vrf_handler->afVrfRegMsgAdd("default", 10, 500, AF_MPLS);
            af_vrf_handler->registerAfVrf(AF_MPLS);
            break;
    }

}

int main(int argc, char** argv) {

    int option_char;

    auto server_ip = getEnvVar("SERVER_IP");
    auto server_port = getEnvVar("SERVER_PORT");

    if (server_ip == "" || server_port == "") {
        if (server_ip == "") {
            LOG(ERROR) << "SERVER_IP environment variable not set";
        }
        if (server_port == "") {
            LOG(ERROR) << "SERVER_PORT environment variable not set";
        }
        return 1;
    }

    while ((option_char = getopt(argc, argv, "u:p:")) != -1) {
        switch (option_char) {
            case 'u':
                username = optarg;
                break;
            case 'p':
                password = optarg;
                break;
            default:
                fprintf (stderr, "usage: %s -u username -p password\n", argv[0]);
                return 1;
        }
    }

    testingData env_data;
    env_data.route_op = (getEnvVar("route_op") != "")?stoi(getEnvVar("route_op")):0;
    env_data.batch_size = (getEnvVar("batch_size") != "")?stoi(getEnvVar("batch_size")):1024;
    env_data.batch_num = (getEnvVar("batch_num") != "")?stoi(getEnvVar("batch_num")):98;

    // For Ipv4
    env_data.first_prefix_ipv4 = (getEnvVar("first_prefix_ipv4") != "")?getEnvVar("first_prefix_ipv4"):"40.0.0.0";
    env_data.prefix_len_ipv4 = (getEnvVar("prefix_len_ipv4") != "")?stoi(getEnvVar("prefix_len_ipv4")):24;
    env_data.next_hop_interface_ipv4 = (getEnvVar("next_hop_interface_ipv4") != "")?getEnvVar("next_hop_interface_ipv4"):"Bundle-Ether1";
    env_data.next_hop_ip_ipv4 = (getEnvVar("next_hop_ip_ipv4") != "")?getEnvVar("next_hop_ip_ipv4"):"14.1.1.10";

    // For Ipv6
    env_data.first_prefix_ipv6 = (getEnvVar("first_prefix_ipv6") != "")?getEnvVar("first_prefix_ipv6"):"2002:aa::0";
    env_data.prefix_len_ipv6 = (getEnvVar("prefix_len_ipv6") != "")?stoi(getEnvVar("prefix_len_ipv6")):64;
    env_data.next_hop_interface_ipv6 = (getEnvVar("next_hop_interface_ipv6") != "")?getEnvVar("next_hop_interface_ipv6"):"Bundle-Ether1";
    env_data.next_hop_ip_ipv6 = (getEnvVar("next_hop_ip_ipv6") != "")?getEnvVar("next_hop_ip_ipv6"):"2002:ae::3";

    // For MPLS
    env_data.first_prefix_mpls = (getEnvVar("first_prefix_mpls") != "")?getEnvVar("first_prefix_mpls"):"11.0.0.1";
    env_data.next_hop_interface_mpls = (getEnvVar("first_prefix_mpls") != "")?getEnvVar("first_prefix_mpls"):"FourHundredGigE0/0/0/0";
    env_data.start_label = (getEnvVar("start_label") != "")?stoi(getEnvVar("start_label")):20000;
    env_data.num_label = (getEnvVar("num_label") != "")?stoi(getEnvVar("num_label")):1000;
    env_data.num_paths = (getEnvVar("num_paths") != "")?stoi(getEnvVar("num_paths")):1;

    std::string grpc_server = server_ip + ":" + server_port;

    LOG(INFO) << "Connecting IOS-XR to gRPC server at " << grpc_server;


    // Create a gRPC channel
    auto channel = grpc::CreateChannel(
                              grpc_server, grpc::InsecureChannelCredentials());

    
    AsyncNotifChannel asynchandler(channel);

    // Acquire the lock
    std::unique_lock<std::mutex> initlock(init_mutex);

    // Spawn reader thread that maintains our Notification Channel
    std::thread thread_ = std::thread(&AsyncNotifChannel::AsyncCompleteRpc, &asynchandler);


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

    // Wait on the mutex lock
    while (!init_success) {
        init_condVar.wait(initlock);
    }

    auto af_vrf_handler = SLAFVrf(channel,username,password);

    // Need to specify ipv4 (default), ipv6(value = 1) or mpls(value = 2)
    if (env_data.route_op == 1) {
        route_operation = AF_INET6;
    } else if (env_data.route_op == 2) {
        route_operation = AF_MPLS;
    } else {
        route_operation = AF_INET;
    }
    run_v2(&af_vrf_handler,route_operation);
    slaf_route_shuttle = new SLAFRShuttle(af_vrf_handler.channel, username, password);

    routepushv2(slaf_route_shuttle, env_data, route_operation);

    asynchandler_signum = &asynchandler;
    afvrfhandler_signum = &af_vrf_handler;
    slaf_rshuttle_signum = slaf_route_shuttle;

    signal(SIGINT, signalHandler);
    LOG(INFO) << "Press control-c to quit";
    thread_.join();

    return 0;
    /*

    auto vrfhandler = SLVrf(channel, username, password);

    // Create a new SLVrfRegMsg batch
    vrfhandler.vrfRegMsgAdd("default", 10, 500);

    // Register the SLVrfRegMsg batch for v4 and v6
    vrfhandler.registerVrf(AF_INET);
    vrfhandler.registerVrf(AF_INET6);

    route_shuttle = new RShuttle(vrfhandler.channel, username, password);

    routepush(route_shuttle, batch_size, batch_num);

    asynchandler_signum = &asynchandler;
    vrfhandler_signum = &vrfhandler;
    rshuttle_signum = route_shuttle;
    

    signal(SIGINT, signalHandler);  
    
    LOG(INFO) << "Press control-c to quit";
    thread_.join();
    */

    return 0;
}

