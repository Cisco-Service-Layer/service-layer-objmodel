#include "ServiceLayerRoute.h"
#include "ServiceLayerRoutev2.h"
#include <getopt.h>
#include <string>
#include <csignal>
#include <utility>

using grpc::ClientContext;
using grpc::ClientReader;
using grpc::ClientReaderWriter;
using grpc::ClientWriter;
using grpc::CompletionQueue;
using grpc::Status;
using grpc::Channel;
using service_layer::SLInitMsg;
using service_layer::SLVersion;
using service_layer::SLGlobal;
using grpc::StatusCode;
std::string username = "";
std::string password = "";

bool version2;
bool global_init_rpc = false;
service_layer::SLTableType table_type;

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

// These signum are used with correspondence to signalHandler and signalHandlerSlaf
SLVrf* vrfhandler_signum;
RShuttle* rshuttle_signum;
SLAFVrf* afvrfhandler_signum;
SLAFRShuttle* slaf_rshuttle_signum;
AsyncNotifChannel* asynchandler_signum;
bool sighandle_initiated = false;

// Number of attempts to retry pushing routes, if failure occurs when pushing routes
int maxAttempts = 5;

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

       vrfhandler_signum->registerVrf(service_layer::SL_IPv4_ROUTE_TABLE, service_layer::SL_REGOP_UNREGISTER);
       vrfhandler_signum->registerVrf(service_layer::SL_IPv6_ROUTE_TABLE, service_layer::SL_REGOP_UNREGISTER);

       delete rshuttle_signum;

       // Shutdown the Async Notification Channel  
       if (global_init_rpc) {
            asynchandler_signum->Shutdown();
       }

       //terminate program  
       exit(signum);  
    } 
}

void 
signalHandlerSlaf(int signum)
{
    if (!sighandle_initiated) {
    sighandle_initiated = true;
    VLOG(1) << "Interrupt signal (" << signum << ") received.";

    // Clear out the last vrfRegMsg batch
    afvrfhandler_signum->af_vrf_msg.clear_vrfregmsgs();

    // Create a fresh SLVrfRegMsg batch for cleanup
    if(table_type == service_layer::SL_IPv4_ROUTE_TABLE){
        afvrfhandler_signum->afVrfRegMsgAdd("default",service_layer::SL_IPv4_ROUTE_TABLE);
        afvrfhandler_signum->registerAfVrf(service_layer::SL_IPv4_ROUTE_TABLE, service_layer::SL_REGOP_UNREGISTER);
    } else if (table_type == service_layer::SL_IPv6_ROUTE_TABLE){
        afvrfhandler_signum->afVrfRegMsgAdd("default",service_layer::SL_IPv6_ROUTE_TABLE);
        afvrfhandler_signum->registerAfVrf(service_layer::SL_IPv6_ROUTE_TABLE, service_layer::SL_REGOP_UNREGISTER);
    } else if(table_type == service_layer::SL_MPLS_LABEL_TABLE){
        afvrfhandler_signum->afVrfRegMsgAdd("default",service_layer::SL_MPLS_LABEL_TABLE);
        afvrfhandler_signum->registerAfVrf(service_layer::SL_MPLS_LABEL_TABLE, service_layer::SL_REGOP_UNREGISTER);
    } else if(table_type == service_layer::SL_PATH_GROUP_TABLE){
        afvrfhandler_signum->afVrfRegMsgAdd("default",service_layer::SL_PATH_GROUP_TABLE);
        afvrfhandler_signum->registerAfVrf(service_layer::SL_PATH_GROUP_TABLE, service_layer::SL_REGOP_UNREGISTER);
    }

    delete slaf_rshuttle_signum;

    // Shutdown the Async Notification Channel  
    if (global_init_rpc) {
        asynchandler_signum->Shutdown();
    }

    //terminate program  
    exit(signum);  
    }  
}

// Goes through the DB and prints errors
void printDbErrors(testingData env_data, service_layer::SLTableType addr_family)
{
    if (addr_family == service_layer::SL_IPv4_ROUTE_TABLE) {
        for (auto ipv4_index = database.db_ipv4.begin(); ipv4_index != database.db_ipv4.end(); ipv4_index++) {
            if (ipv4_index->second.second.fib_req == true) {
                if (ipv4_index->second.second.fib_success == false || ipv4_index->second.second.rib_success == false) {
                    LOG(ERROR) << ipv4_index->second.second.error;
                }
            } else {
                if (ipv4_index->second.second.rib_success == false) {
                    LOG(ERROR) << ipv4_index->second.second.error;
                }
            }
        }
    } else if (addr_family == service_layer::SL_IPv6_ROUTE_TABLE) {
        for (auto ipv6_index = database.db_ipv6.begin(); ipv6_index != database.db_ipv6.end(); ipv6_index++) {
            if (ipv6_index->second.second.fib_req == true) {
                if (ipv6_index->second.second.fib_success == false || ipv6_index->second.second.rib_success == false) {
                    LOG(ERROR) << ipv6_index->second.second.error;
                }
            } else {
                if (ipv6_index->second.second.rib_success == false) {
                    LOG(ERROR) << ipv6_index->second.second.error;
                }
            }
        }
    } else if (addr_family == service_layer::SL_MPLS_LABEL_TABLE) {
        for (auto mpls_index = database.db_mpls.begin(); mpls_index != database.db_mpls.end(); mpls_index++) {
            if (mpls_index->second.second.fib_req == true) {
                if (mpls_index->second.second.fib_success == false || mpls_index->second.second.rib_success == false) {
                    LOG(ERROR) << mpls_index->second.second.error;
                }
            } else {
                if (mpls_index->second.second.rib_success == false) {
                    LOG(ERROR) << mpls_index->second.second.error;
                }
            }
        }
    } else if (addr_family == service_layer::SL_PATH_GROUP_TABLE) {
        for (auto pg_index = database.db_pg.begin(); pg_index != database.db_pg.end(); pg_index++) {
            if (pg_index->second.second.fib_req == true) {
                if (pg_index->second.second.fib_success == false || pg_index->second.second.rib_success == false) {
                    LOG(ERROR) << pg_index->second.second.error;
                }
            } else {
                if (pg_index->second.second.rib_success == false) {
                    LOG(ERROR) << pg_index->second.second.error;
                }
            }
        }
    }
}

void routepush(RShuttle* route_shuttle,
               unsigned int batchSize,
               unsigned int batchNum,
               service_layer::SLObjectOp route_oper)

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
            route_shuttle->insertAddBatchV4(route_shuttle->longToIpv4(prefix), prefix_len, 99, "14.1.1.10", "Bundle-Ether1", route_oper);
            totalroutes++;
        }
        route_shuttle->routev4Op(route_oper);
    }

    auto time_taken = tmr.elapsed();

    LOG(INFO) << "\nTime taken to program "<< totalroutes << " routes\n " 
              << time_taken
              << "\nRoute programming rate\n"
              << float(totalroutes)/time_taken << " routes/sec\n";

}

void routepush_slaf(SLAFRShuttle* slaf_route_shuttle,
               testingData env_data,
               service_layer::SLTableType addr_family)
{
    Timer tmr;
    unsigned int totalroutes = 0;

    // Clears all of the DB's
    slaf_route_shuttle->clearDB();

    // Depending on table type, perform stream or non-stream rpc
    if (addr_family == service_layer::SL_IPv4_ROUTE_TABLE) {
        LOG(INFO) << "Starting IPV4 Route batch";

        // Populate IPV4 DB
        auto prefix = slaf_route_shuttle->ipv4ToLong(env_data.first_prefix_ipv4.c_str());
        uint8_t prefix_len = env_data.prefix_len_ipv4;
        database.ipv4_start_index = prefix;
        // Push all routes these onto the db based off their prefix
        for(int i = 1; i <= env_data.num_operations; i++, prefix=incrementIpv4Pfx(prefix,prefix_len)){
            statusObject dummy;
            std::pair<testingData, statusObject> temp = std::make_pair(env_data, dummy);
            database.db_ipv4[prefix] = temp;
            if (i == env_data.num_operations) {
                database.ipv4_last_index = prefix;
            }
            database.db_count++;
        }
        if (env_data.stream_case == true) {
            totalroutes = slaf_route_shuttle->routeSLAFOpStream(addr_family, env_data.route_oper);
        } else {
            totalroutes = slaf_route_shuttle->pushFromDB(false,env_data.route_oper,addr_family);
        }

    } else if (addr_family == service_layer::SL_IPv6_ROUTE_TABLE) {
        LOG(INFO) << "Starting IPV6 Route batch";

        // Populate IPV6 DB
        std::string prefix_str = env_data.first_prefix_ipv6;
        auto prefix = slaf_route_shuttle->ipv6ToByteArrayString(prefix_str.c_str());
        uint8_t prefix_len = env_data.prefix_len_ipv6;
        // Push all routes these onto the db based off their prefix
        database.ipv6_start_index = prefix;
        for(int i = 1; i <= env_data.num_operations; i++, prefix=slaf_route_shuttle->incrementIpv6Pfx(prefix,prefix_len)){
            statusObject dummy;
            std::pair<testingData, statusObject> temp = std::make_pair(env_data, dummy);
            database.db_ipv6[prefix] = temp;
            if (i == env_data.num_operations) {
                database.ipv6_last_index = prefix;
            }
            database.db_count++;
        }
        if (env_data.stream_case == true) {
            totalroutes = slaf_route_shuttle->routeSLAFOpStream(addr_family, env_data.route_oper);
        } else {
            totalroutes = slaf_route_shuttle->pushFromDB(false,env_data.route_oper,addr_family);
        }

    } else if (addr_family == service_layer::SL_MPLS_LABEL_TABLE) {
        LOG(INFO) << "Starting MPLS";

        // Populate MPLS DB
        unsigned int start_label = env_data.start_label;
        database.mpls_start_index = start_label;
        for(int i = 0; i < env_data.num_operations; i++){
            statusObject dummy;
            std::pair<testingData, statusObject> temp = std::make_pair(env_data, dummy);
            database.db_mpls[start_label+i] = temp;
            database.db_count++;
        }
        database.mpls_last_index = start_label+env_data.num_operations-1;

        if (env_data.stream_case == true) {
            totalroutes = slaf_route_shuttle->routeSLAFOpStream(addr_family, env_data.route_oper);
        } else {
            totalroutes = slaf_route_shuttle->pushFromDB(false,env_data.route_oper,addr_family);
        }
    } else if (addr_family == service_layer::SL_PATH_GROUP_TABLE) {

        if (env_data.num_operations > env_data.max_paths) {
            LOG(ERROR) << "FOR PG, MAX operations has to be <= " << env_data.max_paths;
            return;
        }
        if (env_data.pg_name == "") {
            LOG(ERROR) << "Path Group required name_id";
            return;
        }

        LOG(INFO) << "Starting PATH_GROUP";
        if (env_data.create_path_group_for == service_layer::SL_IPv4_ROUTE_TABLE || env_data.create_path_group_for == service_layer::SL_MPLS_LABEL_TABLE) {
            // Add ipv4 paths and mpls label if needed
            uint32_t prefix;
            // For mpls we use the first_mpls_path_nhip (next hop ip address for mpls)
            if (env_data.create_path_group_for == service_layer::SL_MPLS_LABEL_TABLE) {
                prefix = slaf_route_shuttle->ipv4ToLong(env_data.first_mpls_path_nhip.c_str());
                env_data.next_hop_interface_ipv4 = env_data.next_hop_interface_mpls;
            } else {
                prefix = slaf_route_shuttle->ipv4ToLong(env_data.next_hop_ip_ipv4.c_str());
            }
            database.ipv4_start_index = prefix;
            // Push all routes these onto the db based off their prefix
            for(int i = 1; i <= env_data.num_operations; i++, prefix=incrementIpv4Pfx(prefix,32)){
                if (i == env_data.num_operations) {
                    database.ipv4_last_index = prefix;
                }
            }
            database.db_count++;
        } else if (env_data.create_path_group_for == service_layer::SL_IPv6_ROUTE_TABLE) {
            // Add ipv6 paths
            std::string prefix_str = env_data.next_hop_ip_ipv6;
            auto prefix = slaf_route_shuttle->ipv6ToByteArrayString(prefix_str.c_str());
            // Push all routes these onto the db based off their prefix
            database.ipv6_start_index = prefix;
            for(int i = 1; i <= env_data.num_operations; i++, prefix=slaf_route_shuttle->incrementIpv6Pfx(prefix,128)){
                if (i == env_data.num_operations) {
                    database.ipv6_last_index = prefix;
                }
            }
            database.db_count++;
        }
        statusObject dummy;
        std::pair<testingData, statusObject> temp = std::make_pair(env_data, dummy);
        database.db_pg[env_data.pg_name] = temp;
        database.pg_name = env_data.pg_name;

         if (env_data.stream_case == true) {
            totalroutes = slaf_route_shuttle->routeSLAFOpStream(addr_family, env_data.route_oper,env_data.create_path_group_for);
        } else {
            totalroutes = slaf_route_shuttle->pushFromDB(false,env_data.route_oper,addr_family,env_data.create_path_group_for);
        }
    }

    auto time_taken = tmr.elapsed();
    LOG(INFO) << "\nTime taken to program "<< totalroutes << " routes\n " 
            << time_taken
            << "\nRoute programming rate\n"
            << float(totalroutes)/time_taken << " routes/sec\n"
            << "Number of Batches sent: "
            << ((totalroutes-1)/env_data.batch_size) + 1 << "\n";

    // prints any errors in DB
    printDbErrors(env_data,addr_family);
}

// Handles VRF registration
void run_slaf(SLAFVrf* af_vrf_handler, service_layer::SLTableType addr_family, service_layer::SLRegOp vrf_reg_oper)
{
    std::string vrf_oper_str = "";
    if(vrf_reg_oper == service_layer::SL_REGOP_REGISTER) {
        vrf_oper_str = "SL_REGOP_REGISTER";
    } else if (vrf_reg_oper == service_layer::SL_REGOP_UNREGISTER) {
        vrf_oper_str = "SL_REGOP_UNREGISTER";
    } else if (vrf_reg_oper == service_layer::SL_REGOP_EOF) {
        vrf_oper_str = "SL_REGOP_EOF";
    }
    switch(addr_family){
        // Create a new SLAFVrfRegMsg batch and Register it
        case service_layer::SL_IPv4_ROUTE_TABLE:
            LOG(INFO) << "Performing " << vrf_oper_str << " VRF for SL_IPv4_ROUTE_TABLE" ;
            af_vrf_handler->afVrfRegMsgAdd("default", 10, 500, service_layer::SL_IPv4_ROUTE_TABLE);
            af_vrf_handler->registerAfVrf(service_layer::SL_IPv4_ROUTE_TABLE, vrf_reg_oper);
            break;
        case service_layer::SL_IPv6_ROUTE_TABLE:
            LOG(INFO) << "Performing " << vrf_oper_str << " VRF for SL_IPv6_ROUTE_TABLE" ;
            af_vrf_handler->afVrfRegMsgAdd("default", 10, 500, service_layer::SL_IPv6_ROUTE_TABLE);
            af_vrf_handler->registerAfVrf(service_layer::SL_IPv6_ROUTE_TABLE, vrf_reg_oper);
            break;
        case service_layer::SL_MPLS_LABEL_TABLE:
            LOG(INFO) << "Performing " << vrf_oper_str << " VRF for SL_MPLS_LABEL_TABLE" ;
            af_vrf_handler->afVrfRegMsgAdd("default", 10, 500, service_layer::SL_MPLS_LABEL_TABLE);
            af_vrf_handler->registerAfVrf(service_layer::SL_MPLS_LABEL_TABLE, vrf_reg_oper);
            break;
        case service_layer::SL_PATH_GROUP_TABLE:
            LOG(INFO) << "Performing " << vrf_oper_str << " VRF for SL_PATH_GROUP_TABLE" ;
            af_vrf_handler->afVrfRegMsgAdd("default", 10, 500, service_layer::SL_PATH_GROUP_TABLE);
            af_vrf_handler->registerAfVrf(service_layer::SL_PATH_GROUP_TABLE, vrf_reg_oper);
            break;
    }
    LOG(INFO) << vrf_oper_str << " VRF Successful";

}

// Version 2: We try to push the routes, but if any UNAVAILABLE rpc error occurs then we retry
void try_route_push_slaf(std::shared_ptr<grpc::Channel> channel,
               std::string grpc_server,
               testingData env_data)
{
    bool exception_caught = true;
    int attempts = 1;
    bool route_shuttle_object_created = false;
    SLGLOBALSHUTTLE* sl_global_shuttle;
    while(attempts <= maxAttempts) {
        try
        {
            route_shuttle_object_created = false;
            // get the globals data info to record the batch size we need. 
            sl_global_shuttle = new SLGLOBALSHUTTLE(channel, username, password);
            sl_global_shuttle->getGlobals(env_data.batch_size, env_data.max_paths);

            auto af_vrf_handler = SLAFVrf(channel,username,password);
            // Need to specify ipv4 (default), ipv6 or mpls
            table_type = env_data.table_type;
            // If vrf_rg_oper not set then we do not register vrf
            if (env_data.vrf_reg_oper != service_layer::SL_REGOP_RESERVED) {
                run_slaf(&af_vrf_handler,table_type, env_data.vrf_reg_oper);
            }

            // If we Unregister, then we do not push routes
            if(env_data.vrf_reg_oper != service_layer::SL_REGOP_UNREGISTER) {
                slaf_route_shuttle = new SLAFRShuttle(af_vrf_handler.channel, username, password);
                route_shuttle_object_created = true;
                routepush_slaf(slaf_route_shuttle, env_data, table_type);
            }
            exception_caught = false;
        }
        // Error Handling: If any RPC fails with UNAVAILABLE code we have to attempt to retry
        catch (grpc::Status status) {
            if(!status.ok()) {
                delete sl_global_shuttle;
                // If we are not below max attempts retry
                LOG(INFO) << "RETRY ATTEMPT Number: " << attempts;
                if(route_shuttle_object_created) {
                    delete slaf_route_shuttle;
                }

                // Only need for non stream case because while exception is thrown, lock on DB is still there, so if retry attempted while lock is taken, then a deadlock occurs
                if (env_data.stream_case == false) {
                    db_mutex.unlock();
                }
            }
            if (status.error_code() != grpc::StatusCode::UNAVAILABLE) {
                LOG(INFO) << "Cannot retry for status code: " << status.error_code();
                attempts = maxAttempts + 1;
                break;
            }
        }
        if (!exception_caught) {
            delete sl_global_shuttle;
            if (route_shuttle_object_created) {
                delete slaf_route_shuttle;
            }
            break;
        }
        attempts++;
        // No need to wait after all attempts are tried
        if (attempts <= maxAttempts) {
            LOG(INFO) << "Waiting 30 Seconds before retrying";
            std::this_thread::sleep_for(std::chrono::seconds(30));
        }
    }
}

// Version 1: We try to push the routes, but if UNAVAILABLE rpc error occurs then we retry
void try_route_push(std::shared_ptr<grpc::Channel> channel,
               std::string grpc_server,
               testingData env_data)
{
    bool exception_caught = true;
    int attempts = 1;
    bool route_shuttle_object_created = false;
    SLGLOBALSHUTTLE* sl_global_shuttle;
    while(attempts <= maxAttempts) {
        try 
        {
            route_shuttle_object_created = false;
            // get the globals data info to record the batch size we need. 
            sl_global_shuttle = new SLGLOBALSHUTTLE(channel, username, password);
            sl_global_shuttle->getGlobals(env_data.batch_size, env_data.max_paths);

            auto vrfhandler = SLVrf(channel, username, password);
            // Create a new SLVrfRegMsg batch
            vrfhandler.vrfRegMsgAdd("default", 10, 500);

            // If vrf_rg_oper not set then we do not register vrf
            if (env_data.vrf_reg_oper != service_layer::SL_REGOP_RESERVED) {
                // Register the SLVrfRegMsg batch for v4
                vrfhandler.registerVrf(service_layer::SL_IPv4_ROUTE_TABLE, env_data.vrf_reg_oper);
            }

            // If we Unregister, then we do not push routes
            if(env_data.vrf_reg_oper != service_layer::SL_REGOP_UNREGISTER) {
                auto batch_size = env_data.batch_size;
                auto batch_num = env_data.batch_num;
                auto route_oper = env_data.route_oper;
                route_shuttle = new RShuttle(vrfhandler.channel, username, password);
                route_shuttle_object_created = true;
                routepush(route_shuttle, batch_size, batch_num, route_oper);
            }
            exception_caught = false;
        }
        // Error Handling: If any RPC fails with UNAVAILABLE code we have to attempt to retry
        catch (grpc::Status status) {
            if(!status.ok()) {
                // If we are not below max attempts retry
                LOG(INFO) << "RETRY ATTEMPT Number: " << attempts;
                delete sl_global_shuttle;
                if(route_shuttle_object_created) {
                    delete route_shuttle;
                }
            }
            if (status.error_code() != grpc::StatusCode::UNAVAILABLE) {
                LOG(INFO) << "Cannot retry for status code: " << status.error_code();
                attempts = maxAttempts + 1;
                break;
            }
        }
        if (!exception_caught) {
            delete sl_global_shuttle;
            if (route_shuttle_object_created) {
                delete route_shuttle;
            }
            break;
        }
        attempts++;
        // No need to wait after all attempts are tried
        if (attempts <= maxAttempts) {
            LOG(INFO) << "Waiting 30 Seconds before retrying";
            std::this_thread::sleep_for(std::chrono::seconds(30));
        }
    }
}

int main(int argc, char** argv) {

    int option_char;
    int option_long;

    auto server_ip = getEnvVar("SERVER_IP");
    auto server_port = getEnvVar("SERVER_PORT");
    std:: string dummy = "";
    version2 = true;

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
    LOG(INFO) << env_data.num_operations;

    const struct option longopts[] = {
        {"table_type", required_argument, nullptr, 't'},
        {"route_oper", required_argument, nullptr, 'a'},
        {"vrf_reg_oper", required_argument, nullptr, 'w'},
        {"num_operations", required_argument, nullptr, 'b'},
        {"batch_size", required_argument, nullptr, 'c'},
        {"stream_case", required_argument, nullptr, 'x'},
        {"first_prefix_ipv4", required_argument, nullptr, 'd'},
        {"prefix_len_ipv4", required_argument, nullptr, 'e'},
        {"next_hop_interface_ipv4", required_argument, nullptr, 'f'},
        {"next_hop_ip_ipv4", required_argument, nullptr, 'g'},
        {"first_prefix_ipv6", required_argument, nullptr, 'i'},
        {"prefix_len_ipv6", required_argument, nullptr, 'j'},
        {"next_hop_interface_ipv6", required_argument, nullptr, 'k'},
        {"next_hop_ip_ipv6", required_argument, nullptr, 'l'},
        {"first_mpls_path_nhip", required_argument, nullptr, 'm'},
        {"next_hop_interface_mpls", required_argument, nullptr, 'n'},
        {"start_label", required_argument, nullptr, 'o'},
        {"num_paths", required_argument, nullptr, 'q'},
        {"create_path_group_for", required_argument, nullptr, 'r'},
        {"path_group_name", required_argument, nullptr, 'y'},

        {"help", no_argument, nullptr, 'h'},
        {"username", required_argument, nullptr, 'u'},
        {"password", required_argument, nullptr, 'p'},
        {"slaf", required_argument, nullptr, 'v'},
        {"global_init", required_argument, nullptr, 's'},

        {nullptr,0,nullptr,0}
    };

    while ((option_long = getopt_long_only(argc, argv, "t:a:w:b:c:x:d:e:f:g:i:j:k:l:m:n:o:q:r:s:hu:p:v:y:",longopts,nullptr)) != -1) {
        switch (option_long) {
            case 't':
                dummy = optarg;
                if(dummy == "ipv6") {
                    env_data.table_type = service_layer::SL_IPv6_ROUTE_TABLE;
                } else if (dummy == "mpls") {
                    env_data.table_type = service_layer::SL_MPLS_LABEL_TABLE;
                } else if (dummy == "pg"){
                    env_data.table_type = service_layer::SL_PATH_GROUP_TABLE;
                } else {
                    env_data.table_type = service_layer::SL_IPv4_ROUTE_TABLE;
                }
                break;
            case 'a':

                dummy = optarg;
                if (dummy == "Add") {
                    env_data.route_oper = service_layer::SL_OBJOP_ADD;
                } else if (dummy == "Update") {
                    env_data.route_oper = service_layer::SL_OBJOP_UPDATE;
                } else if (dummy == "Delete") {
                    env_data.route_oper = service_layer::SL_OBJOP_DELETE;
                } else {
                    fprintf (stderr, "Requires: %s --route_oper (Add), (Update), (Delete) \n", argv[0]);
                    return 1;
                }
                break;
            case 'w':
                dummy = optarg;
                if (dummy == "Register") {
                    env_data.vrf_reg_oper = service_layer::SL_REGOP_REGISTER;
                } else if (dummy == "Unregister") {
                    env_data.vrf_reg_oper = service_layer::SL_REGOP_UNREGISTER;
                } else if (dummy == "EOF") {
                    env_data.vrf_reg_oper = service_layer::SL_REGOP_EOF;
                } else {
                    fprintf (stderr, "Requires: %s --vrf_reg_oper (Register), (Unregister), (EOF) \n", argv[0]);
                    return 1;
                }
                break;
            case 'b':
                env_data.num_operations = std::stoi(optarg);
                break;
            case 'c':
                env_data.batch_size = std::stoi(optarg);
                break;
            case 'x':
                dummy = optarg;
                if(dummy == "false") {
                    env_data.stream_case = false;
                }
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
                env_data.first_mpls_path_nhip = optarg;
                break;
            case 'n':
                env_data.next_hop_interface_mpls = optarg;
                break;
            case 'o':
                env_data.start_label = std::stoi(optarg);
                break;
            case 'q':
                env_data.num_paths = std::stoi(optarg);
                break;
            case 'r':
                dummy = optarg;
                if(dummy == "ipv6") {
                    env_data.create_path_group_for = service_layer::SL_IPv6_ROUTE_TABLE;
                } else if (dummy == "mpls") {
                    env_data.create_path_group_for = service_layer::SL_MPLS_LABEL_TABLE;
                } else {
                    env_data.create_path_group_for = service_layer::SL_IPv4_ROUTE_TABLE;
                }
                break;
            case 'y':
                env_data.pg_name = optarg;
                break;
            case 's':
                dummy = optarg;
                if (dummy == "true") {
                    global_init_rpc = true;
                }
                break;

            case 'h':
                LOG(INFO) << "Usage:";
                LOG(INFO) << "Required Arguments: ";
                LOG(INFO) << "| -u/--username                    | Username (Required argument) |";
                LOG(INFO) << "| -p/--password                    | Password (Required argument) |";
                LOG(INFO) << "| -a/--route_oper                  | Route Operation: Add, Update, Delete (Required argument) |";
                LOG(INFO) << "| -w/--vrf_reg_oper                | VRF registration Operation: Register, Unregister, EOF. When Unregister, all existing pushed routes will be deleted and route pushing will not be performed. Remember to specific correct table_type when Unregistering (Required argument) |";
                LOG(INFO) << "Optional arguments you can set in environment:";
                LOG(INFO) << "| -h/--help                        | Help |";
                LOG(INFO) << "| -t/--table_type                  | Specify whether to do ipv4, ipv6 or mpls operation, PG (default ipv4) |";
                LOG(INFO) << "| -v/--slaf                        | Specify if you want to use slaf proto RPCs to program objects or not. If not, no other configuration possible and will only run 100k ipv4 routes (default true) |";
                LOG(INFO) << "| -s/--global_init                 | Enable our Async Global Init RPC to handshake the API version number with the server (default false) |";
                LOG(INFO) << "| -b/--num_operations              | Configure the number of ipv4 routes, ipv6 routes, or MPLS entires to be added to a batch. If table_type is set to pg then 0 < num_operations <= 64 (default 1) |";
                LOG(INFO) << "| -c/--batch_size                  | Configure the number of ipv4 routes ipv6 routes, or ILM entires for MPLS to be added to a batch (default 1024) |";
                LOG(INFO) << "| -x/--stream_case                 | Want to use the streaming rpc or unary rpc (default true) |";
                LOG(INFO) << "| -y/--path_group_name             | Configure the name of the path group to use. This is the name for the new path you want to create when when table_type is set to pg."
                               << "When table_type is any other option then this will specify the existing path group to use for pushing routes. In this case, make sure path group name exist (default "") | \n";
                LOG(INFO) << "IPv4 Testing";
                LOG(INFO) << "| -d/--first_prefix_ipv4           | Configure the starting address for this test for IPV4 (default 40.0.0.0) |";
                LOG(INFO) << "| -e/--prefix_len_ipv4             | Configure the prefix length for this test for IPV4 address (default 24) |";
                LOG(INFO) << "| -f/--next_hop_interface_ipv4     | Configure the next hop interface for IPV4 (default Bundle-Ether1) |";
                LOG(INFO) << "| -g/--next_hop_ip_ipv4            | Configure the next hop ip address for IPV4 (default 14.1.1.10) | \n";
                LOG(INFO) << "IPv6 Testing";
                LOG(INFO) << "| -i/--first_prefix_ipv6           | Configure the starting address for this test for IPV6 (default 2002:aa::0) |";
                LOG(INFO) << "| -j/--prefix_len_ipv6             | Configure the prefix length for this test for IPV6 address (default 64) |";
                LOG(INFO) << "| -k/--next_hop_interface_ipv6     | Configure the next hop interface for IPV6 (default Bundle-Ether1) |";
                LOG(INFO) << "| -l/--next_hop_ip_ipv6            | Configure the next hop ip address for IPV6 (default 2002:ae::3) | \n";
                LOG(INFO) << "MPLS Testing";
                LOG(INFO) << "| -m/--first_mpls_path_nhip        | Configure the starting address for this test for MPLS (default 11.0.0.1) |";
                LOG(INFO) << "| -n/--next_hop_interface_mpls     | Configure the next hop interface for MPLS (default FourHundredGigE0/0/0/0) |";
                LOG(INFO) << "| -o/--start_label                 | Configure the starting label for this test for MPLS (default 20000) |";
                LOG(INFO) << "| -q/--num_paths                   | Configure the number of paths for MPLS labels (default 1)";
                LOG(INFO) << "PG Testing";
                LOG(INFO) << "| -r/--create_path_group_for       | Configure the table_type for which path group is being made (default ipv4)";
                return 1;
            case 'u':
                username = optarg;
                break;
            case 'p':
                password = optarg;
                break;
            case 'v':
                dummy = optarg;
                if(dummy == "false") {
                    version2 = false;
                }
                break;
            default:
                fprintf (stderr, "usage: %s --username --password --route_oper --vrf_reg_oper\n", argv[0]);
                return 1;
        }
    }

    if(username == "" || password == ""){
        LOG(INFO) << "Did not provide a Username and Password";
    }
    if(env_data.route_oper == service_layer::SL_OBJOP_RESERVED && env_data.vrf_reg_oper != service_layer::SL_REGOP_UNREGISTER) {
        LOG(ERROR) << "Need to provide the route_oper. Or set vrf_reg_oper to Unregister";
        return 0;
    }

    std::string grpc_server = server_ip + ":" + server_port;
    LOG(INFO) << "Connecting IOS-XR to gRPC server at " << grpc_server;
    auto channel = grpc::CreateChannel(grpc_server, grpc::InsecureChannelCredentials());

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
        try_route_push_slaf(channel, grpc_server, env_data);
        if (global_init_rpc) {
            asynchandler.Shutdown();
            thread_.join();
        }

    } else {
        try_route_push(channel, grpc_server, env_data);
        if (global_init_rpc) {
            asynchandler.Shutdown();
            thread_.join();
        }
    }

    return 0;
}

