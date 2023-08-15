// <auto-generated>
//     Generated by the protocol buffer compiler.  DO NOT EDIT!
//     source: sl_af.proto
// </auto-generated>
// Original file comments:
// @file
// @brief Client RPC proto file for operations on objects in a address family.
// This file defines SL-API service and messages for operations
// on IP routes, MPLS objects, Path Groups and Policy Forwarding Entries.
//
// The RPCs and messages defined here are experimental and subject to
// change without notice and such changes can break backwards compatibility.
//
// ----------------------------------------------------------------
//  Copyright (c) 2023 by Cisco Systems, Inc.
//  All rights reserved.
// -----------------------------------------------------------------
//
//
//
// @defgroup AF
// @brief Address family service definitions.
//
#pragma warning disable 0414, 1591
#region Designer generated code

using grpc = global::Grpc.Core;

namespace ServiceLayer {
  /// <summary>
  ///@addtogroup SLAF
  ///@{
  ///;
  /// </summary>
  public static partial class SLAF
  {
    static readonly string __ServiceName = "service_layer.SLAF";

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
    static readonly grpc::Marshaller<global::ServiceLayer.SLAFVrfRegMsg> __Marshaller_service_layer_SLAFVrfRegMsg = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLAFVrfRegMsg.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::ServiceLayer.SLAFVrfRegMsgRsp> __Marshaller_service_layer_SLAFVrfRegMsgRsp = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLAFVrfRegMsgRsp.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::ServiceLayer.SLAFMsg> __Marshaller_service_layer_SLAFMsg = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLAFMsg.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::ServiceLayer.SLAFMsgRsp> __Marshaller_service_layer_SLAFMsgRsp = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLAFMsgRsp.Parser));

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Method<global::ServiceLayer.SLAFVrfRegMsg, global::ServiceLayer.SLAFVrfRegMsgRsp> __Method_SLAFVrfRegOp = new grpc::Method<global::ServiceLayer.SLAFVrfRegMsg, global::ServiceLayer.SLAFVrfRegMsgRsp>(
        grpc::MethodType.Unary,
        __ServiceName,
        "SLAFVrfRegOp",
        __Marshaller_service_layer_SLAFVrfRegMsg,
        __Marshaller_service_layer_SLAFVrfRegMsgRsp);

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Method<global::ServiceLayer.SLAFMsg, global::ServiceLayer.SLAFMsgRsp> __Method_SLAFOp = new grpc::Method<global::ServiceLayer.SLAFMsg, global::ServiceLayer.SLAFMsgRsp>(
        grpc::MethodType.Unary,
        __ServiceName,
        "SLAFOp",
        __Marshaller_service_layer_SLAFMsg,
        __Marshaller_service_layer_SLAFMsgRsp);

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Method<global::ServiceLayer.SLAFMsg, global::ServiceLayer.SLAFMsgRsp> __Method_SLAFOpStream = new grpc::Method<global::ServiceLayer.SLAFMsg, global::ServiceLayer.SLAFMsgRsp>(
        grpc::MethodType.DuplexStreaming,
        __ServiceName,
        "SLAFOpStream",
        __Marshaller_service_layer_SLAFMsg,
        __Marshaller_service_layer_SLAFMsgRsp);

    /// <summary>Service descriptor</summary>
    public static global::Google.Protobuf.Reflection.ServiceDescriptor Descriptor
    {
      get { return global::ServiceLayer.SlAfReflection.Descriptor.Services[0]; }
    }

    /// <summary>Base class for server-side implementations of SLAF</summary>
    [grpc::BindServiceMethod(typeof(SLAF), "BindService")]
    public abstract partial class SLAFBase
    {
      /// <summary>
      ///
      /// VRF registration operations. The client MUST register with
      /// the corresponding VRF table before programming objects in that table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_REGISTER:
      ///     VRF table registration: Sends a list of VRF table registration
      ///     messages and expects a list of registration responses.
      ///     A client Must Register a VRF table BEFORE objects can be
      ///     added/modified in the associated VRF table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_UNREGISTER:
      ///     VRF table Un-registration: Sends a list of VRF table un-registration
      ///     messages and expects a list of un-registration responses.
      ///     This can be used to convey that the client is no longer interested
      ///     in these VRF tables. All previously installed objects would be
      ///     remove.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_EOF:
      ///     VRF table End Of File message.
      ///     After Registration, the client is expected to send an EOF
      ///     message to convey the end of replay of the client's known objects.
      ///     This is especially useful under certain restart scenarios when the
      ///     client and the server are trying to synchronize their objects.
      ///
      /// The VRF table registration operations can be used by the client to
      /// synchronize objects with the device. When the client re-registers the
      /// VRF table with the server using SL_REGOP_REGISTER, server marks
      /// objects in that table as stale.
      /// Client then MUST reprogram objects it is interested in.
      /// When client sends SL_REGOP_EOF, any objects not reprogrammed
      /// are removed from the device. This feature can be turned
      /// off by setting SLVrfReg.NoMarking flag to True.
      ///
      /// The client MUST perform all operations (VRF registration, objects)
      /// from a single execution context.
      /// </summary>
      /// <param name="request">The request received from the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>The response to send back to the client (wrapped by a task).</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::System.Threading.Tasks.Task<global::ServiceLayer.SLAFVrfRegMsgRsp> SLAFVrfRegOp(global::ServiceLayer.SLAFVrfRegMsg request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      /// <summary>
      /// SLAFMsg.Oper = SL_OBJOP_ADD:
      ///     Object add. Fails if the objects already exists and is not stale.
      ///     First ADD operation on a stale object is allowed and the object
      ///     is no longer considered stale.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_UPDATE:
      ///     Object update. Creates or updates the objects.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_DELETE:
      ///     Object delete. The object's key is enough to delete the object.
      ///     Delete of a non-existant object is returned as success.
      /// </summary>
      /// <param name="request">The request received from the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>The response to send back to the client (wrapped by a task).</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::System.Threading.Tasks.Task<global::ServiceLayer.SLAFMsgRsp> SLAFOp(global::ServiceLayer.SLAFMsg request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      /// <summary>
      /// SLAFMsg.Oper = SL_OBJOP_ADD:
      ///     Object add. Fails if the objects already exists and is not stale.
      ///     First ADD operation on a stale object is allowed and the object
      ///     is no longer considered stale.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_UPDATE:
      ///     Object update. Creates or updates the object.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_DELETE:
      ///     Object delete. The object's key is enough to delete the object.
      ///     Delete of a non-existant object is returned as success.
      /// </summary>
      /// <param name="requestStream">Used for reading requests from the client.</param>
      /// <param name="responseStream">Used for sending responses back to the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>A task indicating completion of the handler.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::System.Threading.Tasks.Task SLAFOpStream(grpc::IAsyncStreamReader<global::ServiceLayer.SLAFMsg> requestStream, grpc::IServerStreamWriter<global::ServiceLayer.SLAFMsgRsp> responseStream, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

    }

    /// <summary>Client for SLAF</summary>
    public partial class SLAFClient : grpc::ClientBase<SLAFClient>
    {
      /// <summary>Creates a new client for SLAF</summary>
      /// <param name="channel">The channel to use to make remote calls.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public SLAFClient(grpc::ChannelBase channel) : base(channel)
      {
      }
      /// <summary>Creates a new client for SLAF that uses a custom <c>CallInvoker</c>.</summary>
      /// <param name="callInvoker">The callInvoker to use to make remote calls.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public SLAFClient(grpc::CallInvoker callInvoker) : base(callInvoker)
      {
      }
      /// <summary>Protected parameterless constructor to allow creation of test doubles.</summary>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected SLAFClient() : base()
      {
      }
      /// <summary>Protected constructor to allow creation of configured clients.</summary>
      /// <param name="configuration">The client configuration.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected SLAFClient(ClientBaseConfiguration configuration) : base(configuration)
      {
      }

      /// <summary>
      ///
      /// VRF registration operations. The client MUST register with
      /// the corresponding VRF table before programming objects in that table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_REGISTER:
      ///     VRF table registration: Sends a list of VRF table registration
      ///     messages and expects a list of registration responses.
      ///     A client Must Register a VRF table BEFORE objects can be
      ///     added/modified in the associated VRF table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_UNREGISTER:
      ///     VRF table Un-registration: Sends a list of VRF table un-registration
      ///     messages and expects a list of un-registration responses.
      ///     This can be used to convey that the client is no longer interested
      ///     in these VRF tables. All previously installed objects would be
      ///     remove.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_EOF:
      ///     VRF table End Of File message.
      ///     After Registration, the client is expected to send an EOF
      ///     message to convey the end of replay of the client's known objects.
      ///     This is especially useful under certain restart scenarios when the
      ///     client and the server are trying to synchronize their objects.
      ///
      /// The VRF table registration operations can be used by the client to
      /// synchronize objects with the device. When the client re-registers the
      /// VRF table with the server using SL_REGOP_REGISTER, server marks
      /// objects in that table as stale.
      /// Client then MUST reprogram objects it is interested in.
      /// When client sends SL_REGOP_EOF, any objects not reprogrammed
      /// are removed from the device. This feature can be turned
      /// off by setting SLVrfReg.NoMarking flag to True.
      ///
      /// The client MUST perform all operations (VRF registration, objects)
      /// from a single execution context.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The response received from the server.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::ServiceLayer.SLAFVrfRegMsgRsp SLAFVrfRegOp(global::ServiceLayer.SLAFVrfRegMsg request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SLAFVrfRegOp(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      ///
      /// VRF registration operations. The client MUST register with
      /// the corresponding VRF table before programming objects in that table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_REGISTER:
      ///     VRF table registration: Sends a list of VRF table registration
      ///     messages and expects a list of registration responses.
      ///     A client Must Register a VRF table BEFORE objects can be
      ///     added/modified in the associated VRF table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_UNREGISTER:
      ///     VRF table Un-registration: Sends a list of VRF table un-registration
      ///     messages and expects a list of un-registration responses.
      ///     This can be used to convey that the client is no longer interested
      ///     in these VRF tables. All previously installed objects would be
      ///     remove.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_EOF:
      ///     VRF table End Of File message.
      ///     After Registration, the client is expected to send an EOF
      ///     message to convey the end of replay of the client's known objects.
      ///     This is especially useful under certain restart scenarios when the
      ///     client and the server are trying to synchronize their objects.
      ///
      /// The VRF table registration operations can be used by the client to
      /// synchronize objects with the device. When the client re-registers the
      /// VRF table with the server using SL_REGOP_REGISTER, server marks
      /// objects in that table as stale.
      /// Client then MUST reprogram objects it is interested in.
      /// When client sends SL_REGOP_EOF, any objects not reprogrammed
      /// are removed from the device. This feature can be turned
      /// off by setting SLVrfReg.NoMarking flag to True.
      ///
      /// The client MUST perform all operations (VRF registration, objects)
      /// from a single execution context.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The response received from the server.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::ServiceLayer.SLAFVrfRegMsgRsp SLAFVrfRegOp(global::ServiceLayer.SLAFVrfRegMsg request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_SLAFVrfRegOp, null, options, request);
      }
      /// <summary>
      ///
      /// VRF registration operations. The client MUST register with
      /// the corresponding VRF table before programming objects in that table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_REGISTER:
      ///     VRF table registration: Sends a list of VRF table registration
      ///     messages and expects a list of registration responses.
      ///     A client Must Register a VRF table BEFORE objects can be
      ///     added/modified in the associated VRF table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_UNREGISTER:
      ///     VRF table Un-registration: Sends a list of VRF table un-registration
      ///     messages and expects a list of un-registration responses.
      ///     This can be used to convey that the client is no longer interested
      ///     in these VRF tables. All previously installed objects would be
      ///     remove.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_EOF:
      ///     VRF table End Of File message.
      ///     After Registration, the client is expected to send an EOF
      ///     message to convey the end of replay of the client's known objects.
      ///     This is especially useful under certain restart scenarios when the
      ///     client and the server are trying to synchronize their objects.
      ///
      /// The VRF table registration operations can be used by the client to
      /// synchronize objects with the device. When the client re-registers the
      /// VRF table with the server using SL_REGOP_REGISTER, server marks
      /// objects in that table as stale.
      /// Client then MUST reprogram objects it is interested in.
      /// When client sends SL_REGOP_EOF, any objects not reprogrammed
      /// are removed from the device. This feature can be turned
      /// off by setting SLVrfReg.NoMarking flag to True.
      ///
      /// The client MUST perform all operations (VRF registration, objects)
      /// from a single execution context.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::ServiceLayer.SLAFVrfRegMsgRsp> SLAFVrfRegOpAsync(global::ServiceLayer.SLAFVrfRegMsg request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SLAFVrfRegOpAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      ///
      /// VRF registration operations. The client MUST register with
      /// the corresponding VRF table before programming objects in that table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_REGISTER:
      ///     VRF table registration: Sends a list of VRF table registration
      ///     messages and expects a list of registration responses.
      ///     A client Must Register a VRF table BEFORE objects can be
      ///     added/modified in the associated VRF table.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_UNREGISTER:
      ///     VRF table Un-registration: Sends a list of VRF table un-registration
      ///     messages and expects a list of un-registration responses.
      ///     This can be used to convey that the client is no longer interested
      ///     in these VRF tables. All previously installed objects would be
      ///     remove.
      ///
      /// SLAFVrfRegMsg.Oper = SL_REGOP_EOF:
      ///     VRF table End Of File message.
      ///     After Registration, the client is expected to send an EOF
      ///     message to convey the end of replay of the client's known objects.
      ///     This is especially useful under certain restart scenarios when the
      ///     client and the server are trying to synchronize their objects.
      ///
      /// The VRF table registration operations can be used by the client to
      /// synchronize objects with the device. When the client re-registers the
      /// VRF table with the server using SL_REGOP_REGISTER, server marks
      /// objects in that table as stale.
      /// Client then MUST reprogram objects it is interested in.
      /// When client sends SL_REGOP_EOF, any objects not reprogrammed
      /// are removed from the device. This feature can be turned
      /// off by setting SLVrfReg.NoMarking flag to True.
      ///
      /// The client MUST perform all operations (VRF registration, objects)
      /// from a single execution context.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::ServiceLayer.SLAFVrfRegMsgRsp> SLAFVrfRegOpAsync(global::ServiceLayer.SLAFVrfRegMsg request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_SLAFVrfRegOp, null, options, request);
      }
      /// <summary>
      /// SLAFMsg.Oper = SL_OBJOP_ADD:
      ///     Object add. Fails if the objects already exists and is not stale.
      ///     First ADD operation on a stale object is allowed and the object
      ///     is no longer considered stale.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_UPDATE:
      ///     Object update. Creates or updates the objects.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_DELETE:
      ///     Object delete. The object's key is enough to delete the object.
      ///     Delete of a non-existant object is returned as success.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The response received from the server.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::ServiceLayer.SLAFMsgRsp SLAFOp(global::ServiceLayer.SLAFMsg request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SLAFOp(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// SLAFMsg.Oper = SL_OBJOP_ADD:
      ///     Object add. Fails if the objects already exists and is not stale.
      ///     First ADD operation on a stale object is allowed and the object
      ///     is no longer considered stale.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_UPDATE:
      ///     Object update. Creates or updates the objects.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_DELETE:
      ///     Object delete. The object's key is enough to delete the object.
      ///     Delete of a non-existant object is returned as success.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The response received from the server.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::ServiceLayer.SLAFMsgRsp SLAFOp(global::ServiceLayer.SLAFMsg request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_SLAFOp, null, options, request);
      }
      /// <summary>
      /// SLAFMsg.Oper = SL_OBJOP_ADD:
      ///     Object add. Fails if the objects already exists and is not stale.
      ///     First ADD operation on a stale object is allowed and the object
      ///     is no longer considered stale.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_UPDATE:
      ///     Object update. Creates or updates the objects.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_DELETE:
      ///     Object delete. The object's key is enough to delete the object.
      ///     Delete of a non-existant object is returned as success.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::ServiceLayer.SLAFMsgRsp> SLAFOpAsync(global::ServiceLayer.SLAFMsg request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SLAFOpAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// SLAFMsg.Oper = SL_OBJOP_ADD:
      ///     Object add. Fails if the objects already exists and is not stale.
      ///     First ADD operation on a stale object is allowed and the object
      ///     is no longer considered stale.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_UPDATE:
      ///     Object update. Creates or updates the objects.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_DELETE:
      ///     Object delete. The object's key is enough to delete the object.
      ///     Delete of a non-existant object is returned as success.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::ServiceLayer.SLAFMsgRsp> SLAFOpAsync(global::ServiceLayer.SLAFMsg request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_SLAFOp, null, options, request);
      }
      /// <summary>
      /// SLAFMsg.Oper = SL_OBJOP_ADD:
      ///     Object add. Fails if the objects already exists and is not stale.
      ///     First ADD operation on a stale object is allowed and the object
      ///     is no longer considered stale.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_UPDATE:
      ///     Object update. Creates or updates the object.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_DELETE:
      ///     Object delete. The object's key is enough to delete the object.
      ///     Delete of a non-existant object is returned as success.
      /// </summary>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncDuplexStreamingCall<global::ServiceLayer.SLAFMsg, global::ServiceLayer.SLAFMsgRsp> SLAFOpStream(grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SLAFOpStream(new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// SLAFMsg.Oper = SL_OBJOP_ADD:
      ///     Object add. Fails if the objects already exists and is not stale.
      ///     First ADD operation on a stale object is allowed and the object
      ///     is no longer considered stale.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_UPDATE:
      ///     Object update. Creates or updates the object.
      ///
      /// SLAFMsg.Oper = SL_OBJOP_DELETE:
      ///     Object delete. The object's key is enough to delete the object.
      ///     Delete of a non-existant object is returned as success.
      /// </summary>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncDuplexStreamingCall<global::ServiceLayer.SLAFMsg, global::ServiceLayer.SLAFMsgRsp> SLAFOpStream(grpc::CallOptions options)
      {
        return CallInvoker.AsyncDuplexStreamingCall(__Method_SLAFOpStream, null, options);
      }
      /// <summary>Creates a new instance of client from given <c>ClientBaseConfiguration</c>.</summary>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected override SLAFClient NewInstance(ClientBaseConfiguration configuration)
      {
        return new SLAFClient(configuration);
      }
    }

    /// <summary>Creates service definition that can be registered with a server</summary>
    /// <param name="serviceImpl">An object implementing the server-side handling logic.</param>
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    public static grpc::ServerServiceDefinition BindService(SLAFBase serviceImpl)
    {
      return grpc::ServerServiceDefinition.CreateBuilder()
          .AddMethod(__Method_SLAFVrfRegOp, serviceImpl.SLAFVrfRegOp)
          .AddMethod(__Method_SLAFOp, serviceImpl.SLAFOp)
          .AddMethod(__Method_SLAFOpStream, serviceImpl.SLAFOpStream).Build();
    }

    /// <summary>Register service method with a service binder with or without implementation. Useful when customizing the service binding logic.
    /// Note: this method is part of an experimental API that can change or be removed without any prior notice.</summary>
    /// <param name="serviceBinder">Service methods will be bound by calling <c>AddMethod</c> on this object.</param>
    /// <param name="serviceImpl">An object implementing the server-side handling logic.</param>
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    public static void BindService(grpc::ServiceBinderBase serviceBinder, SLAFBase serviceImpl)
    {
      serviceBinder.AddMethod(__Method_SLAFVrfRegOp, serviceImpl == null ? null : new grpc::UnaryServerMethod<global::ServiceLayer.SLAFVrfRegMsg, global::ServiceLayer.SLAFVrfRegMsgRsp>(serviceImpl.SLAFVrfRegOp));
      serviceBinder.AddMethod(__Method_SLAFOp, serviceImpl == null ? null : new grpc::UnaryServerMethod<global::ServiceLayer.SLAFMsg, global::ServiceLayer.SLAFMsgRsp>(serviceImpl.SLAFOp));
      serviceBinder.AddMethod(__Method_SLAFOpStream, serviceImpl == null ? null : new grpc::DuplexStreamingServerMethod<global::ServiceLayer.SLAFMsg, global::ServiceLayer.SLAFMsgRsp>(serviceImpl.SLAFOpStream));
    }

  }
}
#endregion