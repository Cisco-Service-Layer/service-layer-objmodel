// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: sl_policy.proto

#include "sl_policy.pb.h"
#include "sl_policy.grpc.pb.h"

#include <functional>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/channel_interface.h>
#include <grpcpp/impl/codegen/client_unary_call.h>
#include <grpcpp/impl/codegen/client_callback.h>
#include <grpcpp/impl/codegen/message_allocator.h>
#include <grpcpp/impl/codegen/method_handler.h>
#include <grpcpp/impl/codegen/rpc_service_method.h>
#include <grpcpp/impl/codegen/server_callback.h>
#include <grpcpp/impl/codegen/server_callback_handlers.h>
#include <grpcpp/impl/codegen/server_context.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/sync_stream.h>
namespace service_layer {

static const char* SLPolicy_method_names[] = {
  "/service_layer.SLPolicy/SLPolicyOp",
  "/service_layer.SLPolicy/SLPolicyGet",
  "/service_layer.SLPolicy/SLPolicyGlobalGet",
};

std::unique_ptr< SLPolicy::Stub> SLPolicy::NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options) {
  (void)options;
  std::unique_ptr< SLPolicy::Stub> stub(new SLPolicy::Stub(channel, options));
  return stub;
}

SLPolicy::Stub::Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options)
  : channel_(channel), rpcmethod_SLPolicyOp_(SLPolicy_method_names[0], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_SLPolicyGet_(SLPolicy_method_names[1], options.suffix_for_stats(),::grpc::internal::RpcMethod::SERVER_STREAMING, channel)
  , rpcmethod_SLPolicyGlobalGet_(SLPolicy_method_names[2], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  {}

::grpc::Status SLPolicy::Stub::SLPolicyOp(::grpc::ClientContext* context, const ::service_layer::SLPolicyOpMsg& request, ::service_layer::SLPolicyOpRsp* response) {
  return ::grpc::internal::BlockingUnaryCall< ::service_layer::SLPolicyOpMsg, ::service_layer::SLPolicyOpRsp, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_SLPolicyOp_, context, request, response);
}

void SLPolicy::Stub::async::SLPolicyOp(::grpc::ClientContext* context, const ::service_layer::SLPolicyOpMsg* request, ::service_layer::SLPolicyOpRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::service_layer::SLPolicyOpMsg, ::service_layer::SLPolicyOpRsp, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_SLPolicyOp_, context, request, response, std::move(f));
}

void SLPolicy::Stub::async::SLPolicyOp(::grpc::ClientContext* context, const ::service_layer::SLPolicyOpMsg* request, ::service_layer::SLPolicyOpRsp* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_SLPolicyOp_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLPolicyOpRsp>* SLPolicy::Stub::PrepareAsyncSLPolicyOpRaw(::grpc::ClientContext* context, const ::service_layer::SLPolicyOpMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::service_layer::SLPolicyOpRsp, ::service_layer::SLPolicyOpMsg, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_SLPolicyOp_, context, request);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLPolicyOpRsp>* SLPolicy::Stub::AsyncSLPolicyOpRaw(::grpc::ClientContext* context, const ::service_layer::SLPolicyOpMsg& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncSLPolicyOpRaw(context, request, cq);
  result->StartCall();
  return result;
}

::grpc::ClientReader< ::service_layer::SLPolicyGetMsgRsp>* SLPolicy::Stub::SLPolicyGetRaw(::grpc::ClientContext* context, const ::service_layer::SLPolicyGetMsg& request) {
  return ::grpc::internal::ClientReaderFactory< ::service_layer::SLPolicyGetMsgRsp>::Create(channel_.get(), rpcmethod_SLPolicyGet_, context, request);
}

void SLPolicy::Stub::async::SLPolicyGet(::grpc::ClientContext* context, const ::service_layer::SLPolicyGetMsg* request, ::grpc::ClientReadReactor< ::service_layer::SLPolicyGetMsgRsp>* reactor) {
  ::grpc::internal::ClientCallbackReaderFactory< ::service_layer::SLPolicyGetMsgRsp>::Create(stub_->channel_.get(), stub_->rpcmethod_SLPolicyGet_, context, request, reactor);
}

::grpc::ClientAsyncReader< ::service_layer::SLPolicyGetMsgRsp>* SLPolicy::Stub::AsyncSLPolicyGetRaw(::grpc::ClientContext* context, const ::service_layer::SLPolicyGetMsg& request, ::grpc::CompletionQueue* cq, void* tag) {
  return ::grpc::internal::ClientAsyncReaderFactory< ::service_layer::SLPolicyGetMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLPolicyGet_, context, request, true, tag);
}

::grpc::ClientAsyncReader< ::service_layer::SLPolicyGetMsgRsp>* SLPolicy::Stub::PrepareAsyncSLPolicyGetRaw(::grpc::ClientContext* context, const ::service_layer::SLPolicyGetMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncReaderFactory< ::service_layer::SLPolicyGetMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLPolicyGet_, context, request, false, nullptr);
}

::grpc::Status SLPolicy::Stub::SLPolicyGlobalGet(::grpc::ClientContext* context, const ::service_layer::SLPolicyGlobalGetMsg& request, ::service_layer::SLPolicyGlobalGetMsgRsp* response) {
  return ::grpc::internal::BlockingUnaryCall< ::service_layer::SLPolicyGlobalGetMsg, ::service_layer::SLPolicyGlobalGetMsgRsp, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_SLPolicyGlobalGet_, context, request, response);
}

void SLPolicy::Stub::async::SLPolicyGlobalGet(::grpc::ClientContext* context, const ::service_layer::SLPolicyGlobalGetMsg* request, ::service_layer::SLPolicyGlobalGetMsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::service_layer::SLPolicyGlobalGetMsg, ::service_layer::SLPolicyGlobalGetMsgRsp, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_SLPolicyGlobalGet_, context, request, response, std::move(f));
}

void SLPolicy::Stub::async::SLPolicyGlobalGet(::grpc::ClientContext* context, const ::service_layer::SLPolicyGlobalGetMsg* request, ::service_layer::SLPolicyGlobalGetMsgRsp* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_SLPolicyGlobalGet_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLPolicyGlobalGetMsgRsp>* SLPolicy::Stub::PrepareAsyncSLPolicyGlobalGetRaw(::grpc::ClientContext* context, const ::service_layer::SLPolicyGlobalGetMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::service_layer::SLPolicyGlobalGetMsgRsp, ::service_layer::SLPolicyGlobalGetMsg, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_SLPolicyGlobalGet_, context, request);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLPolicyGlobalGetMsgRsp>* SLPolicy::Stub::AsyncSLPolicyGlobalGetRaw(::grpc::ClientContext* context, const ::service_layer::SLPolicyGlobalGetMsg& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncSLPolicyGlobalGetRaw(context, request, cq);
  result->StartCall();
  return result;
}

SLPolicy::Service::Service() {
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      SLPolicy_method_names[0],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< SLPolicy::Service, ::service_layer::SLPolicyOpMsg, ::service_layer::SLPolicyOpRsp, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](SLPolicy::Service* service,
             ::grpc::ServerContext* ctx,
             const ::service_layer::SLPolicyOpMsg* req,
             ::service_layer::SLPolicyOpRsp* resp) {
               return service->SLPolicyOp(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      SLPolicy_method_names[1],
      ::grpc::internal::RpcMethod::SERVER_STREAMING,
      new ::grpc::internal::ServerStreamingHandler< SLPolicy::Service, ::service_layer::SLPolicyGetMsg, ::service_layer::SLPolicyGetMsgRsp>(
          [](SLPolicy::Service* service,
             ::grpc::ServerContext* ctx,
             const ::service_layer::SLPolicyGetMsg* req,
             ::grpc::ServerWriter<::service_layer::SLPolicyGetMsgRsp>* writer) {
               return service->SLPolicyGet(ctx, req, writer);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      SLPolicy_method_names[2],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< SLPolicy::Service, ::service_layer::SLPolicyGlobalGetMsg, ::service_layer::SLPolicyGlobalGetMsgRsp, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](SLPolicy::Service* service,
             ::grpc::ServerContext* ctx,
             const ::service_layer::SLPolicyGlobalGetMsg* req,
             ::service_layer::SLPolicyGlobalGetMsgRsp* resp) {
               return service->SLPolicyGlobalGet(ctx, req, resp);
             }, this)));
}

SLPolicy::Service::~Service() {
}

::grpc::Status SLPolicy::Service::SLPolicyOp(::grpc::ServerContext* context, const ::service_layer::SLPolicyOpMsg* request, ::service_layer::SLPolicyOpRsp* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SLPolicy::Service::SLPolicyGet(::grpc::ServerContext* context, const ::service_layer::SLPolicyGetMsg* request, ::grpc::ServerWriter< ::service_layer::SLPolicyGetMsgRsp>* writer) {
  (void) context;
  (void) request;
  (void) writer;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SLPolicy::Service::SLPolicyGlobalGet(::grpc::ServerContext* context, const ::service_layer::SLPolicyGlobalGetMsg* request, ::service_layer::SLPolicyGlobalGetMsgRsp* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


}  // namespace service_layer
