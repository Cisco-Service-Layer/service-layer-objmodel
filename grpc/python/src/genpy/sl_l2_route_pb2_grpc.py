# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import sl_l2_route_pb2 as sl__l2__route__pb2


class SLL2OperStub(object):
    """@defgroup SLRouteL2Oper
    @ingroup L2Route
    Defines RPC calls for L2 route changes and Bridge-Domain (BD) registration.
    This service declares calls for adding, deleting, updating and getting
    L2 routes.
    @{
    @addtogroup SLRouteL2Oper
    @{
    ;
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SLL2GlobalsGet = channel.unary_unary(
                '/service_layer.SLL2Oper/SLL2GlobalsGet',
                request_serializer=sl__l2__route__pb2.SLL2GlobalsGetMsg.SerializeToString,
                response_deserializer=sl__l2__route__pb2.SLL2GlobalsGetMsgRsp.FromString,
                )
        self.SLL2RegOp = channel.unary_unary(
                '/service_layer.SLL2Oper/SLL2RegOp',
                request_serializer=sl__l2__route__pb2.SLL2RegMsg.SerializeToString,
                response_deserializer=sl__l2__route__pb2.SLL2RegMsgRsp.FromString,
                )
        self.SLL2BdRegOp = channel.unary_unary(
                '/service_layer.SLL2Oper/SLL2BdRegOp',
                request_serializer=sl__l2__route__pb2.SLL2BdRegMsg.SerializeToString,
                response_deserializer=sl__l2__route__pb2.SLL2BdRegMsgRsp.FromString,
                )
        self.SLL2RouteOp = channel.unary_unary(
                '/service_layer.SLL2Oper/SLL2RouteOp',
                request_serializer=sl__l2__route__pb2.SLL2RouteMsg.SerializeToString,
                response_deserializer=sl__l2__route__pb2.SLL2RouteMsgRsp.FromString,
                )
        self.SLL2RouteOpStream = channel.stream_stream(
                '/service_layer.SLL2Oper/SLL2RouteOpStream',
                request_serializer=sl__l2__route__pb2.SLL2RouteMsg.SerializeToString,
                response_deserializer=sl__l2__route__pb2.SLL2RouteMsgRsp.FromString,
                )
        self.SLL2GetNotifStream = channel.stream_stream(
                '/service_layer.SLL2Oper/SLL2GetNotifStream',
                request_serializer=sl__l2__route__pb2.SLL2GetNotifMsg.SerializeToString,
                response_deserializer=sl__l2__route__pb2.SLL2Notif.FromString,
                )


class SLL2OperServicer(object):
    """@defgroup SLRouteL2Oper
    @ingroup L2Route
    Defines RPC calls for L2 route changes and Bridge-Domain (BD) registration.
    This service declares calls for adding, deleting, updating and getting
    L2 routes.
    @{
    @addtogroup SLRouteL2Oper
    @{
    ;
    """

    def SLL2GlobalsGet(self, request, context):
        """
        Global L2 route operations


        Used to retrieve global L2 info from the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLL2RegOp(self, request, context):
        """
        L2 Registration Operations


        SLL2RegMsg.Oper = SL_REGOP_REGISTER:
        Global L2 registration.
        A client Must Register BEFORE sending BD registration messages
        (to add/update/delete routes) or BEFORE requesting for L2 route
        notifications.

        SLL2RegMsg.Oper = SL_REGOP_UNREGISTER:
        Global L2 un-registration.
        This call is used to convey that the client is no longer
        interested in programming L2 routes and in receiving L2 route
        notifications. All programmed L2 routes will be deleted on the
        server and the server will stop sending L2 route notifications.

        SLL2RegMsg.Oper = SL_REGOP_EOF:
        Global L2 End Of File message.
        After Registration, the client is expected to send an EOF
        message to convey the end of replay of the client's known
        objects and to convey the end of requests for L2 route
        notifications.
        This is especially useful under certain restart scenarios when the
        client and the server are trying to synchronize their routes.

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLL2BdRegOp(self, request, context):
        """
        L2 Bridge-Domain (BD) Registration Operations


        SLL2BdRegMsg.Oper = SL_REGOP_REGISTER:
        BD registration: Sends a list of BD registration messages and
        expects a list of registration responses.
        A client Must Register a BD BEFORE L2 Routes can be added/modified
        in that BD.

        SLL2BdRegMsg.Oper = SL_REGOP_UNREGISTER:
        BD un-registration: Sends a list of BD un-registration messages
        and expects a list of un-registration responses.
        This can be used to convey that the client is no longer
        interested in programming routes in this BD. All installed L2
        routes will be removed.

        SLL2BdRegMsg.Oper = SL_REGOP_EOF:
        BD End Of File message.
        After Registration, the client is expected to send an EOF
        message to convey the end of replay of the client's known objects
        in that BD.
        This is especially useful under certain restart scenarios when the
        client and the server are trying to synchronize their routes.

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLL2RouteOp(self, request, context):
        """
        L2 Route Operations


        SLL2RouteMsg.Oper = SL_OBJOP_ADD:
        Route add. Fails if the route already exists.

        SLL2RouteMsg.Oper = SL_OBJOP_UPDATE:
        Route update. Creates or updates the route.

        SLL2RouteMsg.Oper = SL_OBJOP_DELETE:
        Route delete. The route path is not necessary to delete the route.

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLL2RouteOpStream(self, request_iterator, context):
        """
        L2 Stream Route Operations


        Stream adds/updates/deletes of L2 Routes.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLL2GetNotifStream(self, request_iterator, context):
        """
        L2 Route Redistribution Operations


        This call is used to get a stream of BD state and route notifications.
        It can be used to get "push" notifications for route
        adds/updates/deletes.
        The caller must maintain the GRPC channel as long as there is
        interest in route notifications.

        The call takes 3 types of notification requests:
        1. Request for BD state notifications only (pass only Oper and
        Correlator).
        2. Request for BD state and Route notifications in all BDs.
        3. Request for Route notifications per-BD.
        This should be sent after requesting for BD state notifications
        and after receiving BD-ready notification.

        The success/failure of the notification request is relayed in the
        SLL2NotifStatusMsg followed by a Start marker, any routes if present,
        and an End Marker.

        After all requests are sent, client should send GetNotifEof = TRUE.

        @}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SLL2OperServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SLL2GlobalsGet': grpc.unary_unary_rpc_method_handler(
                    servicer.SLL2GlobalsGet,
                    request_deserializer=sl__l2__route__pb2.SLL2GlobalsGetMsg.FromString,
                    response_serializer=sl__l2__route__pb2.SLL2GlobalsGetMsgRsp.SerializeToString,
            ),
            'SLL2RegOp': grpc.unary_unary_rpc_method_handler(
                    servicer.SLL2RegOp,
                    request_deserializer=sl__l2__route__pb2.SLL2RegMsg.FromString,
                    response_serializer=sl__l2__route__pb2.SLL2RegMsgRsp.SerializeToString,
            ),
            'SLL2BdRegOp': grpc.unary_unary_rpc_method_handler(
                    servicer.SLL2BdRegOp,
                    request_deserializer=sl__l2__route__pb2.SLL2BdRegMsg.FromString,
                    response_serializer=sl__l2__route__pb2.SLL2BdRegMsgRsp.SerializeToString,
            ),
            'SLL2RouteOp': grpc.unary_unary_rpc_method_handler(
                    servicer.SLL2RouteOp,
                    request_deserializer=sl__l2__route__pb2.SLL2RouteMsg.FromString,
                    response_serializer=sl__l2__route__pb2.SLL2RouteMsgRsp.SerializeToString,
            ),
            'SLL2RouteOpStream': grpc.stream_stream_rpc_method_handler(
                    servicer.SLL2RouteOpStream,
                    request_deserializer=sl__l2__route__pb2.SLL2RouteMsg.FromString,
                    response_serializer=sl__l2__route__pb2.SLL2RouteMsgRsp.SerializeToString,
            ),
            'SLL2GetNotifStream': grpc.stream_stream_rpc_method_handler(
                    servicer.SLL2GetNotifStream,
                    request_deserializer=sl__l2__route__pb2.SLL2GetNotifMsg.FromString,
                    response_serializer=sl__l2__route__pb2.SLL2Notif.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_layer.SLL2Oper', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SLL2Oper(object):
    """@defgroup SLRouteL2Oper
    @ingroup L2Route
    Defines RPC calls for L2 route changes and Bridge-Domain (BD) registration.
    This service declares calls for adding, deleting, updating and getting
    L2 routes.
    @{
    @addtogroup SLRouteL2Oper
    @{
    ;
    """

    @staticmethod
    def SLL2GlobalsGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLL2Oper/SLL2GlobalsGet',
            sl__l2__route__pb2.SLL2GlobalsGetMsg.SerializeToString,
            sl__l2__route__pb2.SLL2GlobalsGetMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLL2RegOp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLL2Oper/SLL2RegOp',
            sl__l2__route__pb2.SLL2RegMsg.SerializeToString,
            sl__l2__route__pb2.SLL2RegMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLL2BdRegOp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLL2Oper/SLL2BdRegOp',
            sl__l2__route__pb2.SLL2BdRegMsg.SerializeToString,
            sl__l2__route__pb2.SLL2BdRegMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLL2RouteOp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLL2Oper/SLL2RouteOp',
            sl__l2__route__pb2.SLL2RouteMsg.SerializeToString,
            sl__l2__route__pb2.SLL2RouteMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLL2RouteOpStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/service_layer.SLL2Oper/SLL2RouteOpStream',
            sl__l2__route__pb2.SLL2RouteMsg.SerializeToString,
            sl__l2__route__pb2.SLL2RouteMsgRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLL2GetNotifStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/service_layer.SLL2Oper/SLL2GetNotifStream',
            sl__l2__route__pb2.SLL2GetNotifMsg.SerializeToString,
            sl__l2__route__pb2.SLL2Notif.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
