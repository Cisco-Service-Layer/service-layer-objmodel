#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
import collections
import ipaddress

from util import util

from genpy import sl_global_pb2
from genpy import sl_common_types_pb2
from genpy import sl_route_ipv4_pb2
from genpy import sl_route_ipv6_pb2
from genpy import sl_route_common_pb2
from genpy import sl_mpls_pb2
from genpy import sl_bfd_common_pb2
from genpy import sl_bfd_ipv4_pb2
from genpy import sl_bfd_ipv6_pb2
from genpy import sl_interface_pb2

def global_route_get_serializer():
    """Global Get Message serializer."""
    serializer = sl_route_common_pb2.SLRouteGlobalsGetMsg()
    return serializer

def global_route_stats_get_serializer():
    """Global Stats Get Message serializer."""
    serializer = sl_route_common_pb2.SLRouteGlobalStatsGetMsg()
    return serializer

def route_get_serializer(get_info, af):
    """Route Get Message serializer."""
    if af == 4:
        serializer = sl_route_ipv4_pb2.SLRoutev4GetMsg()
    elif af == 6:
        serializer = sl_route_ipv6_pb2.SLRoutev6GetMsg()
    if "correlator" in get_info:
        serializer.Correlator = get_info["correlator"]
    if "vrf_name" in get_info:
        serializer.VrfName = get_info["vrf_name"]
    if af == 4 and "v4_prefix" in get_info:
        serializer.Prefix = int(ipaddress.ip_address(get_info['v4_prefix']))
    if af == 6 and "v6_prefix" in get_info:
        serializer.Prefix = ipaddress.IPv6Address(get_info['v6_prefix']).packed
    if "prefix_len" in get_info:
        serializer.PrefixLen = get_info["prefix_len"]
    if "count" in get_info:
        serializer.EntriesCount = get_info["count"]
    if "get_next" in get_info:
        serializer.GetNext = (get_info["get_next"] != 0)
    return serializer

def route_serializer(batch, paths, next_hops):
    """Agnostic function that returns either an IPv4 or IPv6 serializer
    instance.

    Not all fields are required to instantiate `SLRoutev4Msg`|
    `SLRoutev6Msg` classes. Therefore, conditions are specified to
    determine if certain keys exist within the dictionary parameters. If
    said keys do exist, then that attribute for the serializer class is
    assigned. Otherwise, fields are omitted, but the class is still
    instantiated.

    Returns: Tuple:
        sl_route_ipv4_pb2.SLRoutev4Msg|sl_route_ipv6_pb2.SLRoutev6Msg
        Next Prefix based on range value
    """
    Message = collections.namedtuple('Message', [
        'af',
        'serializer',
        'route',
    ])
    if batch['af'] == 4:
        # IPv4 message types.
        ipv4_or_ipv6 = Message(
            batch['af'],
            sl_route_ipv4_pb2.SLRoutev4Msg,
            sl_route_ipv4_pb2.SLRoutev4
        )
    elif batch['af'] == 6:
        # IPv6 message types.
        ipv4_or_ipv6 = Message(
            batch['af'],
            sl_route_ipv6_pb2.SLRoutev6Msg,
            sl_route_ipv6_pb2.SLRoutev6
        )
    # Create either a `SLRoutev4Msg` message or a `SLRoutev6Msg`
    # message.
    serializer = ipv4_or_ipv6.serializer()
    if 'vrf_name' in batch:
        serializer.VrfName = batch['vrf_name']
    if 'correlator' in batch:
        serializer.Correlator = batch['correlator']
    if 'routes' in batch:
        routes = []
        for route in batch['routes']:
            # Create either a `SLRoutev4` message or a `SLRoutev6`
            # message.
            if 'prefix' in route:
                if ipv4_or_ipv6.af == 4:
                    value = int(ipaddress.ip_address(route['prefix']))
                elif ipv4_or_ipv6.af == 6:
                    value = int(ipaddress.ip_address(route['prefix']))
            #
            local_label = 0
            if 'local_label' in route:
                local_label = route['local_label']
            #
            for i in range(route['range']):

                r = ipv4_or_ipv6.route()
                if 'prefix' in route:
                    if ipv4_or_ipv6.af == 4:
                        r.Prefix = value
                    elif ipv4_or_ipv6.af == 6:
                        r.Prefix = (
                            ipaddress.IPv6Address(value).packed
                        )
                if 'prefix_len' in route:
                    if ipv4_or_ipv6.af == 4:
                        r.PrefixLen = (
                            route['prefix_len']
                        )
                    elif ipv4_or_ipv6.af == 6:
                        r.PrefixLen = (
                            route['prefix_len']
                        )
                if 'admin_dist' in route:
                    r.RouteCommon.AdminDistance = route['admin_dist']
                if 'local_label' in route:
                    r.RouteCommon.LocalLabel = local_label
                    local_label = local_label + 1
                if 'tag' in route:
                    r.RouteCommon.Tag = route['tag']
                ps = []
                for path in paths[route['path']]:
                    p = sl_route_common_pb2.SLRoutePath()
                    if ipv4_or_ipv6.af == 4:
                        if (path['nexthop'] and
                                'v4_addr' in next_hops[path['nexthop']]):
                            p.NexthopAddress.V4Address = (
                                int(ipaddress.ip_address(
                                    next_hops[path['nexthop']]['v4_addr']))
                            )
                    elif ipv4_or_ipv6.af == 6:
                        if (path['nexthop'] and
                                'v6_addr' in next_hops[path['nexthop']]):
                            p.NexthopAddress.V6Address = (
                                ipaddress.ip_address(
                                    (next_hops[path['nexthop']]['v6_addr']))
                                    .packed
                            )
                    if 'if_name' in next_hops[path['nexthop']]:
                        p.NexthopInterface.Name = (
                            next_hops[path['nexthop']]['if_name']
                        )
                    if 'load_metric' in path:
                        p.LoadMetric = path['load_metric']
                    if 'metric' in path:
                        p.Metric = path['metric']
                    if 'vrf_name' in next_hops[path['nexthop']]:
                        p.VrfName = next_hops[path['nexthop']]['vrf_name']
                    if 'path_id' in path:
                        p.PathId = path['path_id']
                    # Bitmap
                    bitmap = []
                    if 'p_bitmap' in path:
                         for bmap in path['p_bitmap']:
                             bitmap.append(bmap)
                         p.ProtectedPathBitmap.extend(bitmap)
                    # Add labels
                    labels = []
                    if 'labels' in path:
                        for label in path['labels']:
                            labels.append(label)
                        p.LabelStack.extend(labels)
                    # Add remote addresses
                    remote_addr = []
                    if ipv4_or_ipv6.af == 4:
                        if 'v4_remote_addr' in path:
                            for r_addr in path['v4_remote_addr']:
                                sl_r_addr = sl_common_types_pb2.SLIpAddress()
                                sl_r_addr.V4Address = (
                                    int(ipaddress.ip_address(r_addr))
                                )
                                remote_addr.append(sl_r_addr)
                            p.RemoteAddress.extend(remote_addr)
                    elif ipv4_or_ipv6.af == 6:
                         if 'v6_remote_addr' in path:
                            for r_addr in path['v6_remote_addr']:
                                sl_r_addr = sl_common_types_pb2.SLIpAddress()
                                sl_r_addr.V6Address = (
                                    ipaddress.ip_address(r_addr).packed
                                )
                                remote_addr.append(sl_r_addr)
                            p.RemoteAddress.extend(remote_addr)
                    # Append the `SLRoutePath` object to the `ps` list
                    # object and extend the `sl_path_list` object of the
                    # route.
                    ps.append(p)
                r.PathList.extend(ps)
                # Append the `SLRoutev4`|`SLRoutev6` object to the `routes`
                # list object and extend the `sl_routes` object of the
                # serializer.
                routes.append(r)
                # Increment prefix
                value = util.sl_util_inc_prefix(
                    value, route['prefix_len'], 1, ipv4_or_ipv6.af
                )
            serializer.Routes.extend(routes)
    if ipv4_or_ipv6.af == 4:
        value_str = str(ipaddress.IPv4Address(value))
    else:
        value_str = str(ipaddress.IPv6Address(value))
    return (serializer, value_str, local_label)


def vrf_registration_serializer(batch):
    """Virtual routing and forwarding serializer."""
    serializer = sl_route_common_pb2.SLVrfRegMsg()
    messages = []
    for message in batch['vrfs']:
        registration_message = sl_route_common_pb2.SLVrfReg()
        if 'vrf_name' in message:
            registration_message.VrfName = message['vrf_name']
        if 'admin_dist' in message:
            registration_message.AdminDistance = message['admin_dist']
        if 'purge_time' in message:
            registration_message.VrfPurgeIntervalSeconds = (
                message['purge_time']
            )
        messages.append(registration_message)
    serializer.VrfRegMsgs.extend(messages)
    return serializer

def global_vrf_get_serializer(get_info):
    """VRF Get Message serializer."""
    serializer = sl_route_common_pb2.SLVrfRegGetMsg()
    if "vrf_name" in get_info:
        serializer.VrfName = get_info["vrf_name"]
    if "count" in get_info:
        serializer.EntriesCount = get_info["count"]
    if "get_next" in get_info:
        serializer.GetNext = (get_info["get_next"] != 0)
    return serializer

def global_init_serializer(init):
    """Global Init Message serializer."""
    serializer = sl_global_pb2.SLInitMsg()
    if 'major' in init:
        serializer.MajorVer = init['major']
    if 'minor' in init:
        serializer.MinorVer = init['minor']
    if 'sub_ver' in init:
        serializer.SubVer = init['sub_ver']
    return serializer

def global_get_serializer():
    """Global Get Message serializer."""
    serializer = sl_global_pb2.SLGlobalsGetMsg()
    return serializer

def mpls_regop_serializer():
    """MPLS Reg Op Message serializer."""
    serializer = sl_mpls_pb2.SLMplsRegMsg()
    return serializer

def mpls_get_serializer():
    """MPLS Get Message serializer."""
    serializer = sl_mpls_pb2.SLMplsGetMsg()
    return serializer

def label_block_serializer(batch):
    """MPLS label block serializer"""
    serializer = sl_mpls_pb2.SLMplsLabelBlockMsg()
    if 'blocks' in batch:
        blk_list=[]
        for block in batch['blocks']:
            b = sl_mpls_pb2.SLMplsLabelBlockKey()
            if 'block_size' in block:
                b.LabelBlockSize = block['block_size']
            if 'start_label' in block:
                b.StartLabel = block['start_label']
            blk_list.append(b)
    serializer.MplsBlocks.extend(blk_list)
    return serializer

def label_block_get_serializer(get_info):
    """MPLS label block Get serializer."""
    serializer = sl_mpls_pb2.SLMplsLabelBlockGetMsg()
    if "start_label" in get_info:
        serializer.Key.StartLabel = get_info["start_label"]
    if "block_size" in get_info:
        serializer.Key.LabelBlockSize = get_info["block_size"]
    if "count" in get_info:
        serializer.EntriesCount = get_info["count"]
    if "get_next" in get_info:
        serializer.GetNext = (get_info["get_next"] != 0)
    return serializer

def ilm_serializer(batch, af, paths, next_hops):
    """Agnostic function that returns either an MPLS IPv4 or IPv6 serializer
    instance.

    Not all fields are required to instantiate `SLMplsIlmMsg` classes.
    Therefore, conditions are specified to
    determine if certain keys exist within the dictionary parameters. If
    said keys do exist, then that attribute for the serializer class is
    assigned. Otherwise, fields are omitted, but the class is still
    instantiated.

    Returns: sl_mpls_pb2.SLMplsIlmMsg
    """
    Message = collections.namedtuple('Message', [
        'serializer',
        'ilm',
    ])
    ipv4_or_ipv6 = Message(
        sl_mpls_pb2.SLMplsIlmMsg,
        sl_mpls_pb2.SLMplsIlmEntry
    )
    # Create either an SLMplsIlmMsg
    serializer = ipv4_or_ipv6.serializer()
    if 'correlator' in batch:
        serializer.Correlator = batch['correlator']
    if 'ilms' in batch:
        ilms = []
        for ilm in batch['ilms']:
            if 'in_label' in ilm:
                value = ilm["in_label"]
            for i in range(ilm['range']):
                # Create SLMplsIlmEntry
                entry = ipv4_or_ipv6.ilm()
                if 'in_label' in ilm:
                    entry.Key.LocalLabel = value
                ps = []
                for path in paths[ilm['path']]:
                    p = sl_mpls_pb2.SLMplsPath()
                    if af == 4:
                        if (path['nexthop'] and
                                'v4_addr' in next_hops[path['nexthop']]):
                            p.NexthopAddress.V4Address = (
                                int(ipaddress.ip_address(
                                    next_hops[path['nexthop']]['v4_addr']))
                            )
                    elif af == 6:
                        if (path['nexthop'] and
                                'v6_addr' in next_hops[path['nexthop']]):
                            p.NexthopAddress.V6Address = (
                                ipaddress.ip_address(
                                    (next_hops[path['nexthop']]['v6_addr']))
                                    .packed
                            )
                    if 'if_name' in next_hops[path['nexthop']]:
                        p.NexthopInterface.Name = (
                            next_hops[path['nexthop']]['if_name']
                        )
                    if 'label_action' in path:
                        p.Action = path['label_action']
                    if 'load_metric' in path:
                        p.LoadMetric = path['load_metric']
                    if 'vrf_name' in next_hops[path['nexthop']]:
                        p.VrfName = next_hops[path['nexthop']]['vrf_name']
                    if 'path_id' in path:
                        p.PathId = path['path_id']
                    # Bitmap
                    bitmap = []
                    if 'p_bitmap' in path:
                         for bmap in path['p_bitmap']:
                             bitmap.append(bmap)
                         p.ProtectedPathBitmap.extend(bitmap)
                    # Add labels
                    labels = []
                    if 'labels' in path:
                        for label in path['labels']:
                            labels.append(label)
                        p.LabelStack.extend(labels)
                    # Add remote addresses
                    remote_addr = []
                    if af == 4:
                        if 'v4_remote_addr' in path:
                            for r_addr in path['v4_remote_addr']:
                                sl_r_addr = sl_common_types_pb2.SLIpAddress()
                                sl_r_addr.V4Address = (
                                    int(ipaddress.ip_address(r_addr))
                                )
                                remote_addr.append(sl_r_addr)
                            p.RemoteAddress.extend(remote_addr)
                    elif af == 6:
                         if 'v6_remote_addr' in path:
                            for r_addr in path['v6_remote_addr']:
                                sl_r_addr = sl_common_types_pb2.SLIpAddress()
                                sl_r_addr.V6Address = (
                                    ipaddress.ip_address(r_addr).packed
                                )
                                remote_addr.append(sl_r_addr)
                            p.RemoteAddress.extend(remote_addr)
                    # Append the `SLMplsPathv4` object to the `ps` list
                    ps.append(p)
                entry.Paths.extend(ps)
                # Append the `SLMplsIlmv4Msg`|`SLMplsIlmv6Msg` object
                ilms.append(entry)
                # Increment label
                value = value + 1
            serializer.MplsIlms.extend(ilms)
    return (serializer, value)

def ilm_get_serializer(get_info):
    """ILM Get Message serializer."""
    serializer = sl_mpls_pb2.SLMplsIlmGetMsg()
    if "correlator" in get_info:
        serializer.Correlator = get_info["correlator"]
    if "in_label" in get_info:
        serializer.Key.LocalLabel = get_info["in_label"]
    if "count" in get_info:
        serializer.EntriesCount = get_info["count"]
    if "get_next" in get_info:
        serializer.GetNext = (get_info["get_next"] != 0)
    return serializer

def bfd_get_serializer():
    """BFD Get Message serializer."""
    serializer = sl_bfd_common_pb2.SLBfdGetMsg()
    return serializer

def bfd_regop_serializer():
    """BFD Reg Op Message serializer."""
    serializer = sl_bfd_common_pb2.SLBfdRegMsg()
    return serializer

def bfd_serializer(batch, next_hops, af):
    """Agnostic function that returns a BFD serializer instance.

    Not all fields are required to instantiate `SLBfdv4Msg` or `SLBfdv6Msg`
    class. Therefore, conditions are specified to
    determine if certain keys exist within the dictionary parameters. If
    said keys do exist, then that attribute for the serializer class is
    assigned. Otherwise, fields are omitted, but the class is still
    instantiated.

    Returns: SLBfdv4Msg or SLBfdv6Msg
    """
    Message = collections.namedtuple('Message', [
        'af',
        'serializer',
        'bfd',
    ])
    if af == 4:
        # IPv4 message types.
        ipv4_or_ipv6 = Message(
            af,
            sl_bfd_ipv4_pb2.SLBfdv4Msg,
            sl_bfd_ipv4_pb2.SLBfdv4SessionCfg
        )
    elif af == 6:
        # IPv4 message types.
        ipv4_or_ipv6 = Message(
            af,
            sl_bfd_ipv6_pb2.SLBfdv6Msg,
            sl_bfd_ipv6_pb2.SLBfdv6SessionCfg
        )
    # Create a `SLBfdv4Msg` or `SLBfdv6Msg` message 
    serializer = ipv4_or_ipv6.serializer()
    if 'sessions' in batch:
        sessions = []
        for sess in batch['sessions']:
            # Create SessionCfg
            entry = ipv4_or_ipv6.bfd()
            if ipv4_or_ipv6.af == 4:
                if (sess['nexthop'] and
                        'v4_addr' in next_hops[sess['nexthop']]):
                    entry.Key.NbrAddr = (
                        int(ipaddress.ip_address(
                            next_hops[sess['nexthop']]['v4_addr']))
                    )
                if 'src_v4_addr' in sess:
                    entry.Key.SourceAddr = (
                        int(ipaddress.ip_address(sess['src_v4_addr']))
                    )
            elif ipv4_or_ipv6.af == 6:
                if (sess['nexthop'] and
                        'v6_addr' in next_hops[sess['nexthop']]):
                    entry.Key.NbrAddr = (
                        ipaddress.ip_address(
                            next_hops[sess['nexthop']]['v6_addr']).packed
                    )
                if 'src_v6_addr' in sess:
                    entry.Key.SourceAddr = (
                        ipaddress.ip_address(sess['src_v6_addr']).packed
                    )
            if 'if_name' in next_hops[sess['nexthop']]:
                entry.Key.Interface.Name = (
                    next_hops[sess['nexthop']]['if_name']
                )
            if 'vrf_name' in next_hops[sess['nexthop']]:
                entry.Key.VrfName = next_hops[sess['nexthop']]['vrf_name']
            if 'type' in sess:
                entry.Key.Type = sess['type']
            if 'cfg_detect_multi' in sess:
                entry.Config.DetectMultiplier = sess['cfg_detect_multi']
            if 'cfg_tx_int_usec' in sess:
                entry.Config.DesiredTxIntUsec = sess['cfg_tx_int_usec']
            sessions.append(entry)
            serializer.Sessions.extend(sessions)
    return serializer

def bfd_session_get_serializer(get_info, af):
    """Agnostic function that returns a BFD IPv4/IPv6 serializer instance.

    Not all fields are required to instantiate `SLBfdv4GetMsg` or 
    SLBfdv6GetMsg class. Therefore, conditions are specified to
    determine if certain keys exist within the dictionary parameters. If
    said keys do exist, then that attribute for the serializer class is
    assigned. Otherwise, fields are omitted, but the class is still
    instantiated.

    Returns: SLBfdv4GetMsg or SLBfdv6GetMsg
    """
    Message = collections.namedtuple('Message', [
        'af',
        'serializer',
    ])
    if af == 4:
        # IPv4 message types.
        ipv4_or_ipv6 = Message(
            af,
            sl_bfd_ipv4_pb2.SLBfdv4GetMsg
        )
    elif af == 6:
        # IPv6 message types.
        ipv4_or_ipv6 = Message(
            af,
            sl_bfd_ipv6_pb2.SLBfdv6GetMsg
        )
    # Create a SLBfdv4GetMsg or SLBfdv6GetMsg message 
    serializer = ipv4_or_ipv6.serializer()
    if ipv4_or_ipv6.af == 4:
        if 'v4_nbr' in get_info:
            serializer.Key.NbrAddr = (
                int(ipaddress.ip_address(get_info['v4_nbr']))
            )
        if 'v4_src' in get_info:
            serializer.Key.SourceAddr = (
                int(ipaddress.ip_address(get_info['v4_src']))
            )
    elif ipv4_or_ipv6.af == 6:
        if 'v6_nbr' in get_info:
            serializer.Key.NbrAddr = (
                ipaddress.ip_address(get_info['v6_nbr']).packed
            )
        if 'v6_src' in get_info:
            serializer.Key.SourceAddr = (
                ipaddress.ip_address(get_info['v6_src']).packed
            )
    if 'if_name' in get_info:
        serializer.Key.Interface.Name = get_info['if_name']
    if 'vrf_name' in get_info:
        serializer.Key.VrfName = get_info['vrf_name']
    if 'type' in get_info:
        serializer.Key.Type = get_info['type']
    if 'type' in get_info:
        serializer.Key.Type = get_info['type']
    if 'count' in get_info:
        serializer.EntriesCount = get_info['count']
    if 'seq_num' in get_info:
        serializer.SeqNum = get_info['seq_num']
    if 'get_next' in get_info:
        serializer.GetNext = get_info['get_next']
    return serializer

def bfd_get_notif_serializer():
    """BFD Get Notif Message serializer."""
    serializer = sl_bfd_common_pb2.SLBfdGetNotifMsg()
    return serializer

def intf_regop_serializer():
    """Interface Registration serializer."""
    serializer = sl_interface_pb2.SLInterfaceGlobalsRegMsg()
    return serializer

def intf_globals_get_serializer():
    """Interface Globals get serializer."""
    serializer = sl_interface_pb2.SLInterfaceGlobalsGetMsg()
    return serializer

def intf_get_serializer(get_info):
    """Interface get serializer."""
    serializer = sl_interface_pb2.SLInterfaceGetMsg()
    if 'if_name' in get_info:
        serializer.Key.Name = get_info['if_name']
    if 'count' in get_info:
        serializer.EntriesCount = get_info['count']
    if 'get_next' in get_info:
        serializer.GetNext = get_info['get_next']
    return serializer

def intf_get_notif_serializer():
    """Interface get notification serializer."""
    serializer = sl_interface_pb2.SLInterfaceGetNotifMsg()
    return serializer

def intf_notif_op_serializer(batch):
    """Interface notification operation serializer."""
    serializer = sl_interface_pb2.SLInterfaceNotifMsg()
    if 'interfaces' in batch:
        interfaces = []
        for interface in batch['interfaces']:
            entry = sl_common_types_pb2.SLInterface()
            if 'if_name' in interface:
                entry.Name = interface['if_name']
            interfaces.append(entry)
        serializer.Entries.extend(interfaces)
    return serializer
