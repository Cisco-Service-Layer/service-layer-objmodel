#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
import json
import ipaddress
import os
import unittest

from lindt import serializers
from genpy import (
    sl_common_types_pb2,
    sl_route_common_pb2,
    sl_route_ipv4_pb2
)


class SerializerTestCase(unittest.TestCase):
    def setUp(self):
        filepath = os.path.join(os.path.dirname(__file__), 'template.json')
        with open(filepath) as fp:
            context = json.loads(fp.read())
        self.context = context

    def test_ipv4_serializer(self):
        # To be completed.
        params = (
            self.context['batch_v4_route'],
            self.context['paths'],
            self.context['nexthops'],
        )
        serializer = serializers.route_serializer(*params)
        self.assertTrue(
            isinstance(serializer, sl_route_ipv4_pb2.SLRoutev4Msg)
        )
        self.assertEqual(serializer.sl_vrf_name, 'default')
        for route in serializer.sl_routes:
            for r in self.context['batch_v4_route']['routes']:
                self.assertTrue(
                    isinstance(route, sl_route_ipv4_pb2.SLRoutev4)
                )
                self.assertTrue(
                    isinstance(
                        route.sl_ipv4_prefix,
                        sl_route_common_pb2.SLIpv4Prefix
                    )
                )
                self.assertTrue(
                    isinstance(
                        route.sl_ipv4_prefix.sl_ipv4_address,
                        sl_common_types_pb2.SLIpv4Address
                    )
                )
                self.assertEqual(
                    route.sl_ipv4_prefix.sl_ipv4_address.sl_ipv4_prefix,
                    int(ipaddress.ip_address(r['prefix']))
                )
                self.assertTrue(
                    isinstance(
                        route.sl_ipv4_prefix.sl_prefix_len,
                        sl_common_types_pb2.SLIpPrefixLen
                    )
                )
                self.assertEqual(
                    route.sl_ipv4_prefix.sl_prefix_len.sl_ip_prefix_len,
                    r['prefix_len']
                )
                self.assertTrue(
                    isinstance(
                        route.sl_route_common,
                        sl_route_common_pb2.SLRouteCommon
                    )
                )

if __name__ == '__main__':
    unittest.main()
