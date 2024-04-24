#pragma once

#include <string>
#include "ServiceLayerAsyncInit.h"
#include <iosxrsl/sl_route_common.pb.h>
#include <iosxrsl/sl_route_ipv4.grpc.pb.h>
#include <iosxrsl/sl_route_ipv6.grpc.pb.h>
#include <iosxrsl/sl_route_ipv4.pb.h>
#include <iosxrsl/sl_route_ipv6.pb.h>
#include <iosxrsl/sl_af.grpc.pb.h>
#include <iosxrsl/sl_af.pb.h>


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

    bool routeSLAFOp(service_layer::SLObjectOp routeOp,
                    service_layer::SLTableType addrFamily,
                    unsigned int timeout=10);
    
    void clearBatch();

    // IPv4 and IPv6 string manipulation methods

    std::string longToIpv4(uint32_t nlprefix);
    uint32_t ipv4ToLong(const char* address);
    std::string ipv6ToByteArrayString(const char* address);
    std::string ByteArrayStringtoIpv6(std::string ipv6ByteArray);

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

    unsigned int insertAddBatchMPLS(unsigned int startLabel,
                            unsigned int numLabel,
                            unsigned int numPaths,
                            unsigned int batchSize,
                            uint32_t nextHopAddress,
                            std::string nextHopInterface,
                            service_layer::SLObjectOp routeOper);

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

    bool unregisterAfVrf(service_layer::SLTableType addrFamily);

    bool afVrfOpAddFam(service_layer::SLRegOp, service_layer::SLTableType addrFamily);

};

