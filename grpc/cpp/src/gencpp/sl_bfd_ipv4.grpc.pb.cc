// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: sl_bfd_ipv4.proto

#include "sl_bfd_ipv4.pb.h"
#include "sl_bfd_ipv4.grpc.pb.h"

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

static const char* SLBfdv4Oper_method_names[] = {
  "/service_layer.SLBfdv4Oper/SLBfdv4RegOp",
  "/service_layer.SLBfdv4Oper/SLBfdv4Get",
  "/service_layer.SLBfdv4Oper/SLBfdv4GetStats",
  "/service_layer.SLBfdv4Oper/SLBfdv4GetNotifStream",
  "/service_layer.SLBfdv4Oper/SLBfdv4SessionOp",
  "/service_layer.SLBfdv4Oper/SLBfdv4SessionGet",
};

std::unique_ptr< SLBfdv4Oper::Stub> SLBfdv4Oper::NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options) {
  (void)options;
  std::unique_ptr< SLBfdv4Oper::Stub> stub(new SLBfdv4Oper::Stub(channel));
  return stub;
}

SLBfdv4Oper::Stub::Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel)
  : channel_(channel), rpcmethod_SLBfdv4RegOp_(SLBfdv4Oper_method_names[0], ::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_SLBfdv4Get_(SLBfdv4Oper_method_names[1], ::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_SLBfdv4GetStats_(SLBfdv4Oper_method_names[2], ::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_SLBfdv4GetNotifStream_(SLBfdv4Oper_method_names[3], ::grpc::internal::RpcMethod::SERVER_STREAMING, channel)
  , rpcmethod_SLBfdv4SessionOp_(SLBfdv4Oper_method_names[4], ::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_SLBfdv4SessionGet_(SLBfdv4Oper_method_names[5], ::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  {}

::grpc::Status SLBfdv4Oper::Stub::SLBfdv4RegOp(::grpc::ClientContext* context, const ::service_layer::SLBfdRegMsg& request, ::service_layer::SLBfdRegMsgRsp* response) {
  return ::grpc::internal::BlockingUnaryCall(channel_.get(), rpcmethod_SLBfdv4RegOp_, context, request, response);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4RegOp(::grpc::ClientContext* context, const ::service_layer::SLBfdRegMsg* request, ::service_layer::SLBfdRegMsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4RegOp_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4RegOp(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdRegMsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4RegOp_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4RegOp(::grpc::ClientContext* context, const ::service_layer::SLBfdRegMsg* request, ::service_layer::SLBfdRegMsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4RegOp_, context, request, response, reactor);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4RegOp(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdRegMsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4RegOp_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdRegMsgRsp>* SLBfdv4Oper::Stub::AsyncSLBfdv4RegOpRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdRegMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdRegMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4RegOp_, context, request, true);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdRegMsgRsp>* SLBfdv4Oper::Stub::PrepareAsyncSLBfdv4RegOpRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdRegMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdRegMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4RegOp_, context, request, false);
}

::grpc::Status SLBfdv4Oper::Stub::SLBfdv4Get(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg& request, ::service_layer::SLBfdGetMsgRsp* response) {
  return ::grpc::internal::BlockingUnaryCall(channel_.get(), rpcmethod_SLBfdv4Get_, context, request, response);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4Get(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg* request, ::service_layer::SLBfdGetMsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4Get_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4Get(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdGetMsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4Get_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4Get(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg* request, ::service_layer::SLBfdGetMsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4Get_, context, request, response, reactor);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4Get(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdGetMsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4Get_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdGetMsgRsp>* SLBfdv4Oper::Stub::AsyncSLBfdv4GetRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdGetMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4Get_, context, request, true);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdGetMsgRsp>* SLBfdv4Oper::Stub::PrepareAsyncSLBfdv4GetRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdGetMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4Get_, context, request, false);
}

::grpc::Status SLBfdv4Oper::Stub::SLBfdv4GetStats(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg& request, ::service_layer::SLBfdGetStatsMsgRsp* response) {
  return ::grpc::internal::BlockingUnaryCall(channel_.get(), rpcmethod_SLBfdv4GetStats_, context, request, response);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4GetStats(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg* request, ::service_layer::SLBfdGetStatsMsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4GetStats_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4GetStats(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdGetStatsMsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4GetStats_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4GetStats(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg* request, ::service_layer::SLBfdGetStatsMsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4GetStats_, context, request, response, reactor);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4GetStats(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdGetStatsMsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4GetStats_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdGetStatsMsgRsp>* SLBfdv4Oper::Stub::AsyncSLBfdv4GetStatsRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdGetStatsMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4GetStats_, context, request, true);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdGetStatsMsgRsp>* SLBfdv4Oper::Stub::PrepareAsyncSLBfdv4GetStatsRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdGetMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdGetStatsMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4GetStats_, context, request, false);
}

::grpc::ClientReader< ::service_layer::SLBfdv4Notif>* SLBfdv4Oper::Stub::SLBfdv4GetNotifStreamRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdGetNotifMsg& request) {
  return ::grpc_impl::internal::ClientReaderFactory< ::service_layer::SLBfdv4Notif>::Create(channel_.get(), rpcmethod_SLBfdv4GetNotifStream_, context, request);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4GetNotifStream(::grpc::ClientContext* context, ::service_layer::SLBfdGetNotifMsg* request, ::grpc::experimental::ClientReadReactor< ::service_layer::SLBfdv4Notif>* reactor) {
  ::grpc_impl::internal::ClientCallbackReaderFactory< ::service_layer::SLBfdv4Notif>::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4GetNotifStream_, context, request, reactor);
}

::grpc::ClientAsyncReader< ::service_layer::SLBfdv4Notif>* SLBfdv4Oper::Stub::AsyncSLBfdv4GetNotifStreamRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdGetNotifMsg& request, ::grpc::CompletionQueue* cq, void* tag) {
  return ::grpc_impl::internal::ClientAsyncReaderFactory< ::service_layer::SLBfdv4Notif>::Create(channel_.get(), cq, rpcmethod_SLBfdv4GetNotifStream_, context, request, true, tag);
}

::grpc::ClientAsyncReader< ::service_layer::SLBfdv4Notif>* SLBfdv4Oper::Stub::PrepareAsyncSLBfdv4GetNotifStreamRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdGetNotifMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncReaderFactory< ::service_layer::SLBfdv4Notif>::Create(channel_.get(), cq, rpcmethod_SLBfdv4GetNotifStream_, context, request, false, nullptr);
}

::grpc::Status SLBfdv4Oper::Stub::SLBfdv4SessionOp(::grpc::ClientContext* context, const ::service_layer::SLBfdv4Msg& request, ::service_layer::SLBfdv4MsgRsp* response) {
  return ::grpc::internal::BlockingUnaryCall(channel_.get(), rpcmethod_SLBfdv4SessionOp_, context, request, response);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4SessionOp(::grpc::ClientContext* context, const ::service_layer::SLBfdv4Msg* request, ::service_layer::SLBfdv4MsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4SessionOp_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4SessionOp(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdv4MsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4SessionOp_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4SessionOp(::grpc::ClientContext* context, const ::service_layer::SLBfdv4Msg* request, ::service_layer::SLBfdv4MsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4SessionOp_, context, request, response, reactor);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4SessionOp(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdv4MsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4SessionOp_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdv4MsgRsp>* SLBfdv4Oper::Stub::AsyncSLBfdv4SessionOpRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdv4Msg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdv4MsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4SessionOp_, context, request, true);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdv4MsgRsp>* SLBfdv4Oper::Stub::PrepareAsyncSLBfdv4SessionOpRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdv4Msg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdv4MsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4SessionOp_, context, request, false);
}

::grpc::Status SLBfdv4Oper::Stub::SLBfdv4SessionGet(::grpc::ClientContext* context, const ::service_layer::SLBfdv4GetMsg& request, ::service_layer::SLBfdv4GetMsgRsp* response) {
  return ::grpc::internal::BlockingUnaryCall(channel_.get(), rpcmethod_SLBfdv4SessionGet_, context, request, response);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4SessionGet(::grpc::ClientContext* context, const ::service_layer::SLBfdv4GetMsg* request, ::service_layer::SLBfdv4GetMsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4SessionGet_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4SessionGet(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdv4GetMsgRsp* response, std::function<void(::grpc::Status)> f) {
  ::grpc_impl::internal::CallbackUnaryCall(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4SessionGet_, context, request, response, std::move(f));
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4SessionGet(::grpc::ClientContext* context, const ::service_layer::SLBfdv4GetMsg* request, ::service_layer::SLBfdv4GetMsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4SessionGet_, context, request, response, reactor);
}

void SLBfdv4Oper::Stub::experimental_async::SLBfdv4SessionGet(::grpc::ClientContext* context, const ::grpc::ByteBuffer* request, ::service_layer::SLBfdv4GetMsgRsp* response, ::grpc::experimental::ClientUnaryReactor* reactor) {
  ::grpc_impl::internal::ClientCallbackUnaryFactory::Create(stub_->channel_.get(), stub_->rpcmethod_SLBfdv4SessionGet_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdv4GetMsgRsp>* SLBfdv4Oper::Stub::AsyncSLBfdv4SessionGetRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdv4GetMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdv4GetMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4SessionGet_, context, request, true);
}

::grpc::ClientAsyncResponseReader< ::service_layer::SLBfdv4GetMsgRsp>* SLBfdv4Oper::Stub::PrepareAsyncSLBfdv4SessionGetRaw(::grpc::ClientContext* context, const ::service_layer::SLBfdv4GetMsg& request, ::grpc::CompletionQueue* cq) {
  return ::grpc_impl::internal::ClientAsyncResponseReaderFactory< ::service_layer::SLBfdv4GetMsgRsp>::Create(channel_.get(), cq, rpcmethod_SLBfdv4SessionGet_, context, request, false);
}

SLBfdv4Oper::Service::Service() {
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      SLBfdv4Oper_method_names[0],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< SLBfdv4Oper::Service, ::service_layer::SLBfdRegMsg, ::service_layer::SLBfdRegMsgRsp>(
          [](SLBfdv4Oper::Service* service,
             ::grpc_impl::ServerContext* ctx,
             const ::service_layer::SLBfdRegMsg* req,
             ::service_layer::SLBfdRegMsgRsp* resp) {
               return service->SLBfdv4RegOp(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      SLBfdv4Oper_method_names[1],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< SLBfdv4Oper::Service, ::service_layer::SLBfdGetMsg, ::service_layer::SLBfdGetMsgRsp>(
          [](SLBfdv4Oper::Service* service,
             ::grpc_impl::ServerContext* ctx,
             const ::service_layer::SLBfdGetMsg* req,
             ::service_layer::SLBfdGetMsgRsp* resp) {
               return service->SLBfdv4Get(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      SLBfdv4Oper_method_names[2],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< SLBfdv4Oper::Service, ::service_layer::SLBfdGetMsg, ::service_layer::SLBfdGetStatsMsgRsp>(
          [](SLBfdv4Oper::Service* service,
             ::grpc_impl::ServerContext* ctx,
             const ::service_layer::SLBfdGetMsg* req,
             ::service_layer::SLBfdGetStatsMsgRsp* resp) {
               return service->SLBfdv4GetStats(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      SLBfdv4Oper_method_names[3],
      ::grpc::internal::RpcMethod::SERVER_STREAMING,
      new ::grpc::internal::ServerStreamingHandler< SLBfdv4Oper::Service, ::service_layer::SLBfdGetNotifMsg, ::service_layer::SLBfdv4Notif>(
          [](SLBfdv4Oper::Service* service,
             ::grpc_impl::ServerContext* ctx,
             const ::service_layer::SLBfdGetNotifMsg* req,
             ::grpc_impl::ServerWriter<::service_layer::SLBfdv4Notif>* writer) {
               return service->SLBfdv4GetNotifStream(ctx, req, writer);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      SLBfdv4Oper_method_names[4],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< SLBfdv4Oper::Service, ::service_layer::SLBfdv4Msg, ::service_layer::SLBfdv4MsgRsp>(
          [](SLBfdv4Oper::Service* service,
             ::grpc_impl::ServerContext* ctx,
             const ::service_layer::SLBfdv4Msg* req,
             ::service_layer::SLBfdv4MsgRsp* resp) {
               return service->SLBfdv4SessionOp(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      SLBfdv4Oper_method_names[5],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< SLBfdv4Oper::Service, ::service_layer::SLBfdv4GetMsg, ::service_layer::SLBfdv4GetMsgRsp>(
          [](SLBfdv4Oper::Service* service,
             ::grpc_impl::ServerContext* ctx,
             const ::service_layer::SLBfdv4GetMsg* req,
             ::service_layer::SLBfdv4GetMsgRsp* resp) {
               return service->SLBfdv4SessionGet(ctx, req, resp);
             }, this)));
}

SLBfdv4Oper::Service::~Service() {
}

::grpc::Status SLBfdv4Oper::Service::SLBfdv4RegOp(::grpc::ServerContext* context, const ::service_layer::SLBfdRegMsg* request, ::service_layer::SLBfdRegMsgRsp* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SLBfdv4Oper::Service::SLBfdv4Get(::grpc::ServerContext* context, const ::service_layer::SLBfdGetMsg* request, ::service_layer::SLBfdGetMsgRsp* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SLBfdv4Oper::Service::SLBfdv4GetStats(::grpc::ServerContext* context, const ::service_layer::SLBfdGetMsg* request, ::service_layer::SLBfdGetStatsMsgRsp* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SLBfdv4Oper::Service::SLBfdv4GetNotifStream(::grpc::ServerContext* context, const ::service_layer::SLBfdGetNotifMsg* request, ::grpc::ServerWriter< ::service_layer::SLBfdv4Notif>* writer) {
  (void) context;
  (void) request;
  (void) writer;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SLBfdv4Oper::Service::SLBfdv4SessionOp(::grpc::ServerContext* context, const ::service_layer::SLBfdv4Msg* request, ::service_layer::SLBfdv4MsgRsp* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SLBfdv4Oper::Service::SLBfdv4SessionGet(::grpc::ServerContext* context, const ::service_layer::SLBfdv4GetMsg* request, ::service_layer::SLBfdv4GetMsgRsp* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


}  // namespace service_layer

