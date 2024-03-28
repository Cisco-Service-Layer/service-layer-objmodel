// <auto-generated>
//     Generated by the protocol buffer compiler.  DO NOT EDIT!
//     source: sl_bgpls_topology.proto
// </auto-generated>
// Original file comments:
// @file
// @brief RPC proto file for BGP-LS Topology Subscription Service.
//
// ----------------------------------------------------------------
//  Copyright (c) 2024 by Cisco Systems, Inc.
//  All rights reserved.
// -----------------------------------------------------------------
//
//
//
// @defgroup BGP-LS Topology Subscription
// @brief BGP-LS Topology Subscription service definitions.
//
#pragma warning disable 0414, 1591
#region Designer generated code

using grpc = global::Grpc.Core;

namespace ServiceLayer {
  /// <summary>
  /// @defgroup SLBgplsTopoSubscription
  /// Defines RPC calls for subscribing to BGP-LS Topology updates.
  /// @{
  /// </summary>
  public static partial class SLBgplsTopoSubscription
  {
    static readonly string __ServiceName = "service_layer.SLBgplsTopoSubscription";

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
    static readonly grpc::Marshaller<global::ServiceLayer.SLBgplsTopoGetUpdMsg> __Marshaller_service_layer_SLBgplsTopoGetUpdMsg = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLBgplsTopoGetUpdMsg.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::ServiceLayer.SLBgplsTopoUpdMsg> __Marshaller_service_layer_SLBgplsTopoUpdMsg = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::ServiceLayer.SLBgplsTopoUpdMsg.Parser));

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Method<global::ServiceLayer.SLBgplsTopoGetUpdMsg, global::ServiceLayer.SLBgplsTopoUpdMsg> __Method_SLBgplsTopoGetUpdStream = new grpc::Method<global::ServiceLayer.SLBgplsTopoGetUpdMsg, global::ServiceLayer.SLBgplsTopoUpdMsg>(
        grpc::MethodType.DuplexStreaming,
        __ServiceName,
        "SLBgplsTopoGetUpdStream",
        __Marshaller_service_layer_SLBgplsTopoGetUpdMsg,
        __Marshaller_service_layer_SLBgplsTopoUpdMsg);

    /// <summary>Service descriptor</summary>
    public static global::Google.Protobuf.Reflection.ServiceDescriptor Descriptor
    {
      get { return global::ServiceLayer.SlBgplsTopologyReflection.Descriptor.Services[0]; }
    }

    /// <summary>Base class for server-side implementations of SLBgplsTopoSubscription</summary>
    [grpc::BindServiceMethod(typeof(SLBgplsTopoSubscription), "BindService")]
    public abstract partial class SLBgplsTopoSubscriptionBase
    {
      /// <summary>
      /// This call is used to get a stream of BGP-LS Topology updates.
      /// It can be used to get "push" information for BGP-LS
      /// adds/updates/deletes.
      ///
      /// The caller must maintain the GRPC channel as long as there is
      /// interest in BGP-LS Topology information.
      ///
      /// The call takes a stream of requests to get updates, with the information on filter
      /// to be applied while sending updates passed in the first request. The request stream
      /// is then only maintained to indicate the interest in BGP-LS Topology information.
      ///
      /// The success/failure of the request is relayed in the response as error status.
      /// If the request was successful, then the initial set of BGP-LS Topology information is sent
      /// as a stream containing a Start marker, any BGP-LS Topology if present, and an End Marker.
      /// The response stream will then be maintained to send subsequent updates and terminated only
      /// when the request stream is terminated.
      /// </summary>
      /// <param name="requestStream">Used for reading requests from the client.</param>
      /// <param name="responseStream">Used for sending responses back to the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>A task indicating completion of the handler.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::System.Threading.Tasks.Task SLBgplsTopoGetUpdStream(grpc::IAsyncStreamReader<global::ServiceLayer.SLBgplsTopoGetUpdMsg> requestStream, grpc::IServerStreamWriter<global::ServiceLayer.SLBgplsTopoUpdMsg> responseStream, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

    }

    /// <summary>Client for SLBgplsTopoSubscription</summary>
    public partial class SLBgplsTopoSubscriptionClient : grpc::ClientBase<SLBgplsTopoSubscriptionClient>
    {
      /// <summary>Creates a new client for SLBgplsTopoSubscription</summary>
      /// <param name="channel">The channel to use to make remote calls.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public SLBgplsTopoSubscriptionClient(grpc::ChannelBase channel) : base(channel)
      {
      }
      /// <summary>Creates a new client for SLBgplsTopoSubscription that uses a custom <c>CallInvoker</c>.</summary>
      /// <param name="callInvoker">The callInvoker to use to make remote calls.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public SLBgplsTopoSubscriptionClient(grpc::CallInvoker callInvoker) : base(callInvoker)
      {
      }
      /// <summary>Protected parameterless constructor to allow creation of test doubles.</summary>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected SLBgplsTopoSubscriptionClient() : base()
      {
      }
      /// <summary>Protected constructor to allow creation of configured clients.</summary>
      /// <param name="configuration">The client configuration.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected SLBgplsTopoSubscriptionClient(ClientBaseConfiguration configuration) : base(configuration)
      {
      }

      /// <summary>
      /// This call is used to get a stream of BGP-LS Topology updates.
      /// It can be used to get "push" information for BGP-LS
      /// adds/updates/deletes.
      ///
      /// The caller must maintain the GRPC channel as long as there is
      /// interest in BGP-LS Topology information.
      ///
      /// The call takes a stream of requests to get updates, with the information on filter
      /// to be applied while sending updates passed in the first request. The request stream
      /// is then only maintained to indicate the interest in BGP-LS Topology information.
      ///
      /// The success/failure of the request is relayed in the response as error status.
      /// If the request was successful, then the initial set of BGP-LS Topology information is sent
      /// as a stream containing a Start marker, any BGP-LS Topology if present, and an End Marker.
      /// The response stream will then be maintained to send subsequent updates and terminated only
      /// when the request stream is terminated.
      /// </summary>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncDuplexStreamingCall<global::ServiceLayer.SLBgplsTopoGetUpdMsg, global::ServiceLayer.SLBgplsTopoUpdMsg> SLBgplsTopoGetUpdStream(grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SLBgplsTopoGetUpdStream(new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// This call is used to get a stream of BGP-LS Topology updates.
      /// It can be used to get "push" information for BGP-LS
      /// adds/updates/deletes.
      ///
      /// The caller must maintain the GRPC channel as long as there is
      /// interest in BGP-LS Topology information.
      ///
      /// The call takes a stream of requests to get updates, with the information on filter
      /// to be applied while sending updates passed in the first request. The request stream
      /// is then only maintained to indicate the interest in BGP-LS Topology information.
      ///
      /// The success/failure of the request is relayed in the response as error status.
      /// If the request was successful, then the initial set of BGP-LS Topology information is sent
      /// as a stream containing a Start marker, any BGP-LS Topology if present, and an End Marker.
      /// The response stream will then be maintained to send subsequent updates and terminated only
      /// when the request stream is terminated.
      /// </summary>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncDuplexStreamingCall<global::ServiceLayer.SLBgplsTopoGetUpdMsg, global::ServiceLayer.SLBgplsTopoUpdMsg> SLBgplsTopoGetUpdStream(grpc::CallOptions options)
      {
        return CallInvoker.AsyncDuplexStreamingCall(__Method_SLBgplsTopoGetUpdStream, null, options);
      }
      /// <summary>Creates a new instance of client from given <c>ClientBaseConfiguration</c>.</summary>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected override SLBgplsTopoSubscriptionClient NewInstance(ClientBaseConfiguration configuration)
      {
        return new SLBgplsTopoSubscriptionClient(configuration);
      }
    }

    /// <summary>Creates service definition that can be registered with a server</summary>
    /// <param name="serviceImpl">An object implementing the server-side handling logic.</param>
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    public static grpc::ServerServiceDefinition BindService(SLBgplsTopoSubscriptionBase serviceImpl)
    {
      return grpc::ServerServiceDefinition.CreateBuilder()
          .AddMethod(__Method_SLBgplsTopoGetUpdStream, serviceImpl.SLBgplsTopoGetUpdStream).Build();
    }

    /// <summary>Register service method with a service binder with or without implementation. Useful when customizing the service binding logic.
    /// Note: this method is part of an experimental API that can change or be removed without any prior notice.</summary>
    /// <param name="serviceBinder">Service methods will be bound by calling <c>AddMethod</c> on this object.</param>
    /// <param name="serviceImpl">An object implementing the server-side handling logic.</param>
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    public static void BindService(grpc::ServiceBinderBase serviceBinder, SLBgplsTopoSubscriptionBase serviceImpl)
    {
      serviceBinder.AddMethod(__Method_SLBgplsTopoGetUpdStream, serviceImpl == null ? null : new grpc::DuplexStreamingServerMethod<global::ServiceLayer.SLBgplsTopoGetUpdMsg, global::ServiceLayer.SLBgplsTopoUpdMsg>(serviceImpl.SLBgplsTopoGetUpdStream));
    }

  }
}
#endregion
