#include "ServiceLayerRoute.h"
#include "ServiceLayerRoutev2.h"
#include <getopt.h>
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

bool version2;

class testingData
{
public:
    // table_type is used to determine if we are doing ipv4(value = 0) ipv6(value = 1), or mpls(value = 2)
    unsigned int table_type = 0;
    unsigned int batch_size = 1024;
    unsigned int batch_num = 98;

    // For Ipv4
    std::string first_prefix_ipv4 = "40.0.0.0";
    unsigned int prefix_len_ipv4 = 24;
    std::string next_hop_interface_ipv4 = "Bundle-Ether1";
    std::string next_hop_ip_ipv4 = "14.1.1.10";

    // For Ipv6
    std::string first_prefix_ipv6 = "2002:aa::0";
    unsigned int prefix_len_ipv6 = 64;
    std::string next_hop_interface_ipv6 = "Bundle-Ether1";
    std::string next_hop_ip_ipv6 = "2002:ae::3";

    // For MPLS
    std::string first_prefix_mpls = "11.0.0.1";
    std::string next_hop_interface_mpls = "FourHundredGigE0/0/0/0";
    unsigned int start_label = 20000;
    unsigned int num_label = 1000;
    unsigned int num_paths = 1;
};
int table_type;

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


SLVrf* vrfhandler_signum;
RShuttle* rshuttle_signum;
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
       vrfhandler_signum->vrf_msg.clear_vrfregmsgs();

       // Create a fresh SLVrfRegMsg batch for cleanup
       vrfhandler_signum->vrfRegMsgAdd("default");

       vrfhandler_signum->unregisterVrf(AF_INET);
       vrfhandler_signum->unregisterVrf(AF_INET6);

       delete rshuttle_signum;

       // Shutdown the Async Notification Channel  
       asynchandler_signum->Shutdown();

       //terminate program  
       exit(signum);  
    } 
}

void 
signalHandlerv2(int signum)
{
    if (!sighandle_initiated) {
    sighandle_initiated = true;
    VLOG(1) << "Interrupt signal (" << signum << ") received.";

    // Clear out the last vrfRegMsg batch
    afvrfhandler_signum->af_vrf_msg.clear_vrfregmsgs();

    // Create a fresh SLVrfRegMsg batch for cleanup
    if(table_type == AF_INET){
        afvrfhandler_signum->afVrfRegMsgAdd("default",AF_INET);
        afvrfhandler_signum->unregisterAfVrf(AF_INET);
    } else if (table_type == AF_INET6){
        afvrfhandler_signum->afVrfRegMsgAdd("default",AF_INET6);
        afvrfhandler_signum->unregisterAfVrf(AF_INET6);
    } else if(table_type == AF_MPLS){
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

void routepush(RShuttle* route_shuttle,
               unsigned int batchSize,
               unsigned int batchNum)

{

    route_shuttle->setVrfV4("default");

    LOG(INFO) << "Starting Route batch";

    std::string prefix_str = "40.0.0.0";
    auto prefix = route_shuttle->ipv4ToLong(prefix_str.c_str());
    uint8_t prefix_len = 24;

    Timer tmr;
    unsigned int totalroutes = 0;

    for (int batchindex = 0; batchindex < batchNum; batchindex++) {
        VLOG(1) << "Batch: " << (batchindex + 1) << "\n";
        VLOG(1) << tmr.elapsed();
        for (int routeindex = 0; routeindex < batchSize; routeindex++, prefix=incrementIpv4Pfx(prefix, prefix_len)) {
            route_shuttle->insertAddBatchV4(route_shuttle->longToIpv4(prefix), prefix_len, 99, "14.1.1.10", "Bundle-Ether1");
            totalroutes++;
        }
        route_shuttle->routev4Op(service_layer::SL_OBJOP_UPDATE);
    }

    auto time_taken = tmr.elapsed();

    LOG(INFO) << "\nTime taken to program "<< totalroutes << " routes\n " 
              << time_taken
              << "\nRoute programming rate\n"
              << float(totalroutes)/time_taken << " routes/sec\n";

}

void routepush_slaf(SLAFRShuttle* slaf_route_shuttle,
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

void run_slaf(SLAFVrf* af_vrf_handler, unsigned int addr_family){

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
    int option_long;

    auto server_ip = getEnvVar("SERVER_IP");
    auto server_port = getEnvVar("SERVER_PORT");
    std:: string dummy = "";
    version2 = true;
    bool global_init_rpc = false;

    // Setting up GLOG (Google Logging)
    FLAGS_logtostderr = 1;
    google::InitGoogleLogging(argv[0]);

    if (server_ip == "" || server_port == "") {
        if (server_ip == "") {
            LOG(ERROR) << "SERVER_IP environment variable not set";
        }
        if (server_port == "") {
            LOG(ERROR) << "SERVER_PORT environment variable not set";
        }
        return 1;
    }

    testingData env_data;

    const struct option longopts[] = {
        {"table_type", required_argument, nullptr, 'a'},
        {"batch_size", required_argument, nullptr, 'b'},
        {"batch_num", required_argument, nullptr, 'c'},
        {"first_prefix_ipv4", required_argument, nullptr, 'd'},
        {"prefix_len_ipv4", required_argument, nullptr, 'e'},
        {"next_hop_interface_ipv4", required_argument, nullptr, 'f'},
        {"next_hop_ip_ipv4", required_argument, nullptr, 'g'},
        {"first_prefix_ipv6", required_argument, nullptr, 'i'},
        {"prefix_len_ipv6", required_argument, nullptr, 'j'},
        {"next_hop_interface_ipv6", required_argument, nullptr, 'k'},
        {"next_hop_ip_ipv6", required_argument, nullptr, 'l'},
        {"first_prefix_mpls", required_argument, nullptr, 'm'},
        {"next_hop_interface_mpls", required_argument, nullptr, 'n'},
        {"start_label", required_argument, nullptr, 'o'},
        {"num_label", required_argument, nullptr, 'q'},
        {"num_paths", required_argument, nullptr, 'r'},

        {"help", no_argument, nullptr, 'h'},
        {"username", required_argument, nullptr, 'u'},
        {"password", required_argument, nullptr, 'p'},
        {"slaf", required_argument, nullptr, 'v'},
        {"global_init_rpc", required_argument, nullptr, 's'},

        {nullptr,0,nullptr,0}
    };

    while ((option_long = getopt_long_only(argc, argv, "a:b:c:d:e:f:g:i:j:k:l:m:n:o:q:r:s:hu:p:v:",longopts,nullptr)) != -1) {
        switch (option_long) {
            case 'a':
                env_data.table_type = std::stoi(optarg);
                break;
            case 'b':
                env_data.batch_size = std::stoi(optarg);
                break;
            case 'c':
                env_data.batch_num = std::stoi(optarg);
                break;
            case 'd':
                env_data.first_prefix_ipv4 = optarg;
                break;
            case 'e':
                env_data.prefix_len_ipv4 = std::stoi(optarg);
                break;
            case 'f':
                env_data.next_hop_interface_ipv4 = optarg;
                break;
            case 'g':
                env_data.next_hop_ip_ipv4 = optarg;
                break;
            case 'i':
                env_data.first_prefix_ipv6 = optarg;
                break;
            case 'j':
                env_data.prefix_len_ipv6 = std::stoi(optarg);
                break;
            case 'k':
                env_data.next_hop_interface_ipv6 = optarg;
                break;
            case 'l':
                env_data.next_hop_ip_ipv6 = optarg;
                break;
            case 'm':
                env_data.first_prefix_mpls = optarg;
                break;
            case 'n':
                env_data.next_hop_interface_mpls = optarg;
                break;
            case 'o':
                env_data.start_label = std::stoi(optarg);
                break;
            case 'q':
                env_data.num_label = std::stoi(optarg);
                break;
            case 'r':
                env_data.num_paths = std::stoi(optarg);
                break;
            case 's':
                dummy = optarg;
                if (dummy == "true") {
                    global_init_rpc = true;
                }
                break;

            case 'h':
                LOG(INFO) <<"Usage:";
                LOG(INFO) <<"| -u/--username                    | Username |";
                LOG(INFO) <<"| -p/--password                    | Password |";
                LOG(INFO) <<"| -a/--table_type                  | Specify whether to do ipv4(value = 0), ipv6(value = 1) or mpls(value = 2) operation, PG is currently not supported (default 0) |";
                LOG(INFO) <<"| -v/--slaf                        | Specify if you want to use proto RPCs to program objects or not. If not, only configurable options are batch_size and batch_num (default true ) |";
                LOG(INFO) <<"| -s/--global_init_rpc             | Enable our Async Global Init RPC to handshake the API version number with the server. If enabled, then once exiting push routes/labels will be deleted. If disabled routes/labels pushed and stay (default false) |";
                LOG(INFO) << "Optional arguments you can set in environment:";
                LOG(INFO) << "| -h/--help                       | Help |";
                LOG(INFO) << "| -b/--batch_size                 | Configure the number of ipv4 routes or ILM entires for MPLS to be added to a batch (default 1024) |";
                LOG(INFO) << "| -c/--batch_num                  | Configure the number of batches (default 98) | \n";
                LOG(INFO) << "IPv4 Testing";
                LOG(INFO) << "| -d/--first_prefix_ipv4          | Configure the starting address for this test for IPV4 (default 40.0.0.0) |";
                LOG(INFO) << "| -e/--prefix_len_ipv4            | Configure the prefix length for this test for IPV4 address (default 24) |";
                LOG(INFO) << "| -f/--next_hop_interface_ipv4    | Configure the next hop interface for IPV4 (default Bundle-Ether1) |";
                LOG(INFO) << "| -g/--next_hop_ip_ipv4           | Configure the next hop ip address for IPV4 (default 14.1.1.10) | \n";
                LOG(INFO) << "IPv6 Testing";
                LOG(INFO) << "| -i/--first_prefix_ipv6          | Configure the starting address for this test for IPV6 (default 2002:aa::0) |";
                LOG(INFO) << "| -j/--prefix_len_ipv6            | Configure the prefix length for this test for IPV6 address (default 64) |";
                LOG(INFO) << "| -k/--next_hop_interface_ipv6    | Configure the next hop interface for IPV6 (default Bundle-Ether1) |";
                LOG(INFO) << "| -l/--next_hop_ip_ipv6           | Configure the next hop ip address for IPV6 (default 2002:ae::3) | \n";
                LOG(INFO) << "MPLS Testing";
                LOG(INFO) << "| -m/--first_prefix_mpls          | Configure the starting address for this test for MPLS (default 11.0.0.1) |";
                LOG(INFO) << "| -n/--next_hop_interface_mpls    | Configure the next hop interface for MPLS (default FourHundredGigE0/0/0/0) |";
                LOG(INFO) << "| -o/--start_label                | Configure the starting label for this test for MPLS (default 20000) |";
                LOG(INFO) << "| -q/--num_label                  | Configure the number of labels to be allocated for MPLS (default 1000) |";
                LOG(INFO) << "| -r/--num_paths                  | Configure the number of paths for MPLS labels (default 1)";
                return 1;
            case 'u':
                LOG(INFO) << " u";
                username = optarg;
                break;
            case 'p':
                LOG(INFO) << " p";
                password = optarg;
                break;
            case 'v':
                LOG(INFO) << " v";
                dummy = optarg;
                if(dummy == "false") {
                    version2 = false;
                }
                break;
            default:
                fprintf (stderr, "usage: %s --username --password\n", argv[0]);
                return 1;
        }
    }

    std::string grpc_server = server_ip + ":" + server_port;

    LOG(INFO) << "Connecting IOS-XR to gRPC server at " << grpc_server;


    // Create a gRPC channel
    auto channel = grpc::CreateChannel(
                              grpc_server, grpc::InsecureChannelCredentials());

    AsyncNotifChannel asynchandler(channel);
    std::thread thread_;
    if (global_init_rpc) {

        // Acquire the lock
        std::unique_lock<std::mutex> initlock(init_mutex);

        // Spawn reader thread that maintains our Notification Channel
        thread_ = std::thread(&AsyncNotifChannel::AsyncCompleteRpc, &asynchandler);


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
    }

    if (version2 == true) {

        auto af_vrf_handler = SLAFVrf(channel,username,password);

        // Need to specify ipv4 (default), ipv6(value = 1) or mpls(value = 2)
        if (env_data.table_type == 1) {
            table_type = AF_INET6;
        } else if (env_data.table_type == 2) {
            table_type = AF_MPLS;
        } else {
            table_type = AF_INET;
        }
        run_slaf(&af_vrf_handler,table_type);
        slaf_route_shuttle = new SLAFRShuttle(af_vrf_handler.channel, username, password);

        routepush_slaf(slaf_route_shuttle, env_data, table_type);

        if (global_init_rpc) {
            asynchandler_signum = &asynchandler;
        }
        afvrfhandler_signum = &af_vrf_handler;
        slaf_rshuttle_signum = slaf_route_shuttle;

        signal(SIGINT, signalHandlerv2);
        if (global_init_rpc) {
            LOG(INFO) << "Press control-c to quit";
            thread_.join();
        }

    } else {
        auto vrfhandler = SLVrf(channel, username, password);

        // Create a new SLVrfRegMsg batch
        vrfhandler.vrfRegMsgAdd("default", 10, 500);

        // Register the SLVrfRegMsg batch for v4 and v6
        vrfhandler.registerVrf(AF_INET);
        vrfhandler.registerVrf(AF_INET6);

        route_shuttle = new RShuttle(vrfhandler.channel, username, password);
        auto batch_size = env_data.batch_size;
        auto batch_num = env_data.batch_num;
        routepush(route_shuttle, batch_size, batch_num);

        if (global_init_rpc) {
            asynchandler_signum = &asynchandler;
        }
        vrfhandler_signum = &vrfhandler;
        rshuttle_signum = route_shuttle;

        signal(SIGINT, signalHandler);  
        if (global_init_rpc) {
            LOG(INFO) << "Press control-c to quit";
            thread_.join();
        }
    }
    return 0;
}

