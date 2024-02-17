import abc
import grpc

try:
    from feature_lib.slapi import serializers
    from feature_lib.slapi.sl_util import L2RouteUtil
    from feature_lib.slapi.sl_util import RouteUtil
    from feature_lib.slapi.sl_util import BDUtil
    from feature_lib.slapi.genpy import (
        sl_common_types_pb2,
        sl_global_pb2,
        sl_route_common_pb2,
        sl_route_ipv4_pb2,
        sl_route_ipv6_pb2,
        sl_mpls_pb2,
        sl_bfd_common_pb2,
        sl_bfd_ipv4_pb2,
        sl_bfd_ipv6_pb2,
        sl_interface_pb2,
        sl_l2_route_pb2,
        sl_common_types_pb2_grpc,
        sl_global_pb2_grpc,
        sl_route_ipv4_pb2_grpc,
        sl_route_ipv6_pb2_grpc,
        sl_mpls_pb2_grpc,
        sl_bfd_common_pb2_grpc,
        sl_bfd_ipv4_pb2_grpc,
        sl_bfd_ipv6_pb2_grpc,
        sl_interface_pb2_grpc,
        sl_l2_route_pb2_grpc,
    )
except ImportError:
    from . import serializers
    from .sl_util import L2RouteUtil
    from .sl_util import RouteUtil
    from .sl_util import BDUtil
    from genpy import (
        sl_common_types_pb2,
        sl_global_pb2,
        sl_route_common_pb2,
        sl_route_ipv4_pb2,
        sl_route_ipv6_pb2,
        sl_mpls_pb2,
        sl_bfd_common_pb2,
        sl_bfd_ipv4_pb2,
        sl_bfd_ipv6_pb2,
        sl_interface_pb2,
        sl_l2_route_pb2,
        sl_common_types_pb2_grpc,
        sl_global_pb2_grpc,
        sl_route_ipv4_pb2_grpc,
        sl_route_ipv6_pb2_grpc,
        sl_mpls_pb2_grpc,
        sl_bfd_common_pb2_grpc,
        sl_bfd_ipv4_pb2_grpc,
        sl_bfd_ipv6_pb2_grpc,
        sl_interface_pb2_grpc,
        sl_l2_route_pb2_grpc,
    )


class AbstractClient(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def route_global_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def route_global_stats_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def route_add(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def route_update(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def route_delete(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def route_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def route_get_stream(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def route_op_stream(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def vrf_registration_add(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def vrf_registration_delete(*args, **kwargs):
        pass

    @abc.abstractmethod
    def vrf_get(*args, **kwargs):
        pass

    @abc.abstractmethod
    def vrf_registration_eof(*args, **kwargs):
        pass

    @abc.abstractmethod
    def mpls_register_oper(*args, **kwargs):
        pass

    @abc.abstractmethod
    def mpls_unregister_oper(*args, **kwargs):
        pass

    @abc.abstractmethod
    def mpls_eof_oper(*args, **kwargs):
        pass

    @abc.abstractmethod
    def mpls_global_get(*args, **kwargs):
        pass

    @abc.abstractmethod
    def mpls_global_get_stats(*args, **kwargs):
        pass

    @abc.abstractmethod
    def label_block_add(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def label_block_delete(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def label_block_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def ilm_add(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def ilm_update(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def ilm_delete(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def ilm_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def ilm_get_stream(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def ilm_op_stream(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def global_bfd_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bfd_global_get_stats(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bfd_register_oper(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bfd_unregister_oper(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bfd_eof_oper(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bfd_add(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bfd_update(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bfd_delete(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bfd_get_notif(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bfd_session_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def global_init(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def global_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def intf_register_op(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def intf_unregister_op(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def intf_eof_oper(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def intf_global_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def intf_global_get_stats(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def intf_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def intf_get_notif(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def intf_subscribe(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def intf_unsubscribe(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def bd_reg_unreg_handle(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def l2route_get_notif(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def l2_route_handle(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def l3route_get_notif(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def l2_global_reg_unreg_handler(self, *args, **kwargs):
        pass

class GrpcClient(AbstractClient):
    TIMEOUT_SECONDS = 20 
    REGISTER_TIMEOUT_SECONDS = 120

    def __init__(self, host, port, channel_credentials=None):
        if channel_credentials is None:
            # Instantiate insecure channel object.
            self.channel = grpc.insecure_channel(str(host) + ":" + str(port))
        else:
            # Instantiate secure channel object.
            self.channel = grpc.secure_channel(str(host) + ":" + str(port),
                                                     channel_credentials)
        self._stubs = (
            # 0
            sl_route_ipv4_pb2_grpc.SLRoutev4OperStub(self.channel),
            # 1
            sl_route_ipv6_pb2_grpc.SLRoutev6OperStub(self.channel),
            # 2
            sl_global_pb2_grpc.SLGlobalStub(self.channel),
            # 3
            sl_mpls_pb2_grpc.SLMplsOperStub(self.channel),
            # 4
            sl_bfd_ipv4_pb2_grpc.SLBfdv4OperStub(self.channel),
            # 5
            sl_bfd_ipv6_pb2_grpc.SLBfdv6OperStub(self.channel),
            # 6
            sl_interface_pb2_grpc.SLInterfaceOperStub(self.channel),
            # 7
            sl_l2_route_pb2_grpc.SLL2OperStub(self.channel),
        )

    def route_global_get(self, af):
        """Global Get"""
        serializer = serializers.route_global_get_serializer()
        response = {
            4: self._stubs[0].SLRoutev4GlobalsGet,
            6: self._stubs[1].SLRoutev6GlobalsGet,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def route_global_stats_get(self, af):
        """Global Get"""
        serializer = serializers.route_global_stats_get_serializer()
        response = {
            4: self._stubs[0].SLRoutev4GlobalStatsGet,
            6: self._stubs[1].SLRoutev6GlobalStatsGet,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def route_add(self, route_info):
        """Add a route to RIB table."""
        serializer = serializers.route_serializer(route_info)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_ADD
        response = {
            4: self._stubs[0].SLRoutev4Op,
            6: self._stubs[1].SLRoutev6Op,
        }[route_info['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def route_update(self, route_info):
        """Update a route in RIB table."""
        serializer = serializers.route_serializer(route_info)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_UPDATE
        response = {
            4: self._stubs[0].SLRoutev4Op,
            6: self._stubs[1].SLRoutev6Op,
        }[route_info['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def route_delete(self, route_info):
        """Delete a route from RIB table."""
        serializer = serializers.route_serializer(route_info)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_DELETE
        for route in serializer.Routes:
            # Remove all `sl_path` objects since they are not required for
            # route delete.
            route.ClearField('PathList')
        response = {
            4: self._stubs[0].SLRoutev4Op,
            6: self._stubs[1].SLRoutev6Op,
        }[route_info['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def route_get(self, get_info):
        """Get route from RIB table."""
        serializer = serializers.route_get_serializer(get_info)
        response = {
            4: self._stubs[0].SLRoutev4Get,
            6: self._stubs[1].SLRoutev6Get,
        }[get_info['af']](serializer, 10*self.TIMEOUT_SECONDS)
        return response

    def route_get_stream(self, stream_info):
        """Get route from RIB table through stream."""
        func = {
            4: self._stubs[0].SLRoutev4GetStream,
            6: self._stubs[1].SLRoutev6GetStream,
        }[stream_info['af']]

        def serialize(route_info):
            serializer = serializers.route_get_serializer(route_info)
            return serializer

        # Use map to set operation
        serialized_itor = map(serialize, stream_info['iterator'])

        # Get iterator of responses
        responses = func(serialized_itor, 100*self.TIMEOUT_SECONDS)
        return responses

    def route_op_stream(self, stream_info, oper):
        """Add/update/delete entries in RIB as a stream."""
        func = {
            4: self._stubs[0].SLRoutev4OpStream,
            6: self._stubs[1].SLRoutev6OpStream,
        }[stream_info['af']]

        def serialize(route_info):
            serializer = serializers.route_serializer(route_info)
            serializer.Oper = oper
            return serializer

        # Use map to set operation
        serialized_itor = map(serialize, stream_info['iterator'])

        # Get iterator of responses
        responses = func(serialized_itor, 100*self.TIMEOUT_SECONDS)
        return responses


    def route_add_stream(self, stream_info):
        return self.route_op_stream(stream_info, 
                sl_common_types_pb2.SL_OBJOP_ADD)

    def route_update_stream(self, stream_info):
        return self.route_op_stream(stream_info, 
                sl_common_types_pb2.SL_OBJOP_UPDATE)

    def route_delete_stream(self, stream_info):
        return self.route_op_stream(stream_info, 
                sl_common_types_pb2.SL_OBJOP_DELETE)

    def vrf_registration_add(self, batch):
        """
        RIB VRF Register Add

        :param batch: dictionary passed to serializer
        :return: response: vrf registration add response
        """
        serializer = serializers.vrf_registration_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_REGOP_REGISTER
        response = {
            4: self._stubs[0].SLRoutev4VrfRegOp,
            6: self._stubs[1].SLRoutev6VrfRegOp,
        }[batch['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def vrf_registration_delete(self, batch):
        """
        RIB VRF Register Delete

        :param batch: dictionary passed to serializer
        :return: response: vrf registration add response
        """
        serializer = serializers.vrf_registration_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_REGOP_UNREGISTER
        response = {
            4: self._stubs[0].SLRoutev4VrfRegOp,
            6: self._stubs[1].SLRoutev6VrfRegOp,
        }[batch['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def vrf_get(self, get_info, stats):
        """Get VRF from RIB table."""
        serializer = serializers.global_vrf_get_serializer(get_info)
        if stats:
            response = {
                4: self._stubs[0].SLRoutev4VrfGetStats,
                6: self._stubs[1].SLRoutev6VrfGetStats,
            }[get_info['af']](serializer, self.TIMEOUT_SECONDS)
        else:
            response = {
                4: self._stubs[0].SLRoutev4VrfRegGet,
                6: self._stubs[1].SLRoutev6VrfRegGet,
            }[get_info['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def vrf_registration_eof(self, batch):
        """
        RIB VRF Register EOF

        :param batch: dictionary passed to serializer
        :return: response: vrf registration eof response
        """
        serializer = serializers.vrf_registration_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_REGOP_EOF
        response = {
            4: self._stubs[0].SLRoutev4VrfRegOp,
            6: self._stubs[1].SLRoutev6VrfRegOp,
        }[batch['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def mpls_register_oper(self, batch):
        """
        MPLS Register operation.

        :param batch: dictionary passed to serializer
        :return: response: mpls registration response
        """
        serializer = serializers.mpls_regop_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_REGOP_REGISTER
        response = self._stubs[3].SLMplsRegOp(serializer, self.REGISTER_TIMEOUT_SECONDS)
        return response

    def mpls_unregister_oper(self):
        """
        MPLS Unregister operation.

        :return: response: mpls registration response
        """
        serializer = serializers.mpls_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_UNREGISTER
        response = self._stubs[3].SLMplsRegOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def mpls_eof_oper(self):
        """
        MPLS EOF operation.

        :return: response: mpls registration response
        """
        serializer = serializers.mpls_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_EOF
        response = self._stubs[3].SLMplsRegOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def mpls_global_get(self):
        """
        MPLS global get operation.

        :return: response: mpls global get response
        """
        serializer = serializers.mpls_get_serializer()
        response = self._stubs[3].SLMplsGet(serializer, self.TIMEOUT_SECONDS)
        return response

    def mpls_global_get_stats(self):
        """
        MPLS get stats operation.

        :return: response: mpls global get response
        """
        serializer = serializers.mpls_get_serializer()
        response = self._stubs[3].SLMplsGetStats(serializer,
            self.TIMEOUT_SECONDS)
        return response

    def label_block_add(self, batch):
        """
        Add a Label Block.

        :param batch: dictionary passed to serializer
        :return: response: mpls block op response
        """
        serializer = serializers.label_block_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_ADD
        response = self._stubs[3].SLMplsLabelBlockOp(serializer,
                self.TIMEOUT_SECONDS)
        return response

    def label_block_delete(self, batch):
        """
        Delete a Label Block.

        :param batch: dictionary passed to serializer
        :return: response: mpls block op response
        """
        serializer = serializers.label_block_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_DELETE
        response = self._stubs[3].SLMplsLabelBlockOp(serializer,
                self.TIMEOUT_SECONDS)
        return response

    def label_block_get(self, get_info):
        """
        Get Label Block from table.

        :param batch: dictionary passed to serializer
        :return: response: mpls block get response
        """
        serializer = serializers.label_block_get_serializer(get_info)
        response = self._stubs[3].SLMplsLabelBlockGet(serializer,
             self.TIMEOUT_SECONDS)
        return response

    def ilm_add(self, ilm_info):
        """Add an ILM entry to LSD table."""
        serializer = serializers.ilm_serializer(ilm_info)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_ADD
        response = self._stubs[3].SLMplsIlmOp(serializer,
            self.TIMEOUT_SECONDS)
        return response

    def ilm_update(self, ilm_info):
        """Update an ILM entry to LSD table."""
        serializer = serializers.ilm_serializer(ilm_info)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_UPDATE
        response = self._stubs[3].SLMplsIlmOp(serializer,
            self.TIMEOUT_SECONDS)
        return response

    def ilm_delete(self, ilm_info):
        """Delete an ILM entry from LSD table."""
        serializer = serializers.ilm_serializer(ilm_info)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_DELETE
        response = self._stubs[3].SLMplsIlmOp(serializer,
            self.TIMEOUT_SECONDS)
        return response

    def ilm_get(self, get_info):
        """
        Get ILM from table.

        :param get_info: dictionary passed to serializer
        :return: response: mpls block get response
        """
        serializer = serializers.ilm_get_serializer(get_info)
        response = self._stubs[3].SLMplsIlmGet(serializer, 10*self.TIMEOUT_SECONDS)
        return response

    def ilm_get_stream(self, stream_info):
        """Get ILM table through stream."""
        func = self._stubs[3].SLMplsIlmGetStream

        def serialize(get_info):
            serializer = serializers.ilm_get_serializer(get_info)
            return serializer

        # Use map to set operation
        serialized_itor = map(serialize, stream_info['iterator'])

        # Get iterator of responses
        responses = func(serialized_itor, 100*self.TIMEOUT_SECONDS)
        return responses

    def ilm_op_stream(self, stream_info, oper):
        """Add/update/delete entries in SL as a bidir stream."""
        func = self._stubs[3].SLMplsIlmOpStream

        def serialize(ilm_info):
            serializer = serializers.ilm_serializer(ilm_info)
            serializer.Oper = oper
            return serializer

        # Use map to set operation
        serialized_itor = map(serialize, stream_info['iterator'])

        # Get iterator of responses
        responses = func(serialized_itor, 100*self.TIMEOUT_SECONDS)
        return responses

    def ilm_add_stream(self, stream_info):
        return self.ilm_op_stream(stream_info, 
                sl_common_types_pb2.SL_OBJOP_ADD)

    def ilm_update_stream(self, stream_info):
        return self.ilm_op_stream(stream_info, 
                sl_common_types_pb2.SL_OBJOP_UPDATE)

    def ilm_delete_stream(self, stream_info):
        return self.ilm_op_stream(stream_info, 
                sl_common_types_pb2.SL_OBJOP_DELETE)

    def global_bfd_get(self, af):
        """BFD Get"""
        serializer = serializers.bfd_get_serializer()
        response = {
            4: self._stubs[4].SLBfdv4Get,
            6: self._stubs[5].SLBfdv6Get,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def bfd_global_get_stats(self, af):
        """BFD Get Stats"""
        serializer = serializers.bfd_get_serializer()
        response = {
            4: self._stubs[4].SLBfdv4GetStats,
            6: self._stubs[5].SLBfdv6GetStats,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def bfd_register_oper(self, af):
        """BFD Register operation."""
        serializer = serializers.bfd_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_REGISTER
        response = {
            4: self._stubs[4].SLBfdv4RegOp,
            6: self._stubs[5].SLBfdv6RegOp,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def bfd_unregister_oper(self, af):
        """BFD UnRegister operation."""
        serializer = serializers.bfd_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_UNREGISTER
        response = {
            4: self._stubs[4].SLBfdv4RegOp,
            6: self._stubs[5].SLBfdv6RegOp,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def bfd_eof_oper(self, af):
        """BFD Register operation."""
        serializer = serializers.bfd_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_EOF
        response = {
            4: self._stubs[4].SLBfdv4RegOp,
            6: self._stubs[5].SLBfdv6RegOp,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def bfd_add(self, batch, next_hops, af):
        """Add a BFD Session."""
        serializer = serializers.bfd_serializer(batch, next_hops, af)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_ADD
        response = {
            4: self._stubs[4].SLBfdv4SessionOp,
            6: self._stubs[5].SLBfdv6SessionOp,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def bfd_update(self, batch, next_hops, af):
        """Update a BFD Session."""
        serializer = serializers.bfd_serializer(batch, next_hops, af)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_UPDATE
        response = {
            4: self._stubs[4].SLBfdv4SessionOp,
            6: self._stubs[5].SLBfdv6SessionOp,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def bfd_delete(self, batch, next_hops, af):
        """Delete a BFD Session."""
        serializer = serializers.bfd_serializer(batch, next_hops, af)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_DELETE
        response = {
            4: self._stubs[4].SLBfdv4SessionOp,
            6: self._stubs[5].SLBfdv6SessionOp,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response
 
    def bfd_get_notif(self, af):
        """BFD Get Notif"""
        serializer = serializers.bfd_get_notif_serializer()
        # Expect a stream of SLBfdv4Notif - XXX Use large timeout for now
        responses = {
            4: self._stubs[4].SLBfdv4GetNotifStream,
            6: self._stubs[5].SLBfdv6GetNotifStream,
        }[af](serializer, 3600*24*365)
        
        return responses

    def bfd_session_get(self, get_info, af):
        """Get BFD entries."""
        serializer = serializers.bfd_session_get_serializer(get_info, af)
        response = {
            4: self._stubs[4].SLBfdv4SessionGet,
            6: self._stubs[5].SLBfdv6SessionGet,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def global_init(self, g_params):
        """Global Init"""
        serializer = serializers.global_init_serializer(g_params)
        # Expect a stream of SLGlobalNotif - XXX Use large timeout for now
        return self._stubs[2].SLGlobalInitNotif(serializer, 3600*24*365)

    def global_get(self):
        """Global Get"""
        serializer = serializers.global_get_serializer()
        response = self._stubs[2].SLGlobalsGet(serializer,
            self.TIMEOUT_SECONDS)
        return response

    def intf_register_op(self):
        """Interface Register operation."""
        serializer = serializers.intf_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_REGISTER
        response = self._stubs[6].SLInterfaceGlobalsRegOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def intf_unregister_op(self):
        """Interface UnRegister operation."""
        serializer = serializers.intf_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_UNREGISTER
        response = self._stubs[6].SLInterfaceGlobalsRegOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def intf_eof_oper(self):
        """Interface Register operation."""
        serializer = serializers.intf_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_EOF
        response = self._stubs[6].SLInterfaceGlobalsRegOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def intf_global_get(self):
        """Interface Global Get operation."""
        serializer = serializers.intf_globals_get_serializer()
        response = self._stubs[6].SLInterfaceGlobalsGet(serializer, self.TIMEOUT_SECONDS)
        return response

    def intf_global_get_stats(self):
        """Interface Global Get Stats operation."""
        serializer = serializers.intf_globals_get_serializer()
        response = self._stubs[6].SLInterfaceGlobalsGetStats(serializer, self.TIMEOUT_SECONDS)
        return response

    def intf_get(self, get_info):
        """Get Interface entries."""
        serializer = serializers.intf_get_serializer(get_info)
        response = self._stubs[6].SLInterfaceGet(serializer, self.TIMEOUT_SECONDS)
        return response

    def intf_get_notif(self):
        """Interface Get Notif"""
        serializer = serializers.intf_get_notif_serializer()
        # Expect a stream of SLInterfaceNotif - XXX Use large timeout for now
        responses =  self._stubs[6].SLInterfaceGetNotifStream(serializer,
            3600*24*365)
        return responses

    def intf_subscribe(self, batch):
        """Subscribe on Interface."""
        serializer = serializers.intf_notif_op_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_NOTIFOP_ENABLE
        response = self._stubs[6].SLInterfaceNotifOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def intf_unsubscribe(self, batch):
        """Un-Subscribe on Interface."""
        serializer = serializers.intf_notif_op_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_NOTIFOP_DISABLE
        response = self._stubs[6].SLInterfaceNotifOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def bd_reg_unreg_handle(self, oper, count, bdRegOper):
        """BD Reg/Unreg."""
        bdprefix = 'bd'
        bdreg_msg = BDUtil.construct_SLL2BdRegMsg(oper, bdprefix, count, bdRegOper)
        BDUtil.print_SLL2BdRegMsg(bdreg_msg)
        # Invoke RPC
        response = self._stubs[7].SLL2BdRegOp(bdreg_msg, self.TIMEOUT_SECONDS)
        return response

    def l2_route_handle(self, oper, count, rtype, is_macip, g_bd, g_route_attrs):
        """L2 Route Oper."""
        route_msg = L2RouteUtil.construct_SLL2RouteMsg(oper, count, rtype, is_macip, g_bd,
                                                          g_route_attrs)
        L2RouteUtil.print_SLL2RouteMsg(route_msg)

        # Invoke RPC
        response = self._stubs[7].SLL2RouteOp(route_msg, self.TIMEOUT_SECONDS)
        return response

    def l2route_get_notif(self,  g_oper, BdAll, BdName):
        """L2 Route Get Notif"""
        # Construct input (currently sending interest for all Bds)
        request = L2RouteUtil.gen_l2route_get_notif_msg(g_oper, BdAll, BdName)

        # Expect a stream of SLL2RouteGetMsgRsp [Use large timeout]
        responses = self._stubs[7].SLL2GetNotifStream(request, 3600*24*365)
        return responses

    def l3route_get_notif(self, af):
        """L3 Route Get Notif"""

        # Expect a stream of SLRoutev4Notif / SLRoutev6Notif [Use large timeout]
        requests = RouteUtil.gen_l3route_get_notif_msg()
        return  {
            4: self._stubs[0].SLRoutev4GetNotifStream,
            6: self._stubs[1].SLRoutev6GetNotifStream,
        }[af](requests, 3600*24*365)

    def l2_global_reg_unreg_handler(self, oper, g_route_attrs):
        """L2 Global reg/unreg"""
        global_reg = L2RouteUtil.construct_SLL2RegMsg(oper, g_route_attrs)
        L2RouteUtil.print_SLL2RegMsg(global_reg)
        # Invoke RPC
        response = self._stubs[7].SLL2RegOp(global_reg, self.TIMEOUT_SECONDS)
        return response

    def l2_globals_get(self):
        parent_message = sl_l2_route_pb2.SLL2GlobalsGetMsg()
        response = self._stubs[7].SLL2GlobalsGet(parent_message, self.TIMEOUT_SECONDS)
        return response

    def l2_route_op_stream(self, oper, count, rtype, is_macip, bdAry, g_route_attrs):
        l2_route_op_msgs = L2RouteUtil.gen_l2_route_msgs(oper, count, rtype, is_macip, bdAry, g_route_attrs)

        responses = self._stubs[7].SLL2RouteOpStream(l2_route_op_msgs, 100*self.TIMEOUT_SECONDS)
        return responses
