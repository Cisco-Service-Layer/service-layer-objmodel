#include "ServiceLayerRoutev2.h"
#include <google/protobuf/text_format.h>

using grpc::ClientContext;
using grpc::ClientReader;
using grpc::ClientReaderWriter;
using grpc::ClientWriter;
using grpc::CompletionQueue;
using grpc::Status;
using service_layer::SLInitMsg;
using service_layer::SLVersion;
using service_layer::SLGlobal;

dbStructure database;
// Mutex used for synchronize access for database
std::mutex db_mutex;

// Mutex used for condition variable, and synchronize access to read_finished
std::mutex finish_m;

// Used for indicating to main thread that the reader thread has received all responses
bool read_finished = false;
std::condition_variable finish_read_cv;

// Mutex used for synchronize the request_deque and condition variable
std::mutex deque_mutex;
std::condition_variable deque_cv;
std::deque<service_layer::SLAFMsg> request_deque;


SLAFRShuttle* slaf_route_shuttle;

// client id has to match for vrf registration (SLAFVrfRegOp) and the routes request (routeSLAFOp) and for unregistering (SLAFVrfRegOp) for ipv4 and ipv6.
// client id (Multi-client) is not supported for MPLS
std::string client_id = "521";

bool 
SLAFRShuttle::routeSLAFOp(service_layer::SLObjectOp routeOp,
                    service_layer::SLTableType addrFamily,
                    unsigned int timeout)
{

    service_layer::SLObjectOp route_op = routeOp;
    if(route_op == service_layer::SL_OBJOP_ADD) {
        routeOp = service_layer::SL_OBJOP_UPDATE;
    }
    route_msg.set_oper(route_op);
    auto stub_ = service_layer::SLAF::NewStub(channel);
    std::string address_family_str = "";
    service_layer::SLTableType addr_family = addrFamily;
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

    if (addr_family == service_layer::SL_IPv4_ROUTE_TABLE) {
        address_family_str = "IPV4";
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addr_family == service_layer::SL_IPv6_ROUTE_TABLE){
        address_family_str = "IPV6";
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addr_family == service_layer::SL_MPLS_LABEL_TABLE){
        address_family_str = "MPLS";
        // Multi-Client not supported in MPLS
    }

    //Issue the RPC         
    std::string s;

    if (google::protobuf::TextFormat::PrintToString(route_msg, &s)) {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Transmitted message: IOSXR-SL " << address_family_str << " " << s;
        VLOG(2) << "###########################" ;
    } else {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Message not valid (partial content: "
                  << route_msg.ShortDebugString() << ")";
        VLOG(2) << "###########################" ;
        return false;
    }

    // Perform the RPC
    status = stub_->SLAFOp(&context, route_msg, &route_msg_resp);

    if (status.ok()) {
        VLOG(1) << "RPC call was successful, checking response...";

        // Print Partial failures within the batch if applicable for responses
        bool route_error = false;
        for (int result = 0; result < route_msg_resp.results_size(); result++) {
                auto slerr_status = 
                static_cast<int>(route_msg_resp.results(result).errstatus().status());
                if (slerr_status != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
                    if (addr_family == service_layer::SL_IPv4_ROUTE_TABLE) {
                        LOG(ERROR) << "Error code for prefix: " 
                            << route_msg_resp.results(result).operation().afobject().ipv4route().prefix()
                            << " prefixlen: " 
                            << route_msg_resp.results(result).operation().afobject().ipv4route().prefixlen()
                            <<" is 0x"<< std::hex << slerr_status;
                    } else if (addr_family == service_layer::SL_IPv6_ROUTE_TABLE) {
                        LOG(ERROR) << "Error code for prefix: " 
                            << route_msg_resp.results(result).operation().afobject().ipv6route().prefix()
                            << " prefixlen: " 
                            << route_msg_resp.results(result).operation().afobject().ipv6route().prefix()
                            <<" is 0x"<< std::hex << slerr_status;
                    } else if (addr_family == service_layer::SL_MPLS_LABEL_TABLE){
                        LOG(ERROR) << "Error code for label: " 
                            << route_msg_resp.results(result).operation().afobject().mplslabel().locallabel()
                            <<" is 0x"<< std::hex << slerr_status;
                    }
                    route_error = true;
                }
        }
        if (!route_error) {
            VLOG(1) << address_family_str << " Route Operation:"<< route_op << " Successful";
        } else {
            VLOG(1) << address_family_str << " Route Operation:"<< route_op << " Unsuccessful";
            return false;
        }

    } else {
        LOG(ERROR) << "RPC failed, error code is " << status.error_code();
        return false; 
    }

    // Clear route batch before the next operation
    this->clearBatch();
    return true;
}

void 
readHelperUpdateDb(int result, service_layer::SLTableType addrFamily, service_layer::SLAFMsgRsp* respMsg, bool fibAndRib)
{
    db_mutex.lock();
    // Update db with status update for rib and/or fib ack
    if (addrFamily == service_layer::SL_IPv4_ROUTE_TABLE) {
        auto prefix_index = respMsg->results(result).operation().afobject().ipv4route().prefix();
        if (fibAndRib == true) {
            database.db_ipv4[prefix_index].second.fib_success = true;
        } else {
            database.db_ipv4[prefix_index].second.rib_success = true;
        }
    } else if (addrFamily == service_layer::SL_IPv6_ROUTE_TABLE) {
        auto prefix_index = respMsg->results(result).operation().afobject().ipv6route().prefix();
        if (fibAndRib == true) {
            database.db_ipv6[prefix_index].second.fib_success = true;
        } else {
            database.db_ipv6[prefix_index].second.rib_success = true;
        }
    } else if (addrFamily == service_layer::SL_MPLS_LABEL_TABLE) {
        auto label_index = respMsg->results(result).operation().afobject().mplslabel().locallabel();
        if (fibAndRib == true) {
            database.db_mpls[label_index].second.fib_success = true;
        } else {
            database.db_mpls[label_index].second.rib_success = true;
        }
    }
    db_mutex.unlock();
}

void 
readHelperError(int result, service_layer::SLTableType addrFamily, service_layer::SLAFMsgRsp* respMsg, int errStatus)
{
    db_mutex.lock();
    // If any errors occur, then place any error messages in the db objects
    if (addrFamily == service_layer::SL_IPv4_ROUTE_TABLE) {
        std::stringstream temp;
        temp << "Error code for prefix: " 
            << respMsg->results(result).operation().afobject().ipv4route().prefix()
            << " prefixlen: " 
            << respMsg->results(result).operation().afobject().ipv4route().prefixlen()
            <<" is 0x"<< std::hex << errStatus;
        std::string error_message = temp.str();

        auto prefix_index = respMsg->results(result).operation().afobject().ipv4route().prefix();
        database.db_ipv4[prefix_index].second.error = error_message;
    } else if (addrFamily == service_layer::SL_IPv6_ROUTE_TABLE) {
        std::stringstream temp;
        temp << "Error code for prefix: " 
            << respMsg->results(result).operation().afobject().ipv6route().prefix()
            << " prefixlen: " 
            << respMsg->results(result).operation().afobject().ipv6route().prefix()
            <<" is 0x"<< std::hex << errStatus;
        std::string error_message = temp.str();

        auto prefix_index = respMsg->results(result).operation().afobject().ipv6route().prefix();
        database.db_ipv6[prefix_index].second.error = error_message;
    } else if (addrFamily == service_layer::SL_MPLS_LABEL_TABLE) {
        std::stringstream temp;
        temp << "Error code for label: " 
            << respMsg->results(result).operation().afobject().mplslabel().locallabel()
            <<" is 0x"<< std::hex << errStatus;
        std::string error_message = temp.str();

        auto label_index = respMsg->results(result).operation().afobject().mplslabel().locallabel();
        database.db_mpls[label_index].second.error = error_message;
    }
    db_mutex.unlock();
}

void
SLAFRShuttle::readStream(std::shared_ptr<grpc::ClientReaderWriter<service_layer::SLAFMsg, service_layer::SLAFMsgRsp>>& stream, service_layer::SLTableType addrFamily,  service_layer::SLObjectOp routeOper, std::string addressFamilyStr)
{
    // Reader thread listens to any responses from the server
    service_layer::SLAFMsgRsp resp_msg;

    int read_count = 0;

    // Waits for response until stream closes, timeout occurs, or response is given
    while (stream->Read(&resp_msg)) {

       // Print Partial failures within the batch if applicable for responses and updated RIB or RIB && FIB ACK
        bool route_error = false;
        for (int result = 0; result < resp_msg.results_size(); result++) {
            auto ack_type = static_cast<int>(resp_msg.results(result).operation().acktype());
            // For RIB Response
            if (ack_type == service_layer::RIB_ACK) {
                auto slerr_status = static_cast<int>(resp_msg.results(result).errstatus().status());
                if (slerr_status != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
                    readHelperError(result,addrFamily,&resp_msg,slerr_status);
                    route_error = true;
                } else {
                    // update with rib or rib and fib when that get's implemented
                    readHelperUpdateDb(result,addrFamily,&resp_msg,false);
                }

            } else if (ack_type == service_layer::RIB_AND_FIB_ACK) {
                // For Fib Response. Only do this if ackType is fib
                auto slerr_status = static_cast<int>(resp_msg.results(result).fibstatus().errorcode().status());
                if (slerr_status != service_layer::SLErrorStatus_SLErrno_SL_FIB_SUCCESS) {
                    readHelperError(result,addrFamily,&resp_msg,slerr_status);
                    route_error = true;
                } else {
                    // update with rib and fib when that get's implemented
                    readHelperUpdateDb(result,addrFamily,&resp_msg,true);
                }
            }
            read_count++;
        }

        if (!route_error) {
            VLOG(1) << addressFamilyStr << " Route Operation:"<< routeOper << " Successful";
        } else {
            VLOG(1) << addressFamilyStr << " Route Operation:"<< routeOper << " Unsuccessful";
        }

        db_mutex.lock();
        // Signifies we have finished all reads
        if(read_count == database.db_count){
            // Notifies main thread to send poison pill
            std::unique_lock<std::mutex> lck(finish_m);
            read_finished = true;
            finish_read_cv.notify_all();
        }
        db_mutex.unlock();
    }
}

void
SLAFRShuttle::writeStream(std::shared_ptr<grpc::ClientReaderWriter<service_layer::SLAFMsg, service_layer::SLAFMsgRsp>>& stream, std::string addressFamilyStr)
{
    bool check_stream_open = true;

    // Writer thread listens to the queue indefinitely, until given poison pill by main thread or timeout occurs
    while(check_stream_open) {
        // Need to get a lock for this dequeue. Will unlock when out of scope
        std::unique_lock<std::mutex> lck(deque_mutex);
        // Wait for the lock along with the deque to be non-empty
        deque_cv.wait(lck, []() { return !request_deque.empty(); });
            service_layer::SLAFMsg message;
            message = request_deque.front();
            request_deque.pop_front();

            // vrfname is a const string
            if(message.vrfname() == "poison_pill") {
                check_stream_open = false;
                break;
            }

            //Issue the RPC
            std::string s;

            if (google::protobuf::TextFormat::PrintToString(message, &s)) {
                VLOG(2) << "###########################" ;
                VLOG(2) << "Transmitted message: IOSXR-SL " << addressFamilyStr << " " << s;
                VLOG(2) << "###########################" ;
            } else {
                VLOG(2) << "###########################" ;
                VLOG(2) << "Message not valid (partial content: "
                        << message.ShortDebugString() << ")";
                VLOG(2) << "###########################" ;
            }
            // Send the write request
            check_stream_open = stream->Write(message);
        // }
    }
    // Signifies the stream write is finished and stops stream
    stream->WritesDone();
}

void 
SLAFRShuttle::stopStream(std::thread* reader, std::thread* writer)
{
    // Wait for all reads to finish before sending poison pill
    std::unique_lock<std::mutex> lck(finish_m);
    finish_read_cv.wait(lck, []() { return read_finished; });

    this->setVrfV4("poison_pill");
    this->routeSLAFOpStreamHelperEnqueue();
    writer->join();
    reader->join();
}
void 
SLAFRShuttle::routeSLAFOpStreamHelperEnqueue()
{
    // lock the queue before pushing SL-API objects to it
    std::unique_lock<std::mutex> lck(deque_mutex);
    request_deque.push_back(route_msg);
    deque_cv.notify_one();
    this->clearBatch();
}
unsigned int 
SLAFRShuttle::routeSLAFOpStream(service_layer::SLTableType addrFamily, service_layer::SLObjectOp routeOper, unsigned int timeout)
{
    // Create the channel object first and start the streaming operation
    auto stub_ = service_layer::SLAF::NewStub(channel);

    // Context for the client. It could be used to convey extra information to the server and/or tweak certain RPC behaviors.
    grpc::ClientContext context;

    // Storage for the status of the RPC upon completion.
    grpc::Status status;

    // Set timeout for RPC
    std::chrono::system_clock::time_point deadline =
        std::chrono::system_clock::now() + std::chrono::seconds(timeout);

    // Setting metadata info in the context
    context.set_deadline(deadline);
    if (username.length() > 0) {
        context.AddMetadata("username", username);
    }
    if (password.length() > 0) {
        context.AddMetadata("password", password);
    }

    // Used for logging
    std::string address_family_str = "";
    if (addrFamily == service_layer::SL_IPv4_ROUTE_TABLE) {
        address_family_str = "IPV4";
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addrFamily == service_layer::SL_IPv6_ROUTE_TABLE){
        address_family_str = "IPV6";
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addrFamily == service_layer::SL_MPLS_LABEL_TABLE){
        address_family_str = "MPLS";
        // Multi-Client not supported in MPLS
    }

    // Send the RPC
    std::shared_ptr<grpc::ClientReaderWriter<service_layer::SLAFMsg, service_layer::SLAFMsgRsp>> stream(
        stub_->SLAFOpStream(&context));

    // Create the Reader Thread
    std::thread reader(this->readStream,std::ref(stream), addrFamily, routeOper, address_family_str);

    request_deque.clear();
    // Start Writer Thread
    std::thread writer(this->writeStream, std::ref(stream), address_family_str);

    this->setVrfV4("default");
    unsigned int route_count = 0;
    unsigned int total_routes = 0;

    // Makes batches from db objects and pushes into request queue
    if (addrFamily == service_layer::SL_IPv4_ROUTE_TABLE) {
        db_mutex.lock();
        auto ipv4_index = database.ipv4_start_index;
        auto ipv4_last = database.ipv4_last_index;
        auto batch_size = database.db_ipv4[ipv4_index].first.batch_size;
        // Every sequential key(prefix) in the ipv4 db is apart by an offset amount
        auto offset = 1 << 32 - database.db_ipv4[ipv4_index].first.prefix_len_ipv4;
        while (ipv4_index <= ipv4_last) {
            auto db_prefix = ipv4_index;
            uint8_t prefix_length = database.db_ipv4[ipv4_index].first.prefix_len_ipv4;
            // Helper function to set all attributes for SLAFMsg
            this->insertAddBatchV4(this->longToIpv4(db_prefix),
                                                prefix_length,
                                                99,
                                                database.db_ipv4[ipv4_index].first.next_hop_ip_ipv4,
                                                database.db_ipv4[ipv4_index].first.next_hop_interface_ipv4,
                                                database.db_ipv4[ipv4_index].first.route_oper);
            route_count++;
            // When maximum allowed batch size is reached or no more remaining routes exist, we need to enqueue that object.
            if(route_count == batch_size || ipv4_index == ipv4_last){
                total_routes += route_count;
                route_count = 0;
                // Write should just pull from queue and be able to send request
                route_msg.set_oper(database.db_ipv4[ipv4_index].first.route_oper);
                db_mutex.unlock();
                this->routeSLAFOpStreamHelperEnqueue();
                db_mutex.lock();
            }
            ipv4_index+= offset;
        }
        db_mutex.unlock();
    } else if (addrFamily == service_layer::SL_IPv6_ROUTE_TABLE) {
        auto ipv6_index = database.db_ipv6.begin();
        // We hardcoded two routes pushed, thus we iterate through entire db mapping
        while (ipv6_index != database.db_ipv6.end()) {
            db_mutex.lock();
            auto db_prefix = ipv6_index->first;
            uint8_t prefix_length = ipv6_index->second.first.prefix_len_ipv6;
            slaf_route_shuttle->insertAddBatchV6(slaf_route_shuttle->ByteArrayStringtoIpv6(db_prefix),
                                            prefix_length,
                                            99,
                                            ipv6_index->second.first.next_hop_ip_ipv6,
                                            ipv6_index->second.first.next_hop_interface_ipv6,
                                            ipv6_index->second.first.route_oper);
            route_msg.set_oper(ipv6_index->second.first.route_oper);
            db_mutex.unlock();
            ipv6_index++;
            route_count++;
        }
        total_routes += route_count;
        this->routeSLAFOpStreamHelperEnqueue();
    } else if (addrFamily == service_layer::SL_MPLS_LABEL_TABLE) {
        db_mutex.lock();
        auto mpls_index = database.mpls_start_index;
        auto mpls_last = database.mpls_last_index;
        unsigned int batch_size = database.db_mpls[mpls_index].first.batch_size;
        // Labels are incremented by 1
        while (mpls_index <= mpls_last) {
            auto db_label = mpls_index;
            auto start_label = database.db_mpls[mpls_index].first.start_label;
            auto next_hop_address = this->ipv4ToLong(database.db_mpls[mpls_index].first.first_mpls_path_nhip.c_str());
            this->batchHelperMPLS(db_label,
                                start_label,
                                database.db_mpls[mpls_index].first.num_paths,
                                next_hop_address,
                                database.db_mpls[mpls_index].first.next_hop_interface_mpls);
            route_count++;

            // When maximum allowed batch size is reached or no more remaining labels exist, we need to enqueue that object.
            if(route_count == batch_size || mpls_index == mpls_last){
                total_routes += route_count;
                route_count = 0;
                // Write thread should just pull from queue and be able to send request, thus set_oper here
                route_msg.set_oper(database.db_mpls[mpls_index].first.route_oper);
                db_mutex.unlock();
                this->routeSLAFOpStreamHelperEnqueue();
                db_mutex.lock();
            }
            mpls_index++;
        }
        db_mutex.unlock();
    }

    stopStream(&reader,&writer);
    status = stream->Finish();
    if (!status.ok()) {
        LOG(ERROR) << "RPC failed, error code is " << status.error_code();
    }
    return total_routes;
}

void 
SLAFRShuttle::clearDB()
{
    database.db_ipv4.clear();
    database.db_ipv6.clear();
    database.db_mpls.clear();
}
void 
SLAFRShuttle::clearBatch()
{
   route_msg.clear_oplist();
   prefix_map_v4.clear();
   prefix_map_v6.clear();
}

uint32_t
SLAFRShuttle::ipv4ToLong(const char* address)
{
    struct sockaddr_in sa;
    if (inet_pton(AF_INET, address, &(sa.sin_addr)) != 1) {
        LOG(ERROR) << "Invalid IPv4 address " << address; 
        return 0;
    }

    return ntohl(sa.sin_addr.s_addr);
}

std::string 
SLAFRShuttle::longToIpv4(uint32_t nlprefix)
{
    struct sockaddr_in sa;
    char str[INET_ADDRSTRLEN];

    // Convert to hostbyte first form
    uint32_t hlprefix = htonl(nlprefix);

    sa.sin_addr.s_addr = hlprefix;

    if (inet_ntop(AF_INET,  &(sa.sin_addr), str, INET_ADDRSTRLEN)) {
        return std::string(str);
    } else {
        LOG(ERROR) << "inet_ntop conversion error: "<< strerror(errno);
        return std::string("");
    }
}


std::string 
SLAFRShuttle::ipv6ToByteArrayString(const char* address)
{
    struct in6_addr ipv6data;
    if (inet_pton(AF_INET6, address, &ipv6data) != 1 ) {
        LOG(ERROR) << "Invalid IPv6 address " << address; 
        return std::string("");
    }

    const char *ptr(reinterpret_cast<const char*>(&ipv6data.s6_addr));
    std::string ipv6_charstr(ptr, ptr+16);
    return ipv6_charstr;
}


std::string 
SLAFRShuttle::ByteArrayStringtoIpv6(std::string ipv6ByteArray)
{

    struct in6_addr ipv6data;
    char str[INET6_ADDRSTRLEN];

    std::copy(ipv6ByteArray.begin(), ipv6ByteArray.end(),ipv6data.s6_addr);


    if (inet_ntop(AF_INET6,  &(ipv6data), str, INET6_ADDRSTRLEN)) {
        return std::string(str);
    } else {
        LOG(ERROR) << "inet_ntop conversion error: "<< strerror(errno);
        return std::string("");
    }
}

SLAFRShuttle::SLAFRShuttle(std::shared_ptr<grpc::Channel> Channel, std::string Username,
                   std::string Password)
    : channel(Channel), username(Username), password(Password) {} 


void 
SLAFRShuttle::setVrfV4(std::string vrfName)
{
    route_msg.set_vrfname(vrfName);
}

// Overloaded routev4Add to be used if vrfname is already set

service_layer::SLRoutev4*
SLAFRShuttle::routev4Add()
{
    if (route_msg.vrfname().empty()) {
        LOG(ERROR) << "vrfname is empty, please set vrf "
                   << "before manipulating routes";
        return 0;
    } else {
        service_layer::SLAFOp* operation = route_msg.add_oplist();
        service_layer::SLAFObject* af_object = operation->mutable_afobject();
        service_layer::SLRoutev4* routev4Ptr = af_object->mutable_ipv4route();
        return routev4Ptr;
    }
}

service_layer::SLRoutev4* 
SLAFRShuttle::routev4Add(std::string vrfName)
{
    route_msg.set_vrfname(vrfName);
    service_layer::SLAFOp* operation = route_msg.add_oplist();
    service_layer::SLAFObject* af_object = operation->mutable_afobject();
    service_layer::SLRoutev4* routev4Ptr = af_object->mutable_ipv4route();
    return routev4Ptr;
}

// Overloaded method to Set V4 route without Admin Distance.
// Used for DELETE Operation

void 
SLAFRShuttle::routev4Set(service_layer::SLRoutev4* routev4Ptr,
                     uint32_t prefix,
                     uint8_t prefixLen)
{   
    routev4Ptr->set_prefix(prefix);
    routev4Ptr->set_prefixlen(prefixLen);
}


// Overloaded method to Set V4 route without Admin Distance.
// Used for ADD or UPDATE Operation


void 
SLAFRShuttle::routev4Set(service_layer::SLRoutev4* routev4Ptr,
                     uint32_t prefix,
                     uint8_t prefixLen,
                     uint32_t adminDistance)
{
    routev4Ptr->set_prefix(prefix);
    routev4Ptr->set_prefixlen(prefixLen);
    routev4Ptr->mutable_routecommon()->set_admindistance(adminDistance);
}


void 
SLAFRShuttle::routev4PathAdd(service_layer::SLRoutev4* routev4Ptr,
                         uint32_t nextHopAddress,
                         std::string nextHopIf)
{
    
    auto routev4PathPtr = routev4Ptr->add_pathlist();
    routev4PathPtr->mutable_nexthopaddress()->set_v4address(nextHopAddress);
    routev4PathPtr->mutable_nexthopinterface()->set_name(nextHopIf);
}

bool 
SLAFRShuttle::insertAddBatchV4(std::string prefix,
                           uint8_t prefixLen,
                           uint32_t adminDistance,
                           std::string nextHopAddress,
                           std::string nextHopIf,
                           service_layer::SLObjectOp routeOper)
{

    auto address = prefix + "/" + std::to_string(prefixLen);
    auto map_index = route_msg.oplist_size();

    if (this->prefix_map_v4.find(address) == this->prefix_map_v4.end()) {
        // Obtain pointer to a new route object within route batch
        auto routev4_ptr = this->routev4Add();

        if (!routev4_ptr) {
            LOG(ERROR) << "Failed to create new route object";
            return false;
        }

        // Set up the new v4 route object
        this->routev4Set(routev4_ptr, 
                         ipv4ToLong(prefix.c_str()),
                         prefixLen, 
                         adminDistance);
        this->prefix_map_v4[address] = map_index;

         /* We dont need to setup the paths for DELETE*/
        if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
            this->routev4PathAdd(routev4_ptr, 
                             ipv4ToLong(nextHopAddress.c_str()), 
                             nextHopIf); 
        }

    } else {
        // no need to make a new route object as one already exists within this route batch
        auto operation = route_msg.mutable_oplist(prefix_map_v4[address]);
        auto af_object = operation->mutable_afobject();
        auto routev4_ptr = af_object->mutable_ipv4route();
         /* We dont need to setup the paths for DELETE*/
        if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
            this->routev4PathAdd(routev4_ptr, 
                             ipv4ToLong(nextHopAddress.c_str()), 
                             nextHopIf); 
        }
    }

    return true;
}

// V6 methods

void
SLAFRShuttle::setVrfV6(std::string vrfName)
{
    route_msg.set_vrfname(vrfName);
}

// Overloaded routev6Add to be used if vrfname is already set

service_layer::SLRoutev6*
SLAFRShuttle::routev6Add()
{
    if (route_msg.vrfname().empty()) {
        LOG(ERROR) << "vrfname is empty, please set vrf " 
                   << "before manipulating v6 routes";
        return 0;
    } else {
        service_layer::SLAFOp* operation = route_msg.add_oplist();
        service_layer::SLAFObject* af_object = operation->mutable_afobject();
        service_layer::SLRoutev6* routev6Ptr = af_object->mutable_ipv6route();
        return routev6Ptr;
    }
}


service_layer::SLRoutev6*
  SLAFRShuttle::routev6Add(std::string vrfName)
{
    route_msg.set_vrfname(vrfName);
    service_layer::SLAFOp* operation = route_msg.add_oplist();
    service_layer::SLAFObject* af_object = operation->mutable_afobject();
    service_layer::SLRoutev6* routev6Ptr = af_object->mutable_ipv6route();
    return routev6Ptr;
}


// Overloaded method to Set V6 route without Admin Distance.
// Used for DELETE Operation

void 
SLAFRShuttle::routev6Set(service_layer::SLRoutev6* routev6Ptr,
                     std::string prefix,
                     uint8_t prefixLen)
{
    routev6Ptr->set_prefix(prefix);
    routev6Ptr->set_prefixlen(prefixLen);
}


// Overloaded method to Set V6 route without Admin Distance.
// Used for ADD or UPDATE Operation

void 
SLAFRShuttle::routev6Set(service_layer::SLRoutev6* routev6Ptr,
                     std::string prefix,
                     uint8_t prefixLen,
                     uint32_t adminDistance)
{
    routev6Ptr->set_prefix(prefix);
    routev6Ptr->set_prefixlen(prefixLen);
    routev6Ptr->mutable_routecommon()->set_admindistance(adminDistance);
}

void 
SLAFRShuttle::routev6PathAdd(service_layer::SLRoutev6* routev6Ptr,
                         std::string nextHopAddress,
                         std::string nextHopIf)
{

    auto routev6PathPtr = routev6Ptr->add_pathlist();
    routev6PathPtr->mutable_nexthopaddress()->set_v6address(nextHopAddress);
    routev6PathPtr->mutable_nexthopinterface()->set_name(nextHopIf);
}


bool 
SLAFRShuttle::insertAddBatchV6(std::string prefix,
                           uint8_t prefixLen,
                           uint32_t adminDistance,
                           std::string nextHopAddress,
                           std::string nextHopIf,
                           service_layer::SLObjectOp routeOper)
{
    auto address = prefix + "/" + std::to_string(prefixLen);
    auto map_index = route_msg.oplist_size();

    if (this->prefix_map_v6.find(address) == this->prefix_map_v6.end()) {
        // Obtain pointer to a new route object within route batch
        auto routev6_ptr = this->routev6Add();

        if (!routev6_ptr) {
            LOG(ERROR) << "Failed to create new route object";
            return false;
        }

        // Set up the new v6 route object
        this->routev6Set(routev6_ptr, 
                         ipv6ToByteArrayString(prefix.c_str()),
                         prefixLen, 
                         adminDistance);
        this->prefix_map_v6[address] = map_index;

         /* We dont need to setup the paths for DELETE*/
        if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
            this->routev6PathAdd(routev6_ptr,
                             ipv6ToByteArrayString(nextHopAddress.c_str()),
                             nextHopIf);
        }
    } else {
        // no need to make a new route object as one already exists within this route batch
        auto operation = route_msg.mutable_oplist(prefix_map_v6[address]);
        auto af_object = operation->mutable_afobject();
        auto routev6_ptr = af_object->mutable_ipv6route();
         /* We dont need to setup the paths for DELETE*/
        if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
            this->routev6PathAdd(routev6_ptr,
                             ipv6ToByteArrayString(nextHopAddress.c_str()),
                             nextHopIf);
        }
    }

    return true;
}
void
SLAFRShuttle::batchHelperMPLS(unsigned int label,
                            unsigned int startLabel,
                            unsigned int numPaths,
                            uint32_t nextHopAddress,
                            std::string nextHopInterface) {

    /* Create a new ilm entry, and the only way to do that with the current proto file
            is to add a new oplist */
    service_layer::SLAFOp* operation = route_msg.add_oplist();
    service_layer::SLAFObject* af_object = operation->mutable_afobject();
    service_layer::SLMplsEntry* ilm = af_object->mutable_mplslabel();
    ilm->set_locallabel(label);

    // Multiple path in entry
    for(int pathIdx = 0; pathIdx < numPaths; pathIdx++){
        service_layer::SLRoutePath* nhlfe = ilm->add_pathlist();
        service_layer::SLIpAddress* slip_add = nhlfe->mutable_nexthopaddress();
        slip_add->set_v4address(nextHopAddress);
        if (nextHopInterface.length() != 0){
            service_layer::SLInterface* sli_add = nhlfe->mutable_nexthopinterface();
            sli_add->set_name(nextHopInterface);
        }
        if (startLabel > 0) {
            int out_label = startLabel;
            nhlfe->add_labelstack(out_label);
        }
    }
}
unsigned int
SLAFRShuttle::insertAddBatchMPLS(unsigned int startLabel,
                            unsigned int numLabel,
                            unsigned int numPaths,
                            unsigned int batchSize,
                            uint32_t nextHopAddress,
                            std::string nextHopInterface,
                            service_layer::SLObjectOp routeOper)
{
    unsigned int sent_mpls_entries = 0;
    unsigned int mpls_entries_in_batch = 0;
    unsigned int batch_index = 0;
    unsigned int label = startLabel;
    unsigned int total_mpls_entries = 0;
    unsigned int num_mpls_entries = 1;
    total_mpls_entries = numLabel * num_mpls_entries;

    if (batchSize > total_mpls_entries) {
        batchSize = total_mpls_entries;
    }

    // Currently no support within proto for EXP entries
    while(sent_mpls_entries < total_mpls_entries){
        this->batchHelperMPLS(label,startLabel,numPaths,nextHopAddress,nextHopInterface);
        sent_mpls_entries = sent_mpls_entries + num_mpls_entries;
        mpls_entries_in_batch += num_mpls_entries;
        label++;

        if (mpls_entries_in_batch == batchSize || sent_mpls_entries == total_mpls_entries)  {
            batch_index++;
            mpls_entries_in_batch = 0;
            slaf_route_shuttle->routeSLAFOp(routeOper, service_layer::SL_MPLS_LABEL_TABLE);
        }
    }

    LOG(INFO) << "Number of Batches Sent: " << batch_index << "\n";
    return sent_mpls_entries;
}

// Version 2 SLAFVFR ----------------------------------------------------------------------------------

SLAFVrf::SLAFVrf(std::shared_ptr<grpc::Channel> Channel, std::string Username, std::string Password)
    : channel(Channel), username(Username), password(Password) {}

// Overloaded variant of afVrfRegMsgAdd without adminDistance and Purgeinterval
// Suitable for VRF UNREGISTER and REGISTER operations

void 
SLAFVrf::afVrfRegMsgAdd(std::string vrfName,
                        service_layer::SLTableType addrFamily)
{

    // Get a pointer to a new af_vrf_reg entry in af_vrf_msg
    service_layer::SLAFVrfReg* af_vrf_reg = af_vrf_msg.add_vrfregmsgs();
    af_vrf_reg->set_table(addrFamily);

    // Get pointer to a new vrf_rg in af_vrf_reg
    service_layer::SLVrfReg* vrf_reg = af_vrf_reg->mutable_vrfreg();
    // Populate the new vrf_reg entry
    vrf_reg->set_vrfname(vrfName);
}

// Overloaded variant of afVrfRegMsgAdd with adminDistance and Purgeinterval
// Suitable for VRF REGISTER

void
SLAFVrf::afVrfRegMsgAdd(std::string vrfName,
                    unsigned int adminDistance,
                    unsigned int vrfPurgeIntervalSeconds,
                    service_layer::SLTableType addrFamily)
{
    // Get a pointer to a new af_vrf_reg entry in af_vrf_msg
    service_layer::SLAFVrfReg* af_vrf_reg = af_vrf_msg.add_vrfregmsgs();
    af_vrf_reg->set_table(addrFamily);

    // Get pointer to a new vrf_rg in af_vrf_reg
    service_layer::SLVrfReg* vrf_reg = af_vrf_reg->mutable_vrfreg();

    // Populate the new vrf_reg entry
    vrf_reg->set_vrfname(vrfName);
    vrf_reg->set_admindistance(adminDistance);
    vrf_reg->set_vrfpurgeintervalseconds(vrfPurgeIntervalSeconds);
}


bool 
SLAFVrf::registerAfVrf(service_layer::SLTableType addrFamily, service_layer::SLRegOp vrfRegOper)
{
    // Send an RPC for VRF registrations

    switch(addrFamily) {
    case service_layer::SL_IPv4_ROUTE_TABLE:
        // Issue VRF Register RPC 
        if (afVrfOpAddFam(vrfRegOper, addrFamily)) {
            return true;
        } else {
            LOG(ERROR) << "Failed to send Register RP";
            return false;
        } 
        break;

    case service_layer::SL_IPv6_ROUTE_TABLE:
        // Issue VRF Register RPC
        if (afVrfOpAddFam(vrfRegOper, addrFamily)) {
            return true;
        } else {
            LOG(ERROR) << "Failed to send Register RPC";
            return false;
        }
        break;

    case service_layer::SL_MPLS_LABEL_TABLE:
        // Issue VRF Register RPC
        if (afVrfOpAddFam(vrfRegOper, addrFamily)) {
            return true;
        } else {
            LOG(ERROR) << "Failed to send Register RPC";
            return false;
        }
        break;

    default:
        LOG(ERROR) << "Invalid Address family, skipping..";
        return false;
        break;
    }

}

bool 
SLAFVrf::afVrfOpAddFam(service_layer::SLRegOp vrfOp, service_layer::SLTableType addrFamily)
{
    // Set up the SLAF Stub
    auto stub_ = service_layer::SLAF::NewStub(channel);

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
    if (username.length() > 0) {
        context.AddMetadata("username", username);
    }
    if (password.length() > 0) {
        context.AddMetadata("password", password);
    }

    if (addrFamily == service_layer::SL_IPv4_ROUTE_TABLE) {
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addrFamily == service_layer::SL_IPv6_ROUTE_TABLE) {
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addrFamily == service_layer::SL_MPLS_LABEL_TABLE) {
        // Multi-Client not supported in MPLS
    }

    // Set up afVrfRegMsg Operation
    af_vrf_msg.set_oper(vrfOp);

    std::string s;

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

    if (status.ok()) {
        VLOG(1) << "RPC call was successful, checking response...";


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
    } else {
        LOG(ERROR) << "RPC failed, error code is " << status.error_code();
        return false;
    }
}

// SLGLOBALSHUTTLE ----------------------------------------------------------------------------------
SLGLOBALSHUTTLE::SLGLOBALSHUTTLE(std::shared_ptr<grpc::Channel> Channel, std::string Username,
                   std::string Password)
    : channel(Channel), username(Username), password(Password) {} 

bool SLGLOBALSHUTTLE::getGlobals(unsigned int &batch_size, unsigned int timeout)
{
    auto stub_ = service_layer::SLGlobal::NewStub(channel);

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

    // Perform the RPC
    service_layer::SLGlobalsGetMsg get_msg;
    service_layer::SLGlobalsGetMsgRsp resp_msg;
    status = stub_->SLGlobalsGet(&context, get_msg, &resp_msg);

    if (status.ok()) {
        VLOG(1) << "RPC call was successful, checking response...";
        auto slerr_status = static_cast<int>(resp_msg.errstatus().status());

        if (slerr_status != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
            VLOG(1) << " GlobalsGet Operation: Unsuccessful";
            return false;
        }
    } else {
        LOG(ERROR) << "getGlobals RPC failed, error code is " << status.error_code();
        return false;
    }

    LOG(INFO) <<"MaxVrfNameLength:              " << resp_msg.maxvrfnamelength()  << std::endl;
    LOG(INFO) <<"MaxInterfaceNameLength:        " << resp_msg.maxinterfacenamelength()  << std::endl;
    LOG(INFO) <<"MaxPathsPerEntry:              " << resp_msg.maxpathsperentry()  << std::endl;
    LOG(INFO) <<"MaxPrimaryPathPerEntry:        " << resp_msg.maxprimarypathperentry()  << std::endl;
    LOG(INFO) <<"MaxBackupPathPerEntry:         " << resp_msg.maxbackuppathperentry()  << std::endl;
    LOG(INFO) <<"MaxMplsLabelsPerPath:          " << resp_msg.maxmplslabelsperpath()  << std::endl;
    LOG(INFO) <<"MinPrimaryPathIdNum:           " << resp_msg.minprimarypathidnum()  << std::endl;
    LOG(INFO) <<"MaxPrimaryPathIdNum:           " << resp_msg.maxprimarypathidnum()  << std::endl;
    LOG(INFO) <<"MinBackupPathIdNum:            " << resp_msg.minbackuppathidnum()  << std::endl;
    LOG(INFO) <<"MaxBackupPathIdNum:            " << resp_msg.maxbackuppathidnum()  << std::endl;
    LOG(INFO) <<"MaxRemoteAddressNum:           " << resp_msg.maxremoteaddressnum()  << std::endl;
    LOG(INFO) <<"MaxL2BdNameLength:             " << resp_msg.maxl2bdnamelength()  << std::endl;
    LOG(INFO) <<"MaxL2PmsiTunnelIdLength:       " << resp_msg.maxl2pmsitunnelidlength()  << std::endl;
    LOG(INFO) <<"MaxLabelBlockClientNameLength: " << resp_msg.maxlabelblockclientnamelength()  << std::endl;
    LOG(INFO) <<"MaxPathsInNexthopNotif:        " << resp_msg.maxpathsinnexthopnotif()  << std::endl;
    LOG(INFO) <<"MaxVrfRegPerMsg:               " << resp_msg.maxvrfregpermsg()  << std::endl;
    LOG(INFO) <<"MaxAFOpsPerMsg:                " << resp_msg.maxafopspermsg()  << std::endl;
    LOG(INFO) <<"MaxNotifReqPerSLAFNotifReq:    " << resp_msg.maxnotifreqperslafnotifreq()  << std::endl;

    batch_size = resp_msg.maxafopspermsg();

    if (batch_size == 0) {
        LOG(INFO) << "WARNING: BATCH SIZE is SET to 0";
    }

    return true;
}
