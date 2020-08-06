# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import sl_mpls_pb2 as sl__mpls__pb2


class SLMplsOperStub(object):
    """@defgroup SLMpls
    @ingroup MPLS
    Defines RPCs for MPLS Registrations, label block reservations, and ILM entries
    manipulations.
    Clients Must register for MPLS operations e.g. Incoming Label Map operations.
    Once registered, a client Must reserve an MPLS label (dynamic allocation) 
    before using it as an incoming label map. 
    Labels are reserved in blocks through the block reservation operations.

    This file also defines RPC calls for adding, deleting, updating, and querying
    incoming label map entries (see RFC 3031)

    Incoming Label Map (ILM): A mapping from incoming labels to 
    corresponding NHLFEs. It is used when forwarding packets that
    arrive as labeled packets. 

    Next Hop Forwarding Entry (NHLE): An entry containing next-hop
    information and label manipulation instructions. This is also referred to
    as the ILM Path.

    @{
    @addtogroup SLMpls
    @{
    /;
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SLMplsRegOp = channel.unary_unary(
                '/service_layer.SLMplsOper/SLMplsRegOp',
                request_serializer=sl__mpls__pb2.SLMplsRegMsg.SerializeToString,
                response_deserializer=sl__mpls__pb2.SLMplsRegMsgRsp.FromString,
                )
        self.SLMplsGet = channel.unary_unary(
                '/service_layer.SLMplsOper/SLMplsGet',
                request_serializer=sl__mpls__pb2.SLMplsGetMsg.SerializeToString,
                response_deserializer=sl__mpls__pb2.SLMplsGetMsgRsp.FromString,
                )
        self.SLMplsGetStats = channel.unary_unary(
                '/service_layer.SLMplsOper/SLMplsGetStats',
                request_serializer=sl__mpls__pb2.SLMplsGetMsg.SerializeToString,
                response_deserializer=sl__mpls__pb2.SLMplsGetStatsMsgRsp.FromString,
                )
        self.SLMplsLabelBlockOp = channel.unary_unary(
                '/service_layer.SLMplsOper/SLMplsLabelBlockOp',
                request_serializer=sl__mpls__pb2.SLMplsLabelBlockMsg.SerializeToString,
                response_deserializer=sl__mpls__pb2.SLMplsLabelBlockMsgRsp.FromString,
                )
        self.SLMplsLabelBlockGet = channel.unary_unary(
                '/service_layer.SLMplsOper/SLMplsLabelBlockGet',
                request_serializer=sl__mpls__pb2.SLMplsLabelBlockGetMsg.SerializeToString,
                response_deserializer=sl__mpls__pb2.SLMplsLabelBlockGetMsgRsp.FromString,
                )
        self.SLMplsIlmOp = channel.unary_unary(
                '/service_layer.SLMplsOper/SLMplsIlmOp',
                request_serializer=sl__mpls__pb2.SLMplsIlmMsg.SerializeToString,
                response_deserializer=sl__mpls__pb2.SLMplsIlmMsgRsp.FromString,
                )
        self.SLMplsIlmGet = channel.unary_unary(
                '/service_layer.SLMplsOper/SLMplsIlmGet',
                request_serializer=sl__mpls__pb2.SLMplsIlmGetMsg.SerializeToString,
                response_deserializer=sl__mpls__pb2.SLMplsIlmGetMsgRsp.FromString,
                )
        self.SLMplsIlmOpStream = channel.stream_stream(
                '/service_layer.SLMplsOper/SLMplsIlmOpStream',
                request_serializer=sl__mpls__pb2.SLMplsIlmMsg.SerializeToString,
                response_deserializer=sl__mpls__pb2.SLMplsIlmMsgRsp.FromString,
                )
        self.SLMplsIlmGetStream = channel.stream_stream(
                '/service_layer.SLMplsOper/SLMplsIlmGetStream',
                request_serializer=sl__mpls__pb2.SLMplsIlmGetMsg.SerializeToString,
                response_deserializer=sl__mpls__pb2.SLMplsIlmGetMsgRsp.FromString,
                )


class SLMplsOperServicer(object):
    """@defgroup SLMpls
    @ingroup MPLS
    Defines RPCs for MPLS Registrations, label block reservations, and ILM entries
    manipulations.
    Clients Must register for MPLS operations e.g. Incoming Label Map operations.
    Once registered, a client Must reserve an MPLS label (dynamic allocation) 
    before using it as an incoming label map. 
    Labels are reserved in blocks through the block reservation operations.

    This file also defines RPC calls for adding, deleting, updating, and querying
    incoming label map entries (see RFC 3031)

    Incoming Label Map (ILM): A mapping from incoming labels to 
    corresponding NHLFEs. It is used when forwarding packets that
    arrive as labeled packets. 

    Next Hop Forwarding Entry (NHLE): An entry containing next-hop
    information and label manipulation instructions. This is also referred to
    as the ILM Path.

    @{
    @addtogroup SLMpls
    @{
    /;
    """

    def SLMplsRegOp(self, request, context):
        """
        MPLS Registration operations.


        SLMplsRegMsg.Oper = SL_REGOP_REGISTER.
        Global MPLS registration.
        A client Must Register BEFORE MPLS objects can be added/modified.

        SLMplsRegMsg.Oper = SL_REGOP_UNREGISTER.
        Global MPLS un-registration.
        This call is used to end all MPLS notifications and unregister any
        interest in MPLS object configuration.
        This call cleans up all MPLS objects previously requested.

        SLMplsRegMsg.Oper = SL_REGOP_EOF.
        MPLS End Of File.
        After Registration, the client is expected to send an EOF
        message to convey the end of replay of the client's known objects.
        This is especially useful under certain restart scenarios when the
        client and the server are trying to synchronize their MPLS objects.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLMplsGet(self, request, context):
        """Retrieve global MPLS info from the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLMplsGetStats(self, request, context):
        """Retrieve global MPLS Stats from the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLMplsLabelBlockOp(self, request, context):
        """
        MPLS Label Block operations


        SLMplsLabelBlockMsg.Oper = SL_OBJOP_ADD.
        Add a contiguous label block.
        Add request may fail if the full block cannot be allocated.

        SLMplsLabelBlockMsg.Oper = SL_OBJOP_DELETE.
        Delete a contiguous label block.
        Delete request may fail if the block is in use or the keys don't
        match the keys used on add.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLMplsLabelBlockGet(self, request, context):
        """Retrieve Label Block attributes.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLMplsIlmOp(self, request, context):
        """
        MPLS ILM operations


        SLMplsIlmMsg.Oper = SL_OBJOP_ADD:
        Add incoming label map entry.

        SLMplsIlmMsg.Oper = SL_OBJOP_UPDATE:
        Update incoming label map entry.

        SLMplsIlmMsg.Oper = SL_OBJOP_DELETE:
        Delete incoming label map entry.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLMplsIlmGet(self, request, context):
        """Retrieve MPLS ILM entry attributes.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLMplsIlmOpStream(self, request_iterator, context):
        """
        MPLS ILM stream operations


        SLMplsIlmMsg.Oper = SL_OBJOP_ADD:
        Add incoming label map entry.

        SLMplsIlmMsg.Oper = SL_OBJOP_UPDATE:
        Update incoming label map entry.

        SLMplsIlmMsg.Oper = SL_OBJOP_DELETE:
        Delete incoming label map entry.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SLMplsIlmGetStream(self, request_iterator, context):
        """Stream-Get of incoming label map
        @}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SLMplsOperServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SLMplsRegOp': grpc.unary_unary_rpc_method_handler(
                    servicer.SLMplsRegOp,
                    request_deserializer=sl__mpls__pb2.SLMplsRegMsg.FromString,
                    response_serializer=sl__mpls__pb2.SLMplsRegMsgRsp.SerializeToString,
            ),
            'SLMplsGet': grpc.unary_unary_rpc_method_handler(
                    servicer.SLMplsGet,
                    request_deserializer=sl__mpls__pb2.SLMplsGetMsg.FromString,
                    response_serializer=sl__mpls__pb2.SLMplsGetMsgRsp.SerializeToString,
            ),
            'SLMplsGetStats': grpc.unary_unary_rpc_method_handler(
                    servicer.SLMplsGetStats,
                    request_deserializer=sl__mpls__pb2.SLMplsGetMsg.FromString,
                    response_serializer=sl__mpls__pb2.SLMplsGetStatsMsgRsp.SerializeToString,
            ),
            'SLMplsLabelBlockOp': grpc.unary_unary_rpc_method_handler(
                    servicer.SLMplsLabelBlockOp,
                    request_deserializer=sl__mpls__pb2.SLMplsLabelBlockMsg.FromString,
                    response_serializer=sl__mpls__pb2.SLMplsLabelBlockMsgRsp.SerializeToString,
            ),
            'SLMplsLabelBlockGet': grpc.unary_unary_rpc_method_handler(
                    servicer.SLMplsLabelBlockGet,
                    request_deserializer=sl__mpls__pb2.SLMplsLabelBlockGetMsg.FromString,
                    response_serializer=sl__mpls__pb2.SLMplsLabelBlockGetMsgRsp.SerializeToString,
            ),
            'SLMplsIlmOp': grpc.unary_unary_rpc_method_handler(
                    servicer.SLMplsIlmOp,
                    request_deserializer=sl__mpls__pb2.SLMplsIlmMsg.FromString,
                    response_serializer=sl__mpls__pb2.SLMplsIlmMsgRsp.SerializeToString,
            ),
            'SLMplsIlmGet': grpc.unary_unary_rpc_method_handler(
                    servicer.SLMplsIlmGet,
                    request_deserializer=sl__mpls__pb2.SLMplsIlmGetMsg.FromString,
                    response_serializer=sl__mpls__pb2.SLMplsIlmGetMsgRsp.SerializeToString,
            ),
            'SLMplsIlmOpStream': grpc.stream_stream_rpc_method_handler(
                    servicer.SLMplsIlmOpStream,
                    request_deserializer=sl__mpls__pb2.SLMplsIlmMsg.FromString,
                    response_serializer=sl__mpls__pb2.SLMplsIlmMsgRsp.SerializeToString,
            ),
            'SLMplsIlmGetStream': grpc.stream_stream_rpc_method_handler(
                    servicer.SLMplsIlmGetStream,
                    request_deserializer=sl__mpls__pb2.SLMplsIlmGetMsg.FromString,
                    response_serializer=sl__mpls__pb2.SLMplsIlmGetMsgRsp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_layer.SLMplsOper', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SLMplsOper(object):
    """@defgroup SLMpls
    @ingroup MPLS
    Defines RPCs for MPLS Registrations, label block reservations, and ILM entries
    manipulations.
    Clients Must register for MPLS operations e.g. Incoming Label Map operations.
    Once registered, a client Must reserve an MPLS label (dynamic allocation) 
    before using it as an incoming label map. 
    Labels are reserved in blocks through the block reservation operations.

    This file also defines RPC calls for adding, deleting, updating, and querying
    incoming label map entries (see RFC 3031)

    Incoming Label Map (ILM): A mapping from incoming labels to 
    corresponding NHLFEs. It is used when forwarding packets that
    arrive as labeled packets. 

    Next Hop Forwarding Entry (NHLE): An entry containing next-hop
    information and label manipulation instructions. This is also referred to
    as the ILM Path.

    @{
    @addtogroup SLMpls
    @{
    /;
    """

    @staticmethod
    def SLMplsRegOp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLMplsOper/SLMplsRegOp',
            sl__mpls__pb2.SLMplsRegMsg.SerializeToString,
            sl__mpls__pb2.SLMplsRegMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLMplsGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLMplsOper/SLMplsGet',
            sl__mpls__pb2.SLMplsGetMsg.SerializeToString,
            sl__mpls__pb2.SLMplsGetMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLMplsGetStats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLMplsOper/SLMplsGetStats',
            sl__mpls__pb2.SLMplsGetMsg.SerializeToString,
            sl__mpls__pb2.SLMplsGetStatsMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLMplsLabelBlockOp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLMplsOper/SLMplsLabelBlockOp',
            sl__mpls__pb2.SLMplsLabelBlockMsg.SerializeToString,
            sl__mpls__pb2.SLMplsLabelBlockMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLMplsLabelBlockGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLMplsOper/SLMplsLabelBlockGet',
            sl__mpls__pb2.SLMplsLabelBlockGetMsg.SerializeToString,
            sl__mpls__pb2.SLMplsLabelBlockGetMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLMplsIlmOp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLMplsOper/SLMplsIlmOp',
            sl__mpls__pb2.SLMplsIlmMsg.SerializeToString,
            sl__mpls__pb2.SLMplsIlmMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLMplsIlmGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_layer.SLMplsOper/SLMplsIlmGet',
            sl__mpls__pb2.SLMplsIlmGetMsg.SerializeToString,
            sl__mpls__pb2.SLMplsIlmGetMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLMplsIlmOpStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/service_layer.SLMplsOper/SLMplsIlmOpStream',
            sl__mpls__pb2.SLMplsIlmMsg.SerializeToString,
            sl__mpls__pb2.SLMplsIlmMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SLMplsIlmGetStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/service_layer.SLMplsOper/SLMplsIlmGetStream',
            sl__mpls__pb2.SLMplsIlmGetMsg.SerializeToString,
            sl__mpls__pb2.SLMplsIlmGetMsgRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
