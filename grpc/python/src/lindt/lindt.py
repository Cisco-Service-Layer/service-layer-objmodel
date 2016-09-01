#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
import abc
import ipaddress

import serializers
from genpy import sl_common_types_pb2
from genpy import sl_global_pb2
from genpy import sl_route_ipv4_pb2
from genpy import sl_route_ipv6_pb2
from genpy import sl_mpls_pb2
from genpy import sl_bfd_common_pb2
from genpy import sl_bfd_ipv4_pb2
from genpy import sl_bfd_ipv6_pb2
from genpy import sl_interface_pb2


from grpc.beta import implementations

class Operation(object):
    ADD = 1
    UPDATE = 2
    DELETE = 3


class AbstractClient(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def global_route_get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def global_route_stats_get(self, *args, **kwargs):
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

class GrpcClient(AbstractClient):
    TIMEOUT_SECONDS = 20

    def __init__(self, host, port, channel_credentials=None):
        if channel_credentials is None:
            # Instantiate insecure channel object.
            channel = implementations.insecure_channel(host, port)
        else:
            # Instantiate secure channel object.
            channel = implementations.secure_channel(host, port,
                                                     channel_credentials)
        self._stubs = (
            # 0
            sl_route_ipv4_pb2.beta_create_SLRoutev4Oper_stub(channel),
            # 1
            sl_route_ipv6_pb2.beta_create_SLRoutev6Oper_stub(channel),
            # 2
            sl_global_pb2.beta_create_SLGlobal_stub(channel),
            # 3
            sl_mpls_pb2.beta_create_SLMplsOper_stub(channel),
            # 4
            sl_bfd_ipv4_pb2.beta_create_SLBfdv4Oper_stub(channel),
            # 5
            sl_bfd_ipv6_pb2.beta_create_SLBfdv6Oper_stub(channel),
            # 6
            sl_interface_pb2.beta_create_SLInterfaceOper_stub(channel),
        )

    def global_route_get(self, af):
        """Global Get"""
        serializer = serializers.global_route_get_serializer()
        response = {
            4: self._stubs[0].SLRoutev4GlobalsGet,
            6: self._stubs[1].SLRoutev6GlobalsGet,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response
    
    def global_route_stats_get(self, af):
        """Global Get"""
        serializer = serializers.global_route_stats_get_serializer()
        response = {
            4: self._stubs[0].SLRoutev4GlobalStatsGet,
            6: self._stubs[1].SLRoutev6GlobalStatsGet,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def route_add(self, batch, paths, next_hops):
        """Add a route to RIB table."""
        serializer, next, label = serializers.route_serializer(batch, paths, next_hops)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_ADD
        response = {
            4: self._stubs[0].SLRoutev4Op,
            6: self._stubs[1].SLRoutev6Op,
        }[batch['af']](serializer, self.TIMEOUT_SECONDS)
        return response, next, label

    def route_update(self, batch, paths, next_hops):
        """Update a route in RIB table."""
        serializer, next, label = serializers.route_serializer(batch, paths, next_hops)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_UPDATE
        response = {
            4: self._stubs[0].SLRoutev4Op,
            6: self._stubs[1].SLRoutev6Op,
        }[batch['af']](serializer, self.TIMEOUT_SECONDS)
        return response, next, label

    def route_delete(self, batch, paths, next_hops):
        """Delete a route from RIB table."""
        serializer, next, label = serializers.route_serializer(batch, paths, next_hops)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_DELETE
        for route in serializer.Routes:
            # Remove all `sl_path` objects since they are not required for
            # route delete.
            route.ClearField('PathList')
        response = {
            4: self._stubs[0].SLRoutev4Op,
            6: self._stubs[1].SLRoutev6Op,
        }[batch['af']](serializer, self.TIMEOUT_SECONDS)
        return response, next, label

    def route_get(self, get_info, af):
        """Get route from RIB table."""
        serializer = serializers.route_get_serializer(get_info, af)
        response = {
            4: self._stubs[0].SLRoutev4Get,
            6: self._stubs[1].SLRoutev6Get,
        }[af](serializer, 10*self.TIMEOUT_SECONDS)
        return response

    def route_get_stream(self, serialized_list, af, cback_func):
        """Get route from RIB table through stream."""
        func = {
            4: self._stubs[0].SLRoutev4GetStream,
            6: self._stubs[1].SLRoutev6GetStream,
        }[af]
        # Iterate over iterator
        count = 0
        #
        # The following func() call sends EOF as soon as we send the last item.
        responses = func(serialized_list, 100*self.TIMEOUT_SECONDS)
        try:
            for response in responses:
                error = cback_func(response, af)
                if not error:
                    print "Validation error"
                    return count, error
                count = count + 1
        except implementations.face.NetworkError as netErr:
            if netErr.details == "EOF":
                # Success case, we send EOF, Server reflects the EOF back
                return count, True
        except Exception as err:
            # Other side exited prematurely?
            print "Exception Received:", err
        return count, False

    def route_op_stream(self, serialized_list, af, cback_func):
        """Add/update/delete entries in RIB as a stream."""
        func = {
            4: self._stubs[0].SLRoutev4OpStream,
            6: self._stubs[1].SLRoutev6OpStream,
        }[af]
        # Iterate over 'serialized_list' iterator
        count = 0
        responses = func(serialized_list, 100*self.TIMEOUT_SECONDS)
        try:
            for response in responses:
                error = cback_func(response, af)
                if not error:
                    print "Validation error"
                    return count, error
                count = count + 1
        except implementations.face.NetworkError as netErr:
            if netErr.details == "EOF":
                # Success case, we send EOF, Server reflects the EOF back
                return count, True
        except Exception as err:
            # Other side exited prematurely?
            print "Exception Received:", err
        return count, False

    def vrf_registration_add(self, batch):
        """RIB VRF Register Add"""
        serializer = serializers.vrf_registration_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_REGOP_REGISTER
        response = {
            4: self._stubs[0].SLRoutev4VrfRegOp,
            6: self._stubs[1].SLRoutev6VrfRegOp,
        }[batch['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def vrf_registration_delete(self, batch):
        """RIB VRF Register Delete"""
        serializer = serializers.vrf_registration_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_REGOP_UNREGISTER
        response = {
            4: self._stubs[0].SLRoutev4VrfRegOp,
            6: self._stubs[1].SLRoutev6VrfRegOp,
        }[batch['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def vrf_get(self, get_info, af, stats):
        """Get VRF from RIB table."""
        serializer = serializers.global_vrf_get_serializer(get_info)
        if stats:
            response = {
                4: self._stubs[0].SLRoutev4VrfGetStats,
                6: self._stubs[1].SLRoutev6VrfGetStats,
            }[af](serializer, self.TIMEOUT_SECONDS)
        else:
            response = {
                4: self._stubs[0].SLRoutev4VrfRegGet,
                6: self._stubs[1].SLRoutev6VrfRegGet,
            }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def vrf_registration_eof(self, batch):
        """RIB VRF Register EOF"""
        serializer = serializers.vrf_registration_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_REGOP_EOF
        response = {
            4: self._stubs[0].SLRoutev4VrfRegOp,
            6: self._stubs[1].SLRoutev6VrfRegOp,
        }[batch['af']](serializer, self.TIMEOUT_SECONDS)
        return response

    def mpls_register_oper(self):
        """MPLS Register operation."""
        serializer = serializers.mpls_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_REGISTER
        response = self._stubs[3].SLMplsRegOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def mpls_unregister_oper(self):
        """MPLS UnRegister operation."""
        serializer = serializers.mpls_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_UNREGISTER
        response = self._stubs[3].SLMplsRegOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def mpls_eof_oper(self):
        """MPLS EOF operation."""
        serializer = serializers.mpls_regop_serializer()
        serializer.Oper = sl_common_types_pb2.SL_REGOP_EOF
        response = self._stubs[3].SLMplsRegOp(serializer, self.TIMEOUT_SECONDS)
        return response

    def mpls_global_get(self):
        """MPLS Get"""
        serializer = serializers.mpls_get_serializer()
        response = self._stubs[3].SLMplsGet(serializer, self.TIMEOUT_SECONDS)
        return response

    def mpls_global_get_stats(self):
        """MPLS Get Stats"""
        serializer = serializers.mpls_get_serializer()
        response = self._stubs[3].SLMplsGetStats(serializer,
            self.TIMEOUT_SECONDS)
        return response

    def label_block_add(self, batch):
        """Add a Label Block."""
        serializer = serializers.label_block_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_ADD
        response = self._stubs[3].SLMplsLabelBlockOp(serializer,
                self.TIMEOUT_SECONDS)
        return response

    def label_block_delete(self, batch):
        """Delete a Label Block."""
        serializer = serializers.label_block_serializer(batch)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_DELETE
        response = self._stubs[3].SLMplsLabelBlockOp(serializer,
                self.TIMEOUT_SECONDS)
        return response

    def label_block_get(self, get_info):
        """Get Label Block from table."""
        serializer = serializers.label_block_get_serializer(get_info)
        response = self._stubs[3].SLMplsLabelBlockGet(serializer,
             self.TIMEOUT_SECONDS)
        return response

    def ilm_add(self, batch, af, paths, next_hops):
        """Add an ILM entry to LSD table."""
        serializer, next  = serializers.ilm_serializer(batch,
            af, paths, next_hops)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_ADD
        response = self._stubs[3].SLMplsIlmOp(serializer,
            self.TIMEOUT_SECONDS)
        return response, next

    def ilm_update(self, batch, af, paths, next_hops):
        """Update an ILM entry to LSD table."""
        serializer, next  = serializers.ilm_serializer(batch,
            af, paths, next_hops)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_UPDATE
        response = self._stubs[3].SLMplsIlmOp(serializer,
            self.TIMEOUT_SECONDS)
        return response, next

    def ilm_delete(self, batch, af, paths, next_hops):
        """Delete an ILM entry from LSD table."""
        serializer, next  = serializers.ilm_serializer(batch,
            af, paths, next_hops)
        serializer.Oper = sl_common_types_pb2.SL_OBJOP_DELETE
        response = self._stubs[3].SLMplsIlmOp(serializer,
            self.TIMEOUT_SECONDS)
        return response, next

    def ilm_get(self, get_info):
        """Get ILM from table."""
        serializer = serializers.ilm_get_serializer(get_info)
        response = self._stubs[3].SLMplsIlmGet(serializer, 10*self.TIMEOUT_SECONDS)
        return response

    def ilm_get_stream(self, serialized_list, cback_func):
        """Get ILM table through stream."""
        func = self._stubs[3].SLMplsIlmGetStream
        # Iterate over iterator
        count = 0
        #
        # The following func() call sends EOF as soon as we send the last item.
        responses = func(serialized_list, 100*self.TIMEOUT_SECONDS)
        try:
            for response in responses:
                error = cback_func(response)
                if not error:
                    print "Validation error"
                    return count, error
                count = count + 1
        except implementations.face.NetworkError as netErr:
            if netErr.details == "EOF":
                # Success case, we send EOF, Server reflects the EOF back
                return count, True
        except Exception as err:
            # Other side exited prematurely?
            print "Exception Received:", err
        return count, False

    def ilm_op_stream(self, serialized_list, cback_func):
        """Add/update/delete entries in SL as a stream."""
        func = self._stubs[3].SLMplsIlmOpStream
        # Iterate over 'serialized_list' iterator
        count = 0
        responses = func(serialized_list, 100*self.TIMEOUT_SECONDS)
        try:
            for response in responses:
                error = cback_func(response)
                if not error:
                    print "Validation error"
                    return count, error
                count = count + 1
        except implementations.face.NetworkError as netErr:
            if netErr.details == "EOF":
                # Success case, we send EOF, Server reflects the EOF back
                return count, True
        except Exception as err:
            # Other side exited prematurely?
            print "Exception Received:", err
        return count, False

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
    
    def bfd_get_notif(self, cback_func, af):
        """BFD Get Notif"""
        serializer = serializers.bfd_get_notif_serializer()
        # Expect a stream of SLBfdv4Notif - XXX Use large timeout for now
        for response in {
            4: self._stubs[4].SLBfdv4GetNotifStream,
            6: self._stubs[5].SLBfdv6GetNotifStream,
        }[af](serializer, 3600*24*365):
            if not cback_func(response, af):
                break
        # Returns on exit
        return response

    def bfd_session_get(self, get_info, af):
        """Get BFD entries."""
        serializer = serializers.bfd_session_get_serializer(get_info, af)
        response = {
            4: self._stubs[4].SLBfdv4SessionGet,
            6: self._stubs[5].SLBfdv6SessionGet,
        }[af](serializer, self.TIMEOUT_SECONDS)
        return response

    def global_init(self, g_params, cback_func, event):
        """Global Init"""
        serializer = serializers.global_init_serializer(g_params)
        # Expect a stream of SLGlobalNotif - XXX Use large timeout for now
        for response in self._stubs[2].SLGlobalInitNotif(serializer,
            3600*24*365):
            if not cback_func(response, event):
                break
        # Returns on exit
        return response
    
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
    
    def intf_get_notif(self, cback_func):
        """Interface Get Notif"""
        serializer = serializers.intf_get_notif_serializer()
        # Expect a stream of SLInterfaceNotif - XXX Use large timeout for now
        for response in self._stubs[6].SLInterfaceGetNotifStream(serializer,
            3600*24*365):
            if not cback_func(response):
                break
        # Returns on exit
        return response
    
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
