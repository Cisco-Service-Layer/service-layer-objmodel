#
# Copyright (c) 2016 by cisco Systems, Inc.
# All rights reserved.
#
import abc
import os
import ipaddress

from . import serializers
from binascii import hexlify, unhexlify
import time
import struct

from genpy import sl_common_types_pb2
from genpy import sl_global_pb2
from genpy import sl_route_common_pb2
from genpy import sl_route_ipv4_pb2
from genpy import sl_route_ipv6_pb2
from genpy import sl_mpls_pb2
from genpy import sl_bfd_common_pb2
from genpy import sl_bfd_ipv4_pb2
from genpy import sl_bfd_ipv6_pb2
from genpy import sl_interface_pb2
from genpy import sl_l2_route_pb2
from genpy import sl_common_types_pb2_grpc
from genpy import sl_global_pb2_grpc
from genpy import sl_route_ipv4_pb2_grpc
from genpy import sl_route_ipv6_pb2_grpc
from genpy import sl_mpls_pb2_grpc
from genpy import sl_bfd_common_pb2_grpc
from genpy import sl_bfd_ipv4_pb2_grpc
from genpy import sl_bfd_ipv6_pb2_grpc
from genpy import sl_interface_pb2_grpc
from genpy import sl_l2_route_pb2_grpc

import grpc
from grpc.framework.interfaces.face.face import NetworkError

def byte_to_mac_str(mac):
    num = 2
    mac_split = [ str[start:start+num] for start in range(0, len(str), num) ]
    result = ''
    for substr in mac_split:
        result = result + elem + ':'
    return result[:-1]

class Operation(object):
    ADD = 1
    UPDATE = 2
    DELETE = 3

class AbstractClient(object, metaclass=abc.ABCMeta):
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

class Route_Util:

    def print_SLL2RegMsg(self, global_msg):
        print((str(global_msg) + "\n"))

    def print_SLL2RouteMsg(self, route_msg):
        print((str(route_msg) + "\n"))

    def construct_SLRouteGetNotifMsg(self, seqno, vrf_name, src_proto, src_proto_tag):
        parent_message = sl_route_common_pb2.SLRouteGetNotifMsg()

        parent_message.Oper = sl_common_types_pb2.SL_NOTIFOP_ENABLE
        parent_message.Correlator = seqno
        parent_message.VrfName = vrf_name
        parent_message.SrcProto = src_proto
        parent_message.SrcProtoTag = src_proto_tag
        return parent_message

    def construct_SLL2GetNotifMsg(self, g_oper, BdAll, BdName):
        g_oper = getattr(sl_common_types_pb2, g_oper)

        parent_message = sl_l2_route_pb2.SLL2GetNotifMsg()
        parent_message.Oper = g_oper

        parent_message.Correlator = 1
        parent_message.BdAll = True
        parent_message.GetNotifEof = False

        if (BdAll):
            parent_message.BdAll = True
        else:
            parent_message.BdName = BdName

        return parent_message

    def construct_SLL2RouteNh(self, g_route_attrs):
        g_encap = getattr(sl_common_types_pb2, g_route_attrs["g_encap"])

        parent_message = sl_l2_route_pb2.SLL2RouteNh()
        parent_message.NhType = g_route_attrs["g_nh_type"]

        if parent_message.NhType == 1:
            # Either interface name or handle (not both) must be present if
            # interface nexthop type selected
            if "g_nh_intf_name" in g_route_attrs:
                parent_message.NhInterface.Name = g_route_attrs["g_nh_intf_name"]
            else:
                parent_message.NhInterface.Handle = g_route_attrs["g_nh_intf_handle"]
        elif parent_message.NhType == 2:
            # IP manipulation
            ip_list = []*1
            for ip in ipaddress.ip_network(g_route_attrs["g_nexthop"][0], strict = False):
                ip_list.append(int(ipaddress.IPv4Address(ip)))

            parent_message.NhOverlay.OverlayNhIp.V4Address = ip_list[0]
            parent_message.NhOverlay.OverlayNhEncap = g_encap
            parent_message.NhOverlay.OverlayNhLabel = g_route_attrs["g_label"]
            # Using a single L3VNI for now
            l3_list = []
            l3_list.append(g_route_attrs["g_l3vni"]) # Single L3VNI for vxlan
            parent_message.NhOverlay.OverlayNhL3Label.extend(l3_list)
            parent_message.NhOverlay.OverlayNhRouterMac = unhexlify(g_route_attrs["g_rmac"].replace(':', ''))

        return parent_message

    def construct_SLL2MacRoute(self, is_macip, ip, mac, g_route_attrs):
        parent_message = sl_l2_route_pb2.SLL2MacRoute()

        if is_macip == True:
            parent_message.RouteKey.IpAddress.V4Address = ip

        parent_message.RouteKey.MacAddress = unhexlify((mac.replace(':', '')))
        parent_message.SequenceNum = 1

        # Construct NH (single next hop for now)
        nh = self.construct_SLL2RouteNh(g_route_attrs)
        message = []
        message.append(nh)
        parent_message.NextHopList.extend(message)
        parent_message.MacEsi.Esi = unhexlify(g_route_attrs["g_esi"])
        return parent_message

    def construct_SLL2ImetRoute(self, ip, g_route_attrs):
        parent_message = sl_l2_route_pb2.SLL2ImetRoute()

        parent_message.RouteKey.EthTagId = 0
        parent_message.RouteKey.IpAddress.V4Address = int(ipaddress.ip_address('1.2.3.4'))
        parent_message.EncapType = sl_common_types_pb2.SL_ENCAP_VXLAN
        parent_message.Label = g_route_attrs["g_label"]
        # For now only ipV4 tunnelId, modify hardcoded PMSI tun type
        parent_message.TunnelType = 6
        parent_message.TunnelIdLength = 4

        ipstr = '2.3.4.5'
        parent_message.TunnelIdValue = unhexlify(ipstr.replace('.',''))
        return parent_message

    def construct_SLL2Route(self, rtype, is_macip, ip, mac, g_bd, g_route_attrs):
        parent_message = sl_l2_route_pb2.SLL2Route()

        parent_message.BdName = g_bd
        parent_message.Type = rtype

        if rtype == sl_l2_route_pb2.SL_L2_ROUTE_MAC:
            # Invoke mac/mac-ip msg construct API
            mac_route = self.construct_SLL2MacRoute(is_macip, ip, mac, g_route_attrs)
            # Above is not iterable
            parent_message.MacRoute.CopyFrom(mac_route)
        else:
            # Invoke imet msg construct API
            imet_route = self.construct_SLL2ImetRoute(ip, g_route_attrs)
            parent_message.ImetRoute.CopyFrom(imet_route)
        return parent_message

    # SLL2RouteMsg
    def construct_SLL2RouteMsg(self, oper, count, rtype, is_macip, g_bd, g_route_attrs):
        parent_message = sl_l2_route_pb2.SLL2RouteMsg()
        parent_message.Correlator = 1
        parent_message.Oper = oper

        # IP manipulation
        ip_list = []*count
        i = 0
        for ip in ipaddress.ip_network(g_route_attrs["g_ip"][0], strict = False):
            ip_list.append(int(ipaddress.IPv4Address(ip)))

        message = []
        g_mac = g_route_attrs["g_mac"]
        # Multiple MAC/MAC-IP/IMET case
        if count > 1:
            index = 0
            while count > 0:
                route = self.construct_SLL2Route(rtype, is_macip,
                                                 ip_list[index], g_mac[index],
                                                 g_bd, g_route_attrs)
                message.append(route)
                parent_message.Routes.extend(message)
                index = index + 1
                count = count - 1

        elif count == 1:
            # Single MAC/MAC-IP/IMET case (won't use g_mac for IMET)
            route = self.construct_SLL2Route(rtype, is_macip, ip_list[0],
                                                g_mac[0], g_bd, g_route_attrs)
            message.append(route)
            parent_message.Routes.extend(message)
        return parent_message

    def validate_l2route_response(self, response):
        if response.Correlator != 1:
            return False

        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
            return True
        elif (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
            response.StatusSummary.Status):
            print("Batch Error code 0x%x" %(response.StatusSummary.Status))
            for result in response.Results:
                print("Error code for oper [%d] is 0x%x" % (result.Oper,
                        result.ErrStatus.Status))
                print("Failed route key: bd[%s], type[%d], mac[%s], ip[%s]" % (result.RouteKey.BdName, result.RouteKey.Type, 
                        byte_to_mac_str(result.RouteKey.Event.MacKey.MacAddress),
                        ipaddress.IPv4Address(result.RouteKey.Event.MacKey.IpAddress.V4Address)))
        else:
            print("Batch Error code 0x%x" %(response.StatusSummary.Status))
        return False

    def construct_SLL2RegMsg(self, oper, g_route_attrs):

        parent_message = sl_l2_route_pb2.SLL2RegMsg()

        if oper == 'SL_REGOP_REGISTER':
            parent_message.Oper = sl_common_types_pb2.SL_REGOP_REGISTER
        elif oper == 'SL_REGOP_UNREGISTER':
            parent_message.Oper = sl_common_types_pb2.SL_REGOP_UNREGISTER
        else:
            parent_message.Oper = sl_common_types_pb2.SL_REGOP_EOF

        parent_message.AdminDistance = g_route_attrs["adminDistance"]
        parent_message.PurgeIntervalSeconds = g_route_attrs["purgeTime"]
        return parent_message

class BD_Util:
    def print_SLL2BdRegMsg(self, bdreg_msg):
        print((str(bdreg_msg) + "\n"))

    def construct_SLL2BdRegMsg(self, oper, bdprefix, count, bdRegOper):
        messages = []

        parent_message = sl_l2_route_pb2.SLL2BdRegMsg()

        if oper in bdRegOper:
            if oper == 'SL_REGOP_REGISTER':
                parent_message.Oper = sl_common_types_pb2.SL_REGOP_REGISTER
            elif oper == 'SL_REGOP_UNREGISTER':
                parent_message.Oper = sl_common_types_pb2.SL_REGOP_UNREGISTER
            else:
                parent_message.Oper = sl_common_types_pb2.SL_REGOP_EOF
            # Repeated SLL2BdReg will be empty
            if oper == 'SL_REGOP_EOF':
                return parent_message
        while count >= 0:
            messages.append(bdprefix + str(count))
            count  = count - 1
        parent_message.BdRegName.extend(messages)

        return parent_message

    def validate_bdreg_response(self, response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
            return True
        # Error cases
        # SOME ERROR
        elif (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
            response.StatusSummary.Status):
            print("Batch Error code 0x%x" %(response.StatusSummary.Status))
            for result in response.Results:
                print("Error code for %s is 0x%x" % (result.BdName, result.ErrStatus.Status))
            return False
        else:
            # Grpc ERROR
            print("Batch Error code 0x%x" %(response.StatusSummary.Status))
            return False

class GrpcClient(AbstractClient):
    TIMEOUT_SECONDS = 20

    def __init__(self, host, port, channel_credentials=None):
        if channel_credentials is None:
            # Instantiate insecure channel object.
            channel = grpc.insecure_channel(str(host) + ":" + str(port))
        else:
            # Instantiate secure channel object.
            channel = grpc.secure_channel(str(host) + ":" + str(port),
                                                     channel_credentials)
        self._stubs = (
            # 0
            sl_route_ipv4_pb2_grpc.SLRoutev4OperStub(channel),
            # 1
            sl_route_ipv6_pb2_grpc.SLRoutev6OperStub(channel),
            # 2
            sl_global_pb2_grpc.SLGlobalStub(channel),
            # 3
            sl_mpls_pb2_grpc.SLMplsOperStub(channel),
            # 4
            sl_bfd_ipv4_pb2_grpc.SLBfdv4OperStub(channel),
            # 5
            sl_bfd_ipv6_pb2_grpc.SLBfdv6OperStub(channel),
            # 6
            sl_interface_pb2_grpc.SLInterfaceOperStub(channel),
            # 7
            sl_l2_route_pb2_grpc.SLL2OperStub(channel),
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
                    print("Validation error")
                    return count, error
                count = count + 1
        except NetworkError as netErr:
            if netErr.details == "EOF":
                # Success case, we send EOF, Server reflects the EOF back
                return count, True
        except Exception as err:
            # Other side exited (Python3 GRPC returns a different exception)
            if "details" in dir(err) and err.details == "EOF":
                return count, True
            # Other side exited (Python GRPC 1.7.0, Protoc 3.5.1 returns different exception)
            if ("_state" in dir(err) and "details" in dir(err._state) and 
                    err._state.details == "EOF".encode()):
                return count, True
            print(("Exception Received:", str(err)))
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
                    print("Validation error")
                    return count, error
                count = count + 1
        except NetworkError as netErr:
            if netErr.details == "EOF":
                # Success case, we send EOF, Server reflects the EOF back
                return count, True
        except Exception as err:
            # Other side exited (GRPCIO 1.7.x returns a different exception)
            if "details" in dir(err) and err.details == "EOF":
                return count, True
            # Other side exited (Python GRPC 1.7.0, Protoc 3.5.1 returns different exception)
            if ("_state" in dir(err) and "details" in dir(err._state) and 
                    err._state.details == "EOF".encode()):
                return count, True
            print(("Exception Received:", str(err)))
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
                    print("Validation error")
                    return count, error
                count = count + 1
        except NetworkError as netErr:
            if netErr.details == "EOF":
                # Success case, we send EOF, Server reflects the EOF back
                return count, True
        except Exception as err:
            # Other side exited (Python3 GRPC returns a different exception)
            if "details" in dir(err) and err.details == "EOF":
                return count, True
            # Other side exited (Python GRPC 1.7.0, Protoc 3.5.1 returns different exception)
            if ("_state" in dir(err) and "details" in dir(err._state) and 
                    err._state.details == "EOF".encode()):
                return count, True
            print(("Exception Received:", str(err)))
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
                    print("Validation error")
                    return count, error
                count = count + 1
        except NetworkError as netErr:
            if netErr.details == "EOF":
                # Success case, we send EOF, Server reflects the EOF back
                return count, True
        except Exception as err:
            # Other side exited (Python3 GRPC returns a different exception)
            if "details" in dir(err) and err.details == "EOF":
                return count, True
            # Other side exited (Python GRPC 1.7.0, Protoc 3.5.1 returns different exception)
            if ("_state" in dir(err) and "details" in dir(err._state) and 
                    err._state.details == "EOF".encode()):
                return count, True
            print(("Exception Received:", str(err)))
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

    def bd_reg_unreg_handle(self, oper, count, bdRegOper):
        """BD Reg/Unreg."""
        bdprefix = 'bd'
        bdutil = BD_Util()
        bdreg_msg = bdutil.construct_SLL2BdRegMsg(oper, bdprefix, count, bdRegOper)
        bdutil.print_SLL2BdRegMsg(bdreg_msg)
        # Invoke RPC
        response = self._stubs[7].SLL2BdRegOp(bdreg_msg, self.TIMEOUT_SECONDS)
        return response

    def l2_route_handle(self, oper, count, rtype, is_macip, g_bd, g_route_attrs):
        """L2 Route Oper."""
        route_util = Route_Util()
        route_msg = route_util.construct_SLL2RouteMsg(oper, count, rtype, is_macip, g_bd,
                                                          g_route_attrs)
        route_util.print_SLL2RouteMsg(route_msg)

        # Invoke RPC
        response = self._stubs[7].SLL2RouteOp(route_msg, self.TIMEOUT_SECONDS)
        return response

    def l2route_get_notif(self, cback_func, g_oper, BdAll, BdName):
        """L2 Route Get Notif"""
        route_util = Route_Util()
        # Construct input (currently sending interest for all Bds)
        request = gen_l2route_get_notif_msg(g_oper, BdAll, BdName)

        # Expect a stream of SLL2RouteGetMsgRsp [Use large timeout]
        responses = self._stubs[7].SLL2GetNotifStream(request, 3600*24*365)
        for response in responses:
            if not cback_func(response):
                break
        # Returns on exit
        return response

    def l3route_get_notif(self, af):
        """L3 Route Get Notif"""

        # Expect a stream of SLRoutev4Notif / SLRoutev6Notif [Use large timeout]
        req1 = gen_l3route_get_notif_msg()
        for response in {
            4: self._stubs[0].SLRoutev4GetNotifStream,
            6: self._stubs[1].SLRoutev6GetNotifStream,
        }[af](req1, 3600*24*365):

            print (response)
        return

    def l2_global_reg_unreg_handler(self, oper, g_route_attrs):
        """L2 Global reg/unreg"""
        route_util = Route_Util()
        global_reg = route_util.construct_SLL2RegMsg(oper, g_route_attrs)
        route_util.print_SLL2RegMsg(global_reg)
        # Invoke RPC
        response = self._stubs[7].SLL2RegOp(global_reg, self.TIMEOUT_SECONDS)
        return response

    def l2_globals_get(self):
        parent_message = sl_l2_route_pb2.SLL2GlobalsGetMsg()
        response = self._stubs[7].SLL2GlobalsGet(parent_message, self.TIMEOUT_SECONDS)
        return response

    def l2_route_op_stream(self, oper, count, rtype, is_macip, bdAry, g_route_attrs):
        route_util = Route_Util()
        count = 0
        l2_route_op_msgs = gen_l2_route_msgs(oper, count, rtype, is_macip, bdAry, g_route_attrs)

        responses = self._stubs[7].SLL2RouteOpStream(l2_route_op_msgs, 100*self.TIMEOUT_SECONDS)
        try:
            for response in responses:
                count = count + 1
                error = route_util.validate_l2route_response(response)
                if not error:
                    return count, error
        except NetworkError as netErr:
            if netErr.details == "EOF":
                # Success case, we send EOF, Server reflects the EOF back
                return count, True
        except Exception as err:
            # Other side exited (GRPCIO 1.7.x returns a different exception)
            if "details" in dir(err) and err.details == "EOF":
                return count, True
            # Other side exited (Python GRPC 1.7.0, Protoc 3.5.1 returns different exception)
            if ("_state" in dir(err) and "details" in dir(err._state) and 
                    err._state.details == "EOF".encode()):
                return count, True
            print(("Exception Received:", str(err)))
        return count, False

def gen_l2_route_msgs(oper, count, rtype, is_macip, bdAry, g_route_attrs):
    route_util = Route_Util()
    for bd in bdAry:
        route_msg = route_util.construct_SLL2RouteMsg(oper, count, rtype,
                                                           is_macip, bd, g_route_attrs)
        yield route_msg

def gen_l2route_get_notif_msg(g_oper, BdAll, BdName):
    """L2 Route Get Notif"""
    route_util = Route_Util()
    # Construct input (currently sending interest for all Bds)
    request = route_util.construct_SLL2GetNotifMsg(g_oper, BdAll, BdName)
    yield request

#
# Iterator to construct input (currently sending interest for default vrf)
#
def gen_l3route_get_notif_msg():
    route_util = Route_Util()
    # construct SLRouteGetNotifMsg for both v4 and v6
    msgs = [
        route_util.construct_SLRouteGetNotifMsg(1, "default", "local", ""),
        route_util.construct_SLRouteGetNotifMsg(2, "default", "connected", ""),
        route_util.construct_SLRouteGetNotifMsg(3, "default", "static", ""),
    ]
    count = 0
    for msg in msgs:
        if count == 0:
            time.sleep(3)
        yield msg
        time.sleep(2)
        count = count + 1
