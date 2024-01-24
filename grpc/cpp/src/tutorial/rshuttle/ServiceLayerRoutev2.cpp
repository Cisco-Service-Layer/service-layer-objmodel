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


RShuttlev2* route_shuttle;

uint32_t
RShuttlev2::ipv4ToLong(const char* address)
{
    struct sockaddr_in sa;
    if (inet_pton(AF_INET, address, &(sa.sin_addr)) != 1) {
        LOG(ERROR) << "Invalid IPv4 address " << address; 
        return 0;
    }

    return ntohl(sa.sin_addr.s_addr);
}

std::string 
RShuttlev2::longToIpv4(uint32_t nlprefix)
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
RShuttlev2::ipv6ToByteArrayString(const char* address)
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
RShuttlev2::ByteArrayStringtoIpv6(std::string ipv6ByteArray)
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

RShuttlev2::RShuttlev2(std::shared_ptr<grpc::Channel> Channel, std::string Username,
                   std::string Password)
    : channel(Channel), username(Username), password(Password) {} 


void 
RShuttlev2::setVrfV4(std::string vrfName)
{
    routev4_version2_msg.set_vrfname(vrfName);
}

// Overloaded routev4Add to be used if vrfname is already set

service_layer::SLRoutev4*
RShuttlev2::routev4Add()
{
    if (routev4_version2_msg.vrfname().empty()) {
        LOG(ERROR) << "vrfname is empty, please set vrf "
                   << "before manipulating routes";
        return 0;
    } else {
        // service_layer::SLAFOp* operation = routev4_version2_msg.add_oplist();
        // // operation->set_operationid(2);
        // service_layer::SLAFObject* af_object = operation->mutable_afobject();
        // service_layer::SLRoutev4* routev4Ptr = af_object->mutable_ipv4route();
        return routev4_version2_msg.add_oplist()->mutable_afobject()->mutable_ipv4route();
    }
}

service_layer::SLRoutev4* 
RShuttlev2::routev4Add(std::string vrfName)
{
    routev4_version2_msg.set_vrfname(vrfName);
    // service_layer::SLAFOp* operation = routev4_version2_msg.add_oplist();
    // // operation->set_operationid(2);
    // service_layer::SLAFObject* af_object = operation->mutable_afobject();
    // service_layer::SLRoutev4* routev4Ptr = af_object->mutable_ipv4route();
    return routev4_version2_msg.add_oplist()->mutable_afobject()->mutable_ipv4route();
}

// Overloaded method to Set V4 route without Admin Distance.
// Used for DELETE Operation

void 
RShuttlev2::routev4Set(service_layer::SLRoutev4* routev4Ptr,
                     uint32_t prefix,
                     uint8_t prefixLen)
{   
    routev4Ptr->set_prefix(prefix);
    routev4Ptr->set_prefixlen(prefixLen);
}


// Overloaded method to Set V4 route without Admin Distance.
// Used for ADD or UPDATE Operation


void 
RShuttlev2::routev4Set(service_layer::SLRoutev4* routev4Ptr,
                     uint32_t prefix,
                     uint8_t prefixLen,
                     uint32_t adminDistance)
{
    routev4Ptr->set_prefix(prefix);
    routev4Ptr->set_prefixlen(prefixLen);
    routev4Ptr->mutable_routecommon()->set_admindistance(adminDistance);
}


void 
RShuttlev2::routev4PathAdd(service_layer::SLRoutev4* routev4Ptr,
                         uint32_t nextHopAddress,
                         std::string nextHopIf)
{
    
    auto routev4PathPtr = routev4Ptr->add_pathlist();
    routev4PathPtr->mutable_nexthopaddress()->set_v4address(nextHopAddress);
    routev4PathPtr->mutable_nexthopinterface()->set_name(nextHopIf);
}

bool 
RShuttlev2::routev4Op(service_layer::SLObjectOp routeOp,
                    unsigned int timeout)
{

    // Convert ADD to UPDATE automatically, it will solve both the 
    // conditions - add or update.

   // if (routeOp == service_layer::SL_OBJOP_ADD) {
   //     routeOp = service_layer::SL_OBJOP_UPDATE;
   // }

    route_op = routeOp;
    routev4_version2_msg.set_oper(route_op);

    auto stub_ = service_layer::SLAF::NewStub(channel);

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

    if (google::protobuf::TextFormat::PrintToString(routev4_version2_msg, &s)) {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Transmitted message: IOSXR-SL Routev4 " << s;
        VLOG(2) << "###########################" ;
    } else {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Message not valid (partial content: "
                  << routev4_version2_msg.ShortDebugString() << ")";
        VLOG(2) << "###########################" ;
        return false;
    }

    status = stub_->SLAFOp(&context, routev4_version2_msg, &routev4_version2_msg_resp);

    if (status.ok()) {
        VLOG(1) << "RPC call was successful, checking response...";

        // // Print Partial failures within the batch if applicable
        // bool ipv4_error = false;
        // for (int result = 0; result < routev4_version2_msg_resp.results_size(); result++) {
        //     ipv4_error = true;
        //         auto slerr_status = 
        //         static_cast<int>(routev4_version2_msg_resp.results(result).errstatus().status());
        //         LOG(ERROR) << "Error code for prefix: " 
        //                     << routev4_version2_msg_resp.results(result).operation().afobject().ipv4route().prefix()
        //                     << " prefixlen: " 
        //                     << routev4_version2_msg_resp.results(result).operation().afobject().ipv4route().prefixlen()
        //                     <<" is 0x"<< std::hex << slerr_status;
        // }
        // if(!ipv4_error){
        //     VLOG(1) << "IPv4 Route Operation:"<< route_op << " Successful";
        // } else {
        //     VLOG(1) << "IPv4 Route Operation:"<< route_op << " Unsuccessful";
        //     return false;
        // }

    } else {
        LOG(ERROR) << "RPC failed, error code is " << status.error_code();
        return false; 
    }

    // Clear route batch before the next operation
    this->clearBatchV4();
    return true;
}

bool 
RShuttlev2::insertAddBatchV4(std::string prefix,
                           uint8_t prefixLen,
                           uint32_t adminDistance,
                           std::string nextHopAddress,
                           std::string nextHopIf)
{

    auto address = prefix + "/" + std::to_string(prefixLen);
    auto map_index = this->routev4_version2_msg.oplist_size();

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
    
        this->routev4PathAdd(routev4_ptr, 
                             ipv4ToLong(nextHopAddress.c_str()), 
                             nextHopIf); 

    } else {
        auto operation = this->routev4_version2_msg.mutable_oplist(prefix_map_v4[address]);
        // operation->set_operationid(1);
        auto af_object = operation->mutable_afobject();
        auto routev4_ptr = af_object->mutable_ipv4route();
        this->routev4PathAdd(routev4_ptr,
                             ipv4ToLong(nextHopAddress.c_str()),
                             nextHopIf);  
    }

    return true;
}

void 
RShuttlev2::clearBatchV4()
{
   routev4_version2_msg.clear_oplist(); 
   prefix_map_v4.clear();
}

// V6 methods

void
RShuttlev2::setVrfV6(std::string vrfName)
{
    routev6_msg.set_vrfname(vrfName);
}

// Overloaded routev6Add to be used if vrfname is already set

service_layer::SLRoutev6*
RShuttlev2::routev6Add()
{
    if (routev6_msg.vrfname().empty()) {
        LOG(ERROR) << "vrfname is empty, please set vrf " 
                   << "before manipulating v6 routes";
        return 0;
    } else {
        return routev6_msg.add_routes();
    }
}


service_layer::SLRoutev6*
  RShuttlev2::routev6Add(std::string vrfName)
{
    routev6_msg.set_vrfname(vrfName);
    return routev6_msg.add_routes();
}


// Overloaded method to Set V4 route without Admin Distance.
// Used for DELETE Operation

void 
RShuttlev2::routev6Set(service_layer::SLRoutev6* routev6Ptr,
                     std::string prefix,
                     uint8_t prefixLen)
{
    routev6Ptr->set_prefix(prefix);
    routev6Ptr->set_prefixlen(prefixLen);
}


// Overloaded method to Set V4 route without Admin Distance.
// Used for ADD or UPDATE Operation

void 
RShuttlev2::routev6Set(service_layer::SLRoutev6* routev6Ptr,
                     std::string prefix,
                     uint8_t prefixLen,
                     uint32_t adminDistance)
{
    routev6Ptr->set_prefix(prefix);
    routev6Ptr->set_prefixlen(prefixLen);
    routev6Ptr->mutable_routecommon()->set_admindistance(adminDistance);
}

void 
RShuttlev2::routev6PathAdd(service_layer::SLRoutev6* routev6Ptr,
                         std::string nextHopAddress,
                         std::string nextHopIf)
{

    auto routev6PathPtr = routev6Ptr->add_pathlist();
    routev6PathPtr->mutable_nexthopaddress()->set_v6address(nextHopAddress);
    routev6PathPtr->mutable_nexthopinterface()->set_name(nextHopIf);
}

bool 
RShuttlev2::routev6Op(service_layer::SLObjectOp routeOp,
                    unsigned int timeout)
{                      

    // Convert ADD to UPDATE automatically, it will solve both the 
    // conditions - add or update.
    
   // if (routeOp == service_layer::SL_OBJOP_ADD) {
    //    routeOp = service_layer::SL_OBJOP_UPDATE;
    //}
    
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
    if (username.length() > 0) {
        context.AddMetadata("username", username);
    }
    if (password.length() > 0) {
        context.AddMetadata("password", password);
    }

    //Issue the RPC         
    std::string s;

    if (google::protobuf::TextFormat::PrintToString(routev6_msg, &s)) {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Transmitted message: IOSXR-SL RouteV6 " << s;
        VLOG(2) << "###########################" ;
    } else {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Message not valid (partial content: "
                << routev6_msg.ShortDebugString() << ")";
        VLOG(2) << "###########################" ;
        return false;
    }

    //Issue the RPC         

    status = stub_->SLRoutev6Op(&context, routev6_msg, &routev6_msg_resp);

    if (status.ok()) {
         VLOG(1) << "RPC call was successful, checking response...";


        if (routev6_msg_resp.statussummary().status() ==
               service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {

            VLOG(1) << "IPv6 Route Operation:"<< route_op << " Successful";
        } else {
            LOG(ERROR) << "Error code for IPv6 Route Operation:" 
                       << route_op 
                       << " is 0x" << std::hex 
                       << routev6_msg_resp.statussummary().status();

            // Print Partial failures within the batch if applicable
            if (routev6_msg_resp.statussummary().status() ==
                    service_layer::SLErrorStatus_SLErrno_SL_SOME_ERR) {
                for (int result = 0; result < routev6_msg_resp.results_size(); result++) {
                      auto slerr_status = 
                      static_cast<int>(routev6_msg_resp.results(result).errstatus().status());
                      LOG(ERROR) << "Error code for prefix: " 
                                 << routev6_msg_resp.results(result).prefix() 
                                 << " prefixlen: " 
                                 << routev6_msg_resp.results(result).prefixlen()
                                 <<" is 0x"<< std::hex << slerr_status; 

                }
            }
            return false;
        }
    } else {
        LOG(ERROR) << "RPC failed, error code is " << status.error_code();
        return false;
    }

    // Clear route batch before the next operation
    this->clearBatchV6();
    return true;
}


bool 
RShuttlev2::insertAddBatchV6(std::string prefix,
                           uint8_t prefixLen,
                           uint32_t adminDistance,
                           std::string nextHopAddress,
                           std::string nextHopIf)
{
    auto address = prefix + "/" + std::to_string(prefixLen);
    auto map_index = this->routev6_msg.routes_size();

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
    
        this->routev6PathAdd(routev6_ptr,
                             ipv6ToByteArrayString(nextHopAddress.c_str()),
                             nextHopIf);

    } else {
        auto routev6_ptr = this->routev6_msg.mutable_routes(prefix_map_v6[address]);
        this->routev6PathAdd(routev6_ptr,
                             ipv6ToByteArrayString(nextHopAddress.c_str()),
                             nextHopIf);
    }

    return true;
}


bool
RShuttlev2::insertDeleteBatchV6(std::string prefix,
                              uint8_t prefixLen)
{   
    
    // Obtain pointer to a new route object within route batch
    auto routev6_ptr = this->routev6Add();

    if (!routev6_ptr) {
        LOG(ERROR) << "Failed to create new route object";
        return false;
    }
    
    // Set up the new v6 route object 
    this->routev6Set(routev6_ptr, 
                     ipv6ToByteArrayString(prefix.c_str()),
                     prefixLen);
    
    return true;
}


// overloaded updateBatchV6 with no admin_distance parameter
bool
RShuttlev2::insertUpdateBatchV6(std::string prefix,
                              uint8_t prefixLen,
                              std::string nextHopAddress,
                              std::string nextHopIf,
                              RShuttlev2::PathUpdateAction action)
{
    service_layer::SLRoutev6 routev6; 
    if (this->routev6_msg.vrfname().empty()) {
        LOG(ERROR) << "Route batch vrf not set, aborting route update...";
        return false;
    } else { 
        bool response = this->getPrefixPathsV6(routev6,
                                               this->routev6_msg.vrfname(),
                                               prefix,
                                               prefixLen);
        if (response) {
            VLOG(2) << "Prefix exists in RIB, updating the batch before push.. "
                    << this->ByteArrayStringtoIpv6(routev6.prefix());
            
            // Use the existing admin distance from the route in RIB
            uint32_t admin_distance = routev6.routecommon().admindistance();
            if (this->insertUpdateBatchV6(prefix,
                                          prefixLen,
                                          admin_distance,
                                          nextHopAddress,
                                          nextHopIf,
                                          action)) {
                return true;
            } else {
                return false;
            }
        } else {
            LOG(ERROR) << "Prefix not found, cannot obtain Admin Distance..";
            return false;        
        }
    }
}


bool
RShuttlev2::insertUpdateBatchV6(std::string prefix,
                              uint8_t prefixLen,
                              uint32_t adminDistance,
                              std::string nextHopAddress,
                              std::string nextHopIf,
                              RShuttlev2::PathUpdateAction action)
{
    bool path_found = false;
    service_layer::SLRoutev6 routev6;
    // check if the prefix exists, and if it does fetch the current 
    // route in RIB

    if (this->routev6_msg.vrfname().empty()) {
        LOG(ERROR) << "Route batch vrf not set, aborting route update...";
        return false;
    } else {
        bool response = this->getPrefixPathsV6(routev6,
                                               this->routev6_msg.vrfname(),
                                               prefix,
                                               prefixLen);
        if (response) {
            VLOG(2) << "Prefix exists in RIB, updating the batch before push.. "
                    << this->ByteArrayStringtoIpv6(routev6.prefix());
            for(int path_cnt=0; path_cnt < routev6.pathlist_size(); path_cnt++) {
                VLOG(3) << "NextHop Interface: "
                        << routev6.pathlist(path_cnt).nexthopinterface().name();

                VLOG(3) << "NextHop Address "
                        << this->ByteArrayStringtoIpv6(routev6.pathlist(path_cnt).nexthopaddress().v6address());

                auto path_nexthop_ip_long = routev6.pathlist(path_cnt).nexthopaddress().v6address();
                auto path_nexthop_ip_str = this->ByteArrayStringtoIpv6(path_nexthop_ip_long);
                auto path_nexthop_if = routev6.pathlist(path_cnt).nexthopinterface().name();

                if (action == RSHUTTLE_PATH_DELETE) {
                    if (path_nexthop_ip_str == nextHopAddress &&
                        path_nexthop_if == nextHopIf) {
                        path_found = true;
                        continue;
                    }
                }

                // Add the existing paths to a route batch again.
                bool batch_add_resp = insertAddBatchV6(prefix,
                                                       prefixLen,
                                                       adminDistance,
                                                       path_nexthop_ip_str,
                                                       path_nexthop_if);

                if (!batch_add_resp) {
                    LOG(ERROR) << "Route insertion into ADD batch unsuccessful \n"
                               << prefix<< "\n"
                               << prefixLen << "\n"
                               << path_nexthop_ip_str << "\n"
                               << path_nexthop_if << "\n";
                    return false;
                }
            }

            switch(action) {
            case RSHUTTLE_PATH_ADD:
                {
                    // Finish off the batch with the new nexthop passed in
                    bool batch_add_resp = insertAddBatchV6(prefix,
                                                           prefixLen,
                                                           adminDistance,
                                                           nextHopAddress,
                                                           nextHopIf);

                    if (!batch_add_resp) {
                        LOG(ERROR) << "Route insertion into ADD batch unsuccessful \n"
                                   << prefix<< "\n"
                                   << prefixLen << "\n"
                                   << nextHopAddress << "\n"
                                   << nextHopIf << "\n";
                        return false;
                    }

                    VLOG(1) << "Path "
                            << "\n  Prefix: " << prefix << "/" << prefixLen
                            << "\n  NextHop Address: " << nextHopAddress
                            << "\n  NextHop Interface: " << nextHopIf
                            << "\nAdded to batch!";
                    return true;
                }
            case RSHUTTLE_PATH_DELETE:
                {
                    if (!path_found) {
                        LOG(ERROR) << "Path not found for delete operation";
                        return false;
                    } else {
                        VLOG(1) << "Path "
                                << "\n  Prefix: " << prefix << "/" << prefixLen
                                << "\n  NextHop Address: " << nextHopAddress
                                << "\n  NextHop Interface: " << nextHopIf
                                << "\nDeleted from batch!";
                        return true;
                    }
                }
            default:
                LOG(ERROR) << "Invalid Path operation";
                return false;
            }
        } else {
            switch(action) {
            case RSHUTTLE_PATH_ADD:
                {
                    VLOG(2) << "Prefix not in RIB, inserting Path into a new Add Batch";
                    bool batch_add_resp = insertAddBatchV6(prefix,
                                                           prefixLen,
                                                           adminDistance,
                                                           nextHopAddress,
                                                           nextHopIf);

                    if (!batch_add_resp) {
                        LOG(ERROR) << "Route insertion into ADD batch unsuccessful \n"
                                   << prefix<< "\n"
                                   << prefixLen << "\n"
                                   << nextHopAddress << "\n"
                                   << nextHopIf << "\n";
                        return false;
                    }
                    VLOG(1) << "Path "
                            << "\n  Prefix: " << prefix << "/" << prefixLen
                            << "\n  NextHop Address: " << nextHopAddress
                            << "\n  NextHop Interface: " << nextHopIf
                            << "\nAdded!";
                    return true;
                }
            case RSHUTTLE_PATH_DELETE:
                {
                    LOG(ERROR) << "Prefix not found, cannot Delete Path..";
                    return false;
                }
            default:
                LOG(ERROR) << "Invalid Path operation";
                return false;
            }
        }
    }
}


void 
RShuttlev2::clearBatchV6()
{
   routev6_msg.clear_routes();
   prefix_map_v6.clear();
}

// Returns true if the prefix exists in Application RIB and route
// gets populated with all the route attributes like Nexthop, adminDistance etc.

bool 
RShuttlev2::getPrefixPathsV6(service_layer::SLRoutev6& route,
                           std::string vrfName,
                           std::string prefix,
                           uint8_t prefixLen,
                           unsigned int timeout)
{

    auto stub_ = service_layer::SLRoutev6Oper::NewStub(channel);
    service_layer::SLRoutev6GetMsg routev6_get_msg;
    service_layer::SLRoutev6GetMsgRsp routev6_get_msg_resp;

    routev6_get_msg.set_vrfname(vrfName);
    routev6_get_msg.set_prefix(ipv6ToByteArrayString(prefix.c_str()));
    routev6_get_msg.set_prefixlen(prefixLen);
    routev6_get_msg.set_entriescount(1);
    routev6_get_msg.set_getnext(false);


    // Context for the client.
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

    if (google::protobuf::TextFormat::PrintToString(routev6_get_msg, &s)) {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Transmitted message: IOSXR-SL Route Get " << s;
        VLOG(2) << "###########################" ;
    } else {
        VLOG(2) << "###########################" ;
        VLOG(2) << "Message not valid (partial content: "
                << routev6_get_msg.ShortDebugString() << ")";
        VLOG(2) << "###########################" ;
        return false;
    }

    //Issue the RPC         

    status = stub_->SLRoutev6Get(&context, routev6_get_msg, &routev6_get_msg_resp);

    if (status.ok()) {
         VLOG(1) << "RPC call was successful, checking response...";


        auto slerr_status =
        static_cast<int>(routev6_get_msg_resp.errstatus().status());


        if (slerr_status ==
               service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {

            VLOG(1) << "IPv6 Route GET Operation successful";

            // We've only requested one entry for prefix in a particular vrf
            // If the returned eof flag is set, then not even one entry was returned,
            // implying the prefix does not exist in the RIB within this vrf.

            if (routev6_get_msg_resp.eof()) {
                return false;
            } else {
                // Successful return and we should get only one entry back
                if (routev6_get_msg_resp.entries_size() == 1) {
                    VLOG(1) << "Received the route from RIB";
                    route = routev6_get_msg_resp.entries(0);
                    return true;
                } else {
                    LOG(ERROR) << "Got more entries than requested, something is wrong";
                    //print the Response         
                    std::string s;

                    if (google::protobuf::TextFormat::PrintToString(routev6_get_msg_resp, &s)) {
                        VLOG(2) << "###########################" ;
                        VLOG(2) << "Received  message: IOSXR-SL Route Get " << s;
                        VLOG(2) << "###########################" ;
                    } else {
                        VLOG(2) << "###########################" ;
                        VLOG(2) << "Message not valid (partial content: "
                                << routev6_get_msg_resp.ShortDebugString() << ")";
                        VLOG(2) << "###########################" ;
                    }
                    return false;
                }
            }

        } else {
            LOG(ERROR) << "Error code for vrf "
                       << routev6_get_msg_resp.vrfname()
                       <<" is 0x"<< std::hex << slerr_status;
            return false;
        }
    } else {
        LOG(ERROR) << "RPC failed, error code is " << status.error_code();
        return false;
    }
}

bool
RShuttlev2::addPrefixPathV6(std::string prefix,
                          uint8_t prefixLen,
                          std::string nextHopAddress,
                          std::string nextHopIf)
{
    // Create a new update batch and push to RIB
    bool 
    batch_update_resp = insertUpdateBatchV6(prefix,
                                            prefixLen,
                                            nextHopAddress,
                                            nextHopIf,
                                            RSHUTTLE_PATH_ADD);
    if (!batch_update_resp) {
        LOG(ERROR) << "Failed to create an update batch";
    } else {
        if (this->routev6Op(service_layer::SL_OBJOP_UPDATE)) {
            return true;
        }
    }
    return false;
}


bool
RShuttlev2::deletePrefixPathV6(std::string prefix,
                             uint8_t prefixLen,
                             std::string nextHopAddress,
                             std::string nextHopIf)
{
    // Create a delete batch and push Delete event to RIB
    bool
    batch_update_resp = insertUpdateBatchV6(prefix,
                                            prefixLen,
                                            nextHopAddress,
                                            nextHopIf,
                                            RSHUTTLE_PATH_DELETE);

    if (!batch_update_resp) {
        LOG(ERROR) << "Failed to create an update batch";
    } else {
        if (this->routev6Op(service_layer::SL_OBJOP_UPDATE)) {
            return true;
        }
    }
    return false;
}


// Version 2 SLAFVFR ----------------------------------------------------------------------------------

SLAFVrf::SLAFVrf(std::shared_ptr<grpc::Channel> Channel, std::string Username, std::string Password)
    : channel(Channel), username(Username), password(Password) {}

// Overloaded variant of vrfRegMsgAdd without adminDistance and Purgeinterval
// Suitable for VRF UNREGISTER and REGISTER operations

void 
SLAFVrf::afVrfRegMsgAdd(std::string vrfName,
                        unsigned int addrFamily)
{

    // Get a pointer to a new af_vrf_reg entry in af_vrf_msg
    service_layer::SLAFVrfReg* af_vrf_reg = af_vrf_msg.add_vrfregmsgs();
    switch(addrFamily) {
        case AF_INET:
            af_vrf_reg->set_table(service_layer::SL_IPv4_ROUTE_TABLE);
        case AF_INET6:
            af_vrf_reg->set_table(service_layer::SL_IPv6_ROUTE_TABLE);
    }

    // Get pointer to a new vrf_rg in af_vrf_reg
    // Double check this
    service_layer::SLVrfReg* vrf_reg = af_vrf_reg->mutable_vrfreg();
    // Populate the new vrf_reg entry
    vrf_reg->set_vrfname(vrfName);

}

// Overloaded variant of vrfRegMsgAdd with adminDistance and Purgeinterval
// Suitable for VRF REGISTER

void
SLAFVrf::afVrfRegMsgAdd(std::string vrfName,
                    unsigned int adminDistance,
                    unsigned int vrfPurgeIntervalSeconds,
                    unsigned int addrFamily)
{
    // Get a pointer to a new af_vrf_reg entry in af_vrf_msg
    service_layer::SLAFVrfReg* af_vrf_reg = af_vrf_msg.add_vrfregmsgs();
    switch(addrFamily) {
        case AF_INET:
            af_vrf_reg->set_table(service_layer::SL_IPv4_ROUTE_TABLE);
        case AF_INET6:
            af_vrf_reg->set_table(service_layer::SL_IPv6_ROUTE_TABLE);
    }

    // Get pointer to a new vrf_rg in af_vrf_reg
    service_layer::SLVrfReg* vrf_reg = af_vrf_reg->mutable_vrfreg();

    // Populate the new vrf_reg entry
    vrf_reg->set_vrfname(vrfName);
    vrf_reg->set_admindistance(adminDistance);
    vrf_reg->set_vrfpurgeintervalseconds(vrfPurgeIntervalSeconds);
}


bool 
SLAFVrf::registerAfVrf(unsigned int addrFamily)
{
    // Send an RPC for VRF registrations

    switch(addrFamily) {
    case AF_INET:
        // Issue VRF Register RPC 
        if (afVrfOpAddFam(service_layer::SL_REGOP_REGISTER)) {
            // RPC EOF to cleanup any previous stale routes
            if (afVrfOpAddFam(service_layer::SL_REGOP_EOF)) {
                return true;
            } else {
                LOG(ERROR) << "Failed to send EOF RPC";
                return false;
            }
        } else {
            LOG(ERROR) << "Failed to send Register RP";
            return false;
        } 
        break;

    case AF_INET6:
        // Issue VRF Register RPC
        if (afVrfOpAddFam(service_layer::SL_REGOP_REGISTER)) {
            // RPC EOF to cleanup any previous stale routes
            if (afVrfOpAddFam(service_layer::SL_REGOP_EOF)) {
                return true;
            } else {
                LOG(ERROR) << "Failed to send EOF RPC";
                return false;
            }
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
SLAFVrf::unregisterAfVrf(unsigned int addrFamily)
{

    //  When done with the VRFs, RPC Delete Registration

    switch(addrFamily) {
    case AF_INET:
        return afVrfOpAddFam(service_layer::SL_REGOP_UNREGISTER);
        break;

    case AF_INET6:
        return afVrfOpAddFam(service_layer::SL_REGOP_UNREGISTER);
        break;

    default:
        LOG(ERROR) << "Invalid Address family, skipping..";
        return false;
        break;
    }
}

bool 
SLAFVrf::afVrfOpAddFam(service_layer::SLRegOp vrfOp)
{
    // Set up the RouteV4Oper Stub
    // auto stub_ = service_layer::SLRoutev4Oper::NewStub(channel);
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

    // Set up vrfRegMsg Operation

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
