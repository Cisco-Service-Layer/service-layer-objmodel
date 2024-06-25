#pragma once

#include <memory>
#include <string>
#include <iostream> 
#include <thread>
#include <mutex>
#include <sstream>  
#include <utility>
#include <unordered_map>
#include <deque>
#include <chrono>
#include <mutex>
#include "ServiceLayerAsyncInit.h"
#include <iosxrsl/sl_route_common.pb.h>
#include <iosxrsl/sl_route_ipv4.grpc.pb.h>
#include <iosxrsl/sl_route_ipv6.grpc.pb.h>
#include <iosxrsl/sl_route_ipv4.pb.h>
#include <iosxrsl/sl_route_ipv6.pb.h>
#include <iosxrsl/sl_af.grpc.pb.h>
#include <iosxrsl/sl_af.pb.h>
#include <nlohmann/json.hpp>

// Data used throughout code. Will change dependent on cli options listed by user
class testingData
{
public:
    // table_type is used to determine if we are doing ipv4(value = 0x1) ipv6(value = 0x2), or mpls(value = 0x3)
    service_layer::SLTableType table_type = service_layer::SL_IPv4_ROUTE_TABLE;

    service_layer::SLObjectOp route_oper = service_layer::SL_OBJOP_RESERVED;
    service_layer::SLRegOp vrf_reg_oper = service_layer::SL_REGOP_RESERVED;

    unsigned int num_operations = 1;
    bool stream_case = true;
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
    std::string first_mpls_path_nhip = "11.0.0.1";
    std::string next_hop_interface_mpls = "FourHundredGigE0/0/0/0";
    unsigned int start_label = 20000;
    unsigned int num_label = 1000;
    unsigned int num_paths = 1;
};

// Status Object is for handling the response messages
class statusObject
{
public:
    // RIB SUCCESS
    bool rib_success = false;
    // FIB SUCCESS
    bool fib_success = false;

    // Requesting FIB
    bool fib_req = false;
    // error message
    std::string error = "";
};

class dbStructure {
public:

    // Stores elements as key value pairs in non-sorted order. Mapping of key(prefix) and value (pair of testingData and statusObject objects)
    // Provides O(1) lookup

    // Key for ipv4 will be the prefix
    std::unordered_map<uint32_t, std::pair<testingData, statusObject>> db_ipv4;
    // Key for ipv6 is the prefix
    std::unordered_map<std::string, std::pair<testingData, statusObject>> db_ipv6;
    // Key for mpls is the label number
    std::unordered_map<unsigned int, std::pair<testingData, statusObject>> db_mpls;

    int db_count;

    // Start and last index allows us to keep track of where we are when converting db objects into slapi objects
    uint32_t ipv4_start_index;
    uint32_t ipv4_last_index;
    std::string ipv6_start_index;
    std::string ipv6_last_index;
    unsigned int mpls_start_index;
    unsigned int mpls_last_index;
};

class SLAFQueueMsg {
public:

    service_layer::SLAFMsg route_msg;
    bool terminate_slaf_stream = false;
};

extern dbStructure database;
// Mutex used for synchronize access for database
extern std::mutex db_mutex;

// Mutex used for synchronize the request_deque and condition variable
extern std::mutex deque_mutex;
extern std::condition_variable deque_cv;

// Stream case: Queue used between main thread for pushing slapi objects and write thread for popping objects
extern std::deque<SLAFQueueMsg> request_deque;

class SLAFRShuttle;
extern SLAFRShuttle* slaf_route_shuttle;
class SLAFRShuttle {
public:
    explicit SLAFRShuttle(std::shared_ptr<grpc::Channel> Channel, std::string Username,
                      std::string Password);

    enum PathUpdateAction
    {
        RSHUTTLE_PATH_ADD,
        RSHUTTLE_PATH_DELETE,
    };

    std::shared_ptr<grpc::Channel> channel;

    std::string username;
    std::string password;

    service_layer::SLObjectOp route_op;
    service_layer::SLAFMsg route_msg;
    service_layer::SLAFMsgRsp route_msg_resp;

    std::map<std::string, int> prefix_map_v4;
    std::map<std::string, int> prefix_map_v6;

    unsigned int pushFromDB(bool streamCase,
                    service_layer::SLObjectOp routeOper,
                    service_layer::SLTableType addrFamily);

    bool routeSLAFOp(service_layer::SLObjectOp routeOp,
                    service_layer::SLTableType addrFamily,
                    unsigned int timeout=30);

    static void readStream(std::shared_ptr<grpc::ClientReaderWriter<service_layer::SLAFMsg, service_layer::SLAFMsgRsp>>& stream,
                          service_layer::SLTableType addrFamily,
                          service_layer::SLObjectOp routeOper,
                          std::string addressFamilyStr);
    static void writeStream(std::shared_ptr<grpc::ClientReaderWriter<service_layer::SLAFMsg, service_layer::SLAFMsgRsp>>& stream, std::string addressFamilyStr);
    void stopStream(std::thread* reader, std::thread* writer);
    void routeSLAFOpStreamHelperEnqueue(bool terminate_slaf_stream);
    unsigned int routeSLAFOpStream(service_layer::SLTableType addrFamily, service_layer::SLObjectOp routeOper, unsigned int timeout=30);
    void clearDB();
    void clearBatch();

    // IPv4 and IPv6 string manipulation methods

    std::string longToIpv4(uint32_t nlprefix);
    uint32_t ipv4ToLong(const char* address);
    std::string ipv6ToByteArrayString(const char* address);
    std::string ByteArrayStringtoIpv6(std::string ipv6ByteArray);
    std::string incrementIpv6Pfx(std::string ipv6ByteArray, uint32_t prefixLen);

    // IPv4 methods

    void setVrfV4(std::string vrfName);


    service_layer::SLRoutev4*
    routev4Add();

    service_layer::SLRoutev4*
    routev4Add(std::string vrfName);


    void routev4Set(service_layer::SLRoutev4* routev4Ptr,
                    uint32_t prefix,
                    uint8_t prefixLen);

    void routev4Set(service_layer::SLRoutev4* routev4Ptr,
                    uint32_t prefix,
                    uint8_t prefixLen,
                    uint32_t adminDistance); 


    void routev4PathAdd(service_layer::SLRoutev4* routev4Ptr,
                        uint32_t nextHopAddress,
                        std::string nextHopIf);

    bool insertAddBatchV4(std::string prefix,
                          uint8_t prefixLen,
                          uint32_t adminDistance,
                          std::string nextHopAddress,
                          std::string nextHopIf,
                          service_layer::SLObjectOp routeOper);

    // IPv6 methods

    void setVrfV6(std::string vrfName);


    service_layer::SLRoutev6*
    routev6Add();

    service_layer::SLRoutev6*
    routev6Add(std::string vrfName);
 

    void routev6Set(service_layer::SLRoutev6* routev6Ptr,
                    std::string prefix,
                    uint8_t prefixLen);


    void routev6Set(service_layer::SLRoutev6* routev6Ptr,
                    std::string prefix,
                    uint8_t prefixLen,
                    uint32_t adminDistance);

    void routev6PathAdd(service_layer::SLRoutev6* routev6Ptr,
                        std::string nextHopAddress,
                        std::string nextHopIf);

    bool insertAddBatchV6(std::string prefix,
                          uint8_t prefixLen,
                          uint32_t adminDistance,
                          std::string nextHopAddress,
                          std::string nextHopIf,
                          service_layer::SLObjectOp routeOper);

    // MPLS methods

    void insertAddBatchMPLS(unsigned int label,
                                unsigned int startLabel,
                                unsigned int numPaths,
                                uint32_t nextHopAddress,
                                std::string nextHopInterface);

};

class SLAFVrf {
public:
    explicit SLAFVrf(std::shared_ptr<grpc::Channel> Channel, std::string Username, std::string Password);

    std::shared_ptr<grpc::Channel> channel;

    std::string username;
    std::string password;

    service_layer::SLAFVrfRegMsg af_vrf_msg;
    service_layer::SLAFVrfRegMsgRsp af_vrf_msg_resp;

    void afVrfRegMsgAdd(std::string vrfName,
                        service_layer::SLTableType addrFamily);

    void afVrfRegMsgAdd(std::string vrfName,
                      unsigned int adminDistance,
                      unsigned int vrfPurgeIntervalSeconds,
                      service_layer::SLTableType addrFamily);

    bool registerAfVrf(service_layer::SLTableType addrFamily, service_layer::SLRegOp vrfRegOper);

    bool afVrfOpAddFam(service_layer::SLRegOp, service_layer::SLTableType addrFamily);

};

class SLGLOBALSHUTTLE {
public:
    explicit SLGLOBALSHUTTLE(std::shared_ptr<grpc::Channel> Channel, std::string Username, std::string Password);

    std::shared_ptr<grpc::Channel> channel;
    std::string username;
    std::string password;

    //Sends a GlobalsGet Request and updates parameter the value for max batch size
    bool getGlobals(unsigned int &batch_size, unsigned int timeout=30);

};

