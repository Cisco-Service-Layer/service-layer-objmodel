# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import sl_route_common_pb2 as sl__route__common__pb2
from . import sl_route_ipv6_pb2 as sl__route__ipv6__pb2


class SLRoutev6OperStub(object):
    """@defgroup SLRouteIPv6Oper
    @ingroup Route
    Defines RPC calls for IPv6 route changes and VRF registration.
    This service declares both the Vrf Registration, as well as adding, deleting
    and getting IPv6 routes.
    @{
    @addtogroup SLRouteIPv6Oper
    @{
    ;
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SLRoutev6GlobalsGet = channel.unary_unary(
                '/service_layer.SLRoutev6Oper/SLRoutev6GlobalsGet',
                request_serializer=sl__route__common__pb2.SLRouteGlobalsGetMsg.SerializeToString,
                response_deserializer=sl__route__common__pb2.SLRouteGlobalsGetMsgRsp.FromString,
                )
        self.SLRoutev6GlobalStatsGet = channel.unary_unary(
                '/service_layer.SLRoutev6Oper/SLRoutev6GlobalStatsGet',
                request_serializer=sl__route__common__pb2.SLRouteGlobalStatsGetMsg.SerializeToString,
                response_deserializer=sl__route__common__pb2.SLRouteGlobalStatsGetMsgRsp.FromString,
                )
        self.SLRoutev6VrfRegOp = channel.unary_unary(
                '/service_layer.SLRoutev6Oper/SLRoutev6VrfRegOp',
                request_serializer=sl__route__common__pb2.SLVrfRegMsg.SerializeToString,
                response_deserializer=sl__route__common__pb2.SLVrfRegMsgRsp.FromString,
                )
        self.SLRoutev6VrfRegGet = channel.unary_unary(
                '/service_layer.SLRoutev6Oper/SLRoutev6VrfRegGet',
                request_serializer=sl__route__common__pb2.SLVrfRegGetMsg.SerializeToString,
                response_deserializer=sl__route__common__pb2.SLVrfRegGetMsgRsp.FromString,
                )
        self.SLRoutev6VrfGetStats = channel.unary_unary(
                '/service_layer.SLRoutev6Oper/SLRoutev6VrfGetStats',
                request_serializer=sl__route__common__pb2.SLVrfRegGetMsg.SerializeToString,
                response_deserializer=sl__route__common__pb2.SLVRFGetStatsMsgRsp.FromString,
                )
        self.SLRoutev6Op = channel.unary_unary(
                '/service_layer.SLRoutev6Oper/SLRoutev6Op',
                request_serializer=sl__route__ipv6__pb2.SLRoutev6Msg.SerializeToString,
                response_deserializer=sl__route__ipv6__pb2.SLRoutev6MsgRsp.FromString,
                )
        self.SLRoutev6Get = channel.unary_unary(
                '/service_layer.SLRoutev6Oper/SLRoutev6Get',
                request_serializer=sl__route__ipv6__pb2.SLRoutev6GetMsg.SerializeToString,
                response_deserializer=sl__route__ipv6__pb2.SLRoutev6GetMsgRsp.FromString,
                )
        self.SLRoutev6OpStream = channel.stream_stream(
                '/service_layer.SLRoutev6Oper/SLRoutev6OpStream',
                request_serializer=sl__route__ipv6__pb2.SLRoutev6Msg.SerializeToString,
                response_deserializer=sl__route__ipv6__pb2.SLRoutev6MsgRsp.FromString,
                )
        self.SLRoutev6GetStream = channel.stream_stream(
                '/service_layer.SLRoutev6Oper/SLRoutev6GetStream',
                request_serializer=sl__route__ipv6__pb2.SLRoutev6GetMsg.SerializeToString,
                response_deserializer=sl__route__ipv6__pb2.SLRoutev6GetMsgRsp.FromString,
                )
        self.SLRoutev6GetNotifStream = channel.stream_stream(
                '/service_layer.SLRoutev6Oper/SLRoutev6GetNotifStream',
                request_serializer=sl__route__common__pb2.SLRouteGetNotifMsg.SerializeToString,
                response_deserializer=sl__route__ipv6__pb2.SLRoutev6Notif.FromString,
                )


class SLRoutev6OperServicer(object):
    """@defgroup SLRouteIPv6Oper
    @ingroup Route
    Defines RPC calls for IPv6 route changes and VRF registration.
    This service declares both the Vrf Registration, as well as adding, deleting
    and getting IPv6 routes.
    @{
    @addtogroup SLRouteIPv6Oper
    @{
    ;
    """

    def SLRoutev6GlobalsGet(self, request, context):
        """
        Global Route operations


        Used to retrieve Global Route information
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLRoutev6GlobalStatsGet(self, request, context):
        """Used to retrieve Global Route Stats
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLRoutev6VrfRegOp(self, request, context):
        """
        VRF registration operations


        SLVrfRegMsg.Oper = SL_REGOP_REGISTER:
        VRF registration: Sends a list of VRF registration messages
        and expects a list of registration responses.
        A client Must Register a VRF BEFORE routes can be added/modified in
        the associated VRF.

        SLVrfRegMsg.Oper = SL_REGOP_UNREGISTER:
        VRF Un-registeration: Sends a list of VRF un-registration messages
        and expects a list of un-registration responses.
        This can be used to convey that the client is no longer interested
        in this VRF. All previously installed routes would be lost.

        SLVrfRegMsg.Oper = SL_REGOP_EOF:
        VRF End Of File message.
        After Registration, the client is expected to send an EOF
        message to convey the end of replay of the client's known objects.
        This is especially useful under certain restart scenarios when the
        client and the server are trying to synchronize their Routes.

        The VRF registration operations can be used by the client to
        synchronize routes with the device. When the client re-registers the VRF
        with the server using SL_REGOP_REGISTER, server marks routes as stale.
        Client then must reprogram routes it is interested in.
        When client sends SL_REGOP_EOF, any routes not reprogrammed
        are removed from the device.

        The client must perform all operations (VRF registration, routes)
        from a single execution context.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLRoutev6VrfRegGet(self, request, context):
        """VRF get. Used to retrieve VRF attributes from the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLRoutev6VrfGetStats(self, request, context):
        """Used to retrieve VRF Stats from the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLRoutev6Op(self, request, context):
        """
        Route operations


        SLRoutev6Msg.Oper = SL_OBJOP_ADD:
        Route add. Fails if the route already exists.

        SLRoutev6Msg.Oper = SL_OBJOP_UPDATE:
        Route update. Creates or updates the route.

        SLRoutev6Msg.Oper = SL_OBJOP_DELETE:
        Route delete. The route path is not necessary to delete the route.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLRoutev6Get(self, request, context):
        """Retrieves route attributes.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLRoutev6OpStream(self, request_iterator, context):
        """
        Stream Route operations


        SLRoutev6Msg.Oper = SL_OBJOP_ADD:
        Route add. Fails if the route already exists.

        SLRoutev6Msg.Oper = SL_OBJOP_UPDATE:
        Route update. Creates or updates the route.

        SLRoutev6Msg.Oper = SL_OBJOP_DELETE:
        Route delete. The route path is not necessary to delete the route.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLRoutev6GetStream(self, request_iterator, context):
        """Retrieves route attributes.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLRoutev6GetNotifStream(self, request_iterator, context):
        """
        Route Redistribution Operations


        This call is used to get a stream of route notifications.
        It can be used to get "push" notifications for route
        adds/updates/deletes.
        The caller must maintain the GRPC channel as long as there is
        interest in route notifications.

        The call takes a stream of per-VRF notification requests.
        The success/failure of the notification request is relayed in the
        SLRouteNotifStatus followed by a Start marker, any routes if present,
        and an End Marker.


        @}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SLRoutev6OperServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SLRoutev6GlobalsGet': grpc.unary_unary_rpc_method_handler(
                    servicer.SLRoutev6GlobalsGet,
                    request_deserializer=sl__route__common__pb2.SLRouteGlobalsGetMsg.FromString,
                    response_serializer=sl__route__common__pb2.SLRouteGlobalsGetMsgRsp.SerializeToString,
            ),
            'SLRoutev6GlobalStatsGet': grpc.unary_unary_rpc_method_handler(
                    servicer.SLRoutev6GlobalStatsGet,
                    request_deserializer=sl__route__common__pb2.SLRouteGlobalStatsGetMsg.FromString,
                    response_serializer=sl__route__common__pb2.SLRouteGlobalStatsGetMsgRsp.SerializeToString,
            ),
            'SLRoutev6VrfRegOp': grpc.unary_unary_rpc_method_handler(
                    servicer.SLRoutev6VrfRegOp,
                    request_deserializer=sl__route__common__pb2.SLVrfRegMsg.FromString,
                    response_serializer=sl__route__common__pb2.SLVrfRegMsgRsp.SerializeToString,
            ),
            'SLRoutev6VrfRegGet': grpc.unary_unary_rpc_method_handler(
                    servicer.SLRoutev6VrfRegGet,
                    request_deserializer=sl__route__common__pb2.SLVrfRegGetMsg.FromString,
                    response_serializer=sl__route__common__pb2.SLVrfRegGetMsgRsp.SerializeToString,
            ),
            'SLRoutev6VrfGetStats': grpc.unary_unary_rpc_method_handler(
                    servicer.SLRoutev6VrfGetStats,
                    request_deserializer=sl__route__common__pb2.SLVrfRegGetMsg.FromString,
                    response_serializer=sl__route__common__pb2.SLVRFGetStatsMsgRsp.SerializeToString,
            ),
            'SLRoutev6Op': grpc.unary_unary_rpc_method_handler(
                    servicer.SLRoutev6Op,
                    request_deserializer=sl__route__ipv6__pb2.SLRoutev6Msg.FromString,
                    response_serializer=sl__route__ipv6__pb2.SLRoutev6MsgRsp.SerializeToString,
            ),
            'SLRoutev6Get': grpc.unary_unary_rpc_method_handler(
                    servicer.SLRoutev6Get,
                    request_deserializer=sl__route__ipv6__pb2.SLRoutev6GetMsg.FromString,
                    response_serializer=sl__route__ipv6__pb2.SLRoutev6GetMsgRsp.SerializeToString,
            ),
            'SLRoutev6OpStream': grpc.stream_stream_rpc_method_handler(
                    servicer.SLRoutev6OpStream,
                    request_deserializer=sl__route__ipv6__pb2.SLRoutev6Msg.FromString,
                    response_serializer=sl__route__ipv6__pb2.SLRoutev6MsgRsp.SerializeToString,
            ),
            'SLRoutev6GetStream': grpc.stream_stream_rpc_method_handler(
                    servicer.SLRoutev6GetStream,
                    request_deserializer=sl__route__ipv6__pb2.SLRoutev6GetMsg.FromString,
                    response_serializer=sl__route__ipv6__pb2.SLRoutev6GetMsgRsp.SerializeToString,
            ),
            'SLRoutev6GetNotifStream': grpc.stream_stream_rpc_method_handler(
                    servicer.SLRoutev6GetNotifStream,
                    request_deserializer=sl__route__common__pb2.SLRouteGetNotifMsg.FromString,
                    response_serializer=sl__route__ipv6__pb2.SLRoutev6Notif.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_layer.SLRoutev6Oper', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SLRoutev6Oper(object):
    """@defgroup SLRouteIPv6Oper
    @ingroup Route
    Defines RPC calls for IPv6 route changes and VRF registration.
    This service declares both the Vrf Registration, as well as adding, deleting
    and getting IPv6 routes.
    @{
    @addtogroup SLRouteIPv6Oper
    @{
    ;
    """

    @staticmethod
    def SLRoutev6GlobalsGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLRoutev6Oper/SLRoutev6GlobalsGet',
            sl__route__common__pb2.SLRouteGlobalsGetMsg.SerializeToString,
            sl__route__common__pb2.SLRouteGlobalsGetMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLRoutev6GlobalStatsGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLRoutev6Oper/SLRoutev6GlobalStatsGet',
            sl__route__common__pb2.SLRouteGlobalStatsGetMsg.SerializeToString,
            sl__route__common__pb2.SLRouteGlobalStatsGetMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLRoutev6VrfRegOp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLRoutev6Oper/SLRoutev6VrfRegOp',
            sl__route__common__pb2.SLVrfRegMsg.SerializeToString,
            sl__route__common__pb2.SLVrfRegMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLRoutev6VrfRegGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLRoutev6Oper/SLRoutev6VrfRegGet',
            sl__route__common__pb2.SLVrfRegGetMsg.SerializeToString,
            sl__route__common__pb2.SLVrfRegGetMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLRoutev6VrfGetStats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLRoutev6Oper/SLRoutev6VrfGetStats',
            sl__route__common__pb2.SLVrfRegGetMsg.SerializeToString,
            sl__route__common__pb2.SLVRFGetStatsMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLRoutev6Op(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLRoutev6Oper/SLRoutev6Op',
            sl__route__ipv6__pb2.SLRoutev6Msg.SerializeToString,
            sl__route__ipv6__pb2.SLRoutev6MsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLRoutev6Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLRoutev6Oper/SLRoutev6Get',
            sl__route__ipv6__pb2.SLRoutev6GetMsg.SerializeToString,
            sl__route__ipv6__pb2.SLRoutev6GetMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLRoutev6OpStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/service_layer.SLRoutev6Oper/SLRoutev6OpStream',
            sl__route__ipv6__pb2.SLRoutev6Msg.SerializeToString,
            sl__route__ipv6__pb2.SLRoutev6MsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLRoutev6GetStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/service_layer.SLRoutev6Oper/SLRoutev6GetStream',
            sl__route__ipv6__pb2.SLRoutev6GetMsg.SerializeToString,
            sl__route__ipv6__pb2.SLRoutev6GetMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLRoutev6GetNotifStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/service_layer.SLRoutev6Oper/SLRoutev6GetNotifStream',
            sl__route__common__pb2.SLRouteGetNotifMsg.SerializeToString,
            sl__route__ipv6__pb2.SLRoutev6Notif.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
