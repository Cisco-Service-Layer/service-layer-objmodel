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
RShuttlev2* rshuttle_signum;
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
       afvrfhandler_signum->afVrfRegMsgAdd("default",AF_INET);

       afvrfhandler_signum->unregisterAfVrf(AF_INET);
    //    afvrfhandler_signum->unregisterAfVrf(AF_INET6);

       delete rshuttle_signum;

       // Shutdown the Async Notification Channel  
       asynchandler_signum->Shutdown();

       //terminate program  
       exit(signum);  
    } 
}


void routepush(RShuttlev2* route_shuttle,
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

    auto batch_size = (getEnvVar("BATCH_SIZE") != "")?stoi(getEnvVar("BATCH_SIZE")):1024;
    auto batch_num = (getEnvVar("BATCH_NUM") != "")?stoi(getEnvVar("BATCH_NUM")):98; 

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

    // Create a new SLAFVrfRegMsg batch
    af_vrf_handler.afVrfRegMsgAdd("default", 10, 500, AF_INET);

    // Register the SLVrfRegMsg batch for v4 and v6
    af_vrf_handler.registerAfVrf(AF_INET);
    // af_vrf_handler.registerAfVrf(AF_INET6);

    route_shuttle = new RShuttlev2(af_vrf_handler.channel, username, password);

    routepush(route_shuttle, batch_size, batch_num);

    asynchandler_signum = &asynchandler;
    afvrfhandler_signum = &af_vrf_handler;
    rshuttle_signum = route_shuttle;
    

    signal(SIGINT, signalHandler);

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
    */
    LOG(INFO) << "Press control-c to quit";
    thread_.join();

    return 0;
}

