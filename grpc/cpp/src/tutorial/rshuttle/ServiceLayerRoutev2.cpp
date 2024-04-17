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


SLAFRShuttle* slaf_route_shuttle;

// client id has to match for vrf registration (SLAFVrfRegOp) and the routes request (routeSLAFOp) and for unregistering (SLAFVrfRegOp) for ipv4 and ipv6.
// client id (Multi-client) is not supported for MPLS
std::string client_id = "521";

bool 
SLAFRShuttle::routeSLAFOp(service_layer::SLObjectOp routeOp,
                    unsigned int addrFamily,
                    unsigned int timeout)
{

    service_layer::SLObjectOp route_op = routeOp;
    route_msg.set_oper(route_op);
    auto stub_ = service_layer::SLAF::NewStub(channel);
    std::string address_family_str = "";
    unsigned int addr_family = addrFamily;
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

    if (addr_family == AF_INET) {
        address_family_str = "IPV4";
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addr_family == AF_INET6){
        address_family_str = "IPV6";
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addr_family == AF_MPLS){
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

    status = stub_->SLAFOp(&context, route_msg, &route_msg_resp);

    if (status.ok()) {
        VLOG(1) << "RPC call was successful, checking response...";

        // // Print Partial failures within the batch if applicable
        bool route_error = false;
        for (int result = 0; result < route_msg_resp.results_size(); result++) {
                auto slerr_status = 
                static_cast<int>(route_msg_resp.results(result).errstatus().status());
                if (slerr_status != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
                    if (addr_family == AF_INET) {
                        LOG(ERROR) << "Error code for prefix: " 
                            << route_msg_resp.results(result).operation().afobject().ipv4route().prefix()
                            << " prefixlen: " 
                            << route_msg_resp.results(result).operation().afobject().ipv4route().prefixlen()
                            <<" is 0x"<< std::hex << slerr_status;
                    } else if (addr_family == AF_INET6) {
                        LOG(ERROR) << "Error code for prefix: " 
                            << route_msg_resp.results(result).operation().afobject().ipv6route().prefix()
                            << " prefixlen: " 
                            << route_msg_resp.results(result).operation().afobject().ipv6route().prefix()
                            <<" is 0x"<< std::hex << slerr_status;
                    } else if (addr_family == AF_MPLS){
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
                           std::string nextHopIf)
{

    auto address = prefix + "/" + std::to_string(prefixLen);
    auto map_index = this->route_msg.oplist_size();

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
        auto operation = this->route_msg.mutable_oplist(prefix_map_v4[address]);
        auto af_object = operation->mutable_afobject();
        auto routev4_ptr = af_object->mutable_ipv4route();
        this->routev4PathAdd(routev4_ptr,
                             ipv4ToLong(nextHopAddress.c_str()),
                             nextHopIf);  
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
                           std::string nextHopIf)
{
    auto address = prefix + "/" + std::to_string(prefixLen);
    auto map_index = this->route_msg.oplist_size();

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
        auto operation = this->route_msg.mutable_oplist(prefix_map_v6[address]);
        auto af_object = operation->mutable_afobject();
        auto routev6_ptr = af_object->mutable_ipv6route();
        this->routev6PathAdd(routev6_ptr,
                             ipv6ToByteArrayString(nextHopAddress.c_str()),
                             nextHopIf);
    }

    return true;
}

unsigned int
SLAFRShuttle::insertAddBatchMPLS(unsigned int startLabel,
                            unsigned int numLabel,
                            unsigned int numPaths,
                            unsigned int batchSize,
                            uint32_t nextHopAddress,
                            std::string nextHopInterface
                            )
{

    unsigned int sent_ilms = 0;
    unsigned int ilms_in_batch = 0;
    unsigned int batch_index = 0;
    unsigned int label = startLabel;
    unsigned int total_ilms = 0;
    unsigned int num_ilms = 1;
    service_layer::SLAFOp* operation = NULL;
    total_ilms = numLabel * num_ilms;

    if (batchSize > total_ilms) {
        batchSize = total_ilms;
    }

    // Currently no support within proto for EXP entries
    while(sent_ilms < total_ilms){
            if (ilms_in_batch + num_ilms > batchSize || sent_ilms + num_ilms >= total_ilms)  {
                batch_index++;
                ilms_in_batch = 0;
                slaf_route_shuttle->routeSLAFOp(service_layer::SL_OBJOP_UPDATE, AF_MPLS);
            }
            /* Create a new ilm entry, and the only way to do that with the current proto file
             is to add a new oplist */
            operation = route_msg.add_oplist();
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
                } else {
                    /* Need an out label for swap */
                    LOG(ERROR) << "Invalid OutLabel \n";
                }
            }
            sent_ilms = sent_ilms + num_ilms;
            ilms_in_batch += num_ilms;
            label++;
        }

        LOG(INFO) << "Number of Batches Sent: " << batch_index << "\n";
        return true;
}

// Version 2 SLAFVFR ----------------------------------------------------------------------------------

SLAFVrf::SLAFVrf(std::shared_ptr<grpc::Channel> Channel, std::string Username, std::string Password)
    : channel(Channel), username(Username), password(Password) {}

// Overloaded variant of afVrfRegMsgAdd without adminDistance and Purgeinterval
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
            break;
        case AF_INET6:
            af_vrf_reg->set_table(service_layer::SL_IPv6_ROUTE_TABLE);
            break;
        case AF_MPLS:
            af_vrf_reg->set_table(service_layer::SL_MPLS_LABEL_TABLE);
            break;
    }

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
                    unsigned int addrFamily)
{
    // Get a pointer to a new af_vrf_reg entry in af_vrf_msg
    service_layer::SLAFVrfReg* af_vrf_reg = af_vrf_msg.add_vrfregmsgs();
    switch(addrFamily) {
        case AF_INET:
            af_vrf_reg->set_table(service_layer::SL_IPv4_ROUTE_TABLE);
            break;
        case AF_INET6:
            af_vrf_reg->set_table(service_layer::SL_IPv6_ROUTE_TABLE);
            break;
        case AF_MPLS:
            af_vrf_reg->set_table(service_layer::SL_MPLS_LABEL_TABLE);
            break;
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
        if (afVrfOpAddFam(service_layer::SL_REGOP_REGISTER, addrFamily)) {
            // RPC EOF to cleanup any previous stale routes
            if (afVrfOpAddFam(service_layer::SL_REGOP_EOF, addrFamily)) {
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
        if (afVrfOpAddFam(service_layer::SL_REGOP_REGISTER, addrFamily)) {
            // RPC EOF to cleanup any previous stale routes
            if (afVrfOpAddFam(service_layer::SL_REGOP_EOF, addrFamily)) {
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

    case AF_MPLS:
        // Issue VRF Register RPC
        if (afVrfOpAddFam(service_layer::SL_REGOP_REGISTER, addrFamily)) {
            // RPC EOF to cleanup any previous stale routes
            if (afVrfOpAddFam(service_layer::SL_REGOP_EOF, addrFamily)) {
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
        return afVrfOpAddFam(service_layer::SL_REGOP_UNREGISTER, addrFamily);
        break;

    case AF_INET6:
        return afVrfOpAddFam(service_layer::SL_REGOP_UNREGISTER, addrFamily);
        break;
    
    case AF_MPLS:
        return afVrfOpAddFam(service_layer::SL_REGOP_UNREGISTER, addrFamily);
        break;

    default:
        LOG(ERROR) << "Invalid Address family, skipping..";
        return false;
        break;
    }
}

bool 
SLAFVrf::afVrfOpAddFam(service_layer::SLRegOp vrfOp, unsigned int addrFamily)
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

    if (addrFamily == AF_INET) {
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addrFamily == AF_INET6) {
        context.AddMetadata("iosxr-slapi-clientid", client_id);
    } else if (addrFamily == AF_MPLS) {
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
