#pragma once

#include <stdint.h>
#include <thread>
#include <typeinfo>
#include <condition_variable>
#include <iostream>
#include <memory>
#include <string>
#include <csignal>
#include <sys/socket.h>

#include <grpc++/grpc++.h>
#include <iosxrsl/sl_global.grpc.pb.h>
#include <iosxrsl/sl_global.pb.h>
#include <iosxrsl/sl_common_types.pb.h>
#include <iosxrsl/sl_version.pb.h>
#include <iosxrsl/sl_route_common.pb.h>
#include <iosxrsl/sl_route_ipv4.grpc.pb.h>
#include <iosxrsl/sl_route_ipv6.grpc.pb.h>
#include <iosxrsl/sl_route_ipv4.pb.h>
#include <iosxrsl/sl_route_ipv6.pb.h>

extern std::mutex init_mutex;
extern std::condition_variable init_condVar;
extern bool init_success;
extern std::shared_ptr<grpc::Channel> route_channel;

class RShuttle {
public:
    explicit RShuttle(std::shared_ptr<grpc::Channel> Channel);

    std::shared_ptr<grpc::Channel> channel;
    service_layer::SLObjectOp route_op;
    service_layer::SLRoutev4Msg routev4_msg;
    service_layer::SLRoutev4MsgRsp routev4_msg_resp;
    service_layer::SLRoutev6Msg routev6_msg;
    service_layer::SLRoutev6MsgRsp routev6_msg_resp;

    // IPv4 and IPv6 string manipulation methods

    uint32_t IPv4ToLong(const char* address);

    std::string IPv6ToByteArrayString(const char* address);

    // IPv4 methods

    service_layer::SLRoutev4*
    routev4Add(std::string vrfName);

    void routev4Set(service_layer::SLRoutev4* routev4Ptr,
                    uint32_t prefix,
                    uint32_t prefixLen,
                    uint32_t adminDistance); 


    void routev4PathAdd(service_layer::SLRoutev4* routev4Ptr,
                        uint32_t nextHopAddress,
                        std::string nextHopIf);
 

    void routev4Op(service_layer::SLObjectOp routeOp,
                   unsigned int timeout=10);



    // IPv6 methods
    service_layer::SLRoutev6*
    routev6Add(std::string vrfName);
 

    void routev6Set(service_layer::SLRoutev6* routev6Ptr,
                    std::string prefix,
                    uint32_t prefixLen,
                    uint32_t adminDistance);

    void routev6PathAdd(service_layer::SLRoutev6* routev6Ptr,
                        std::string nextHopAddress,
                        std::string nextHopIf);
 

    void routev6Op(service_layer::SLObjectOp routeOp,
                   unsigned int timeout=10);

};


class SLVrf {
public:
    explicit SLVrf(std::shared_ptr<grpc::Channel> Channel);

    std::shared_ptr<grpc::Channel> channel;
    service_layer::SLRegOp vrf_op;
    service_layer::SLVrfRegMsg vrf_msg;
    service_layer::SLVrfRegMsgRsp vrf_msg_resp;

    void vrfRegMsgAdd(std::string vrfName);

    void vrfRegMsgAdd(std::string vrfName,
                      unsigned int adminDistance,
                      unsigned int vrfPurgeIntervalSeconds);

    void registerVrf(unsigned int addrFamily);

    void unregisterVrf(unsigned int addrFamily);

    void vrfOpv4();

    void vrfOpv6();

};


class AsyncNotifChannel {
public:
    explicit AsyncNotifChannel(std::shared_ptr<grpc::Channel> channel);

    void SendInitMsg(const service_layer::SLInitMsg init_msg);

    void AsyncCompleteRpc();

    void Shutdown();
    void Cleanup();

    std::mutex channel_mutex;
    std::condition_variable channel_condVar;
    bool channel_closed = false;

private:
    // Out of the passed in Channel comes the stub, stored here, our view of the
    // server's exposed services.
    std::unique_ptr<service_layer::SLGlobal::Stub> stub_;

    // The producer-consumer queue we use to communicate asynchronously with the
    // gRPC runtime.
    grpc::CompletionQueue cq_;


    // Used as an indicator to exit completion queue thread upon queue shutdown.
    bool tear_down = false;

    class AsyncClientCall {
    private:
        enum CallStatus {CREATE, PROCESS, FINISH};
        CallStatus callStatus_;
    public:
        AsyncClientCall();
        // Container for the data we expect from the server.
        service_layer::SLGlobalNotif notif;
        // Context for the client. It could be used to convey extra information to
        // the server and/or tweak certain RPC behaviors.
        grpc::ClientContext context;

        // Storage for the status of the RPC upon completion.
        grpc::Status status;

        std::unique_ptr< ::grpc::ClientAsyncReaderInterface< ::service_layer::SLGlobalNotif>> response_reader;

        void HandleResponse(bool responseStatus, grpc::CompletionQueue* pcq_);      
    }call;

};
