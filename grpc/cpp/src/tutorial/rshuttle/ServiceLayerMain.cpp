#include "ServiceLayerRoute.h"
#include "ServiceLayerRoutev2.h"
#include <cstdint>
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

// Converts string to int safely
int
stringToInt(const std::string& input) {
    int ret = 0;
    try
    {
        ret = std::stoi(input);
    } catch (...) {
        LOG(ERROR) << "Error when Converting String to Int. User did not provide a valid entry. Terminating...";
        exit(1);
    }
    return ret;
}
// Splits a comma separated string into a vector
std::vector<std::string> splitString(const std::string& input) {
    std::vector<std::string> result;
    std::stringstream ss(input);
    std::string item;

    while (std::getline(ss, item, ',')) {
        std::string trimmedItem;
        for (char c : item) {
            if (c != ' ') {  // Check if the character is not a space
                trimmedItem += c; // Add non-space characters to the trimmed string
            }
        }
        if (!trimmedItem.empty()) {
            result.push_back(trimmedItem);
        }
    }

    return result;
}

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

// Checks if rib and/or fib response is what we expect
std::pair<bool,bool> checkRibFibRequired(bool ack_rib_fib_set)
{
    bool rib_req = false;
    bool fib_req = false;
    if (ack_rib_fib_set) {
        rib_req = true;
        fib_req = true;
    } else {
        rib_req = true;
    }

    return std::make_pair(rib_req, fib_req);
}

void
printHelperSlRoutePath(SLAFRShuttle* slaf_route_shuttle, service_layer::SLRoutePath path_object) {
    LOG(INFO) << "\t\t\tSLRoutePath:";
    // If path group key is set, all other fields are ignored
    if (path_object.has_pathgroupkey()) {
        service_layer::SLPathGroupRefKey path_group_key = path_object.pathgroupkey();
        LOG(INFO) << "\t\t\t\tSLPathGroupRefKey:";
        LOG(INFO) << "\t\t\t\t\tVrfName: " << path_group_key.vrfname();
        if (path_group_key.pathgroupid().has_name()) {
            LOG(INFO) << "\t\t\t\t\tPathGroupID: " << path_group_key.pathgroupid().name();
        }
    } else {
        if (path_object.has_nexthopaddress()) {
            service_layer::SLIpAddress address = path_object.nexthopaddress();
            LOG(INFO) << "\t\t\t\tNextHopAddress: ";
            if (address.has_v4address()) {
                LOG(INFO) << "\t\t\t\t\tV4 Address: " << address.v4address();
            }
            if (address.has_v6address()) {
                LOG(INFO) << "\t\t\t\t\tV6 Address: " << slaf_route_shuttle->ByteArrayStringtoIpv6(address.v6address());
            }
        }
        if (path_object.has_nexthopinterface()) {
            service_layer::SLInterface intf = path_object.nexthopinterface();
            LOG(INFO) << "\t\t\t\tNextHopInterface: ";
            if (intf.has_name()) {
                LOG(INFO) << "\t\t\t\t\tName: " << intf.name();
            }
            if(intf.has_handle()) {
                LOG(INFO) << "\t\t\t\t\tHandle: " << intf.handle();
            }
        }
        LOG(INFO) << "\t\t\t\tLoad Metric: " << path_object.loadmetric();
        LOG(INFO) << "\t\t\t\tVRF Name: " << path_object.vrfname();
        LOG(INFO) << "\t\t\t\tMetric: " << path_object.metric();
        LOG(INFO) << "\t\t\t\tPath ID: " << path_object.pathid();

        for (int temp_index = 0; temp_index < path_object.protectedpathbitmap_size(); temp_index++) {
            LOG(INFO) << "\t\t\t\tProtected Path Bitmap: " << path_object.protectedpathbitmap(temp_index);
        }
        for (int temp_index = 0; temp_index < path_object.labelstack_size(); temp_index++) {
            LOG(INFO) << "\t\t\t\tLabel Stack: " << path_object.labelstack(temp_index);
        }
        for (int temp_index = 0; temp_index < path_object.remoteaddress_size(); temp_index++) {
            service_layer::SLIpAddress address = path_object.remoteaddress(temp_index);
            LOG(INFO) << "\t\t\t\tRemote Address:";
            if (address.has_v4address()) {
                LOG(INFO) << "\t\t\t\t\tV4 Address: " << address.v4address();
            }
            if (address.has_v6address()) {
                LOG(INFO) << "\t\t\t\t\tV6 Address: " << slaf_route_shuttle->ByteArrayStringtoIpv6(address.v6address());
            }
        }

        if (path_object.has_vxlanpath()) {
            service_layer::SLVxLANPath vxlan_path = path_object.vxlanpath();
            LOG(INFO) << "\t\t\t\tSLVxLANPath:";
            LOG(INFO) << "\t\t\t\t\tVNI: " << vxlan_path.vni();
            LOG(INFO) << "\t\t\t\t\tSource Mac Address: " << vxlan_path.sourcemacaddress();
            LOG(INFO) << "\t\t\t\t\tDest Mac Address: " << vxlan_path.destmacaddress();

            LOG(INFO) << "\t\t\t\t\tSrc Ip Address:";
            service_layer::SLIpAddress src_address = vxlan_path.srcipaddress();
            if (src_address.has_v4address()) {
                LOG(INFO) << "\t\t\t\t\t\tV4 Address: " << src_address.v4address();
            }
            if(src_address.has_v6address()) {
                LOG(INFO) << "\t\t\t\t\t\tV6 Address: " << slaf_route_shuttle->ByteArrayStringtoIpv6(src_address.v6address());
            }

            LOG(INFO) << "\t\t\t\t\tDest Ip Address:";
            service_layer::SLIpAddress dest_address = vxlan_path.destipaddress();
            if (dest_address.has_v4address()) {
                LOG(INFO) << "\t\t\t\t\t\tV4 Address: " << dest_address.v4address();
            }
            if(dest_address.has_v6address()) {
                LOG(INFO) << "\t\t\t\t\t\tV6 Address: " << slaf_route_shuttle->ByteArrayStringtoIpv6(dest_address.v6address());
            }
        }
        for (int temp_index = 0; temp_index < path_object.pathflags_size(); temp_index++) {
            LOG(INFO) << "\t\t\t\t\tPath Flag: " << path_object.pathflags(temp_index);
        }
    }
}

void
printHelperSLAFObject(SLAFRShuttle* slaf_route_shuttle, service_layer::SLAFObject af_object) {
    LOG(INFO) << "\t\tSLAFObject:";
    if (af_object.has_iproute()) {
        service_layer::SLAFIPRoute ip_route = af_object.iproute();
        LOG(INFO) << "\t\t\tSLAFIPRoute:";
        if (ip_route.has_iprouteprefix()) {
            service_layer::SLRoutePrefix ip_route_prefix = ip_route.iprouteprefix();
            LOG(INFO) << "\t\t\t\tSLRoutePrefix:";
            if (ip_route_prefix.has_prefix()) {
                service_layer::SLIpAddress address = ip_route_prefix.prefix();
                LOG(INFO) << "\t\t\t\t\tPrefix: ";
                if (address.has_v4address()) {
                    LOG(INFO) << "\t\t\t\t\t\tV4 Address: " << address.v4address();
                }
                if (address.has_v6address()) {
                    LOG(INFO) << "\t\t\t\t\t\tV6 Address: " << slaf_route_shuttle->ByteArrayStringtoIpv6(address.v6address());
                }
            }

            LOG(INFO) << "\t\t\t\tPrefixLen: " << ip_route_prefix.prefixlen();
        }

        if (ip_route.has_routecommon()) {
            service_layer::SLRouteCommon route_common = ip_route.routecommon();
            LOG(INFO) << "\t\t\tSLRouteCommon:";
            LOG(INFO) << "\t\t\t\tAdminDistance: " << route_common.admindistance();
            LOG(INFO) << "\t\t\t\tLocalLabel: " << route_common.locallabel();
            LOG(INFO) << "\t\t\t\tTag: " << route_common.tag();
            LOG(INFO) << "\t\t\t\tSrcProto: " << route_common.srcproto();
            LOG(INFO) << "\t\t\t\tSrcProtoTag: " << route_common.srcprototag();
            for (int route_flag_index = 0; route_flag_index < route_common.routeflags_size(); route_flag_index++) {
                LOG(INFO) << "\t\t\t\tRouteFlags Set: " << route_common.routeflags(route_flag_index);
            }
        }

        for (int path_index = 0; path_index < ip_route.pathlist_size(); path_index++) {
            service_layer::SLRoutePath path_object = ip_route.pathlist(path_index);
            printHelperSlRoutePath(slaf_route_shuttle, path_object);
        }
    } else if (af_object.has_mplslabel()) {
        service_layer::SLMplsEntry mpls_entry_key = af_object.mplslabel();
        LOG(INFO) << "\t\tSLMplsEntry: ";

        if (mpls_entry_key.has_mplskey()) {
            LOG(INFO) << "\t\t\t Mpls Key: " << mpls_entry_key.mplskey().label();
        }
        LOG(INFO) << "\t\t\tAdminDistance: " << mpls_entry_key.admindistance();
        for (int path_index = 0; path_index < mpls_entry_key.pathlist_size(); path_index++) {
            service_layer::SLRoutePath path_object = mpls_entry_key.pathlist(path_index);
            printHelperSlRoutePath(slaf_route_shuttle, path_object);
        }

        for (int route_flag_index = 0; route_flag_index < mpls_entry_key.mplsflags_size(); route_flag_index++) {
            LOG(INFO) << "\t\t\tMPLSFlags: " << mpls_entry_key.mplsflags(route_flag_index);
        }
    } else if (af_object.has_pathgroup()) {
        service_layer::SLPathGroup pg = af_object.pathgroup();
        LOG(INFO) << "\t\tSLPathGroup:";

        if (pg.has_pathgroupid()) {
            if (pg.pathgroupid().has_name()) {
                LOG(INFO) << "\t\t\tPath Group ID:" << pg.pathgroupid().name();
            }
        }
        LOG(INFO) << "\t\t\tAdminDistance: " << pg.admindistance();
        if (pg.has_pathlist()) {
            service_layer::SLPathGroup::SLPathList path_list = pg.pathlist();
            LOG(INFO) << "\t\tPaths List";
            for(int path_list_index = 0; path_list_index < path_list.paths_size(); path_list_index++) {
                service_layer::SLPathGroup::SLPath path = path_list.paths(path_list_index);
                if (path.has_path()) {
                    service_layer::SLRoutePath path_object = path.path();
                    printHelperSlRoutePath(slaf_route_shuttle, path_object);
                }
            }
        }
        for (int route_flag_index = 0; route_flag_index < pg.pgflags_size(); route_flag_index++) {
            LOG(INFO) << "\t\t\tPGFlags: " << pg.pgflags(route_flag_index);
        }
    }
}

// Prints all the values from the SLAFGet responses
void
printNotifStreamResponses(SLAFRShuttle* slaf_route_shuttle, std::vector<service_layer::SLAFNotifMsg> responses){
    for (service_layer::SLAFNotifMsg response_msg: responses) {
        LOG(INFO) << "-----------------------------------Notif Stream Response Messsage-----------------------------------";
        LOG(INFO) << "VrfName: " << response_msg.vrfname();

        for (int afnotif_index = 0; afnotif_index < response_msg.afnotifs_size(); afnotif_index++) {
            service_layer::SLAFNotif afnotif = response_msg.afnotifs(afnotif_index);
            LOG(INFO) << "service_layer::SLAFNotif with index: " << afnotif_index;

            if (afnotif.has_notifstatus()) {
                LOG(INFO) << "\tNotifStatus:";
                service_layer::SLAFNotifRsp notif_rsp = afnotif.notifstatus();

                if (notif_rsp.notifstatus().status() != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
                    LOG(ERROR) << "\t\tError in response message. Error type : 0x" << std::hex << notif_rsp.notifstatus().status();
                }

                if (notif_rsp.has_notifreq()) {
                    LOG(INFO) << "\t\tNotif Request:";
                    service_layer::SLAFNotifRegReq notif_request = notif_rsp.notifreq();
                    if (notif_request.has_redistreq()) {
                        LOG(INFO) << "\t\t\tRedistReq:";
                        service_layer::SLAFRedistRegMsg redist_req = notif_request.redistreq();
                        LOG(INFO) << "\t\t\t\tSrcProto: " << redist_req.srcproto();
                        LOG(INFO) << "\t\t\t\tSrcProtoTag: " << redist_req.srcprototag();
                        LOG(INFO) << "\t\t\t\tTable: " << redist_req.table();
                    }
                    if (notif_request.has_nexthopreq()) {
                        LOG(INFO) << "\t\t\tNextHopReq: ";
                        service_layer::SLAFNextHopRegMsg next_hop_req = notif_request.nexthopreq();

                        if (next_hop_req.has_nexthopkey()) {
                            service_layer::SLAFNextHopRegKey next_hop_key = next_hop_req.nexthopkey();
                            LOG(INFO) << "\t\t\t\tNextHopKey:";

                            if (next_hop_key.has_nexthop()) {
                                service_layer::SLAFNextHopRegKey_SLNextHopKey next_hop = next_hop_key.nexthop();
                                LOG(INFO) << "\t\t\t\t\tNextHop:";

                                if (next_hop.has_nexthopip()) {
                                    service_layer::SLRoutePrefix next_hop_ip = next_hop.nexthopip();
                                    LOG(INFO) << "\t\t\t\t\tNextHopIP:";
                                    if (next_hop_ip.has_prefix()) {
                                        service_layer::SLIpAddress address = next_hop_ip.prefix();
                                        LOG(INFO) << "\t\t\t\t\t\tPrefix: ";
                                        if (address.has_v4address()) {
                                            LOG(INFO) << "\t\t\t\t\t\t\tV4 Address: " << address.v4address();
                                        }
                                        if (address.has_v6address()) {
                                            LOG(INFO) << "\t\t\t\t\t\t\tV6 Address: " << slaf_route_shuttle->ByteArrayStringtoIpv6(address.v6address());
                                        }
                                    }
                                    LOG(INFO) << "\t\t\t\t\tPrefixLen: " << next_hop_ip.prefixlen();
                                }
                                LOG(INFO) << "\t\t\t\t\t\tExactMatch: " << next_hop.exactmatch();
                                LOG(INFO) << "\t\t\t\t\t\tAllowDefault: " << next_hop.allowdefault();
                                LOG(INFO) << "\t\t\t\t\t\tRecurse: " << next_hop.recurse();
                            }
                        }
                    }
                    LOG(INFO) << "\t\t\tOperationID: " << notif_request.operationid();
                }
            }

            if (afnotif.has_startmarker()) {
                service_layer::SLAFNotif_SLRedistMarker start_marker = afnotif.startmarker();
                LOG(INFO) << "\tStartMarker:";
                LOG(INFO) << "\t\tTable: " << start_marker.table();
            }
            if (afnotif.has_endmarker()) {
                service_layer::SLAFNotif_SLRedistMarker end_marker = afnotif.endmarker();
                LOG(INFO) << "\tEndMarker:";
                LOG(INFO) << "\t\tTable: " << end_marker.table();
            }
            if (afnotif.has_redistobject()) {
                service_layer::SLAFObject redist_object = afnotif.redistobject();
                LOG(INFO) << "\tRedistObject:";
                printHelperSLAFObject(slaf_route_shuttle, redist_object);
            }

            if (afnotif.has_nexthop()) {
                service_layer::SLNextHop sl_next_hop = afnotif.nexthop();
                LOG(INFO) << "\tSLNextHop:";

                if (sl_next_hop.has_nexthopkey()) {
                    service_layer::SLAFNextHopRegKey next_hop_key = sl_next_hop.nexthopkey();
                    LOG(INFO) << "\t\tNextHopKey:";
                    if (next_hop_key.has_nexthop()) {
                        service_layer::SLAFNextHopRegKey_SLNextHopKey next_hop = next_hop_key.nexthop();
                        LOG(INFO) << "\t\t\tNextHop:";

                        if (next_hop.has_nexthopip()) {
                            service_layer::SLRoutePrefix next_hop_ip = next_hop.nexthopip();
                            LOG(INFO) << "\t\t\t\tNextHopIP:";
                            if (next_hop_ip.has_prefix()) {
                                service_layer::SLIpAddress address = next_hop_ip.prefix();
                                LOG(INFO) << "\t\t\t\t\tPrefix: ";
                                if (address.has_v4address()) {
                                    LOG(INFO) << "\t\t\t\t\t\tV4 Address: " << address.v4address();
                                }
                                if (address.has_v6address()) {
                                    LOG(INFO) << "\t\t\t\t\t\tV6 Address: " << slaf_route_shuttle->ByteArrayStringtoIpv6(address.v6address());
                                }
                            }
                            LOG(INFO) << "\t\t\t\t\tPrefixLen: " << next_hop_ip.prefixlen();
                        }
                        LOG(INFO) << "\t\t\t\t\t\tExactMatch: " << next_hop.exactmatch();
                        LOG(INFO) << "\t\t\t\t\t\tAllowDefault: " << next_hop.allowdefault();
                        LOG(INFO) << "\t\t\t\t\t\tRecurse: " << next_hop.recurse();
                    }
                }

                if (sl_next_hop.has_resolvingprefix()) {
                    service_layer::SLRoutePrefix resolving_prefix = sl_next_hop.resolvingprefix();
                    LOG(INFO) << "\t\tResolvingPrefix:";
                    if (resolving_prefix.has_prefix()) {
                        service_layer::SLIpAddress address = resolving_prefix.prefix();
                        LOG(INFO) << "\t\t\tPrefix: ";
                        if (address.has_v4address()) {
                            LOG(INFO) << "\t\t\t\tV4 Address: " << address.v4address();
                        }
                        if (address.has_v6address()) {
                            LOG(INFO) << "\t\t\t\tV6 Address: " << slaf_route_shuttle->ByteArrayStringtoIpv6(address.v6address());
                        }
                    }
                    LOG(INFO) << "\t\t\tPrefixLen: " << resolving_prefix.prefixlen();
                }

                LOG(INFO) << "\t\tSrcProto: " << sl_next_hop.srcproto();
                LOG(INFO) << "\t\tSrcProtoTag: " << sl_next_hop.srcprototag();
                LOG(INFO) << "\t\tAdminDistance: " << sl_next_hop.admindistance();
                LOG(INFO) << "\t\tMetric: " << sl_next_hop.metric();
                for (int path_index = 0; path_index < sl_next_hop.paths_size(); path_index++) {
                    service_layer::SLRoutePath path_object = sl_next_hop.paths(path_index);
                    printHelperSlRoutePath(slaf_route_shuttle, path_object);
                }
            }
        }
    }
}

// Prints all the values from the SLAFGet responses
void
printVrfGetResponses(SLAFRShuttle* slaf_route_shuttle, std::vector<service_layer::SLAFVrfRegGetMsgRsp> responses){
    for (service_layer::SLAFVrfRegGetMsgRsp response_msg: responses) {
        LOG(INFO) << "-----------------------------------Get VRF Response Messsage-----------------------------------";
        if (response_msg.errstatus().status() != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
            LOG(ERROR) << "Error in response message. Error type : 0x" << std::hex << response_msg.errstatus().status();
        }
        LOG(INFO) << "ClientID: " << response_msg.clientid();
        LOG(INFO) << "Table: " << response_msg.table();
        for (int vrf_reg_index = 0; vrf_reg_index < response_msg.entries_size(); vrf_reg_index++) {
            service_layer::SLVrfReg vrf_reg = response_msg.entries(vrf_reg_index);
            LOG(INFO) << "\tVrfName: " << vrf_reg.vrfname();
            LOG(INFO) << "\tAdminDistance: " << vrf_reg.admindistance();
            LOG(INFO) << "\tVrfPurgeIntervalSeconds: " << vrf_reg.vrfpurgeintervalseconds();
        }
    }
}

// Prints all the values from the SLAFGet responses
void
printGetResponses(SLAFRShuttle* slaf_route_shuttle, std::vector<service_layer::SLAFGetMsgRsp> responses)
{
    for (service_layer::SLAFGetMsgRsp response_msg: responses) {
        LOG(INFO) << "-----------------------------------Get Response Messsage-----------------------------------";
        if (response_msg.errstatus().status() != service_layer::SLErrorStatus_SLErrno_SL_SUCCESS) {
            LOG(ERROR) << "Error in response message. Error type : 0x" << std::hex << response_msg.errstatus().status();
        }

        LOG(INFO) << "Vrfname: " << response_msg.vrfname();
        LOG(INFO) << "ClientID: " << response_msg.clientid();
        for (int index = 0; index < response_msg.aflist_size(); index++) {
            service_layer::SLAFGetMsgRspEntry af_entry = response_msg.aflist(index);
            LOG(INFO) << "service_layer::SLAFGetMsgRspEntry with index " << index;
            if (af_entry.has_afopmsg()) {
                service_layer::SLAFOpMsg af_op_msg = af_entry.afopmsg();
                LOG(INFO) << "\tSLAFOpMsg:";

                service_layer::SLAFObject af_object = af_op_msg.afobject();
                printHelperSLAFObject(slaf_route_shuttle, af_object);
                LOG(INFO) << "\tOperationID: " << af_op_msg.operationid();
                LOG(INFO) << "\tAckType: " << af_op_msg.acktype();
                for (int permit_index = 0; permit_index < af_op_msg.ackpermits_size(); permit_index++) {
                    LOG(INFO) << "\tAckPermit: " << af_op_msg.ackpermits(permit_index);
                }
                LOG(INFO) << "\tAck Cadence: " << af_op_msg.ackcadence();
            }
            LOG(INFO) << "FIB Status: " << af_entry.fibstatus();
        }
    }
}

// Goes through the DB and prints errors
void printDbErrors(testingData env_data, service_layer::SLTableType addr_family)
{
    if (addr_family == service_layer::SL_IPv4_ROUTE_TABLE) {
        for (auto ipv4_index = database.db_ipv4.begin(); ipv4_index != database.db_ipv4.end(); ipv4_index++) {
            std::pair<bool, bool> check = checkRibFibRequired(
                        ipv4_index->second.first.response_acks.response_ack_type_rib_fib_set);
            if (check.second == true && env_data.stream_case == true) {
                if (ipv4_index->second.second.fib_success == false || ipv4_index->second.second.rib_success == false) {
                    LOG(ERROR) << ipv4_index->second.second.error;
                }
            }
            if (check.first == true) {
                if (ipv4_index->second.second.rib_success == false) {
                    LOG(ERROR) << ipv4_index->second.second.error;
                }
            }
        }
    } else if (addr_family == service_layer::SL_IPv6_ROUTE_TABLE) {
        for (auto ipv6_index = database.db_ipv6.begin(); ipv6_index != database.db_ipv6.end(); ipv6_index++) {
            std::pair<bool, bool> check = checkRibFibRequired(
                        ipv6_index->second.first.response_acks.response_ack_type_rib_fib_set);
            if (check.second == true && env_data.stream_case == true) {
                if (ipv6_index->second.second.fib_success == false || ipv6_index->second.second.rib_success == false) {
                    LOG(ERROR) << ipv6_index->second.second.error;
                }
            }
            if (check.first == true) {
                if (ipv6_index->second.second.rib_success == false) {
                    LOG(ERROR) << ipv6_index->second.second.error;
                }
            }
        }
    } else if (addr_family == service_layer::SL_MPLS_LABEL_TABLE) {
        for (auto mpls_index = database.db_mpls.begin(); mpls_index != database.db_mpls.end(); mpls_index++) {
            std::pair<bool, bool> check = checkRibFibRequired(
                        mpls_index->second.first.response_acks.response_ack_type_rib_fib_set);
            if (check.second == true && env_data.stream_case == true) {
                if (mpls_index->second.second.fib_success == false || mpls_index->second.second.rib_success == false) {
                    LOG(ERROR) << mpls_index->second.second.error;
                }
            }
            if (check.first == true) {
                if (mpls_index->second.second.rib_success == false) {
                    LOG(ERROR) << mpls_index->second.second.error;
                }
            }
        }
    } else if (addr_family == service_layer::SL_PATH_GROUP_TABLE) {
        for (auto pg_index = database.db_pg.begin(); pg_index != database.db_pg.end(); pg_index++) {
            std::pair<bool, bool> check = checkRibFibRequired(
                        pg_index->second.first.response_acks.response_ack_type_rib_fib_set);
            if (check.second == true && env_data.stream_case == true) {
                if (pg_index->second.second.fib_success == false || pg_index->second.second.rib_success == false) {
                    LOG(ERROR) << pg_index->second.second.error;
                }
            }
            if (check.first == true) {
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
        uint32_t prefix_len = env_data.prefix_len_ipv4;
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
        uint32_t prefix_len = env_data.prefix_len_ipv6;
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
        uint32_t local_label = env_data.local_label;
        database.mpls_start_index = local_label;
        for(int i = 0; i < env_data.num_operations; i++){
            statusObject dummy;
            std::pair<testingData, statusObject> temp = std::make_pair(env_data, dummy);
            database.db_mpls[local_label+i] = temp;
            database.db_count++;
        }
        database.mpls_last_index = local_label+env_data.num_operations-1;

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
            // If vrf_reg_oper not set then we do not register vrf
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
                if (route_shuttle_object_created) {
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

void get_slaf(SLAFRShuttle* slaf_route_shuttle,
               testingData env_data)
{
    Timer tmr;
    int total_responses = 0;

    if (env_data.get_vrf_request == true) {
        std::vector<service_layer::SLAFVrfRegGetMsgRsp> responses = slaf_route_shuttle->routeSLAFVrfGet();
        total_responses = responses.size();
        auto time_taken = tmr.elapsed();

        LOG(INFO) << "\nTime taken to get "<< total_responses << " responses\n " 
                << time_taken
                << "\nGet Vrf programming rate\n"
                << float(total_responses)/time_taken << " responses/sec\n";
        // Print the responses from the getvrf request
        printVrfGetResponses(slaf_route_shuttle, responses);
    } else {
        getMatchObjects objs_to_search;

        LOG(INFO) << "Starting Get Request Message";
        if (env_data.get_match == true && env_data.get_match_route == true) {
            // Populate all types of Objects needed
            objs_to_search.pg_regexs = env_data.get_route_match_list.pg_regex;
            objs_to_search.vxlan_vn_ids = env_data.get_route_match_list.vxlan_vn_id;
            for (auto slaf_obj: env_data.get_route_match_list.slaf_obj_key) {
                if (slaf_obj.addr_family == service_layer::SL_IPv4_ROUTE_TABLE) {
                    auto prefix = slaf_route_shuttle->ipv4ToLong(slaf_obj.start_ipv4.c_str());
                    uint32_t prefix_len = slaf_obj.prefix_len_ipv4;
                    for (int j = 1; j <= slaf_obj.num_operations; j++, prefix=incrementIpv4Pfx(prefix,prefix_len)) {
                        objs_to_search.ipv4_routes.push_back(std::make_pair(prefix, prefix_len));
                    }
                } else if (slaf_obj.addr_family == service_layer::SL_IPv6_ROUTE_TABLE) {
                    auto prefix = slaf_route_shuttle->ipv6ToByteArrayString(slaf_obj.start_ipv6.c_str());
                    uint32_t prefix_len = slaf_obj.prefix_len_ipv6;
                    for (int j = 1; j <= slaf_obj.num_operations; j++, prefix=slaf_route_shuttle->incrementIpv6Pfx(prefix,prefix_len)) {
                        objs_to_search.ipv6_routes.push_back(std::make_pair(prefix, prefix_len));
                    }
                } else if (slaf_obj.addr_family == service_layer::SL_MPLS_LABEL_TABLE) {
                    uint32_t local_label = slaf_obj.start_mpls;
                    for (int j = 0; j < slaf_obj.num_operations; j++){
                        objs_to_search.mpls_labels.push_back(local_label+j);
                    }

                } else if (slaf_obj.addr_family == service_layer::SL_PATH_GROUP_TABLE) {
                    objs_to_search.pg_ids.push_back(slaf_obj.pg_name);
                }
            }
        }

        std::vector<service_layer::SLAFGetMsgRsp> responses =
            slaf_route_shuttle->routeSLAFGet(env_data.get_vrf_name, env_data.get_match, env_data.get_match_route,
                        env_data.get_client_all,objs_to_search,env_data.get_client_id_list,
                        env_data.get_table_type_list);

        total_responses = responses.size();

        auto time_taken = tmr.elapsed();
        LOG(INFO) << "\nTime taken to get "<< total_responses << " responses\n " 
                << time_taken
                << "\nGet programming rate\n"
                << float(total_responses)/time_taken << " responses/sec\n";
        // Print the responses from the get request
        printGetResponses(slaf_route_shuttle, responses);
    }
}

void try_get_slaf(std::shared_ptr<grpc::Channel> channel,
               std::string grpc_server,
               testingData env_data)
{
    bool exception_caught = true;
    int attempts = 1;
    bool route_shuttle_object_created = false;
    while(attempts <= maxAttempts) {
        try
        {
            route_shuttle_object_created = false;
            slaf_route_shuttle = new SLAFRShuttle(channel, username, password);
            route_shuttle_object_created = true;
            get_slaf(slaf_route_shuttle, env_data);

            exception_caught = false;
        }
        // Error Handling: If any RPC fails with UNAVAILABLE code we have to attempt to retry
        catch (grpc::Status status) {
            if (!status.ok()) {
                // If we are not below max attempts retry
                LOG(INFO) << "RETRY ATTEMPT Number: " << attempts;
                if (route_shuttle_object_created) {
                    delete slaf_route_shuttle;
                }
            }
            if (status.error_code() != grpc::StatusCode::UNAVAILABLE) {
                LOG(INFO) << "Cannot retry for status code: " << status.error_code();
                attempts = maxAttempts + 1;
                break;
            }
        }
        if (!exception_caught) {
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

void
notif_slaf (SLAFRShuttle *slaf_route_shuttle, testingData env_data)
{
    Timer tmr;
    int   total_responses = 0;
    getMatchObjects objs_to_search;
    std::vector<service_layer::SLAFNotifMsg> responses;

    LOG(INFO) << "Starting Notif Stream Message";
    // Update the notifNextHopObj with the correct address types
    for (int i = 0; i < env_data.notif_next_hop.size(); i++) {
        if (env_data.notif_next_hop[i].v4_set) {
            env_data.notif_next_hop[i].ipv4_address_uint = slaf_route_shuttle->ipv4ToLong(env_data.notif_next_hop[i].ipv4_address.c_str());
        } else {
            env_data.notif_next_hop[i].ipv6_address = slaf_route_shuttle->ipv6ToByteArrayString(env_data.notif_next_hop[i].ipv6_address.c_str());
        }
    }
    responses = slaf_route_shuttle->routeSLAFNotifStream(env_data.batch_size,
                            env_data.notif_oper, env_data.notif_vrfname,
                            env_data.notif_route, env_data.notif_next_hop,
                            env_data.notification_stream_duration);

    auto time_taken = tmr.elapsed();
    total_responses = responses.size();
    LOG(INFO) << "\nTime taken to get " << total_responses
                << " responses\n " << time_taken
                << "\nGet programming rate\n"
                << float(total_responses) / time_taken << " responses/sec\n";
    printNotifStreamResponses(slaf_route_shuttle, responses);
}

void try_notif_slaf(std::shared_ptr<grpc::Channel> channel,
                std::string grpc_server,
                testingData env_data)
{
    bool exception_caught = true;
    int attempts = 1;
    bool route_shuttle_object_created = false;
    while(attempts <= maxAttempts) {
        try
        {
            SLGLOBALSHUTTLE* sl_global_shuttle;
            sl_global_shuttle = new SLGLOBALSHUTTLE(channel, username, password);
            sl_global_shuttle->getGlobals(env_data.batch_size, env_data.max_paths);
            delete sl_global_shuttle;
            route_shuttle_object_created = false;
            slaf_route_shuttle = new SLAFRShuttle(channel, username, password);
            route_shuttle_object_created = true;
            notif_slaf(slaf_route_shuttle, env_data);

            exception_caught = false;
        }
        // Error Handling: If any RPC fails with UNAVAILABLE code we have to attempt to retry
        catch (grpc::Status status) {
            if (!status.ok()) {
                // If we are not below max attempts retry
                LOG(INFO) << "RETRY ATTEMPT Number: " << attempts;
                if (route_shuttle_object_created) {
                    delete slaf_route_shuttle;
                }
            }
            if (status.error_code() != grpc::StatusCode::UNAVAILABLE || status.error_code() != grpc::StatusCode::CANCELLED) {
                LOG(INFO) << "Cannot retry for status code: " << status.error_code();
                attempts = maxAttempts + 1;
                break;
            }
        }
        if (!exception_caught) {
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
        {"operation", required_argument, nullptr, 'a'},
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
        {"local_label", required_argument, nullptr, 'o'},
        {"out_label", required_argument, nullptr, 'K'},
        {"num_paths", required_argument, nullptr, 'q'},
        {"create_path_group_for", required_argument, nullptr, 'r'},
        {"path_group_name", required_argument, nullptr, 'y'},
        {"response_ack_type", required_argument, nullptr, 'A'},
        {"response_ack_permit", required_argument, nullptr, 'B'},
        {"response_ack_cadence", required_argument, nullptr, 'C'},
        {"vrf_name", required_argument, nullptr, 'D'},
        {"client_id", required_argument, nullptr, 'E'},
        {"match_table_list", required_argument, nullptr, 'F'},
        {"match_route_list", no_argument, nullptr, 'G'},
        {"add_vxlanvn_id", required_argument, nullptr, 'H'},
        {"add_pg_regex", required_argument, nullptr, 'I'},
        {"add_object_type", required_argument, nullptr, 'J'},
        {"notif_stream_duration", required_argument, nullptr, 'L'},
        {"notif_oper", required_argument, nullptr, 'M'},
        {"notif_vrfname", required_argument, nullptr, 'N'},
        {"notif_route", required_argument, nullptr, 'O'},
        {"notif_nh", required_argument, nullptr, 'P'},

        {"help", no_argument, nullptr, 'h'},
        {"username", required_argument, nullptr, 'u'},
        {"password", required_argument, nullptr, 'p'},
        {"slaf", required_argument, nullptr, 'v'},
        {"global_init", required_argument, nullptr, 's'},

        {nullptr,0,nullptr,0}
    };

    while ((option_long = getopt_long_only(argc, argv, "t:a:w:b:c:x:d:e:f:g:i:j:k:l:m:n:o:K:q:r:s:hu:p:v:y:A:B:C:D:E:F:GH:I:J:L:M:N:O:P:",longopts,nullptr)) != -1) {
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
                } else if (dummy == "Get") {
                    env_data.get_request = true;
                } else if (dummy == "GetVrf") {
                    env_data.get_vrf_request = true;
                }  else if (dummy == "Notification") {
                    env_data.notif_request = true;
                } else {
                    fprintf (stderr, "Requires: %s --operation (Add), (Update), (Delete), (Get), (GetVrf) \n", argv[0]);
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
                env_data.num_operations = stringToInt(optarg);
                break;
            case 'c':
                env_data.batch_size = stringToInt(optarg);
                break;
            case 'x':
                dummy = optarg;
                if (dummy == "false") {
                    env_data.stream_case = false;
                }
                break;
            case 'd':
                env_data.first_prefix_ipv4 = optarg;
                break;
            case 'e':
                env_data.prefix_len_ipv4 = stringToInt(optarg);
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
                env_data.prefix_len_ipv6 = stringToInt(optarg);
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
                env_data.local_label = stringToInt(optarg);
                break;
            case 'K':
                env_data.out_label = stringToInt(optarg);
                break;
            case 'q':
                env_data.num_paths = stringToInt(optarg);
                break;
            case 'r':
                dummy = optarg;
                if (dummy == "ipv6") {
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
                LOG(INFO) << "For specific examples please refer to the README";
                LOG(INFO) << "Usage:";
                LOG(INFO) << "Required Arguments: ";
                LOG(INFO) << "| -u/--username                    | Username (Required argument) |";
                LOG(INFO) << "| -p/--password                    | Password (Required argument) |";
                LOG(INFO) << "| -a/--operation                   | Operation: Add, Update, Delete, Get, GetVrf, Notification. For GetVrf no commands below required. (Required argument) |";
                LOG(INFO) << "| -w/--vrf_reg_oper                | VRF registration Operation: Register, Unregister, EOF. Used only when operation set to Add, Update, or Delete. When Unregister, all existing pushed routes will be deleted and route pushing will not be performed. Remember to specify correct table_type when Unregistering (Required argument) |";
                LOG(INFO) << "Optional arguments you can set for programming routes of ipv4, ipv6, mpls, and path groups (Add, Update, Delete) and vrf registration:";
                LOG(INFO) << "| -h/--help                        | Help |";
                LOG(INFO) << "| -t/--table_type                  | Specify whether to do ipv4, ipv6 or mpls operation, PG (default ipv4) |";
                LOG(INFO) << "| -v/--slaf                        | Specify if you want to use slaf proto RPCs to program objects or not. If not, no other configurations will be used and it will only push 100k ipv4 routes in a unary rpc. (default true) |";
                LOG(INFO) << "| -s/--global_init                 | Enable our Async Global Init RPC to handshake the API version number with the server (default false) |";
                LOG(INFO) << "| -b/--num_operations              | Configure the number of ipv4 routes, ipv6 routes, or MPLS entires to be added to a batch. If table_type is set to pg then 0 < num_operations <= 64 (default 1) |";
                LOG(INFO) << "| -c/--batch_size                  | Configure the number of ipv4 routes ipv6 routes, or ILM entires for MPLS to be added to a batch (default 1024) |";
                LOG(INFO) << "| -x/--stream_case                 | Want to use the streaming rpc (true) or unary rpc (false). Only used with slaf protos. When using unary, the response Ack given from server will always be RIB status. (default true) |";
                LOG(INFO) << "| -y/--path_group_name             | Configure the name of the path group to use. This is the name for the new path you want to create when when table_type is set to pg. \n"
                            << "                                    When table_type is any other option then this will specify the existing path group to use for pushing routes. In this case, make sure path group name exist (default "") |";
                LOG(INFO) << "| -A/--response_ack_type           | Configure the type of response that the client expects from the network element for any object programming operation. Please see Proto file for all options. If typed incorrectly, will resort to default (default RIB_ACK) |";
                LOG(INFO) << "| -B/--response_ack_permit         | Configure the list that controls the types of hardware programming responses as defined in SLAFFibStatus that the client is interested in. \n"
                            << "                                     For this tutorial we allow one option to be set. Please see Proto file for all options. If typed incorrectly, will resort to default (default SL_PERMIT_FIB_STATUS_ALL)"
                            << "                                     Regardless of the response ack permit set, this tutorial does not verify any response other than RIB or FIB Success based on ack type. This option is just to demonstrate how to set this field. (default "") |";
                LOG(INFO) << "| -C/--response_ack_cadence        | Configure the cadence of hardware programming responses. Defining response_ack_permit is a pre-requisite. Please see Proto file for all options. If typed incorrectly, will resort to default (default SL_RSP_CONTINUOUS) |";
                LOG(INFO) << "Programming IPv4 Routes (table_type is set to ipv4)";
                LOG(INFO) << "| -d/--first_prefix_ipv4           | Configure the starting address for this test for IPV4 (default 40.0.0.0) |";
                LOG(INFO) << "| -e/--prefix_len_ipv4             | Configure the prefix length for this test for IPV4 address (default 24) |";
                LOG(INFO) << "| -f/--next_hop_interface_ipv4     | Configure the next hop interface for IPV4 (default Bundle-Ether1) |";
                LOG(INFO) << "| -g/--next_hop_ip_ipv4            | Configure the next hop ip address for IPV4 (default 14.1.1.10) | \n";
                LOG(INFO) << "Programming IPv6 Routes (table_type is set to ipv6)";
                LOG(INFO) << "| -i/--first_prefix_ipv6           | Configure the starting address for this test for IPV6 (default 2002:aa::0) |";
                LOG(INFO) << "| -j/--prefix_len_ipv6             | Configure the prefix length for this test for IPV6 address (default 64) |";
                LOG(INFO) << "| -k/--next_hop_interface_ipv6     | Configure the next hop interface for IPV6 (default Bundle-Ether1) |";
                LOG(INFO) << "| -l/--next_hop_ip_ipv6            | Configure the next hop ip address for IPV6 (default 2002:ae::3) | \n";
                LOG(INFO) << "Programming MPLS Labels (table_type is set to mpls)";
                LOG(INFO) << "| -m/--first_mpls_path_nhip        | Configure the starting address for this test for MPLS (default 11.0.0.1) |";
                LOG(INFO) << "| -n/--next_hop_interface_mpls     | Configure the next hop interface for MPLS (default FourHundredGigE0/0/0/0) |";
                LOG(INFO) << "| -o/--local_label                 | Configure the starting local label for this test for MPLS (default 12000) |";
                LOG(INFO) << "| -K/--out_label                   | Configure the starting out label for this test for MPLS (default 20000) |";
                LOG(INFO) << "| -q/--num_paths                   | Configure the number of paths for MPLS labels (default 1) |";
                LOG(INFO) << "Programming PG (table_type is set to pg)";
                LOG(INFO) << "| -r/--create_path_group_for       | Configure the table_type for which path group is being made (default ipv4) |";
                LOG(INFO) << "Optional arguments you can set for Get Request Only:";
                LOG(INFO) << "| -D/--vrf_name                    | User can provide a vrfname for object search (default 'default') |";
                LOG(INFO) << "| -E/--client_id                   | If set, user will provide a client id (int) for the object user wishes to search for, or input 'all' to return all routes programmed by this client (default 'all') |";
                LOG(INFO) << "| -F/--match_table_list            | Provide one or more table types you wish to get in comma separated list with no spaces. The choices are : ipv4,ipv6,mpls,pg (default ipv4). |";
                LOG(INFO) << "| -G/--match_route_list            | If set, will override --match_table_list. This command will be used in conjunction with the commands --add_vxlanvn_id, --add_pg_regex, and --add_object_type. (No argument required) \n"
                            << "The commands below can be repeatedly added and in combination with each other to the SLAFGetMsg. See their criteria on how to use them |";
                LOG(INFO) << "| -H/--add_vxlanvn_id              | Configure one vxlanvnid the user wishes to search for. Will be added as a field within the route match list message. (default "") ";
                LOG(INFO) << "| -I/--add_pg_regex                | Configure one Path Group Name Regex expression the user wishes to search for. Will be added as a field within the route match list message. (default "") ";
                LOG(INFO) << "| -J/--add_object_type             | Configure the object type the user wishes to search for. User will need to provide a comma seperated list of arguments and in proper format, for every instance of this command. See below (default "") \n"
                            << "    The user needs to provide the following for the specific object key type: \n"
                            << "    For ipv4 the user provides the table_type, starting ipv4 address, prefix length, and a number indicating how many addresses to search for incrementing from the starting ip address. For example: ipv4,40.0.0.0,24,100 \n"
                            << "    For ipv6 the user provides the table_type, starting ipv6 address, prefix length, and a number indicating how many addresses to search for incrementing from the starting ip address. For example: ipv6,2002:aa::0,64,100 \n"
                            << "    For mpls the user provides the table_type, starting label, and a number indicating how many labels to search for incrementing from the starting label. For example: mpls,20000,100 \n"
                            << "    For pg the user provides the table_type, and path group name. For example: pg,default |";
                LOG(INFO) << "Optional arguments you can set for Notification Stream Only:";
                LOG(INFO) << "| -L/--notif_stream_duration       | Enter number of seconds notification stream should stay up for. (Default 10) |";
                LOG(INFO) << "| -M/--notif_oper                  | Operation to enable or disable notifications. Choices are enable or disable. (Needs to be set for Notification stream) |";
                LOG(INFO) << "| -N/--notif_vrfname               | Vrf that the client is interested in (default 'default') |";
                LOG(INFO) << "| -O/--notif_route                 | Route redistribution registration. Format for this input is a comma seperated list of these three strings : (SrcProto, SrcProtoTag, SLTableType) \n"
                            << "                                    For the SrcProto, the user enters the string. \n"
                            << "                                    For the SrcProtoTag, the user enters the string. \n"
                            << "                                    For the Table type, the valid options are ipv4,ipv6,mpls,pg. |";
                LOG(INFO) << "| -P/--notif_nh                    | Next hop notification registration. Format for this input in a comma seperated list of (SLTableType,ipv4/v6 address,Prefix length, Exact match, Allow default, Recurse) \n"
                            << "                                    For the SLTableType, the valid options are only ipv4 or ipv6 \n"
                            << "                                    For the address, put in a v4 address or v6 address associated with table type \n"
                            << "                                    Prefix length refers to the ip address' prefix length \n"
                            << "                                    Configure the Exact Match. Choices are true or false. If set to false, it will do best match \n"
                            << "                                    Configure to Allow default route to be returned. Choices are true or false \n"
                            << "                                    Configure the recurse flag to return a flattened path list of nexthop's (true) or the immediately viable path list (false). Choices are true or false \n";
                return 1;
            case 'u':
                username = optarg;
                break;
            case 'p':
                password = optarg;
                break;
            case 'v':
                dummy = optarg;
                if (dummy == "false") {
                    version2 = false;
                }
                break;
            case 'A':
                dummy = optarg;
                if (dummy == "RIB_AND_FIB_ACK") {
                    env_data.response_acks.response_ack_type_rib_fib_set = true;
                    env_data.response_acks.response_ack_type = service_layer::RIB_AND_FIB_ACK;
                } else if (dummy == "RIB_FIB_INUSE_ACK") {
                    env_data.response_acks.response_ack_type_rib_fib_set = true;
                    env_data.response_acks.response_ack_type = service_layer::RIB_FIB_INUSE_ACK;
                } else {
                    env_data.response_acks.response_ack_type = service_layer::RIB_ACK;
                }
                break;
            case 'B':
                dummy = optarg;
                if (dummy == "SL_PERMIT_FIB_STATUS_ALL") {
                    env_data.response_acks.response_ack_permit_set = true;
                    env_data.response_acks.response_ack_permit = service_layer::SL_PERMIT_FIB_STATUS_ALL;
                } else if (dummy == "SL_PERMIT_FIB_SUCCESS") {
                    env_data.response_acks.response_ack_permit_set = true;
                    env_data.response_acks.response_ack_permit = service_layer::SL_PERMIT_FIB_SUCCESS;
                } else if (dummy == "SL_PERMIT_FIB_FAILED") {
                    env_data.response_acks.response_ack_permit_set = true;
                    env_data.response_acks.response_ack_permit = service_layer::SL_PERMIT_FIB_FAILED;
                } else if (dummy == "SL_PERMIT_FIB_INELIGIBLE") {
                    env_data.response_acks.response_ack_permit_set = true;
                    env_data.response_acks.response_ack_permit = service_layer::SL_PERMIT_FIB_INELIGIBLE;
                } else if (dummy == "SL_PERMIT_FIB_INUSE_SUCCESS") {
                    env_data.response_acks.response_ack_permit_set = true;
                    env_data.response_acks.response_ack_permit = service_layer::SL_PERMIT_FIB_INUSE_SUCCESS;
                }
                break;
            case 'C':
                dummy = optarg;
                if (dummy == "SL_RSP_JUST_ONCE") {
                    env_data.response_acks.response_ack_cadence = service_layer::SL_RSP_JUST_ONCE;
                } else if (dummy == "SL_RSP_ONCE_EACH") {
                    env_data.response_acks.response_ack_cadence = service_layer::SL_RSP_ONCE_EACH;
                } else if (dummy == "SL_RSP_NONE") {
                    env_data.response_acks.response_ack_cadence = service_layer::SL_RSP_NONE;
                } else {
                    env_data.response_acks.response_ack_cadence = service_layer::SL_RSP_CONTINUOUS;
                }
                break;
            case 'D':
                env_data.get_vrf_name = optarg;
                break;
            case 'E':
                dummy = optarg;
                if (dummy == "all" || dummy == "") {
                    env_data.get_client_all = true;
                } else {
                    env_data.get_client_id_list.push_back(stringToInt(dummy));
                }
                break;
            case 'F':
                dummy = optarg;
                env_data.get_match = true;
                for (auto i: splitString(dummy)) {
                    if (i == "ipv6") {
                        env_data.get_table_type_list.push_back(service_layer::SL_IPv6_ROUTE_TABLE);
                    } else if (i == "mpls") {
                        env_data.get_table_type_list.push_back(service_layer::SL_MPLS_LABEL_TABLE);
                    } else if (i == "pg"){
                        env_data.get_table_type_list.push_back(service_layer::SL_PATH_GROUP_TABLE);
                    } else if (i == "ipv4") {
                        env_data.get_table_type_list.push_back(service_layer::SL_IPv4_ROUTE_TABLE);
                    } else {
                        LOG(INFO) << "Entered an invalid entry for match_table_list. Will add the default of ipv4";
                        env_data.get_table_type_list.push_back(service_layer::SL_IPv4_ROUTE_TABLE);
                    }
                }
                break;
            case 'G':
                env_data.get_match = true;
                break;
            case 'H':
                dummy = optarg;
                env_data.get_route_match_list.vxlan_vn_id.push_back(stringToInt(dummy));
                env_data.get_match_route = true;
                break;
            case 'I':
                dummy = optarg;
                env_data.get_route_match_list.pg_regex.push_back(dummy);
                env_data.get_match_route = true;
                break;
            case 'J':
                dummy = optarg;
                // Do while loop used for creating object within longopts
                do {
                    slafObjKey key = {};
                    auto j = splitString(dummy);
                    if (j.size() == 0) {
                        fprintf (stderr, "Requires: %s user to enter in exact format. -h for more information \n", argv[0]);
                        return 1;
                    }
                    if (j[0] == "ipv4") {
                        if (j.size() != 4) {
                            fprintf (stderr, "Requires: %s user to enter in exact format. -h for more information \n", argv[0]);
                            return 1;
                        }
                        key.addr_family = service_layer::SL_IPv4_ROUTE_TABLE;
                        key.start_ipv4 = j[1];
                        key.prefix_len_ipv4 = stringToInt(j[2]);
                        key.num_operations = stringToInt(j[3]);
                    } else if (j[0] == "ipv6") {
                        if (j.size() != 4) {
                            fprintf (stderr, "Requires: %s user to enter in exact format. -h for more information \n", argv[0]);
                            return 1;
                        }
                        key.addr_family = service_layer::SL_IPv6_ROUTE_TABLE;
                        key.start_ipv6 = j[1];
                        key.prefix_len_ipv6 = stringToInt(j[2]);
                        key.num_operations = stringToInt(j[3]);
                    } else if (j[0] == "mpls") {
                        if (j.size() != 3) {
                            fprintf (stderr, "Requires: %s user to enter in exact format. -h for more information \n", argv[0]);
                            return 1;
                        }
                        key.addr_family = service_layer::SL_MPLS_LABEL_TABLE;
                        key.start_mpls = stringToInt(j[1]);
                        key.num_operations = stringToInt(j[2]);
                    } else if (j[0] == "pg") {
                        if (j.size() != 2) {
                            fprintf (stderr, "Requires: %s user to enter in exact format. -h for more information \n", argv[0]);
                            return 1;
                        }
                        key.addr_family = service_layer::SL_PATH_GROUP_TABLE;
                        key.pg_name = j[1];
                    } else {
                        fprintf (stderr, "Requires: %s user to pick a selectable table type for --add_object_type \n", argv[0]);
                        return 1;
                    }
                    env_data.get_route_match_list.slaf_obj_key.push_back(key);

                } while (false);
                env_data.get_match_route = true;
                break;
            case 'L':
                dummy = optarg;
                env_data.notification_stream_duration = stringToInt(dummy);
                break;
            case 'M':
                dummy = optarg;
                if (dummy == "enable") {
                    env_data.notif_oper = service_layer::SL_NOTIFOP_ENABLE;
                } else if (dummy == "disable") {
                    env_data.notif_oper = service_layer::SL_NOTIFOP_DISABLE;
                } else {
                    fprintf (stderr, "--notif_oper Requires: %s user to pick enable or disable \n", argv[0]);
                    return 1;
                }
                break;
            case 'N':
                dummy = optarg;
                env_data.notif_vrfname = dummy;
                break;
            case 'O':
                dummy = optarg;
                // Do while loop used for creating object within longopts
                do {
                    auto notif_route_vector = splitString(dummy);
                    if (notif_route_vector.size() != 3) {
                        fprintf (stderr, "Requires: %s user to enter in exact format. -h for more information \n", argv[0]);
                        return 1;
                    }
                    notifRouteObj notif_route_obj = {};
                    notif_route_obj.src_proto = notif_route_vector[0];
                    notif_route_obj.src_proto_tag = notif_route_vector[1];
                    if (notif_route_vector[2] == "ipv4") {
                        notif_route_obj.addr_family = service_layer::SL_IPv4_ROUTE_TABLE;
                    } else if (notif_route_vector[2] == "ipv6") {
                        notif_route_obj.addr_family = service_layer::SL_IPv6_ROUTE_TABLE;
                    } else if (notif_route_vector[2] == "mpls") {
                        notif_route_obj.addr_family = service_layer::SL_MPLS_LABEL_TABLE;
                    } else if (notif_route_vector[2] == "pg") {
                        notif_route_obj.addr_family = service_layer::SL_PATH_GROUP_TABLE;
                    } else {
                        fprintf (stderr, "Requires: %s user to pick selectable table type for --notif_route \n", argv[0]);
                        return 1;
                    }
                    env_data.notif_route.push_back(notif_route_obj);
                } while(false);
                break;
            case 'P':
                dummy = optarg;
                // Do while loop used for creating object within longopts
                do {
                    auto notif_nexthop_vector = splitString(dummy);
                    if (notif_nexthop_vector.size() != 6) {
                        fprintf (stderr, "Requires: %s user to enter in exact format. -h for more information \n", argv[0]);
                        return 1;
                    }
                    notifNextHopObj notif_nexthop_obj = {};
                    if (notif_nexthop_vector[0] == "ipv4") {
                        notif_nexthop_obj.addr_family = service_layer::SL_IPv4_ROUTE_TABLE;
                        notif_nexthop_obj.v4_set = true;
                    } else if (notif_nexthop_vector[0] == "ipv6") {
                        notif_nexthop_obj.addr_family = service_layer::SL_IPv6_ROUTE_TABLE;
                    } else {
                        fprintf (stderr, "Requires: %s user to pick selectable table type for --notif_nh \n", argv[0]);
                        return 1;
                    }

                    if (notif_nexthop_obj.v4_set == true) {
                        notif_nexthop_obj.ipv4_address = notif_nexthop_vector[1];
                    } else {
                        notif_nexthop_obj.ipv6_address = notif_nexthop_vector[1];
                    }
                    notif_nexthop_obj.prefix_len = stringToInt(notif_nexthop_vector[2]);

                    if (notif_nexthop_vector[3] == "true") {
                        notif_nexthop_obj.exact_match = true;
                    } else if (notif_nexthop_vector[3] == "false") {
                        notif_nexthop_obj.exact_match = false;
                    } else {
                        fprintf (stderr, "--notif_nh Requires: %s user to pick true or false for Exact Match \n", argv[0]);
                        return 1;
                    }
                    if (notif_nexthop_vector[4] == "true") {
                        notif_nexthop_obj.allow_default = true;
                    } else if (notif_nexthop_vector[4] == "false") {
                        notif_nexthop_obj.allow_default = false;
                    } else {
                        fprintf (stderr, "--notif_nh Requires: %s user to pick true or false for Allow Deafult \n", argv[0]);
                        return 1;
                    }
                    if (notif_nexthop_vector[5] == "true") {
                        notif_nexthop_obj.recurse = true;
                    } else if (notif_nexthop_vector[5] == "false") {
                        notif_nexthop_obj.recurse = false;
                    } else {
                        fprintf (stderr, "--notif_nh Requires: %s user to pick true or false for Recurse Flag \n", argv[0]);
                        return 1;
                    }

                    env_data.notif_next_hop.push_back(notif_nexthop_obj);
                } while(false);
                break;
            default:
                fprintf (stderr, "usage: %s --help for more information \n", argv[0]);
                return 1;
        }
    }

    if (username == "" || password == ""){
        LOG(INFO) << "Did not provide a Username and Password";
    }

    if (env_data.route_oper == service_layer::SL_OBJOP_RESERVED &&
        env_data.vrf_reg_oper != service_layer::SL_REGOP_UNREGISTER &&
        env_data.get_request == false && env_data.get_vrf_request == false &&
        env_data.notif_request == false) {
        LOG(ERROR) << "Need to provide the route_oper. Or set vrf_reg_oper to Unregister";
        return 0;
    }

    std::string grpc_server = server_ip + ":" + server_port;
    LOG(INFO) << "Connecting IOS-XR to gRPC server at " << grpc_server;
    auto channel = grpc::CreateChannel(grpc_server, grpc::InsecureChannelCredentials());

    AsyncNotifChannel asynchandler(channel);
    std::thread asyncchandler_thread;
    if (global_init_rpc) {

        // Acquire the lock
        std::unique_lock<std::mutex> initlock(init_mutex);

        // Spawn reader thread that maintains our Notification Channel
        asyncchandler_thread = std::thread(&AsyncNotifChannel::AsyncCompleteRpc, &asynchandler);


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

    if (env_data.notif_request == true) {
        try_notif_slaf(channel, grpc_server, env_data);
    } else {
        if (env_data.get_request == true || env_data.get_vrf_request == true) {
            try_get_slaf(channel, grpc_server, env_data);
            if (global_init_rpc) {
                asynchandler.Shutdown();
                asyncchandler_thread.join();
            }
        } else {
            if (version2 == true) {
                try_route_push_slaf(channel, grpc_server, env_data);
                if (global_init_rpc) {
                    asynchandler.Shutdown();
                    asyncchandler_thread.join();
                }
            } else {
                try_route_push(channel, grpc_server, env_data);
                if (global_init_rpc) {
                    asynchandler.Shutdown();
                    asyncchandler_thread.join();
                }
            }
        }
    }

    return 0;
}
