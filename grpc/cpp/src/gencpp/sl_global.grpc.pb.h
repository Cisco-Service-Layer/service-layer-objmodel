// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: sl_global.proto
// Original file comments:
// @file
// @brief Server RPC proto file. Client invokes to init the session
// on server.
//
// ----------------------------------------------------------------
//  Copyright (c) 2019 by Cisco Systems, Inc.
//  All rights reserved.
// -----------------------------------------------------------------
//
//
//
#ifndef GRPC_sl_5fglobal_2eproto__INCLUDED
#define GRPC_sl_5fglobal_2eproto__INCLUDED

#include "sl_global.pb.h"

#include <functional>
#include <grpcpp/impl/codegen/async_generic_service.h>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/client_callback.h>
#include <grpcpp/impl/codegen/client_context.h>
#include <grpcpp/impl/codegen/completion_queue.h>
#include <grpcpp/impl/codegen/message_allocator.h>
#include <grpcpp/impl/codegen/method_handler.h>
#include <grpcpp/impl/codegen/proto_utils.h>
#include <grpcpp/impl/codegen/rpc_method.h>
#include <grpcpp/impl/codegen/server_callback.h>
#include <grpcpp/impl/codegen/server_callback_handlers.h>
#include <grpcpp/impl/codegen/server_context.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/status.h>
#include <grpcpp/impl/codegen/stub_options.h>
#include <grpcpp/impl/codegen/sync_stream.h>

namespace service_layer {

// @defgroup SLGlobal
// @ingroup Common
// Global Initialization and Notifications.
// The following RPCs are used in global initialization and capability queries.
// @{
class SLGlobal final {
 public:
  static constexpr char const* service_full_name() {
    return "service_layer.SLGlobal";
  }
  class StubInterface {
   public:
    virtual ~StubInterface() {}
    // Initialize the connection, and setup a application level heartbeat channel.
    //
    // The caller must send its version information as part of the SLInitMsg
    // message. The server will reply with SL_GLOBAL_EVENT_TYPE_VERSION
    // that tells the caller whether he can proceed or not.
    // Refer to message SLGlobalNotif below for further details.
    //
    // After the version handshake, the notification channel is used for
    // "push" event notifications, such as:
    //    - SLGlobalNotif.EventType = SL_GLOBAL_EVENT_TYPE_HEARTBEAT
    //        heartbeat notification messages are sent to the client on
    //        a periodic basis.
    //    Refer to SLGlobalNotif definition for further info.
    std::unique_ptr< ::grpc::ClientReaderInterface< ::service_layer::SLGlobalNotif>> SLGlobalInitNotif(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request) {
      return std::unique_ptr< ::grpc::ClientReaderInterface< ::service_layer::SLGlobalNotif>>(SLGlobalInitNotifRaw(context, request));
    }
    std::unique_ptr< ::grpc::ClientAsyncReaderInterface< ::service_layer::SLGlobalNotif>> AsyncSLGlobalInitNotif(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request, ::grpc::CompletionQueue* cq, void* tag) {
      return std::unique_ptr< ::grpc::ClientAsyncReaderInterface< ::service_layer::SLGlobalNotif>>(AsyncSLGlobalInitNotifRaw(context, request, cq, tag));
    }
    std::unique_ptr< ::grpc::ClientAsyncReaderInterface< ::service_layer::SLGlobalNotif>> PrepareAsyncSLGlobalInitNotif(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncReaderInterface< ::service_layer::SLGlobalNotif>>(PrepareAsyncSLGlobalInitNotifRaw(context, request, cq));
    }
    // Get platform specific globals
    virtual ::grpc::Status SLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::service_layer::SLGlobalsGetMsgRsp* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::service_layer::SLGlobalsGetMsgRsp>> AsyncSLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::service_layer::SLGlobalsGetMsgRsp>>(AsyncSLGlobalsGetRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::service_layer::SLGlobalsGetMsgRsp>> PrepareAsyncSLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::service_layer::SLGlobalsGetMsgRsp>>(PrepareAsyncSLGlobalsGetRaw(context, request, cq));
    }
    // @}
    class async_interface {
     public:
      virtual ~async_interface() {}
      // Initialize the connection, and setup a application level heartbeat channel.
      //
      // The caller must send its version information as part of the SLInitMsg
      // message. The server will reply with SL_GLOBAL_EVENT_TYPE_VERSION
      // that tells the caller whether he can proceed or not.
      // Refer to message SLGlobalNotif below for further details.
      //
      // After the version handshake, the notification channel is used for
      // "push" event notifications, such as:
      //    - SLGlobalNotif.EventType = SL_GLOBAL_EVENT_TYPE_HEARTBEAT
      //        heartbeat notification messages are sent to the client on
      //        a periodic basis.
      //    Refer to SLGlobalNotif definition for further info.
      virtual void SLGlobalInitNotif(::grpc::ClientContext* context, const ::service_layer::SLInitMsg* request, ::grpc::ClientReadReactor< ::service_layer::SLGlobalNotif>* reactor) = 0;
      // Get platform specific globals
      virtual void SLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg* request, ::service_layer::SLGlobalsGetMsgRsp* response, std::function<void(::grpc::Status)>) = 0;
      virtual void SLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg* request, ::service_layer::SLGlobalsGetMsgRsp* response, ::grpc::ClientUnaryReactor* reactor) = 0;
      // @}
    };
    typedef class async_interface experimental_async_interface;
    virtual class async_interface* async() { return nullptr; }
    class async_interface* experimental_async() { return async(); }
   private:
    virtual ::grpc::ClientReaderInterface< ::service_layer::SLGlobalNotif>* SLGlobalInitNotifRaw(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request) = 0;
    virtual ::grpc::ClientAsyncReaderInterface< ::service_layer::SLGlobalNotif>* AsyncSLGlobalInitNotifRaw(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request, ::grpc::CompletionQueue* cq, void* tag) = 0;
    virtual ::grpc::ClientAsyncReaderInterface< ::service_layer::SLGlobalNotif>* PrepareAsyncSLGlobalInitNotifRaw(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::service_layer::SLGlobalsGetMsgRsp>* AsyncSLGlobalsGetRaw(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::service_layer::SLGlobalsGetMsgRsp>* PrepareAsyncSLGlobalsGetRaw(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::grpc::CompletionQueue* cq) = 0;
  };
  class Stub final : public StubInterface {
   public:
    Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());
    std::unique_ptr< ::grpc::ClientReader< ::service_layer::SLGlobalNotif>> SLGlobalInitNotif(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request) {
      return std::unique_ptr< ::grpc::ClientReader< ::service_layer::SLGlobalNotif>>(SLGlobalInitNotifRaw(context, request));
    }
    std::unique_ptr< ::grpc::ClientAsyncReader< ::service_layer::SLGlobalNotif>> AsyncSLGlobalInitNotif(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request, ::grpc::CompletionQueue* cq, void* tag) {
      return std::unique_ptr< ::grpc::ClientAsyncReader< ::service_layer::SLGlobalNotif>>(AsyncSLGlobalInitNotifRaw(context, request, cq, tag));
    }
    std::unique_ptr< ::grpc::ClientAsyncReader< ::service_layer::SLGlobalNotif>> PrepareAsyncSLGlobalInitNotif(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncReader< ::service_layer::SLGlobalNotif>>(PrepareAsyncSLGlobalInitNotifRaw(context, request, cq));
    }
    ::grpc::Status SLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::service_layer::SLGlobalsGetMsgRsp* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::service_layer::SLGlobalsGetMsgRsp>> AsyncSLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::service_layer::SLGlobalsGetMsgRsp>>(AsyncSLGlobalsGetRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::service_layer::SLGlobalsGetMsgRsp>> PrepareAsyncSLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::service_layer::SLGlobalsGetMsgRsp>>(PrepareAsyncSLGlobalsGetRaw(context, request, cq));
    }
    class async final :
      public StubInterface::async_interface {
     public:
      void SLGlobalInitNotif(::grpc::ClientContext* context, const ::service_layer::SLInitMsg* request, ::grpc::ClientReadReactor< ::service_layer::SLGlobalNotif>* reactor) override;
      void SLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg* request, ::service_layer::SLGlobalsGetMsgRsp* response, std::function<void(::grpc::Status)>) override;
      void SLGlobalsGet(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg* request, ::service_layer::SLGlobalsGetMsgRsp* response, ::grpc::ClientUnaryReactor* reactor) override;
     private:
      friend class Stub;
      explicit async(Stub* stub): stub_(stub) { }
      Stub* stub() { return stub_; }
      Stub* stub_;
    };
    class async* async() override { return &async_stub_; }

   private:
    std::shared_ptr< ::grpc::ChannelInterface> channel_;
    class async async_stub_{this};
    ::grpc::ClientReader< ::service_layer::SLGlobalNotif>* SLGlobalInitNotifRaw(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request) override;
    ::grpc::ClientAsyncReader< ::service_layer::SLGlobalNotif>* AsyncSLGlobalInitNotifRaw(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request, ::grpc::CompletionQueue* cq, void* tag) override;
    ::grpc::ClientAsyncReader< ::service_layer::SLGlobalNotif>* PrepareAsyncSLGlobalInitNotifRaw(::grpc::ClientContext* context, const ::service_layer::SLInitMsg& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::service_layer::SLGlobalsGetMsgRsp>* AsyncSLGlobalsGetRaw(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::service_layer::SLGlobalsGetMsgRsp>* PrepareAsyncSLGlobalsGetRaw(::grpc::ClientContext* context, const ::service_layer::SLGlobalsGetMsg& request, ::grpc::CompletionQueue* cq) override;
    const ::grpc::internal::RpcMethod rpcmethod_SLGlobalInitNotif_;
    const ::grpc::internal::RpcMethod rpcmethod_SLGlobalsGet_;
  };
  static std::unique_ptr<Stub> NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());

  class Service : public ::grpc::Service {
   public:
    Service();
    virtual ~Service();
    // Initialize the connection, and setup a application level heartbeat channel.
    //
    // The caller must send its version information as part of the SLInitMsg
    // message. The server will reply with SL_GLOBAL_EVENT_TYPE_VERSION
    // that tells the caller whether he can proceed or not.
    // Refer to message SLGlobalNotif below for further details.
    //
    // After the version handshake, the notification channel is used for
    // "push" event notifications, such as:
    //    - SLGlobalNotif.EventType = SL_GLOBAL_EVENT_TYPE_HEARTBEAT
    //        heartbeat notification messages are sent to the client on
    //        a periodic basis.
    //    Refer to SLGlobalNotif definition for further info.
    virtual ::grpc::Status SLGlobalInitNotif(::grpc::ServerContext* context, const ::service_layer::SLInitMsg* request, ::grpc::ServerWriter< ::service_layer::SLGlobalNotif>* writer);
    // Get platform specific globals
    virtual ::grpc::Status SLGlobalsGet(::grpc::ServerContext* context, const ::service_layer::SLGlobalsGetMsg* request, ::service_layer::SLGlobalsGetMsgRsp* response);
    // @}
  };
  template <class BaseClass>
  class WithAsyncMethod_SLGlobalInitNotif : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_SLGlobalInitNotif() {
      ::grpc::Service::MarkMethodAsync(0);
    }
    ~WithAsyncMethod_SLGlobalInitNotif() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalInitNotif(::grpc::ServerContext* /*context*/, const ::service_layer::SLInitMsg* /*request*/, ::grpc::ServerWriter< ::service_layer::SLGlobalNotif>* /*writer*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestSLGlobalInitNotif(::grpc::ServerContext* context, ::service_layer::SLInitMsg* request, ::grpc::ServerAsyncWriter< ::service_layer::SLGlobalNotif>* writer, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncServerStreaming(0, context, request, writer, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithAsyncMethod_SLGlobalsGet : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_SLGlobalsGet() {
      ::grpc::Service::MarkMethodAsync(1);
    }
    ~WithAsyncMethod_SLGlobalsGet() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalsGet(::grpc::ServerContext* /*context*/, const ::service_layer::SLGlobalsGetMsg* /*request*/, ::service_layer::SLGlobalsGetMsgRsp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestSLGlobalsGet(::grpc::ServerContext* context, ::service_layer::SLGlobalsGetMsg* request, ::grpc::ServerAsyncResponseWriter< ::service_layer::SLGlobalsGetMsgRsp>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  typedef WithAsyncMethod_SLGlobalInitNotif<WithAsyncMethod_SLGlobalsGet<Service > > AsyncService;
  template <class BaseClass>
  class WithCallbackMethod_SLGlobalInitNotif : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithCallbackMethod_SLGlobalInitNotif() {
      ::grpc::Service::MarkMethodCallback(0,
          new ::grpc::internal::CallbackServerStreamingHandler< ::service_layer::SLInitMsg, ::service_layer::SLGlobalNotif>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::service_layer::SLInitMsg* request) { return this->SLGlobalInitNotif(context, request); }));
    }
    ~WithCallbackMethod_SLGlobalInitNotif() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalInitNotif(::grpc::ServerContext* /*context*/, const ::service_layer::SLInitMsg* /*request*/, ::grpc::ServerWriter< ::service_layer::SLGlobalNotif>* /*writer*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerWriteReactor< ::service_layer::SLGlobalNotif>* SLGlobalInitNotif(
      ::grpc::CallbackServerContext* /*context*/, const ::service_layer::SLInitMsg* /*request*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithCallbackMethod_SLGlobalsGet : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithCallbackMethod_SLGlobalsGet() {
      ::grpc::Service::MarkMethodCallback(1,
          new ::grpc::internal::CallbackUnaryHandler< ::service_layer::SLGlobalsGetMsg, ::service_layer::SLGlobalsGetMsgRsp>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::service_layer::SLGlobalsGetMsg* request, ::service_layer::SLGlobalsGetMsgRsp* response) { return this->SLGlobalsGet(context, request, response); }));}
    void SetMessageAllocatorFor_SLGlobalsGet(
        ::grpc::MessageAllocator< ::service_layer::SLGlobalsGetMsg, ::service_layer::SLGlobalsGetMsgRsp>* allocator) {
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::GetHandler(1);
      static_cast<::grpc::internal::CallbackUnaryHandler< ::service_layer::SLGlobalsGetMsg, ::service_layer::SLGlobalsGetMsgRsp>*>(handler)
              ->SetMessageAllocator(allocator);
    }
    ~WithCallbackMethod_SLGlobalsGet() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalsGet(::grpc::ServerContext* /*context*/, const ::service_layer::SLGlobalsGetMsg* /*request*/, ::service_layer::SLGlobalsGetMsgRsp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* SLGlobalsGet(
      ::grpc::CallbackServerContext* /*context*/, const ::service_layer::SLGlobalsGetMsg* /*request*/, ::service_layer::SLGlobalsGetMsgRsp* /*response*/)  { return nullptr; }
  };
  typedef WithCallbackMethod_SLGlobalInitNotif<WithCallbackMethod_SLGlobalsGet<Service > > CallbackService;
  typedef CallbackService ExperimentalCallbackService;
  template <class BaseClass>
  class WithGenericMethod_SLGlobalInitNotif : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_SLGlobalInitNotif() {
      ::grpc::Service::MarkMethodGeneric(0);
    }
    ~WithGenericMethod_SLGlobalInitNotif() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalInitNotif(::grpc::ServerContext* /*context*/, const ::service_layer::SLInitMsg* /*request*/, ::grpc::ServerWriter< ::service_layer::SLGlobalNotif>* /*writer*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithGenericMethod_SLGlobalsGet : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_SLGlobalsGet() {
      ::grpc::Service::MarkMethodGeneric(1);
    }
    ~WithGenericMethod_SLGlobalsGet() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalsGet(::grpc::ServerContext* /*context*/, const ::service_layer::SLGlobalsGetMsg* /*request*/, ::service_layer::SLGlobalsGetMsgRsp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithRawMethod_SLGlobalInitNotif : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_SLGlobalInitNotif() {
      ::grpc::Service::MarkMethodRaw(0);
    }
    ~WithRawMethod_SLGlobalInitNotif() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalInitNotif(::grpc::ServerContext* /*context*/, const ::service_layer::SLInitMsg* /*request*/, ::grpc::ServerWriter< ::service_layer::SLGlobalNotif>* /*writer*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestSLGlobalInitNotif(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncWriter< ::grpc::ByteBuffer>* writer, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncServerStreaming(0, context, request, writer, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithRawMethod_SLGlobalsGet : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_SLGlobalsGet() {
      ::grpc::Service::MarkMethodRaw(1);
    }
    ~WithRawMethod_SLGlobalsGet() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalsGet(::grpc::ServerContext* /*context*/, const ::service_layer::SLGlobalsGetMsg* /*request*/, ::service_layer::SLGlobalsGetMsgRsp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestSLGlobalsGet(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithRawCallbackMethod_SLGlobalInitNotif : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawCallbackMethod_SLGlobalInitNotif() {
      ::grpc::Service::MarkMethodRawCallback(0,
          new ::grpc::internal::CallbackServerStreamingHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
                   ::grpc::CallbackServerContext* context, const::grpc::ByteBuffer* request) { return this->SLGlobalInitNotif(context, request); }));
    }
    ~WithRawCallbackMethod_SLGlobalInitNotif() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalInitNotif(::grpc::ServerContext* /*context*/, const ::service_layer::SLInitMsg* /*request*/, ::grpc::ServerWriter< ::service_layer::SLGlobalNotif>* /*writer*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerWriteReactor< ::grpc::ByteBuffer>* SLGlobalInitNotif(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithRawCallbackMethod_SLGlobalsGet : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawCallbackMethod_SLGlobalsGet() {
      ::grpc::Service::MarkMethodRawCallback(1,
          new ::grpc::internal::CallbackUnaryHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::grpc::ByteBuffer* request, ::grpc::ByteBuffer* response) { return this->SLGlobalsGet(context, request, response); }));
    }
    ~WithRawCallbackMethod_SLGlobalsGet() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SLGlobalsGet(::grpc::ServerContext* /*context*/, const ::service_layer::SLGlobalsGetMsg* /*request*/, ::service_layer::SLGlobalsGetMsgRsp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* SLGlobalsGet(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_SLGlobalsGet : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithStreamedUnaryMethod_SLGlobalsGet() {
      ::grpc::Service::MarkMethodStreamed(1,
        new ::grpc::internal::StreamedUnaryHandler<
          ::service_layer::SLGlobalsGetMsg, ::service_layer::SLGlobalsGetMsgRsp>(
            [this](::grpc::ServerContext* context,
                   ::grpc::ServerUnaryStreamer<
                     ::service_layer::SLGlobalsGetMsg, ::service_layer::SLGlobalsGetMsgRsp>* streamer) {
                       return this->StreamedSLGlobalsGet(context,
                         streamer);
                  }));
    }
    ~WithStreamedUnaryMethod_SLGlobalsGet() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status SLGlobalsGet(::grpc::ServerContext* /*context*/, const ::service_layer::SLGlobalsGetMsg* /*request*/, ::service_layer::SLGlobalsGetMsgRsp* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status StreamedSLGlobalsGet(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::service_layer::SLGlobalsGetMsg,::service_layer::SLGlobalsGetMsgRsp>* server_unary_streamer) = 0;
  };
  typedef WithStreamedUnaryMethod_SLGlobalsGet<Service > StreamedUnaryService;
  template <class BaseClass>
  class WithSplitStreamingMethod_SLGlobalInitNotif : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithSplitStreamingMethod_SLGlobalInitNotif() {
      ::grpc::Service::MarkMethodStreamed(0,
        new ::grpc::internal::SplitServerStreamingHandler<
          ::service_layer::SLInitMsg, ::service_layer::SLGlobalNotif>(
            [this](::grpc::ServerContext* context,
                   ::grpc::ServerSplitStreamer<
                     ::service_layer::SLInitMsg, ::service_layer::SLGlobalNotif>* streamer) {
                       return this->StreamedSLGlobalInitNotif(context,
                         streamer);
                  }));
    }
    ~WithSplitStreamingMethod_SLGlobalInitNotif() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status SLGlobalInitNotif(::grpc::ServerContext* /*context*/, const ::service_layer::SLInitMsg* /*request*/, ::grpc::ServerWriter< ::service_layer::SLGlobalNotif>* /*writer*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with split streamed
    virtual ::grpc::Status StreamedSLGlobalInitNotif(::grpc::ServerContext* context, ::grpc::ServerSplitStreamer< ::service_layer::SLInitMsg,::service_layer::SLGlobalNotif>* server_split_streamer) = 0;
  };
  typedef WithSplitStreamingMethod_SLGlobalInitNotif<Service > SplitStreamedService;
  typedef WithSplitStreamingMethod_SLGlobalInitNotif<WithStreamedUnaryMethod_SLGlobalsGet<Service > > StreamedService;
};
// @addtogroup SLGlobal
// @{
// /;

}  // namespace service_layer


#endif  // GRPC_sl_5fglobal_2eproto__INCLUDED
