
import ipaddress
from binascii import hexlify, unhexlify
import time
import itertools

try:
    from feature_lib.slapi.genpy import sl_common_types_pb2
    from feature_lib.slapi.genpy import sl_route_common_pb2
    from feature_lib.slapi.genpy import sl_bfd_common_pb2
    from feature_lib.slapi.genpy import sl_interface_pb2
    from feature_lib.slapi.genpy import sl_l2_route_pb2
    from logger.cafylog import CafyLog as Logger
except ImportError:
    from genpy import sl_common_types_pb2
    from genpy import sl_route_common_pb2
    from genpy import sl_bfd_common_pb2
    from genpy import sl_interface_pb2
    from genpy import sl_l2_route_pb2
    from tests.base_ap import LoggerStub as Logger

log = Logger(name="SLApiUtil")

def print_globals(response):
    # Print Received Globals
    if (response.ErrStatus.Status ==
        sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
        log.info('Max VRF Name Len                      : %d' %(response.MaxVrfNameLength))
        log.info('Max Iface Name Len                    : %d' %(response.MaxInterfaceNameLength))
        log.info('Max Paths per Entry                   : %d' %(response.MaxPathsPerEntry))
        log.info('Max Prim per Entry                    : %d' %(response.MaxPrimaryPathPerEntry))
        log.info('Max Bckup per Entry                   : %d' %(response.MaxBackupPathPerEntry))
        log.info('Max Labels per Entry                  : %d' %(response.MaxMplsLabelsPerPath))
        log.info('Min Prim Path-id                      : %d' %(response.MinPrimaryPathIdNum))
        log.info('Max Prim Path-id                      : %d' %(response.MaxPrimaryPathIdNum))
        log.info('Min Bckup Path-id                     : %d' %(response.MinBackupPathIdNum))
        log.info('Max Bckup Path-id                     : %d' %(response.MaxBackupPathIdNum))
        log.info('Max Remote Bckup Addr                 : %d' %(response.MaxRemoteAddressNum))
        log.info('Max L2 Bd Name Length                 : %d' %(response.MaxL2BdNameLength))
        log.info('Max L2 PMSI Tunnel Id Length %d' %(response.MaxL2PmsiTunnelIdLength))
        log.info('Max Label Block Client Name Length    : %d' %(
            response.MaxLabelBlockClientNameLength))

    else:
        log.error('Globals response Error 0x%x' %(response.ErrStatus.Status))
        return False
    return True


class RouteUtil:
    @staticmethod
    def print_route_globals(response):
        'Print Received Route Globals'
        if (response.ErrStatus.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            log.info('Max VRF Reg Per VRF Msg : %d' %
                response.MaxVrfregPerVrfregmsg)
            log.info('Max Routes per Route Msg: %d' %
                response.MaxRoutePerRoutemsg)
        else:
            log.error('Route Globals response Error 0x%x' %(response.ErrStatus.Status))
            return False
        return True

    @staticmethod
    def print_route_stats_globals(response):
        if (response.ErrStatus.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            log.info('')
            log.info('VrfCount   : %d' % response.VrfCount)
            log.info('RouteCount : %d' % response.RouteCount)
        else:
            log.error('Route Get Stats response Error 0x%x' %(response.ErrStatus.Status))
            return False
        return True

    @staticmethod
    def validate_vrf_response(response):
        if (response.StatusSummary.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            return True
        # Error cases
        log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
        # SOME ERROR
        if (response.StatusSummary.Status ==
                sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR):
            for result in response.Results:
                log.error('Error code for %s is 0x%x' %(result.VrfName,
                    result.ErrStatus.Status
                ))
        return False

    @staticmethod
    def validate_route_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.StatusSummary.Status):
            return True
        # Error cases
        log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
        # SOME ERROR
        if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
                response.StatusSummary.Status):
            for result in response.Results:
                log.error('Error code for %s/%d is 0x%x' %(
                    str(ipaddress.ip_address(result.Prefix)),
                    result.PrefixLen,
                    result.ErrStatus.Status
                ))
        return False

    @staticmethod
    def validate_route_get_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.ErrStatus.Status):
            log.info('Route Get Msg Resp:')
            log.info('Corr:%d, Eof:%r, VRF:%s ErrStatus: 0x%x' % (
                response.Correlator, response.Eof,
                response.VrfName, response.ErrStatus.Status))
            for elem in response.Entries:
                prefix = ipaddress.ip_address(elem.Prefix)
                log.info('  %s/%d' %(str(prefix), elem.PrefixLen))
                for path in elem.PathList:
                    try:
                        addr = path.NexthopAddress.V4Address
                    except AttributeError:
                        addr = path.NexthopAddress.V6Address

                    log.info('    via %s' %
                    str(ipaddress.ip_address(addr)))

                    for addr in path.RemoteAddress:
                        try:
                            _addr = ipaddress.ip_address(addr.V4Address)
                        except AttributeError:
                            _addr = ipaddress.ip_address(addr.V6Address)
                        log.info('      Remote:%s' %
                            str(ipaddress.ip_address(_addr)))
                log.info('Details:')
                log.info(elem)
            return True
        log.error('Route Get Error code 0x%x' % response.ErrStatus.Status)
        return False

    @staticmethod
    def validate_vrf_get_response(response):
        log.info('VRF Get Attributes:')
        log.info(response)
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
                response.ErrStatus.Status):
            return False
        return True

    @staticmethod
    def validate_vrf_stats_get_response(response):
        log.info('VRF Get Stats:')
        log.info(response)
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
                response.ErrStatus.Status):
            return False
        return True

    @staticmethod
    def get_last_vrf(response):
        yield 'vrf_name', response.Entries[-1].VrfName

    @staticmethod
    def get_last_prefix_v4(response):
        last_prefix = ipaddress.ip_address(response.Entries[-1].Prefix)
        last_prefix_len = response.Entries[-1].PrefixLen

        yield 'v4_prefix' , str(last_prefix)
        yield 'prefix_len', last_prefix_len 

    @staticmethod
    def get_last_prefix_v6(response):
        last_prefix = ipaddress.IPv6Address(
            int(hexlify(response.Entries[-1].Prefix), 16)
        )

        last_prefix_len = response.Entries[-1].PrefixLen

        yield 'v6_prefix' , str(last_prefix)
        yield 'prefix_len', last_prefix_len 

    @staticmethod
    def construct_SLRouteGetNotifMsg(seqno, vrf_name, src_proto, src_proto_tag):
        parent_message = sl_route_common_pb2.SLRouteGetNotifMsg()

        parent_message.Oper = sl_common_types_pb2.SL_NOTIFOP_ENABLE
        parent_message.Correlator = seqno
        parent_message.VrfName = vrf_name
        parent_message.SrcProto = src_proto
        parent_message.SrcProtoTag = src_proto_tag
        return parent_message

    # Iterator to construct input (currently sending interest for default vrf)
    @classmethod
    def gen_l3route_get_notif_msg(cls):
        # construct SLRouteGetNotifMsg for both v4 and v6
        msgs = [
            cls.construct_SLRouteGetNotifMsg(1, 'default', 'local', ''),
            cls.construct_SLRouteGetNotifMsg(2, 'default', 'connected', ''),
            cls.construct_SLRouteGetNotifMsg(3, 'default', 'static', ''),
        ]
        for msg in msgs:
            yield msg

        # On stop iteration the client will close the request channel.
        # The server will respond by closing the response channel.
        # This sleep allow time for the server to respond before the
        # channels are closed.
        time.sleep(1)

        # FIXME: The correct way to do this would be to have to this iterator
        #        wait for a signal (event) from the thread handling the
        #        responses before returning

    @staticmethod
    def is_valid_route_batch_info(op_info):
        '''
        Validate batch info schema

        This method does not verify nested fields
        '''

        if 'prefix_range' not in op_info:
            raise ValueError('must define prefix range')

        if 'prefix_len' not in op_info:
            raise ValueError('must define prefix length')

        if 'path' not in op_info:
            raise ValueError('must define either paths')

        return True

    @classmethod
    def retrieve_routes(cls, op_info, af, paths):
        if 'routes' in op_info:
            # Use statically created ilm list
            routes = iter(op_info['routes'])
        elif 'routes' not in op_info and cls.is_valid_route_batch_info(op_info):
            # Dynamically generate routes from batch info
            routes = cls.generate_routes(op_info, af, paths)
        else:
            assert False, 'must specify a list of routes or valid batch info'

        return 'routes', routes

    @staticmethod
    def generate_routes(batch_info, af, paths):
        def generate_prefixes(addr_range):
            lo, hi = map(int, map(ipaddress.ip_address, addr_range))
            max_prefix_len = 32 if af == 4 else 128
            prefix_len = batch_info['prefix_len']
            assert prefix_len < max_prefix_len

            # Increment prefix by subnet size
            increment = 1 << (max_prefix_len - prefix_len)

            for addr in range(lo, hi + 1, increment):
                yield str(ipaddress.ip_address(addr))

        def generate_paths(path_info):
            # Generate slice of paths
            all_paths = paths[path_info]
            for path in all_paths:
                yield path

        def make_route(prefix):
            route = {
                    'admin_dist': batch_info['admin_dist'],
                    'path': generate_paths(batch_info['path']),
                    'prefix': prefix,
                    'prefix_len': batch_info['prefix_len'],
                    'tag': batch_info['tag'],
                    'vrf_name': batch_info['vrf_name']
            }

            if 'local_label' in batch_info: 
                route['local_label'] = batch_info['local_label']
            if 'flags' in batch_info:
                route['flags'] = batch_info['flags']

            return route

        for prefix in generate_prefixes(batch_info['prefix_range']):
            yield make_route(prefix)


class L2RouteUtil:
    @staticmethod
    def print_SLL2RegMsg(global_msg):
        log.info((str(global_msg) + '\n'))

    @staticmethod
    def print_SLL2RouteMsg(route_msg):
        log.info((str(route_msg) + '\n'))

    @staticmethod
    def construct_SLL2GetNotifMsg(g_oper, BdAll, BdName):
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

    @staticmethod
    def construct_SLL2RouteNh(g_route_attrs):
        g_encap = getattr(sl_common_types_pb2, g_route_attrs['g_encap'])

        parent_message = sl_l2_route_pb2.SLL2RouteNh()
        parent_message.NhType = g_route_attrs['g_nh_type']

        if parent_message.NhType == 1:
            # Either interface name or handle (not both) must be present if
            # interface nexthop type selected
            if 'g_nh_intf_name' in g_route_attrs:
                parent_message.NhInterface.Name = g_route_attrs['g_nh_intf_name']
            else:
                parent_message.NhInterface.Handle = g_route_attrs['g_nh_intf_handle']
        elif parent_message.NhType == 2:
            # IP manipulation
            ip_list = []*1
            for ip in ipaddress.ip_network(g_route_attrs['g_next_hop'][0], strict = False):
                ip_list.append(int(ipaddress.IPv4Address(ip)))

            parent_message.NhOverlay.OverlayNhIp.V4Address = ip_list[0]
            parent_message.NhOverlay.OverlayNhEncap = g_encap
            parent_message.NhOverlay.OverlayNhLabel = g_route_attrs['g_label']
            # Using a single L3VNI for now
            l3_list = []
            l3_list.append(g_route_attrs['g_l3vni']) # Single L3VNI for vxlan
            parent_message.NhOverlay.OverlayNhL3Label.extend(l3_list)
            parent_message.NhOverlay.OverlayNhRouterMac = unhexlify(g_route_attrs['g_rmac'].replace(':', ''))

        return parent_message

    @classmethod
    def construct_SLL2MacRoute(cls, is_macip, ip, mac, g_route_attrs):
        parent_message = sl_l2_route_pb2.SLL2MacRoute()

        if is_macip == True:
            parent_message.RouteKey.IpAddress.V4Address = ip

        parent_message.RouteKey.MacAddress = unhexlify((mac.replace(':', '')))
        parent_message.SequenceNum = 1

        # Construct NH (single next hop for now)
        nh = cls.construct_SLL2RouteNh(g_route_attrs)
        message = []
        message.append(nh)
        parent_message.NextHopList.extend(message)
        parent_message.MacEsi.Esi = unhexlify(g_route_attrs['g_esi'])
        return parent_message

    @staticmethod
    def construct_SLL2ImetRoute(ip, g_route_attrs):
        parent_message = sl_l2_route_pb2.SLL2ImetRoute()

        parent_message.RouteKey.EthTagId = 0
        parent_message.RouteKey.IpAddress.V4Address = int(ipaddress.ip_address('1.2.3.4'))
        parent_message.EncapType = sl_common_types_pb2.SL_ENCAP_VXLAN
        parent_message.Label = g_route_attrs['g_label']
        # For now only ipV4 tunnelId, modify hardcoded PMSI tun type
        parent_message.TunnelType = 6
        parent_message.TunnelIdLength = 4

        ipstr = '2.3.4.5'
        parent_message.TunnelIdValue = unhexlify(ipstr.replace('.',''))
        return parent_message

    @classmethod
    def construct_SLL2Route(cls, rtype, is_macip, ip, mac, g_bd, g_route_attrs):
        parent_message = sl_l2_route_pb2.SLL2Route()

        parent_message.BdName = g_bd
        parent_message.Type = rtype

        if rtype == sl_l2_route_pb2.SL_L2_ROUTE_MAC:
            # Invoke mac/mac-ip msg construct API
            mac_route = cls.construct_SLL2MacRoute(is_macip, ip, mac, g_route_attrs)
            # Above is not iterable
            parent_message.MacRoute.CopyFrom(mac_route)
        else:
            # Invoke imet msg construct API
            imet_route = cls.construct_SLL2ImetRoute(ip, g_route_attrs)
            parent_message.ImetRoute.CopyFrom(imet_route)
        return parent_message

    @classmethod
    def construct_SLL2RouteMsg(cls, oper, count, rtype, is_macip, g_bd, g_route_attrs):
        parent_message = sl_l2_route_pb2.SLL2RouteMsg()
        parent_message.Correlator = 1
        parent_message.Oper = oper

        # IP manipulation
        ip_list = []*count
        i = 0
        for ip in ipaddress.ip_network(g_route_attrs['g_ip'][0], strict = False):
            ip_list.append(int(ipaddress.IPv4Address(ip)))

        message = []
        g_mac = g_route_attrs['g_mac']
        # Multiple MAC/MAC-IP/IMET case
        if count > 1:
            index = 0
            while count > 0:
                route = cls.construct_SLL2Route(rtype, is_macip,
                                                 ip_list[index], g_mac[index],
                                                 g_bd, g_route_attrs)
                message.append(route)
                parent_message.Routes.extend(message)
                index = index + 1
                count = count - 1

        elif count == 1:
            # Single MAC/MAC-IP/IMET case (won't use g_mac for IMET)
            route = cls.construct_SLL2Route(rtype, is_macip, ip_list[0],
                                                g_mac[0], g_bd, g_route_attrs)
            message.append(route)
            parent_message.Routes.extend(message)
        return parent_message

    @staticmethod
    def validate_l2route_response(response):
        def byte_to_mac_str(mac):
            num = 2
            mac_split = [ mac[start:start+num] for start in range(0, len(str), num) ]
            result = ''
            for elem in mac_split:
                result = result + elem + ':'
            return result[:-1]

        if response.Correlator != 1:
            return False

        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
            return True
        elif (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
            response.StatusSummary.Status):
            log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
            for result in response.Results:
                log.error('Error code for oper [%d] is 0x%x' % (result.Oper,
                        result.ErrStatus.Status))
                log.error('Failed route key: bd[%s], type[%d], mac[%s], ip[%s]' % (result.RouteKey.BdName, result.RouteKey.Type, 
                        byte_to_mac_str(result.RouteKey.Event.MacKey.MacAddress),
                        ipaddress.IPv4Address(result.RouteKey.Event.MacKey.IpAddress.V4Address)))
        else:
            log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
        return False

    @staticmethod
    def construct_SLL2RegMsg(oper, g_route_attrs):
        parent_message = sl_l2_route_pb2.SLL2RegMsg()

        if oper == 'SL_REGOP_REGISTER':
            parent_message.Oper = sl_common_types_pb2.SL_REGOP_REGISTER
        elif oper == 'SL_REGOP_UNREGISTER':
            parent_message.Oper = sl_common_types_pb2.SL_REGOP_UNREGISTER
        else:
            parent_message.Oper = sl_common_types_pb2.SL_REGOP_EOF

        parent_message.AdminDistance = g_route_attrs['adminDistance']
        parent_message.PurgeIntervalSeconds = g_route_attrs['purgeTime']
        return parent_message

    @classmethod
    def gen_l2_route_msgs(cls, oper, count, rtype, is_macip, bdAry, g_route_attrs):
        for bd in bdAry:
            route_msg = cls.construct_SLL2RouteMsg(oper, count, rtype,
                                                   is_macip, bd, g_route_attrs)
            yield route_msg

    @staticmethod
    def gen_l2route_get_notif_msg(g_oper, BdAll, BdName):
        '''L2 Route Get Notif'''
        # Construct input (currently sending interest for all Bds)
        request = L2RouteUtil.construct_SLL2GetNotifMsg(g_oper, BdAll, BdName)
        yield request

    @staticmethod
    def validate_l2route_notif(response):
        if response.EventType == sl_l2_route_pb2.SL_L2_EVENT_TYPE_ERROR:
            if (response.ErrStatus.Status ==
                    sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
                log.error('Received notification to Terminate, Stream taken over?')
            else:
                log.error('Received error 0x%x' % (response.ErrStatus.Status))
                return False
        else:
            log.info('Received L2route/Bd Notif Event Type: %d' %(response.EventType))
        return True


class BDUtil:
    @staticmethod
    def print_SLL2BdRegMsg(bdreg_msg):
        log.info((str(bdreg_msg) + '\n'))

    @staticmethod
    def construct_SLL2BdRegMsg(oper, bdprefix, count, bdRegOper):
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

    @staticmethod
    def validate_bdreg_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
            return True
        # Error cases
        # SOME ERROR
        elif (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
            response.StatusSummary.Status):
            log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
            for result in response.Results:
                log.error('Error code for %s is 0x%x' % (result.BdName, result.ErrStatus.Status))
            return False
        else:
            # Grpc ERROR
            log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
            return False


class MplsUtil:
    # Print Received MPLS Globals
    @staticmethod
    def validate_mpls_globals(response):
        if (response.ErrStatus.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            log.info('Max labels per label block            : %d' %(
                response.MaxLabelsPerBlock))
            log.info('Max label blocks per MplsLabelBlockMsg: %d' %(
                response.MaxLabelblocksPerLabelblockmsg))
            log.info('Min Start Label                       : %d' %(
                response.MinStartLabel))
            log.info('Label Table Size                      : %d' %(
                response.LabelTableSize))
            log.info('Max ILMs per IlmMsg                   : %d' %(
                response.MaxIlmPerIlmmsg))
            log.info('Max Paths per Ilm                     : %d' %(
                response.MaxPathsPerIlm))
        else:
            log.error('MPLS Globals response Error 0x%x' %(response.ErrStatus.Status))
            return False
        return True

    @staticmethod
    def print_mpls_stats(response):
        '''Print Received MPLS Stats'''
        if (response.ErrStatus.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            log.info('LabelBlockCount : %d' %(response.LabelBlockCount))
            log.info('IlmCount : %d' %(response.IlmCount))
        else:
            log.error('MPLS Stats response Error 0x%x' %(response.ErrStatus.Status))
            return False
        return True

    @staticmethod
    def validate_mpls_regop_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.ErrStatus.Status):
            return True
        # Error cases
        log.error('Response Error code 0x%x' %(response.ErrStatus.Status))
        return False

    @staticmethod
    def validate_lbl_blk_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.StatusSummary.Status):
            return True
        # Error cases
        log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
        # SOME ERROR
        if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
                response.StatusSummary.Status):
            for result in response.Results:
                log.error('Error code for %d is 0x%x' %(
                    result.Key.StartLabel,
                    result.ErrStatus.Status
                ))
        return False

    @staticmethod
    def validate_lbl_blk_get_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.ErrStatus.Status):
            log.info(response)
            return True
        log.error('Label Block Get Error code 0x%x' %(response.ErrStatus.Status))
        return False

    @staticmethod
    def validate_ilm_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.StatusSummary.Status):
            return True
        # Error cases
        log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
        # SOME ERROR
        if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
                response.StatusSummary.Status):
            for result in response.Results:
                log.error('Error code for %d is 0x%x' %(
                    result.Key.LocalLabel,
                    result.ErrStatus.Status
                ))
        return False

    @staticmethod
    def validate_ilm_get_response(response, expectedCount=None):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.ErrStatus.Status):
            # log.info(response)
            if expectedCount:
                assert expectedCount == len(response.Entries) or response.Eof
            return True
        log.error('ILM Get Error code 0x%x' %(response.ErrStatus.Status))
        return False

    @staticmethod
    def get_last_ilm(response):
        key = response.Entries[-1].Key
        last_ilm = {'in_label': key.LocalLabel}
        if key.SlMplsCosVal.WhichOneof('value') == 'Exp':
            last_ilm['exp'] = key.SlMplsCosVal.Exp
        elif key.SlMplsCosVal.WhichOneof('value') == 'DefaultElspPath':
            last_ilm['default_elsp'] = key.SlMplsCosVal.DefaultElspPath

        yield 'ilm', last_ilm

    @staticmethod
    def get_last_label_block(response):
        key = response.Entries[-1]
        last_block = {'block_size': key.LabelBlockSize,
                      'client_name': key.ClientName, 
                      'block_type': key.BlockType, 
                      'start_label': key.StartLabel
                }

        yield 'block_key', last_block

    @staticmethod
    def get_label_range(batch_info):
        if 'label_ranges' in batch_info:
            start = batch_info['label_ranges'][0]['range'][0]
            end = batch_info['label_ranges'][-1]['range'][1]
            return start, end

        return batch_info.get('label_range')

    @staticmethod
    def get_expected_ilm_count(batch_info):
        '''Used to determine how many ILMs a scale testcase wil return'''
        if 'exps' in batch_info:
            ilmsPerLabel = len(batch_info['exps'])
        else:
            ilmsPerLabel = 1

        assert ilmsPerLabel > 0, 'Exp dictionary is empty'

        if 'label_range' in batch_info:
            lo, hi = batch_info['label_range']
            assert hi - lo + 1 > 0, 'Invalid label range'
            num_labels = hi - lo + 1 
        elif 'label_ranges' in batch_info:
            num_labels = 0
            for label_range in batch_info['label_ranges']:
                lo, hi = label_range['range']
                assert hi - lo + 1 > 0, 'Invalid label range'
                num_labels += hi - lo + 1 
        
        return num_labels * ilmsPerLabel 

    @staticmethod
    def is_valid_ilm_batch_info(info):
        '''
        Validate batch info schema

        This method does not verify nested fields
        '''

        if 'label_ranges' not in info and 'label_range' not in info and 'ip_or_label_ranges' not in info:
            raise ValueError('must define either ip_or_label_ranges, label_range, label_ranges, or ilms')

        if 'label_ranges' not in info and 'label_range' not in info:
            raise ValueError('must define either label_range, label_ranges, or ilms')

        if 'exps' in info and 'label_path' in info:
            raise ValueError('cannot define both exps and label_path')

        if 'exps' not in info and 'label_path' not in info:
            if 'ip_or_label_ranges' not in info:
                raise ValueError('must define exps or label_path')

        return True

    @classmethod
    def retrieve_ilms(cls, op_info, af, paths):
        if 'ilms' in op_info:
            # use statically created ilm list
            ilms = iter(op_info['ilms'])
        elif 'ilms' not in op_info and MplsUtil.is_valid_ilm_batch_info(op_info):
            # dynamically generate ilms from batch info
            ilms = MplsUtil.generate_ilms(op_info, af, paths)
        else:
            assert False, 'must specify a list of ilms or valid batch info'

        return 'ilms', ilms

    @staticmethod
    def generate_ilms(batch_info, af, paths):
        '''
        Generator of ILMs based on the parameters passed in
        '''
        def generate_labels(label_range):
            lo, hi = label_range
            assert hi - lo + 1 > 0, 'Invalid label range'
            for label in range(lo, hi + 1):
                yield label

        def generate_paths(path_info):
            # Generate slice of paths
            all_paths = paths[path_info['path']]
            lo, hi = path_info['path_range']
            assert hi - lo + 1 > 0, 'Invalid path range'
            for path in itertools.islice(all_paths, lo, hi + 1):
                yield path

        def make_ilm(label, path_info, exp=None, default_elsp=False, af=None):
            ilm = {
                    'in_label': label,
                    'path': generate_paths(path_info),
                    'range': 1  # NOTE: Range must be 1
            }

            if default_elsp:
                ilm['default_elsp'] = default_elsp
            elif exp is not None:
                ilm['exp'] = exp

            if af:
                ilm['af'] = af

            return ilm

        def make_ip_ilm(ip, path_info, af):
            ilm = {
                    'path': generate_paths(path_info),
                    'range': 1
            }

            ilm['af'] = af
            if type(ip) is ipaddress.IPv4Address:
                ip_dict = {"ipv4_prefix": str(ip)}
                ilm["ip_prefix"] = ip_dict
            else:
                ip_dict = {"ipv6_prefix": str(ip)}
                ilm["ip_prefix"] = ip_dict

            return ilm

        if 'ip_or_label_ranges' in batch_info.keys():
            ip_or_label_ranges = batch_info.get('ip_or_label_ranges')
            for range_info in ip_or_label_ranges:
                if 'start_ip' in range_info:
                    base_ip = ipaddress.ip_address(range_info['start_ip'])
                    for idx in range(range_info['num_routes']):
                        ip = ipaddress.ip_address(int(base_ip) + idx)
                        yield make_ip_ilm(ip, range_info['label_path'], range_info['af'])
                elif 'label_ranges' in range_info or 'label_range' in batch_info:
                    label_ranges = range_info.get('label_ranges', [{'range': range_info.get('label_range', None), 'af': af}])
                    for label_range in label_ranges:
                        for label in generate_labels(label_range['range']):
                            if 'exps' in range_info:
                                for exp, path_info in sorted(range_info['exps'].items(), key=lambda x: x[0]):
                                    if exp == 'default':
                                        yield make_ilm(label, path_info, default_elsp=True, af=label_range['af'])
                                    else:
                                        yield make_ilm(label, path_info, exp=int(exp), af=label_range['af'])
                            elif 'label_path' in range_info:
                                # Non-elsp (no exp or default elsp)
                                yield make_ilm(label, range_info['label_path'])

        elif 'label_ranges' in batch_info or 'label_range' in batch_info:
            ranges = batch_info.get('label_ranges', [{'range': batch_info.get('label_range', None), 'af': af}])
            for range_info in ranges:
                for label in generate_labels(range_info['range']):
                    if 'exps' in batch_info:
                        for exp, path_info in sorted(batch_info['exps'].items(), key=lambda x: x[0]):
                            if exp == 'default':
                                yield make_ilm(label, path_info, default_elsp=True, af=range_info['af'])
                            else:
                                yield make_ilm(label, path_info, exp=int(exp), af=range_info['af'])
                    elif 'label_path' in batch_info:
                        # Non-elsp (no exp or default elsp)
                        yield make_ilm(label, batch_info['label_path'])
 




class BatchUtil:
    @staticmethod
    def resolve_next_hop(path, next_hops):
        'Lookup next hop names and replace with actual next hop dicts'
        if type(path.get('next_hop')) is str:
            path['next_hop'] = next_hops[path['next_hop']]

        return path

    @staticmethod
    def resolve_paths(obj, paths):
        'Lookup path names and replace with actual path dicts'
        if type(obj.get('path')) is str:
            obj['path'] = paths[obj['path']]

        return obj

    @classmethod
    def remove_indirection(cls, obj, af, paths, next_hops):
        '''
        Replace next_hop and path names with the actual dictionaries they refer to
        '''
        # Add af if it hasn't been set by batch generator
        if 'af' not in obj:
            obj['af'] = af

        obj = cls.resolve_paths(obj, paths)

        # Using map is actually not any faster here (path list size is bounded < 64 or 128)
        obj['path'] = [cls.resolve_next_hop(path, next_hops) for path in obj['path']]

        return obj

    @staticmethod
    def has_next(iterator):
        def prepend(value, iterator):
            'Prepend a single value in front of an iterator'
            return itertools.chain([value], iterator)

        # Emulate a peek by getting next and the putting it back
        try:
            peek = next(iterator)
        except StopIteration:
            return None, False

        # Put it back and return True
        return prepend(peek, iterator), True

    @classmethod
    def make_batch(cls, iterable, size, af, paths, next_hops, correlator):
        '''
        This function returns an iterator that will return n ilms
        Must check for empty iterator as it will lead to an empty ILM list
        which will throw an error
        '''

        iterable, hasNext = cls.has_next(iterable)

        if not hasNext:
            return None

        batch = itertools.islice(iterable, size)

        if paths and next_hops:
            def without_indirection(iterable):
                return cls.remove_indirection(iterable, af, paths, next_hops)

            # A map will apply the function without consuming the iterator
            batch = map(without_indirection, batch)

        return batch

    @classmethod
    def gen_batches(cls, **kwargs):
        batch = cls.make_batch(**kwargs)
        while batch:
            yield batch
            batch = cls.make_batch(**kwargs)


class BfdUtil:
    # Print Received BFD Globals
    @staticmethod
    def print_bfd_globals(af, response):
        if (response.ErrStatus.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            log.info('Max v%d BFD Sess Per BFD Msg : %d' %(af,
                response.MaxBfdSessionCfgPerSLBfdMsg))
            log.info('Min v%d BFD Tx Interval Single hop  : %d' %(af,
                response.MinBfdTxIntervalSingleHop))
            log.info('Min v%d BFD Tx Interval Multi hop   : %d' %(af,
                response.MinBfdTxIntervalMultiHop))
            log.info('Min v%d BFD Detect Multi Single hop : %d' %(af,
                response.MinBfdDetectMultiplierSingleHop))
            log.info('Min v%d BFD Detect Multi Multi hop  : %d' %(af,
                response.MinBfdDetectMultiplierMultiHop))
        else:
            log.info('BFD Globals response Error 0x%x' %(response.ErrStatus.Status))
            return False
        return True

    # Print Received BFD Stats
    @staticmethod
    def print_bfd_stats(af, response):
        if (response.ErrStatus.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            log.info(response)
        else:
            log.error('BFD Stats response Error 0x%x' %(response.ErrStatus.Status))
            return False
        return True

    # BFD notification Callback
    # This function is called from the BFD thread context
    # To break the stream recv(), return False
    @staticmethod
    def verify_bfd_notif(response, af):
        if response.EventType == sl_bfd_common_pb2.SL_BFD_EVENT_TYPE_ERROR:
            if (response.ErrStatus.Status ==
                    sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
                log.info('Received notification to Terminate, Stream taken over?')
            else:
                log.info('Received error 0x%x' %(response.ErrStatus.Status))
            return False
        elif response.EventType == sl_bfd_common_pb2.SL_BFD_EVENT_TYPE_SESSION_STATE:
            log.info('Received BFD Event:')
            if af == 4:
                log.info('Nbr : %s' %(
                    str(ipaddress.ip_address(response.Session.Key.NbrAddr))))
            elif af == 6:
                log.info('Nbr : %s' %(
                    str(ipaddress.IPv6Address(
                        int(hexlify(response.Session.Key.NbrAddr), 16)))))
            log.info(response)
        else:
            log.error('Received an unexpected event type %d' %(
                response.EventType))
            return False
        # Continue looping on events
        return True

    # Wait on BFD notification events
    @staticmethod
    def bfd_get_notif(event, af, thread_count):
        # This would notify the main thread to proceed
        event[af].set()
        # RPC to get Notifications
        response = TestSuite_005_BFD_IPv4.bfd_notif[af].bfd_get_notif(bfd_notif_cback, af)
        # Above, Should return on errors
        log.info('bfd_get_notif: thread %d exiting. response: %s' %(thread_count,
            response))
        # Do not exit the process, as other tests could be still going

    @staticmethod
    def validate_bfd_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.StatusSummary.Status):
            return True
        # Error cases
        log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
        # SOME ERROR
        if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
                response.StatusSummary.Status):
            for result in response.Results:
                log.error('Error code for %s is 0x%x' %(
                    str(ipaddress.ip_address(result.Key.NbrAddr)),
                    result.ErrStatus.Status
                ))
        return False

    @staticmethod
    def validate_bfd_regop_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.ErrStatus.Status):
            return True
        # Error cases
        log.error('Response Error code 0x%x' %(response.ErrStatus.Status))
        return False

    @staticmethod
    def validate_bfd_get_response(response, af):
        log.info('BFD Get Attributes:')
        log.info(response)
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
                response.ErrStatus.Status):
            return False
        return True


class IntfUtil:
    # Print Received Interface Globals
    @staticmethod
    def print_intf_globals(response):
        if (response.ErrStatus.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            log.info('Max Intf Per Msg : %d' %(response.MaxInterfacesPerBatch))
        else:
            log.error('Intf Globals response Error 0x%x' %(response.ErrStatus.Status))
            return False
        return True

    # Interface notification Callback
    # This function is called from the Interface thread context
    # To break the stream recv(), return False
    @staticmethod
    def validate_intf_notif(response):
        if response.EventType == sl_interface_pb2.SL_INTERFACE_EVENT_TYPE_ERROR:
            if (response.ErrStatus.Status ==
                    sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
                log.error('Received notification to Terminate, Stream taken over?')
            else:
                log.error('Received error 0x%x' %(response.ErrStatus.Status))
            return False
        elif response.EventType == sl_interface_pb2.SL_INTERFACE_EVENT_TYPE_INTERFACE_INFO:
            log.error('Received Interface Event:', response)
        else:
            log.error('Received an unexpected event type %d' %(
                response.EventType))
            return False
        # Continue looping on events
        return True

    # Wait on Intf notification events
    @staticmethod
    def intf_get_notif(event, thread_count):
        # This would notify the main thread to proceed
        event.set()
        # RPC to get Notifications
        response = TestSuite_009_INTERFACE.intf_notif.intf_get_notif(intf_notif_cback)
        # Above, Should return on errors
        log.info('intf_get_notif: thread %d exiting. response: %s' %(thread_count,
            response))
        # Do not exit the process, as other tests could be still going

    @staticmethod
    def validate_intf_regop_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.ErrStatus.Status):
            return True
        # Error cases
        log.error('Response Error code 0x%x' %(response.ErrStatus.Status))
        return False

    # Print Received BFD Stats
    @staticmethod
    def print_intf_stats(response):
        if (response.ErrStatus.Status ==
            sl_common_types_pb2.SLErrorStatus.SL_SUCCESS):
            log.info(response)
        else:
            log.error('Intf Stats response Error 0x%x' %(response.ErrStatus.Status))
            return False
        return True


    @staticmethod
    def validate_intf_response(response):
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
                response.StatusSummary.Status):
            return True
        # Error cases
        log.error('Batch Error code 0x%x' %(response.StatusSummary.Status))
        # SOME ERROR
        if (sl_common_types_pb2.SLErrorStatus.SL_SOME_ERR ==
                response.StatusSummary.Status):
            log.error(response)
        return False

    @staticmethod
    def validate_intf_get_response(response):
        log.info('Intf Get Attributes:')
        log.info(response)
        if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS !=
                response.ErrStatus.Status):
            return False
        return True
