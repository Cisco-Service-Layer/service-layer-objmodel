// <auto-generated>
//     Generated by the protocol buffer compiler.  DO NOT EDIT!
//     source: sl_global.proto
// </auto-generated>
// Original file comments:
// @file
// @brief Server RPC proto file. Client invokes to init the session
// on server.
//
// ----------------------------------------------------------------
//  Copyright (c) 2019, 2023 by Cisco Systems, Inc.
//  All rights reserved.
// -----------------------------------------------------------------
//
//
//
#pragma warning disable 0414, 1591
#region Designer generated code

using grpc = global::Grpc.Core;

namespace ServiceLayer {
  /// <summary>
  /// @defgroup SLGlobal
  /// @ingroup Common
  /// Global Initialization and Notifications.
  /// The following RPCs are used in global initialization and capability queries.
  /// @{
  /// </summary>
  public static partial class SLGlobal
  {
    static readonly string __ServiceName = "service_layer.SLGlobal";

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static void __Helper_SerializeMessage(global::Google.Protobuf.IMessage message, grpc::SerializationContext context)
    {
      #if !GRPC_DISABLE_PROTOBUF_BUFFER_SERIALIZATION
      if (message is global::Google.Protobuf.IBufferMessage)
      {
        context.SetPayloadLength(message.CalculateSize());
        global::Google.Protobuf.MessageExtensions.WriteTo(message, context.GetBufferWriter());
        context.Complete();
        return;
      }
      #endif
      context.Complete(global::Google.Protobuf.MessageExtensions.ToByteArray(message));
    }

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static class __Helper_MessageCache<T>
    {
      public static readonly bool IsBufferMessage = global::System.Reflection.IntrospectionExtensions.GetTypeInfo(typeof(global::Google.Protobuf.IBufferMessage)).IsAssignableFrom(typeof(T));
    }

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static T __Helper_DeserializeMessage<T>(grpc::DeserializationContext context, global::Google.Protobuf.MessageParser<T> parser) where T : global::Google.Protobuf.IMessage<T>
    {
      #if !GRPC_DISABLE_PROTOBUF_BUFFER_SERIALIZATION
      if (__Helper_MessageCache<T>.IsBufferMessage)
      {
        return parser.ParseFrom(context.PayloadAsReadOnlySequence());
      }
      #endif
      return parser.ParseFrom(context.PayloadAsNewBuffer());
    }

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::ServiceLayer.SLInitMsg> __Marshaller_service_layer_SLInitMsg = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLInitMsg.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::ServiceLayer.SLGlobalNotif> __Marshaller_service_layer_SLGlobalNotif = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLGlobalNotif.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::ServiceLayer.SLGlobalsGetMsg> __Marshaller_service_layer_SLGlobalsGetMsg = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLGlobalsGetMsg.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::ServiceLayer.SLGlobalsGetMsgRsp> __Marshaller_service_layer_SLGlobalsGetMsgRsp = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLGlobalsGetMsgRsp.Parser));

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Method<global::ServiceLayer.SLInitMsg, global::ServiceLayer.SLGlobalNotif> __Method_SLGlobalInitNotif = new grpc::Method<global::ServiceLayer.SLInitMsg, global::ServiceLayer.SLGlobalNotif>(
        grpc::MethodType.ServerStreaming,
        __ServiceName,
        "SLGlobalInitNotif",
        __Marshaller_service_layer_SLInitMsg,
        __Marshaller_service_layer_SLGlobalNotif);

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Method<global::ServiceLayer.SLGlobalsGetMsg, global::ServiceLayer.SLGlobalsGetMsgRsp> __Method_SLGlobalsGet = new grpc::Method<global::ServiceLayer.SLGlobalsGetMsg, global::ServiceLayer.SLGlobalsGetMsgRsp>(
        grpc::MethodType.Unary,
        __ServiceName,
        "SLGlobalsGet",
        __Marshaller_service_layer_SLGlobalsGetMsg,
        __Marshaller_service_layer_SLGlobalsGetMsgRsp);

    /// <summary>Service descriptor</summary>
    public static global::Google.Protobuf.Reflection.ServiceDescriptor Descriptor
    {
      get { return global::ServiceLayer.SlGlobalReflection.Descriptor.Services[0]; }
    }

    /// <summary>Base class for server-side implementations of SLGlobal</summary>
    [grpc::BindServiceMethod(typeof(SLGlobal), "BindService")]
    public abstract partial class SLGlobalBase
    {
      /// <summary>
      /// Initialize the connection, and setup a application level heartbeat channel.
      ///
      /// The caller must send its version information as part of the SLInitMsg
      /// message. The server will reply with SL_GLOBAL_EVENT_TYPE_VERSION
      /// that tells the caller whether he can proceed or not.
      /// Refer to message SLGlobalNotif below for further details.
      ///
      /// After the version handshake, the notification channel is used for
      /// "push" event notifications, such as:
      ///    - SLGlobalNotif.EventType = SL_GLOBAL_EVENT_TYPE_HEARTBEAT
      ///        heartbeat notification messages are sent to the client on
      ///        a periodic basis.
      ///    Refer to SLGlobalNotif definition for further info.
      /// </summary>
      /// <param name="request">The request received from the client.</param>
      /// <param name="responseStream">Used for sending responses back to the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>A task indicating completion of the handler.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::System.Threading.Tasks.Task SLGlobalInitNotif(global::ServiceLayer.SLInitMsg request, grpc::IServerStreamWriter<global::ServiceLayer.SLGlobalNotif> responseStream, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      /// <summary>
      /// Get platform specific globals
      /// </summary>
      /// <param name="request">The request received from the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>The response to send back to the client (wrapped by a task).</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::System.Threading.Tasks.Task<global::ServiceLayer.SLGlobalsGetMsgRsp> SLGlobalsGet(global::ServiceLayer.SLGlobalsGetMsg request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

    }

    /// <summary>Client for SLGlobal</summary>
    public partial class SLGlobalClient : grpc::ClientBase<SLGlobalClient>
    {
      /// <summary>Creates a new client for SLGlobal</summary>
      /// <param name="channel">The channel to use to make remote calls.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public SLGlobalClient(grpc::ChannelBase channel) : base(channel)
      {
      }
      /// <summary>Creates a new client for SLGlobal that uses a custom <c>CallInvoker</c>.</summary>
      /// <param name="callInvoker">The callInvoker to use to make remote calls.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public SLGlobalClient(grpc::CallInvoker callInvoker) : base(callInvoker)
      {
      }
      /// <summary>Protected parameterless constructor to allow creation of test doubles.</summary>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected SLGlobalClient() : base()
      {
      }
      /// <summary>Protected constructor to allow creation of configured clients.</summary>
      /// <param name="configuration">The client configuration.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected SLGlobalClient(ClientBaseConfiguration configuration) : base(configuration)
      {
      }

      /// <summary>
      /// Initialize the connection, and setup a application level heartbeat channel.
      ///
      /// The caller must send its version information as part of the SLInitMsg
      /// message. The server will reply with SL_GLOBAL_EVENT_TYPE_VERSION
      /// that tells the caller whether he can proceed or not.
      /// Refer to message SLGlobalNotif below for further details.
      ///
      /// After the version handshake, the notification channel is used for
      /// "push" event notifications, such as:
      ///    - SLGlobalNotif.EventType = SL_GLOBAL_EVENT_TYPE_HEARTBEAT
      ///        heartbeat notification messages are sent to the client on
      ///        a periodic basis.
      ///    Refer to SLGlobalNotif definition for further info.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncServerStreamingCall<global::ServiceLayer.SLGlobalNotif> SLGlobalInitNotif(global::ServiceLayer.SLInitMsg request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SLGlobalInitNotif(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// Initialize the connection, and setup a application level heartbeat channel.
      ///
      /// The caller must send its version information as part of the SLInitMsg
      /// message. The server will reply with SL_GLOBAL_EVENT_TYPE_VERSION
      /// that tells the caller whether he can proceed or not.
      /// Refer to message SLGlobalNotif below for further details.
      ///
      /// After the version handshake, the notification channel is used for
      /// "push" event notifications, such as:
      ///    - SLGlobalNotif.EventType = SL_GLOBAL_EVENT_TYPE_HEARTBEAT
      ///        heartbeat notification messages are sent to the client on
      ///        a periodic basis.
      ///    Refer to SLGlobalNotif definition for further info.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncServerStreamingCall<global::ServiceLayer.SLGlobalNotif> SLGlobalInitNotif(global::ServiceLayer.SLInitMsg request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncServerStreamingCall(__Method_SLGlobalInitNotif, null, options, request);
      }
      /// <summary>
      /// Get platform specific globals
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The response received from the server.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::ServiceLayer.SLGlobalsGetMsgRsp SLGlobalsGet(global::ServiceLayer.SLGlobalsGetMsg request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SLGlobalsGet(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// Get platform specific globals
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The response received from the server.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::ServiceLayer.SLGlobalsGetMsgRsp SLGlobalsGet(global::ServiceLayer.SLGlobalsGetMsg request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_SLGlobalsGet, null, options, request);
      }
      /// <summary>
      /// Get platform specific globals
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::ServiceLayer.SLGlobalsGetMsgRsp> SLGlobalsGetAsync(global::ServiceLayer.SLGlobalsGetMsg request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SLGlobalsGetAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// Get platform specific globals
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::ServiceLayer.SLGlobalsGetMsgRsp> SLGlobalsGetAsync(global::ServiceLayer.SLGlobalsGetMsg request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_SLGlobalsGet, null, options, request);
      }
      /// <summary>Creates a new instance of client from given <c>ClientBaseConfiguration</c>.</summary>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected override SLGlobalClient NewInstance(ClientBaseConfiguration configuration)
      {
        return new SLGlobalClient(configuration);
      }
    }

    /// <summary>Creates service definition that can be registered with a server</summary>
    /// <param name="serviceImpl">An object implementing the server-side handling logic.</param>
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    public static grpc::ServerServiceDefinition BindService(SLGlobalBase serviceImpl)
    {
      return grpc::ServerServiceDefinition.CreateBuilder()
          .AddMethod(__Method_SLGlobalInitNotif, serviceImpl.SLGlobalInitNotif)
          .AddMethod(__Method_SLGlobalsGet, serviceImpl.SLGlobalsGet).Build();
    }

    /// <summary>Register service method with a service binder with or without implementation. Useful when customizing the service binding logic.
    /// Note: this method is part of an experimental API that can change or be removed without any prior notice.</summary>
    /// <param name="serviceBinder">Service methods will be bound by calling <c>AddMethod</c> on this object.</param>
    /// <param name="serviceImpl">An object implementing the server-side handling logic.</param>
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    public static void BindService(grpc::ServiceBinderBase serviceBinder, SLGlobalBase serviceImpl)
    {
      serviceBinder.AddMethod(__Method_SLGlobalInitNotif, serviceImpl == null ? null : new grpc::ServerStreamingServerMethod<global::ServiceLayer.SLInitMsg, global::ServiceLayer.SLGlobalNotif>(serviceImpl.SLGlobalInitNotif));
      serviceBinder.AddMethod(__Method_SLGlobalsGet, serviceImpl == null ? null : new grpc::UnaryServerMethod<global::ServiceLayer.SLGlobalsGetMsg, global::ServiceLayer.SLGlobalsGetMsgRsp>(serviceImpl.SLGlobalsGet));
    }

  }
}
#endregion
