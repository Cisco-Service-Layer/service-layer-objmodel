# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import sl_global_pb2 as sl__global__pb2


class SLGlobalStub(object):
    """@defgroup SLGlobal
    @ingroup Common
    Global Initialization and Notifications.
    The following RPCs are used in global initialization and capability queries.
    @{
    @addtogroup SLGlobal
    @{
    /;
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SLGlobalInitNotif = channel.unary_stream(
                '/service_layer.SLGlobal/SLGlobalInitNotif',
                request_serializer=sl__global__pb2.SLInitMsg.SerializeToString,
                response_deserializer=sl__global__pb2.SLGlobalNotif.FromString,
                )
        self.SLGlobalsGet = channel.unary_unary(
                '/service_layer.SLGlobal/SLGlobalsGet',
                request_serializer=sl__global__pb2.SLGlobalsGetMsg.SerializeToString,
                response_deserializer=sl__global__pb2.SLGlobalsGetMsgRsp.FromString,
                )


class SLGlobalServicer(object):
    """@defgroup SLGlobal
    @ingroup Common
    Global Initialization and Notifications.
    The following RPCs are used in global initialization and capability queries.
    @{
    @addtogroup SLGlobal
    @{
    /;
    """

    def SLGlobalInitNotif(self, request, context):
        """Initialize the connection, and setup a notification channel.
        This MUST be the first call to setup the Service Layer connection.

        The caller MUST maintain the notification channel to be able to
        communicate with the server.
        If this channel is not properly established and maintained, all other
        RPC requests are rejected.

        The caller must send its version information as part of the SLInitMsg
        message. The server will reply with SL_GLOBAL_EVENT_TYPE_VERSION
        that tells the caller whether he can proceed or not.
        Refer to message SLGlobalNotif below for further details.

        After the version handshake, the notification channel is used for
        "push" event notifications, such as:
        - SLGlobalNotif.EventType = SL_GLOBAL_EVENT_TYPE_HEARTBEAT
        heartbeat notification messages are sent to the client on
        a periodic basis.
        Refer to SLGlobalNotif definition for further info.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLGlobalsGet(self, request, context):
        """Get platform specific globals
        @}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SLGlobalServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SLGlobalInitNotif': grpc.unary_stream_rpc_method_handler(
                    servicer.SLGlobalInitNotif,
                    request_deserializer=sl__global__pb2.SLInitMsg.FromString,
                    response_serializer=sl__global__pb2.SLGlobalNotif.SerializeToString,
            ),
            'SLGlobalsGet': grpc.unary_unary_rpc_method_handler(
                    servicer.SLGlobalsGet,
                    request_deserializer=sl__global__pb2.SLGlobalsGetMsg.FromString,
                    response_serializer=sl__global__pb2.SLGlobalsGetMsgRsp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_layer.SLGlobal', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SLGlobal(object):
    """@defgroup SLGlobal
    @ingroup Common
    Global Initialization and Notifications.
    The following RPCs are used in global initialization and capability queries.
    @{
    @addtogroup SLGlobal
    @{
    /;
    """

    @staticmethod
    def SLGlobalInitNotif(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/service_layer.SLGlobal/SLGlobalInitNotif',
            sl__global__pb2.SLInitMsg.SerializeToString,
            sl__global__pb2.SLGlobalNotif.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLGlobalsGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLGlobal/SLGlobalsGet',
            sl__global__pb2.SLGlobalsGetMsg.SerializeToString,
            sl__global__pb2.SLGlobalsGetMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
