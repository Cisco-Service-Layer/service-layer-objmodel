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
std::deque<SLAFQueueMsg> request_deque;


SLAFRShuttle* slaf_route_shuttle;

// client id has to match for vrf registration (SLAFVrfRegOp) and the routes request (routeSLAFOp) and for unregistering (SLAFVrfRegOp) for ipv4 and ipv6.
// client id (Multi-client) is not supported for MPLS
std::string client_id = "521";

// Updates DB Objects with rib/fib success
void 
DbHelperUpdate(int result, service_layer::SLTableType addrFamily, service_layer::SLAFMsgRsp* respMsg, bool fibAndRib)
{
    // Update db with status update for rib and/or fib ack
    if (addrFamily == service_layer::SL_IPv4_ROUTE_TABLE) {
        auto prefix_index = respMsg->results(result).key().iprouteprefix().prefix().v4address();
        if (fibAndRib == true) {
            database.db_ipv4[prefix_index].second.fib_success = true;
        } else {
            database.db_ipv4[prefix_index].second.rib_success = true;
        }
    } else if (addrFamily == service_layer::SL_IPv6_ROUTE_TABLE) {
        auto prefix_index = respMsg->results(result).key().iprouteprefix().prefix().v6address();
        if (fibAndRib == true) {
            database.db_ipv6[prefix_index].second.fib_success = true;
        } else {
            database.db_ipv6[prefix_index].second.rib_success = true;
        }
    } else if (addrFamily == service_layer::SL_MPLS_LABEL_TABLE) {
        auto label_index = respMsg->results(result).key().mplslabel().label();
        if (fibAndRib == true) {
            database.db_mpls[label_index].second.fib_success = true;
        } else {
            database.db_mpls[label_index].second.rib_success = true;
        }
    } else if (addrFamily == service_layer::SL_PATH_GROUP_TABLE) {
        auto pg_index = respMsg->results(result).key().pathgroupid().name();
        if (fibAndRib == true) {
            database.db_pg[pg_index].second.fib_success = true;
        } else {
            database.db_pg[pg_index].second.rib_success = true;
        }
    }
}

// Update DB Objects with error messages
void 
DbHelperError(int result, service_layer::SLTableType addrFamily, service_layer::SLAFMsgRsp* respMsg, int errStatus, bool fib)
{
    // If any errors occur, then place any error messages in the db objects
    if (addrFamily == service_layer::SL_IPv4_ROUTE_TABLE) {
        std::stringstream temp;
        temp << "Error code for prefix: " 
            << respMsg->results(result).key().iprouteprefix().prefix().v4address()
            << " prefixlen: " 
            << respMsg->results(result).key().iprouteprefix().prefixlen()
            << " Operation ID: "
            << respMsg->results(result).operationid()
            << " is ";
        // When fib is true, add the FibStatus message which is not converted to hex
        if (fib) {
            temp << errStatus;
        } else {
            temp << "0x" << std::hex << errStatus;
        }
        std::string error_message = temp.str();

        auto prefix_index = respMsg->results(result).key().iprouteprefix().prefix().v4address();
        database.db_ipv4[prefix_index].second.error = error_message;
    } else if (addrFamily == service_layer::SL_IPv6_ROUTE_TABLE) {
        std::stringstream temp;
        temp << "Error code for prefix: " 
            << respMsg->results(result).key().iprouteprefix().prefix().v6address()
            << " prefixlen: " 
            << respMsg->results(result).key().iprouteprefix().prefixlen()
            << " Operation ID: "
            << respMsg->results(result).operationid()
            <<" is ";
        if (fib) {
            temp << errStatus;
        } else {
            temp << "0x" << std::hex << errStatus;
        }
        std::string error_message = temp.str();

        auto prefix_index = respMsg->results(result).key().iprouteprefix().prefix().v6address();
        database.db_ipv6[prefix_index].second.error = error_message;
    } else if (addrFamily == service_layer::SL_MPLS_LABEL_TABLE) {
        std::stringstream temp;
        temp << "Error code for label: " 
            << respMsg->results(result).key().mplslabel().label()
            << " Operation ID: "
            << respMsg->results(result).operationid()
            <<" is ";
        if (fib) {
            temp << errStatus;
        } else {
            temp << "0x" << std::hex << errStatus;
        }
        std::string error_message = temp.str();

        auto label_index = respMsg->results(result).key().mplslabel().label();
        database.db_mpls[label_index].second.error = error_message;
    } else if (addrFamily == service_layer::SL_PATH_GROUP_TABLE) {
        std::stringstream temp;
        temp << "Error code for pg: " 
            << respMsg->results(result).key().pathgroupid().name()
            << " Operation ID: "
            << respMsg->results(result).operationid()
            <<" is ";
        if (fib) {
            temp << errStatus;
        } else {
            temp << "0x" << std::hex << errStatus;
        }
        std::string error_message = temp.str();
        auto pg_index = respMsg->results(result).key().pathgroupid().name();
        database.db_pg[pg_index].second.error = error_message;
    }
}

// Puts objects from the DB into requests. Based on steam_case pushes onto request_queue or sends the request for unary
unsigned int
SLAFRShuttle::pushFromDB(bool streamCase, service_layer::SLObjectOp routeOper, service_layer::SLTableType addrFamily, service_layer::SLTableType createPathGroupFor)
{
    this->setVrfV4("default");
    unsigned int route_count = 0;
    unsigned int total_routes = 0;
    if (routeOper == service_layer::SL_OBJOP_ADD) {
        routeOper = service_layer::SL_OBJOP_UPDATE;
    }

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
            uint32_t prefix_length = database.db_ipv4[ipv4_index].first.prefix_len_ipv4;
            // Helper function to set all attributes for SLAFOpMsg
            this->insertAddBatchV4(this->longToIpv4(db_prefix),
                                                prefix_length,
                                                99,
                                                database.db_ipv4[ipv4_index].first.next_hop_ip_ipv4,
                                                database.db_ipv4[ipv4_index].first.next_hop_interface_ipv4,
                                                routeOper,
                                                database.db_ipv4[ipv4_index].first.pg_name,
                                                database.db_ipv4[ipv4_index].first.response_acks);
            route_count++;
            // When maximum allowed batch size is reached or no more remaining routes exist, we need to enqueue that object.
            if(route_count == batch_size || ipv4_index == ipv4_last){
                total_routes += route_count;
                route_count = 0;
                if (streamCase) {
                    // Write should just pull from queue and be able to send request
                    route_msg.set_oper(routeOper);
                    db_mutex.unlock();
                    this->routeSLAFOpStreamHelperEnqueue(false);
                    db_mutex.lock();
                } else {
                    this->routeSLAFOp(routeOper, addrFamily);
                }
            }
            ipv4_index+= offset;
        }
        db_mutex.unlock();
    } else if (addrFamily == service_layer::SL_IPv6_ROUTE_TABLE) {
        db_mutex.lock();
        auto ipv6_index = database.ipv6_start_index;
        auto ipv6_last = database.ipv6_last_index;
        auto batch_size = database.db_ipv6[ipv6_index].first.batch_size;
        // Every key(prefix) in incremented based off the prefix length
        uint32_t prefix_length = database.db_ipv6[ipv6_index].first.prefix_len_ipv6;

        // lexicographical order comparison
        while (ipv6_index <= ipv6_last) {
            auto db_prefix = ipv6_index;
            prefix_length = database.db_ipv6[ipv6_index].first.prefix_len_ipv6;
            this->insertAddBatchV6(slaf_route_shuttle->ByteArrayStringtoIpv6(db_prefix),
                                                prefix_length,
                                                99,
                                                database.db_ipv6[ipv6_index].first.next_hop_ip_ipv6,
                                                database.db_ipv6[ipv6_index].first.next_hop_interface_ipv6,
                                                routeOper,
                                                database.db_ipv6[ipv6_index].first.pg_name,
                                                database.db_ipv6[ipv6_index].first.response_acks);
            route_count++;
            // When maximum allowed batch size is reached or no more remaining routes exist, we need to enqueue that object.
            if(route_count == batch_size || ipv6_index == ipv6_last){
                total_routes += route_count;
                route_count = 0;
                if (streamCase) {
                    // Write should just pull from queue and be able to send request
                    route_msg.set_oper(routeOper);
                    db_mutex.unlock();
                    this->routeSLAFOpStreamHelperEnqueue(false);
                    db_mutex.lock();
                } else {
                    this->routeSLAFOp(routeOper, addrFamily);
                }
            }
            ipv6_index = this->incrementIpv6Pfx(ipv6_index, prefix_length);
        }
        db_mutex.unlock();
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
            this->insertAddBatchMPLS(db_label,
                                start_label,
                                database.db_mpls[mpls_index].first.num_paths,
                                next_hop_address,
                                database.db_mpls[mpls_index].first.next_hop_interface_mpls,
                                database.db_mpls[mpls_index].first.pg_name,
                                database.db_mpls[mpls_index].first.response_acks);
            route_count++;

            // When maximum allowed batch size is reached or no more remaining labels exist, we need to enqueue that object.
            if(route_count == batch_size || mpls_index == mpls_last){
                total_routes += route_count;
                route_count = 0;
                if (streamCase) {
                    // Write thread should just pull from queue and be able to send request, thus set_oper here
                    route_msg.set_oper(routeOper);
                    db_mutex.unlock();
                    this->routeSLAFOpStreamHelperEnqueue(false);
                    db_mutex.lock();
                } else {
                    this->routeSLAFOp(routeOper, addrFamily);
                }
            }
            mpls_index++;
        }
        db_mutex.unlock();
    } else if (addrFamily == service_layer::SL_PATH_GROUP_TABLE) {
        service_layer::SLAFOpMsg* operation = route_msg.add_oplist();
        service_layer::SLAFObject* af_object = operation->mutable_afobject();
        service_layer::SLPathGroup* pg_ptr = af_object->mutable_pathgroup();
        service_layer::SLObjectId* pg_id = pg_ptr->mutable_pathgroupid();
        service_layer::SLPathGroup_SLPathList* path_list = pg_ptr->mutable_pathlist();
        pg_ptr->set_admindistance(98);

        db_mutex.lock();
        auto pg_name = database.pg_name;
        operation->set_operationid(database.operation_id++);
        this->responseAckSet(operation, database.db_pg[pg_name].first.response_acks);
        pg_id->set_name(pg_name);

        // Set up the new v4 route object
        if (createPathGroupFor == service_layer::SL_IPv4_ROUTE_TABLE || createPathGroupFor == service_layer::SL_MPLS_LABEL_TABLE) {
            auto ipv4_index = database.ipv4_start_index;
            auto ipv4_last = database.ipv4_last_index;
            if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
                while (ipv4_index <= ipv4_last) {
                    auto db_prefix = ipv4_index;
                    service_layer::SLPathGroup_SLPath* path = path_list->add_paths();
                    service_layer::SLRoutePath* route_path = path->mutable_path();
                    route_path->mutable_nexthopaddress()->set_v4address(db_prefix);
                    route_path->mutable_nexthopinterface()->set_name(database.db_pg[pg_name].first.next_hop_interface_ipv4);
                    if (createPathGroupFor == service_layer::SL_MPLS_LABEL_TABLE) {
                        route_path->add_labelstack(database.db_pg[pg_name].first.start_label);
                    }
                    route_count++;
                    ipv4_index++;
                }
            } else {
                route_count++;
            }

        } else if (createPathGroupFor == service_layer::SL_IPv6_ROUTE_TABLE) {
            auto ipv6_index = database.ipv6_start_index;
            auto ipv6_last = database.ipv6_last_index;
            if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
                while (ipv6_index <= ipv6_last) {
                    auto db_prefix = ipv6_index;
                    service_layer::SLPathGroup_SLPath* path = path_list->add_paths();
                    service_layer::SLRoutePath* route_path = path->mutable_path();
                    route_path->mutable_nexthopaddress()->set_v6address(db_prefix);
                    route_path->mutable_nexthopinterface()->set_name(database.db_pg[pg_name].first.next_hop_interface_ipv6);

                    route_count++;
                    ipv6_index = this->incrementIpv6Pfx(ipv6_index, 128);
                }
            } else {
                route_count++;
            }

        }
        total_routes += route_count;
        if (streamCase) {
            // Write should just pull from queue and be able to send request
            route_msg.set_oper(routeOper);
            db_mutex.unlock();
            this->routeSLAFOpStreamHelperEnqueue(false);
            db_mutex.lock();
        } else {
            this->routeSLAFOp(routeOper, addrFamily);
        }

        db_mutex.unlock();
    }
    return total_routes;
}
bool 
SLAFRShuttle::routeSLAFOp(service_layer::SLObjectOp routeOp,
                    service_layer::SLTableType addrFamily,
                    unsigned int timeout)
{
    route_msg.set_oper(routeOp);
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
        context.AddMetadata("iosxr-slapi-clientid", client_id);
        // Multi-Client not supported in MPLS
    } else if (addr_family == service_layer::SL_PATH_GROUP_TABLE){
        address_family_str = "PATH GROUP";
        context.AddMetadata("iosxr-slapi-clientid", client_id);
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
                static_cast<int>(route_msg_resp.results(result).status().status());
                if (slerr_status != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
                    DbHelperError(result,addr_family,&route_msg_resp,slerr_status,false);
                    route_error = true;
                } else {
                     // Only RIB response received for Unary RPC.
                    DbHelperUpdate(result,addr_family,&route_msg_resp,false);
                }
        }
        if (!route_error) {
            VLOG(1) << address_family_str << " Route Operation:"<< route_op << " Successful";
        } else {
            VLOG(1) << address_family_str << " Route Operation:"<< route_op << " Unsuccessful";
            return false;
        }
    } else {
        LOG(ERROR) << "RPC failed, error code is " << status.error_code() << " tid: " << std::this_thread::get_id();
        throw(status);
        return false; 
    }

    // Clear route batch before the next operation
    this->clearBatch();
    return true;
}

void
SLAFRShuttle::readStream(std::shared_ptr<grpc::ClientReaderWriter<service_layer::SLAFMsg, service_layer::SLAFMsgRsp>>& stream, service_layer::SLTableType addrFamily,  service_layer::SLObjectOp routeOper, std::string addressFamilyStr)
{
    // Reader thread listens to any responses from the server
    service_layer::SLAFMsgRsp resp_msg;

    int read_count = 0;
    bool read_successful = true;

    // Waits for response until stream closes, timeout occurs, or response is given
    while (read_successful = stream->Read(&resp_msg)) {

       // Print Partial failures within the batch if applicable for responses and updated RIB && FIB ACK
        for (int result = 0; result < resp_msg.results_size(); result++) {
            db_mutex.lock();
            bool increment_count = false;
            bool check_rib_and_fib_set = false;

            auto slerr_status_rib = static_cast<int>(resp_msg.results(result).status().status());
            if (slerr_status_rib != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
                DbHelperError(result,addrFamily,&resp_msg,slerr_status_rib,false);
            } else {
                DbHelperUpdate(result,addrFamily,&resp_msg,false);
            }

            // Used for checking if response was already received at least once for prefix/label/PG name
            if (addrFamily == service_layer::SL_IPv4_ROUTE_TABLE) {
                auto index = resp_msg.results(result).key().iprouteprefix().prefix().v4address();
                check_rib_and_fib_set = database.db_ipv4[index].first.response_acks.response_ack_type_rib_fib_set;
            } else if (addrFamily == service_layer::SL_IPv6_ROUTE_TABLE) {
                auto index = resp_msg.results(result).key().iprouteprefix().prefix().v6address();
                check_rib_and_fib_set = database.db_ipv6[index].first.response_acks.response_ack_type_rib_fib_set;
            } else if (addrFamily == service_layer::SL_MPLS_LABEL_TABLE) {
                auto index = resp_msg.results(result).key().mplslabel().label();
                check_rib_and_fib_set = database.db_mpls[index].first.response_acks.response_ack_type_rib_fib_set;
            } else if (addrFamily == service_layer::SL_PATH_GROUP_TABLE) {
                auto index = resp_msg.results(result).key().pathgroupid().name();
                check_rib_and_fib_set = database.db_pg[index].first.response_acks.response_ack_type_rib_fib_set;
            }

            // For Fib Response
            auto slerr_status_fib = static_cast<int>(resp_msg.results(result).fibstatus());
            if (check_rib_and_fib_set) {
                if (slerr_status_fib != service_layer::SLAFFibStatus::SL_FIB_SUCCESS &&
                    slerr_status_fib != service_layer::SLAFFibStatus::SL_FIB_INUSE_SUCCESS) {
                    DbHelperError(result,addrFamily,&resp_msg,slerr_status_fib,true);
                } else {
                    DbHelperUpdate(result,addrFamily,&resp_msg,true);
                }
            }

            db_mutex.unlock();

            if (check_rib_and_fib_set == true) {
                if(slerr_status_fib != service_layer::SLAFFibStatus::SL_FIB_UNKNOWN) {
                    increment_count = true;
                }
                // service_layer::SLAFFibStatus::SL_FIB_UNKNOWN indicates that a fib ack was not sent
            } else {
                // In this case we only care about the RIB ack
                increment_count = true;
            }

            // Used to prevent incrementing the read count when multiple responses are sent for one prefix/label/PG name
            if (increment_count == true) {
                read_count++;
            }
        }

        db_mutex.lock();
        // Signifies we have finished all reads
        if (read_count == database.db_count) {
            // Notifies main thread to tell write to terminate stream
            std::unique_lock<std::mutex> lck(finish_m);
            read_finished = true;
            finish_read_cv.notify_all();
        }
        db_mutex.unlock();
    }
    db_mutex.lock();
    // Signifies we have closed stream due to abort or failure in write rpc. Thus signal main thread to wake up
    if (read_count != database.db_count) {
        // In this instance telling main thread to tell write thread to end terminate stream doesn't matter
        std::unique_lock<std::mutex> lck(finish_m);
        read_finished = true;
        finish_read_cv.notify_all();
    }
    db_mutex.unlock();
}

void
SLAFRShuttle::writeStream(std::shared_ptr<grpc::ClientReaderWriter<service_layer::SLAFMsg, service_layer::SLAFMsgRsp>>& stream, std::string addressFamilyStr)
{
    bool check_stream_open = true;
    // Writer thread listens to the queue indefinitely, until given signal by main thread or timeout occurs
    while(check_stream_open) {
        // Need to get a lock for this dequeue. Will unlock when out of scope
        std::unique_lock<std::mutex> lck(deque_mutex);
        // Wait for the lock along with the deque to be non-empty
        deque_cv.wait(lck, []() { return !request_deque.empty(); });
        SLAFQueueMsg queue_message = request_deque.front();
        request_deque.pop_front();
        service_layer::SLAFMsg message = queue_message.route_msg;

        // vrfname is a const string
        if (queue_message.terminate_slaf_stream) {
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
    }
    // Signifies the stream write is finished and stops stream
   stream->WritesDone();
}

void 
SLAFRShuttle::stopStream(std::thread* reader, std::thread* writer)
{
    // Wait for all reads to finish before telling write to terminate
    std::unique_lock<std::mutex> lck(finish_m);
    finish_read_cv.wait(lck, []() { return read_finished; });

    // this->setVrfV4("poison_pill");
    this->routeSLAFOpStreamHelperEnqueue(true);
    writer->join();
    reader->join();
}
void 
SLAFRShuttle::routeSLAFOpStreamHelperEnqueue(bool terminate_slaf_stream)
{
    SLAFQueueMsg queue_msg;
    queue_msg.route_msg = route_msg;
    if  (terminate_slaf_stream) {
        queue_msg.terminate_slaf_stream = true;
    }
    // lock the queue before pushing SL-API objects to it
    std::unique_lock<std::mutex> lck(deque_mutex);
    request_deque.push_back(queue_msg);
    deque_cv.notify_one();
    this->clearBatch();
}
unsigned int 
SLAFRShuttle::routeSLAFOpStream(service_layer::SLTableType addrFamily, service_layer::SLObjectOp routeOper, service_layer::SLTableType createPathGroupFor, unsigned int timeout)
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
        context.AddMetadata("iosxr-slapi-clientid", client_id);
        // Multi-Client not supported in MPLS
    } else if (addrFamily == service_layer::SL_PATH_GROUP_TABLE){
        address_family_str = "PATH GROUP";
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    }

    // Send the RPC
    std::shared_ptr<grpc::ClientReaderWriter<service_layer::SLAFMsg, service_layer::SLAFMsgRsp>> stream(
        stub_->SLAFOpStream(&context));

    // Create the Reader Thread
    std::thread reader(this->readStream,std::ref(stream), addrFamily, routeOper, address_family_str);

    request_deque.clear();
    // Start Writer Thread
    std::thread writer(this->writeStream, std::ref(stream), address_family_str);
    unsigned int total_routes = 0;

    // Makes batches from db objects and pushes into request queue
    total_routes = this->pushFromDB(true,routeOper,addrFamily,createPathGroupFor);

    stopStream(&reader,&writer);
    status = stream->Finish();
    if (!status.ok()) {
        LOG(ERROR) << "RPC failed, error code is " << status.error_code() << " tid: " << std::this_thread::get_id();
        throw(status);
    }
    return total_routes;
}

void 
SLAFRShuttle::clearDB()
{
    database.db_ipv4.clear();
    database.db_ipv6.clear();
    database.db_mpls.clear();
    database.db_pg.clear();
    database.db_count = 0;
    database.operation_id = 0;
    // Set read_finished to false for retry attempt
    read_finished = false;
}
void 
SLAFRShuttle::clearBatch()
{
   route_msg.clear_oplist();
   prefix_map_v4.clear();
   prefix_map_v6.clear();
}

void
SLAFRShuttle::responseAckSet(service_layer::SLAFOpMsg* operation, responseAcks responseAck)
{
    operation->set_acktype(responseAck.response_ack_type);
    if (responseAck.response_ack_type_rib_fib_set) {
        operation->add_ackpermits(responseAck.response_ack_permit);
        if (responseAck.response_ack_permit_set) {
            operation->set_ackcadence(responseAck.response_ack_cadence);
        }
    }
}

std::vector<service_layer::SLAFVrfRegGetMsgRsp>
SLAFRShuttle::routeSLAFVrfGet(unsigned int timeout)
{
    std::vector<service_layer::SLAFVrfRegGetMsgRsp> responses;

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
    // When this request has false value set, uses client id from context
    context.AddMetadata("iosxr-slapi-clientid", client_id);

    std::string s;
    if (google::protobuf::TextFormat::PrintToString(get_vrf_msg, &s)) {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Transmitted message: IOSXR-SL GET " << s;
        VLOG(2) << "###########################" ;
    } else {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Message not valid (partial content: "
                << get_vrf_msg.ShortDebugString() << ")";
        VLOG(2) << "###########################" ;
    }

    // Set the message
    get_vrf_msg.set_getall(true);

    // Send the RPC
    std::unique_ptr<grpc::ClientReader<service_layer::SLAFVrfRegGetMsgRsp>> reader(
        stub_->SLAFVrfRegGet(&context, get_vrf_msg));

    while (reader->Read(&get_vrf_msg_resp)) {
        responses.push_back(get_vrf_msg_resp);
    }
    status = reader->Finish();
    return responses;
}

std::vector<service_layer::SLAFGetMsgRsp>
SLAFRShuttle::routeSLAFget(std::string vrfname, bool get_match, bool get_match_route, bool get_client_all,
                        getMatchObjects match_objects, std::vector<uint64_t> client_list,
                        std::vector<service_layer::SLTableType> table_type_list, unsigned int timeout)
{
    std::vector<service_layer::SLAFGetMsgRsp> responses;
    unsigned int total_responses = 0;

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
    context.AddMetadata("iosxr-slapi-clientid", client_id);

    std::string s;
    if (google::protobuf::TextFormat::PrintToString(get_msg, &s)) {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Transmitted message: IOSXR-SL GET " << s;
        VLOG(2) << "###########################" ;
    } else {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Message not valid (partial content: "
                << get_msg.ShortDebugString() << ")";
        VLOG(2) << "###########################" ;
    }

    // Fill in the message
    get_msg.set_vrfname(vrfname);
    if (get_match == true) {
        if (get_match_route == true) {
            service_layer::SLAFGetMatchList* route_match_list = get_msg.mutable_routematchlist();
            // Set all Path group regexs
            for (auto regex: match_objects.pg_regexs) {
                service_layer::SLAFGetMatch* match = route_match_list->add_match();
                match->set_pathgroupregex(regex);
            }

            // Set all VxlanVn IDs
            for (auto vxlan_id: match_objects.vxlan_vn_ids) {
                service_layer::SLAFGetMatch* match = route_match_list->add_match();
                match->set_vxlanvniid(vxlan_id);
            }

            // Set all the SLAFObject Key types. ipv4, ipv6, mpls, pg
            for (auto ipv4_route: match_objects.ipv4_routes) {
                service_layer::SLAFGetMatch* match = route_match_list->add_match();
                service_layer::SLAFObjectKey* slaf_obj_key = match->mutable_key();
                service_layer::SLRoutePrefix* route_prefix = slaf_obj_key->mutable_iprouteprefix();
                service_layer::SLIpAddress* ip_address = route_prefix->mutable_prefix();
                ip_address->set_v4address(ipv4_route.first);
                route_prefix->set_prefixlen(ipv4_route.second);
            }

            for (auto ipv6_route: match_objects.ipv6_routes) {
                service_layer::SLAFGetMatch* match = route_match_list->add_match();
                service_layer::SLAFObjectKey* slaf_obj_key = match->mutable_key();
                service_layer::SLRoutePrefix* route_prefix = slaf_obj_key->mutable_iprouteprefix();
                service_layer::SLIpAddress* ip_address = route_prefix->mutable_prefix();
                ip_address->set_v6address(ipv6_route.first);
                route_prefix->set_prefixlen(ipv6_route.second);
            }

            for (uint32_t mpls_label: match_objects.mpls_labels) {
                service_layer::SLAFGetMatch* match = route_match_list->add_match();
                service_layer::SLAFObjectKey* slaf_obj_key = match->mutable_key();
                service_layer::SLMplsEntryKey* mpls_entry_key = slaf_obj_key->mutable_mplslabel();
                mpls_entry_key->set_label(mpls_label);
            }

            for (auto pg_id: match_objects.pg_ids) {
                service_layer::SLAFGetMatch* match = route_match_list->add_match();
                service_layer::SLAFObjectKey* slaf_obj_key = match->mutable_key();
                service_layer::SLObjectId* object_id = slaf_obj_key->mutable_pathgroupid();
                object_id->set_name(pg_id);
            }

        } else {
            service_layer::SLTableTypeList* table_list = get_msg.mutable_tablelist();
            for (auto table_type: table_type_list) {
                table_list->add_table(table_type);
            }
        }
    } else {
        if (get_client_all == true) {
            get_msg.set_allclients(get_client_all);
        } else {
            service_layer::SLAFClientIDList* client_id_list = get_msg.mutable_clientidlist();
            for (auto client_id: client_list) {
                client_id_list->add_clientidlist(client_id);
            }
        }
    }
    // Send the RPC
    std::unique_ptr<grpc::ClientReader<service_layer::SLAFGetMsgRsp>> reader(
        stub_->SLAFGet(&context, get_msg));

    while (reader->Read(&get_msg_resp)) {
        responses.push_back(get_msg_resp);
    }
    status = reader->Finish();
    return responses;
}

uint32_t
SLAFRShuttle::ipv4ToLong(const char* address)
{
    struct sockaddr_in sa;
    if (inet_pton(AF_INET, address, &(sa.sin_addr)) != 1) {
        LOG(ERROR) << "Invalid IPv4 address " << address << " tid: " << std::this_thread::get_id(); 
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
        LOG(ERROR) << "inet_ntop conversion error: "<< strerror(errno) << " tid: " << std::this_thread::get_id();
        return std::string("");
    }
}


std::string 
SLAFRShuttle::ipv6ToByteArrayString(const char* address)
{
    struct in6_addr ipv6data;
    if (inet_pton(AF_INET6, address, &ipv6data) != 1 ) {
        LOG(ERROR) << "Invalid IPv6 address " << address << " tid: " << std::this_thread::get_id(); 
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
        LOG(ERROR) << "inet_ntop conversion error: "<< strerror(errno) << " tid: " << std::this_thread::get_id();
        return std::string("");
    }
}

std::string 
SLAFRShuttle::incrementIpv6Pfx(std::string ipv6ByteArray, uint32_t prefixLen) {
    if (prefixLen > 128) {
        LOG(ERROR) << "PrefixLen > 128" << " tid: " << std::this_thread::get_id();
    }

    // prefix will always be 16 chars long for ipv6
    struct in6_addr  ipv6_data;
    char             str[INET6_ADDRSTRLEN]; /* 46 */

    // We copy the address which is already a byte array
    std::copy(ipv6ByteArray.begin(), ipv6ByteArray.end(),ipv6_data.s6_addr);
    auto offset = (prefixLen - 1)/8;
    auto bit_num = (prefixLen-1)%8;
    bit_num = 7 - bit_num;
    // increment byte array
    ipv6_data.s6_addr[offset] += (1 << bit_num);
    while (offset > 0 && !ipv6_data.s6_addr[offset--]) {
        ipv6_data.s6_addr[offset]++;
    }
    // convert it back into a string
    const char *ptr(reinterpret_cast<const char*>(&ipv6_data.s6_addr));
    std::string ipv6_charstr(ptr, ptr+16);
    return ipv6_charstr;
}

SLAFRShuttle::SLAFRShuttle(std::shared_ptr<grpc::Channel> Channel, std::string Username,
                   std::string Password)
    : channel(Channel), username(Username), password(Password) {} 

// Overloaded routeIpAdd to be used if vrfname is already set

service_layer::SLAFIPRoute*
SLAFRShuttle::routeIpAdd(responseAcks responseAck)
{
    if (route_msg.vrfname().empty()) {
        LOG(ERROR) << "vrfname is empty, please set vrf "
                   << "before manipulating routes" << " tid: " << std::this_thread::get_id();
        return 0;
    } else {
        service_layer::SLAFOpMsg* operation = route_msg.add_oplist();
        service_layer::SLAFObject* af_object = operation->mutable_afobject();
        service_layer::SLAFIPRoute* routeIpPtr = af_object->mutable_iproute();

        operation->set_operationid(database.operation_id++);
        this->responseAckSet(operation, responseAck);
        return routeIpPtr;
    }
}

service_layer::SLAFIPRoute* 
SLAFRShuttle::routeIpAdd(std::string vrfName, responseAcks responseAck)
{
    route_msg.set_vrfname(vrfName);
    service_layer::SLAFOpMsg* operation = route_msg.add_oplist();
    service_layer::SLAFObject* af_object = operation->mutable_afobject();
    service_layer::SLAFIPRoute* routeIpPtr = af_object->mutable_iproute();

    operation->set_operationid(database.operation_id++);
    this->responseAckSet(operation, responseAck);

    return routeIpPtr;
}

void 
SLAFRShuttle::setVrfV4(std::string vrfName)
{
    route_msg.set_vrfname(vrfName);
}

// Overloaded method to Set V4 route without Admin Distance.
// Used for DELETE Operation

void 
SLAFRShuttle::routev4Set(service_layer::SLAFIPRoute* routeIpPtr,
                     uint32_t prefix,
                     uint32_t prefixLen)
{   
    service_layer::SLRoutePrefix* route_prefix = routeIpPtr->mutable_iprouteprefix();
    service_layer::SLIpAddress* ip_address = route_prefix->mutable_prefix();
    ip_address->set_v4address(prefix);
    route_prefix->set_prefixlen(prefixLen);
}


// Overloaded method to Set V4 route without Admin Distance.
// Used for ADD or UPDATE Operation

void 
SLAFRShuttle::routev4Set(service_layer::SLAFIPRoute* routeIpPtr,
                     uint32_t prefix,
                     uint32_t prefixLen,
                     uint32_t adminDistance)
{
    service_layer::SLRoutePrefix* route_prefix = routeIpPtr->mutable_iprouteprefix();
    service_layer::SLIpAddress* ip_address = route_prefix->mutable_prefix();
    ip_address->set_v4address(prefix);
    route_prefix->set_prefixlen(prefixLen);
    routeIpPtr->mutable_routecommon()->set_admindistance(adminDistance);
}

void 
SLAFRShuttle::routev4PathAdd(service_layer::SLAFIPRoute* routeIpPtr,
                         uint32_t nextHopAddress,
                         std::string nextHopIf,
                         std::string pgName)
{
    auto routeIpPathPtr = routeIpPtr->add_pathlist();
    if (pgName == "") {
        routeIpPathPtr->mutable_nexthopaddress()->set_v4address(nextHopAddress);
        routeIpPathPtr->mutable_nexthopinterface()->set_name(nextHopIf);
        routeIpPathPtr->set_vrfname("default");
    } else {
        auto pathGroup = routeIpPathPtr->mutable_pathgroupkey();
        pathGroup->set_vrfname("default");
        service_layer::SLObjectId* pgId = pathGroup->mutable_pathgroupid();
        pgId->set_name(pgName);
    }
}

bool 
SLAFRShuttle::insertAddBatchV4(std::string prefix,
                           uint32_t prefixLen,
                           uint32_t adminDistance,
                           std::string nextHopAddress,
                           std::string nextHopIf,
                           service_layer::SLObjectOp routeOper,
                           std::string pgName,
                           responseAcks responseAck)
{

    auto address = prefix + "/" + std::to_string(prefixLen);
    auto map_index = route_msg.oplist_size();

    if (this->prefix_map_v4.find(address) == this->prefix_map_v4.end()) {
        // Obtain pointer to a new route object within route batch
        auto routeip_ptr = this->routeIpAdd(responseAck);

        if (!routeip_ptr) {
            LOG(ERROR) << "Failed to create new route object" << " tid: " << std::this_thread::get_id();
            return false;
        }

        // Set up the new v4 route object
        this->routev4Set(routeip_ptr, 
                         ipv4ToLong(prefix.c_str()),
                         prefixLen, 
                         adminDistance);
        this->prefix_map_v4[address] = map_index;

         /* We dont need to setup the paths for DELETE*/
        if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
            this->routev4PathAdd(routeip_ptr, 
                             ipv4ToLong(nextHopAddress.c_str()), 
                             nextHopIf,
                             pgName); 
        }

    } else {
        // no need to make a new route object as one already exists within this route batch
        auto operation = route_msg.mutable_oplist(prefix_map_v4[address]);
        auto af_object = operation->mutable_afobject();
        auto routeIpPtr = af_object->mutable_iproute();
         /* We dont need to setup the paths for DELETE*/
        if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
            this->routev4PathAdd(routeIpPtr, 
                             ipv4ToLong(nextHopAddress.c_str()), 
                             nextHopIf,
                             pgName); 
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


// Overloaded method to Set V6 route without Admin Distance.
// Used for DELETE Operation

void 
SLAFRShuttle::routev6Set(service_layer::SLAFIPRoute* routeIpPtr,
                     std::string prefix,
                     uint32_t prefixLen)
{
    service_layer::SLRoutePrefix* route_prefix = routeIpPtr->mutable_iprouteprefix();
    service_layer::SLIpAddress* ip_address = route_prefix->mutable_prefix();
    ip_address->set_v6address(prefix);
    route_prefix->set_prefixlen(prefixLen);
}


// Overloaded method to Set V6 route without Admin Distance.
// Used for ADD or UPDATE Operation

void 
SLAFRShuttle::routev6Set(service_layer::SLAFIPRoute* routeIpPtr,
                     std::string prefix,
                     uint32_t prefixLen,
                     uint32_t adminDistance)
{
    service_layer::SLRoutePrefix* route_prefix = routeIpPtr->mutable_iprouteprefix();
    service_layer::SLIpAddress* ip_address = route_prefix->mutable_prefix();
    ip_address->set_v6address(prefix);
    route_prefix->set_prefixlen(prefixLen);
    routeIpPtr->mutable_routecommon()->set_admindistance(adminDistance);
}

void 
SLAFRShuttle::routev6PathAdd(service_layer::SLAFIPRoute* routeIpPtr,
                         std::string nextHopAddress,
                         std::string nextHopIf,
                         std::string pgName)
{
    auto routeIpPathPtr = routeIpPtr->add_pathlist();
    if (pgName == "") {
        routeIpPathPtr->mutable_nexthopaddress()->set_v6address(nextHopAddress);
        routeIpPathPtr->mutable_nexthopinterface()->set_name(nextHopIf);
        routeIpPathPtr->set_vrfname("default");
    } else {
        auto pathGroup = routeIpPathPtr->mutable_pathgroupkey();
        pathGroup->set_vrfname("default");
        service_layer::SLObjectId* pgId = pathGroup->mutable_pathgroupid();
        pgId->set_name(pgName);
    }
}

bool 
SLAFRShuttle::insertAddBatchV6(std::string prefix,
                           uint32_t prefixLen,
                           uint32_t adminDistance,
                           std::string nextHopAddress,
                           std::string nextHopIf,
                           service_layer::SLObjectOp routeOper,
                           std::string pgName,
                           responseAcks responseAck)
{
    auto address = prefix + "/" + std::to_string(prefixLen);
    auto map_index = route_msg.oplist_size();

    if (this->prefix_map_v6.find(address) == this->prefix_map_v6.end()) {
        // Obtain pointer to a new route object within route batch
        auto routeip_ptr = this->routeIpAdd(responseAck);

        if (!routeip_ptr) {
            LOG(ERROR) << "Failed to create new route object" << " tid: " << std::this_thread::get_id();
            return false;
        }

        // Set up the new v6 route object
        this->routev6Set(routeip_ptr, 
                         ipv6ToByteArrayString(prefix.c_str()),
                         prefixLen, 
                         adminDistance);
        this->prefix_map_v6[address] = map_index;

         /* We dont need to setup the paths for DELETE*/
        if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
            this->routev6PathAdd(routeip_ptr,
                             ipv6ToByteArrayString(nextHopAddress.c_str()),
                             nextHopIf,
                             pgName);
        }
    } else {
        // no need to make a new route object as one already exists within this route batch
        auto operation = route_msg.mutable_oplist(prefix_map_v6[address]);
        auto af_object = operation->mutable_afobject();
        auto routeIpPtr = af_object->mutable_iproute();
         /* We dont need to setup the paths for DELETE*/
        if (routeOper !=  service_layer::SL_OBJOP_DELETE) {
            this->routev6PathAdd(routeIpPtr,
                             ipv6ToByteArrayString(nextHopAddress.c_str()),
                             nextHopIf,
                             pgName);
        }
    }

    return true;
}
void
SLAFRShuttle::insertAddBatchMPLS(uint32_t label,
                            uint32_t startLabel,
                            unsigned int numPaths,
                            uint32_t nextHopAddress,
                            std::string nextHopInterface,
                            std::string pgName,
                            responseAcks responseAck) {

    /* Create a new ilm entry, and the only way to do that with the current proto file
            is to add a new oplist */
    service_layer::SLAFOpMsg* operation = route_msg.add_oplist();
    service_layer::SLAFObject* af_object = operation->mutable_afobject();
    service_layer::SLMplsEntry* ilm = af_object->mutable_mplslabel();
    service_layer::SLMplsEntryKey* ilm_key = ilm->mutable_mplskey();

    operation->set_operationid(database.operation_id++);
    this->responseAckSet(operation, responseAck);
    ilm_key->set_label(label);

    if (pgName == "") {
        // Multiple path in entry
        for(int pathIdx = 0; pathIdx < numPaths; pathIdx++){
            service_layer::SLRoutePath* nhlfe = ilm->add_pathlist();
            service_layer::SLIpAddress* slip_add = nhlfe->mutable_nexthopaddress();
            slip_add->set_v4address(nextHopAddress);
            nhlfe->set_vrfname("default");
            if (nextHopInterface.length() != 0){
                service_layer::SLInterface* sli_add = nhlfe->mutable_nexthopinterface();
                sli_add->set_name(nextHopInterface);
            }
            if (startLabel > 0) {
                int out_label = startLabel;
                nhlfe->add_labelstack(out_label);
            }
        }
    } else {
        service_layer::SLRoutePath* nhlfe = ilm->add_pathlist();
        auto pathGroup = nhlfe->mutable_pathgroupkey();
        pathGroup->set_vrfname("default");
        service_layer::SLObjectId* pgId = pathGroup->mutable_pathgroupid();
        pgId->set_name(pgName);
    }
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
            LOG(ERROR) << "Failed to send Register RP" << " tid: " << std::this_thread::get_id();
            return false;
        } 
        break;

    case service_layer::SL_IPv6_ROUTE_TABLE:
        // Issue VRF Register RPC
        if (afVrfOpAddFam(vrfRegOper, addrFamily)) {
            return true;
        } else {
            LOG(ERROR) << "Failed to send Register RPC" << " tid: " << std::this_thread::get_id();
            return false;
        }
        break;

    case service_layer::SL_MPLS_LABEL_TABLE:
        // Issue VRF Register RPC
        if (afVrfOpAddFam(vrfRegOper, addrFamily)) {
            return true;
        } else {
            LOG(ERROR) << "Failed to send Register RPC" << " tid: " << std::this_thread::get_id();
            return false;
        }
        break;

    case service_layer::SL_PATH_GROUP_TABLE:
        // Issue VRF Register RPC
        if (afVrfOpAddFam(vrfRegOper, addrFamily)) {
            return true;
        } else {
            LOG(ERROR) << "Failed to send Register RPC";
            return false;
        }
        break;

    default:
        LOG(ERROR) << "Invalid Address family, skipping.." << " tid: " << std::this_thread::get_id();
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

    unsigned int timeout = 30;
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
        context.AddMetadata("iosxr-slapi-clientid", client_id);
        // Multi-Client not supported in MPLS
    } else if (addrFamily == service_layer::SL_PATH_GROUP_TABLE) {
        // Multi-Client not supported in PATHGROUP
        context.AddMetadata("iosxr-slapi-clientid", client_id);
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
                       << " is " << std::hex 
                       << af_vrf_msg_resp.statussummary().status()
                       << " tid: " << std::this_thread::get_id();

            // Print Partial failures within the batch if applicable
            if (af_vrf_msg_resp.statussummary().status() ==
                    service_layer::SLErrorStatus_SLErrno_SL_SOME_ERR) {
                for (int result = 0; result < af_vrf_msg_resp.results_size(); result++) {
                      auto slerr_status = 
                      static_cast<int>(af_vrf_msg_resp.results(result).errstatus().status());
                      LOG(ERROR) << "Error code for vrf " 
                                 << af_vrf_msg_resp.results(result).vrfname() 
                                 << " is " << std::hex 
                                 << slerr_status
                                 << " tid: " << std::this_thread::get_id();
                }
            }
            return false;
        }
    } else {
        LOG(ERROR) << "RPC failed, error code is " << status.error_code() << " tid: " << std::this_thread::get_id();
        throw(status);
        return false;
    }
}

// SLGLOBALSHUTTLE ----------------------------------------------------------------------------------
SLGLOBALSHUTTLE::SLGLOBALSHUTTLE(std::shared_ptr<grpc::Channel> Channel, std::string Username,
                   std::string Password)
    : channel(Channel), username(Username), password(Password) {} 

bool SLGLOBALSHUTTLE::getGlobals(unsigned int &batch_size, unsigned int &max_paths, unsigned int timeout)
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
        }
    } else {
        LOG(ERROR) << "getGlobals RPC failed, error code is " << status.error_code() << " tid: " << std::this_thread::get_id();
        throw(status);
        return false;
    }

    LOG(INFO) <<"MaxVrfNameLength:              " << resp_msg.maxvrfnamelength() << std::endl;
    LOG(INFO) <<"MaxInterfaceNameLength:        " << resp_msg.maxinterfacenamelength() << std::endl;
    LOG(INFO) <<"MaxPathsPerEntry:              " << resp_msg.maxpathsperentry() << std::endl;
    LOG(INFO) <<"MaxPrimaryPathPerEntry:        " << resp_msg.maxprimarypathperentry() << std::endl;
    LOG(INFO) <<"MaxBackupPathPerEntry:         " << resp_msg.maxbackuppathperentry() << std::endl;
    LOG(INFO) <<"MaxMplsLabelsPerPath:          " << resp_msg.maxmplslabelsperpath() << std::endl;
    LOG(INFO) <<"MinPrimaryPathIdNum:           " << resp_msg.minprimarypathidnum() << std::endl;
    LOG(INFO) <<"MaxPrimaryPathIdNum:           " << resp_msg.maxprimarypathidnum() << std::endl;
    LOG(INFO) <<"MinBackupPathIdNum:            " << resp_msg.minbackuppathidnum() << std::endl;
    LOG(INFO) <<"MaxBackupPathIdNum:            " << resp_msg.maxbackuppathidnum() << std::endl;
    LOG(INFO) <<"MaxRemoteAddressNum:           " << resp_msg.maxremoteaddressnum() << std::endl;
    LOG(INFO) <<"MaxL2BdNameLength:             " << resp_msg.maxl2bdnamelength() << std::endl;
    LOG(INFO) <<"MaxL2PmsiTunnelIdLength:       " << resp_msg.maxl2pmsitunnelidlength() << std::endl;
    LOG(INFO) <<"MaxLabelBlockClientNameLength: " << resp_msg.maxlabelblockclientnamelength() << std::endl;
    LOG(INFO) <<"MaxPathsInNexthopNotif:        " << resp_msg.maxpathsinnexthopnotif() << std::endl;
    LOG(INFO) <<"MaxVrfRegPerMsg:               " << resp_msg.maxvrfregpermsg() << std::endl;
    LOG(INFO) <<"MaxAFOpsPerMsg:                " << resp_msg.maxafopspermsg() << std::endl;
    LOG(INFO) <<"MaxNotifReqPerSLAFNotifReq:    " << resp_msg.maxnotifreqperslafnotifreq() << std::endl;
    unsigned int temp = resp_msg.maxafopspermsg();

    if (temp <= 0) {
        LOG(INFO) << "WARNING: MaxAFOpsPerMsg (BATCH SIZE ) is 0. Batch Size will remain at value given: " << batch_size
                  << " tid: " << std::this_thread::get_id();
    } else {
        if (batch_size > temp) {
            batch_size = resp_msg.maxafopspermsg();
            LOG(INFO) << "BATCH SIZE is set to " << temp << " tid: " << std::this_thread::get_id();
        } else {
            LOG(INFO) << "BATCH SIZE will remain as " << batch_size << " tid: " << std::this_thread::get_id();
        }
    }

    if (max_paths > resp_msg.maxprimarypathidnum()) {
        max_paths = resp_msg.maxprimarypathidnum();
        LOG(INFO) << "MAX PATHS is limited to " << resp_msg.maxprimarypathidnum();
    } else {
        LOG(INFO) << "MAX PATHS will remain as " << max_paths;
    }

    return true;
}
