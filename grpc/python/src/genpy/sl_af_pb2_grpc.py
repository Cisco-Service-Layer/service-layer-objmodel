# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import sl_af_pb2 as sl__af__pb2


class SLAFStub(object):
    """@defgroup SLAF
    @ingroup Common
    SL-API messages for a address family.
    Defines SL-API operations service.
    @{
    ;

    This API supports programming the device by multiple clients.

    If there are multiple clients intending to program the network
    element using this API, the clients initiating a programming or get
    RPC MUST pass a gRPC-context metadata identifying itself.
    The client application MUST set the gRPC metadata key
    named "iosxr-slapi-clientid" with a numeric string holding a
    number between 0 and 65535.

    Each client application MUST use a unique client ID identifying itself
    that is seperate from other clients programming the server. If there
    are multiple instances of the client application, then each such
    instance MUST be uniquely idenified.

    If "iosxr-slapi-clientid" gRPC metadata is missing, server assumes
    a default client id of 0 for that RPC invocation and associates
    objects programmed by that RPC with the default client id of 0.

    The co-ordination of the ClientId amongst these instances is outside
    the scope of this specification.

    Clients MUST not change their identity for their lifetime - such as
    RPC disconnects, process restarts or software update.

    SL-API stores the objects programmed by clients and preserves them across
    RPC disconnects, client restarts and server gRPC process restarts. As such
    if a client application or instance is no longer needed, the client
    MUST remove all its programming from the server before it is disabled
    or removed.

    The route redistribution and notifications are scoped to the RPC
    and as such do not require a client ID.

    @addtogroup SLAF
    @{
    ;
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SLAFVrfRegOp = channel.unary_unary(
                '/service_layer.SLAF/SLAFVrfRegOp',
                request_serializer=sl__af__pb2.SLAFVrfRegMsg.SerializeToString,
                response_deserializer=sl__af__pb2.SLAFVrfRegMsgRsp.FromString,
                )
        self.SLAFOp = channel.unary_unary(
                '/service_layer.SLAF/SLAFOp',
                request_serializer=sl__af__pb2.SLAFMsg.SerializeToString,
                response_deserializer=sl__af__pb2.SLAFMsgRsp.FromString,
                )
        self.SLAFOpStream = channel.stream_stream(
                '/service_layer.SLAF/SLAFOpStream',
                request_serializer=sl__af__pb2.SLAFMsg.SerializeToString,
                response_deserializer=sl__af__pb2.SLAFMsgRsp.FromString,
                )


class SLAFServicer(object):
    """@defgroup SLAF
    @ingroup Common
    SL-API messages for a address family.
    Defines SL-API operations service.
    @{
    ;

    This API supports programming the device by multiple clients.

    If there are multiple clients intending to program the network
    element using this API, the clients initiating a programming or get
    RPC MUST pass a gRPC-context metadata identifying itself.
    The client application MUST set the gRPC metadata key
    named "iosxr-slapi-clientid" with a numeric string holding a
    number between 0 and 65535.

    Each client application MUST use a unique client ID identifying itself
    that is seperate from other clients programming the server. If there
    are multiple instances of the client application, then each such
    instance MUST be uniquely idenified.

    If "iosxr-slapi-clientid" gRPC metadata is missing, server assumes
    a default client id of 0 for that RPC invocation and associates
    objects programmed by that RPC with the default client id of 0.

    The co-ordination of the ClientId amongst these instances is outside
    the scope of this specification.

    Clients MUST not change their identity for their lifetime - such as
    RPC disconnects, process restarts or software update.

    SL-API stores the objects programmed by clients and preserves them across
    RPC disconnects, client restarts and server gRPC process restarts. As such
    if a client application or instance is no longer needed, the client
    MUST remove all its programming from the server before it is disabled
    or removed.

    The route redistribution and notifications are scoped to the RPC
    and as such do not require a client ID.

    @addtogroup SLAF
    @{
    ;
    """

    def SLAFVrfRegOp(self, request, context):
        """
        RPCs for object programming and access. Supported objects are
        IP Routes, MPLS Labels, and Path Group objects and Policy
        Forwarding Entries.

        A Path Group object created by one client can be referenced by
        any other object (e.g. IP Route and MPLS label object) created by
        ANY other client.

        Only the client that created the object (IP/MPLS, Policy Forwarding
        Entry and Path Group included) can manipulate that object.


        VRF registration operations. The client MUST register with
        the corresponding VRF table before programming objects in that table.

        SLAFVrfRegMsg.Oper = SL_REGOP_REGISTER:
        VRF table registration: Sends a list of VRF table registration
        messages and expects a list of registration responses.
        A client Must Register a VRF table BEFORE objects can be
        added/modified in the associated VRF table.

        SLAFVrfRegMsg.Oper = SL_REGOP_UNREGISTER:
        VRF table Un-registration: Sends a list of VRF table un-registration
        messages and expects a list of un-registration responses.
        This can be used to convey that the client is no longer interested
        in these VRF tables. All previously installed objects would be
        remove.

        SLAFVrfRegMsg.Oper = SL_REGOP_EOF:
        VRF table End Of File message.
        After Registration, the client is expected to send an EOF
        message to convey the end of replay of the client's known objects.
        This is especially useful under certain restart scenarios when the
        client and the server are trying to synchronize their objects.

        The VRF table registration operations can be used by the client to
        synchronize objects with the device. When the client re-registers the
        VRF table with the server using SL_REGOP_REGISTER, server marks
        objects in that table as stale.
        Client then MUST reprogram objects it is interested in.
        When client sends SL_REGOP_EOF, any objects not reprogrammed
        are removed from the device. This feature can be turned
        off by setting SLVrfReg.NoMarking flag to True.

        The client MUST perform all operations (VRF registration, objects)
        from a single execution context.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLAFOp(self, request, context):
        """
        Route, MPLS label and Path operations.


        SLAFMsg.Oper = SL_OBJOP_ADD:
        Object add. Fails if the objects already exists and is not stale.
        First ADD operation on a stale object is allowed and the object
        is no longer considered stale.

        SLAFMsg.Oper = SL_OBJOP_UPDATE:
        Object update. Creates or updates the objects.

        SLAFMsg.Oper = SL_OBJOP_DELETE:
        Object delete. The object's key is enough to delete the object.
        Delete of a non-existant object is returned as success.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLAFOpStream(self, request_iterator, context):
        """
        Stream object operations


        SLAFMsg.Oper = SL_OBJOP_ADD:
        Object add. Fails if the objects already exists and is not stale.
        First ADD operation on a stale object is allowed and the object
        is no longer considered stale.

        SLAFMsg.Oper = SL_OBJOP_UPDATE:
        Object update. Creates or updates the object.

        SLAFMsg.Oper = SL_OBJOP_DELETE:
        Object delete. The object's key is enough to delete the object.
        Delete of a non-existant object is returned as success.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SLAFServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SLAFVrfRegOp': grpc.unary_unary_rpc_method_handler(
                    servicer.SLAFVrfRegOp,
                    request_deserializer=sl__af__pb2.SLAFVrfRegMsg.FromString,
                    response_serializer=sl__af__pb2.SLAFVrfRegMsgRsp.SerializeToString,
            ),
            'SLAFOp': grpc.unary_unary_rpc_method_handler(
                    servicer.SLAFOp,
                    request_deserializer=sl__af__pb2.SLAFMsg.FromString,
                    response_serializer=sl__af__pb2.SLAFMsgRsp.SerializeToString,
            ),
            'SLAFOpStream': grpc.stream_stream_rpc_method_handler(
                    servicer.SLAFOpStream,
                    request_deserializer=sl__af__pb2.SLAFMsg.FromString,
                    response_serializer=sl__af__pb2.SLAFMsgRsp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_layer.SLAF', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SLAF(object):
    """@defgroup SLAF
    @ingroup Common
    SL-API messages for a address family.
    Defines SL-API operations service.
    @{
    ;

    This API supports programming the device by multiple clients.

    If there are multiple clients intending to program the network
    element using this API, the clients initiating a programming or get
    RPC MUST pass a gRPC-context metadata identifying itself.
    The client application MUST set the gRPC metadata key
    named "iosxr-slapi-clientid" with a numeric string holding a
    number between 0 and 65535.

    Each client application MUST use a unique client ID identifying itself
    that is seperate from other clients programming the server. If there
    are multiple instances of the client application, then each such
    instance MUST be uniquely idenified.

    If "iosxr-slapi-clientid" gRPC metadata is missing, server assumes
    a default client id of 0 for that RPC invocation and associates
    objects programmed by that RPC with the default client id of 0.

    The co-ordination of the ClientId amongst these instances is outside
    the scope of this specification.

    Clients MUST not change their identity for their lifetime - such as
    RPC disconnects, process restarts or software update.

    SL-API stores the objects programmed by clients and preserves them across
    RPC disconnects, client restarts and server gRPC process restarts. As such
    if a client application or instance is no longer needed, the client
    MUST remove all its programming from the server before it is disabled
    or removed.

    The route redistribution and notifications are scoped to the RPC
    and as such do not require a client ID.

    @addtogroup SLAF
    @{
    ;
    """

    @staticmethod
    def SLAFVrfRegOp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLAF/SLAFVrfRegOp',
            sl__af__pb2.SLAFVrfRegMsg.SerializeToString,
            sl__af__pb2.SLAFVrfRegMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLAFOp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLAF/SLAFOp',
            sl__af__pb2.SLAFMsg.SerializeToString,
            sl__af__pb2.SLAFMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLAFOpStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/service_layer.SLAF/SLAFOpStream',
            sl__af__pb2.SLAFMsg.SerializeToString,
            sl__af__pb2.SLAFMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
