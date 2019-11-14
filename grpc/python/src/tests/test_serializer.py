#
# Copyright (c) 2016 by cisco Systems, Inc.
# All rights reserved.
#
import json
import ipaddress
import os
import unittest
import ipaddress
import itertools
from collections import Counter
from sl_api import serializers
from genpy import (
    sl_common_types_pb2,
    sl_route_common_pb2,
    sl_route_ipv4_pb2,
    sl_route_ipv4_pb2,
    sl_mpls_pb2
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


class IlmSerializerTestCase(unittest.TestCase):
    def setUp(self):
        filepath = os.path.join(os.path.dirname(__file__), 'template.json')
        with open(filepath) as fp:
            context = json.loads(fp.read())
        self.context = context

    def test_ilm_serializer_v4(self):
        params = (
            self.context['batch_ilm'],
            4,
            self.context['paths'],
            self.context['nexthops'],
        )
        serializer, _ = serializers.ilm_serializer(*params)
        self.assertTrue(
            isinstance(serializer, sl_mpls_pb2.SLMplsIlmMsg)
        )
        batch = self.context['batch_ilm']
        expectedLabel = (ilm['in_label'] + i for ilm in batch['ilms'] for i in range(ilm['range']))

        print('Number of ILMs', len(serializer.MplsIlms))
        for ilm in sorted(serializer.MplsIlms, key=lambda x: x.Key.LocalLabel):
            self.assertTrue(
                isinstance(ilm, sl_mpls_pb2.SLMplsIlmEntry)
            )

            print('Label:', ilm.Key.LocalLabel)
            self.assertEqual(next(expectedLabel), ilm.Key.LocalLabel)
            for path in ilm.Paths:
                self.assertTrue(
                    isinstance(path, sl_mpls_pb2.SLMplsPath)
                )
                self.assertTrue(
                    isinstance(path.NexthopAddress, sl_common_types_pb2.SLIpAddress)
                )
                self.assertTrue(
                    isinstance(path.NexthopInterface, sl_common_types_pb2.SLInterface)
                )
                print('Address:', ipaddress.ip_address(path.NexthopAddress.V4Address))
                print('Name:', path.NexthopInterface.Name)

            print()

class CosIlmSerializerTestCase1(unittest.TestCase):
    testCase = 'scale_cos_ilm_1'

    def getLabelRange(self, batch):
        if 'label_ranges' in batch:
            start = batch['label_ranges'][0]['range'][0]
            end = batch['label_ranges'][-1]['range'][1]
            return start, end

        return batch.get('label_range') 

    def ilm_op_stub(self, params):
        # Create generator for all the ILMS
        start, end = self.getLabelRange(params[0])
        ilms = serializers.generateIlms(*params)

        output = []
        numIlms = (end - start + 1) * len(params[0]['exps'])
        label_counts = Counter()
        exp_counts = Counter()
        # Create generator for all the ILMS
        ilms = serializers.generateIlms(*params)

        for batch in serializers.genBatches(ilms, params[0]['batch_size']):
            params[0]['ilms'] = batch
            serializer, _ = serializers.ilm_serializer(*params)
            assert (len(serializer.MplsIlms) == params[0]['batch_size'] or 
                    len(serializer.MplsIlms) == numIlms % params[0]['batch_size'])
            output.extend(serializer.MplsIlms)
            for ilm in serializer.MplsIlms:
                label_counts[str(ilm.Key.LocalLabel)] += 1
                exp_counts[str(ilm.Key.SlMplsCosVal)] += 1
       
        # Check each label has the right number of exps
        assert all(v == len(params[0]['exps']) for v in label_counts.values()) 
        # Check the same but in reverse 
        assert all(v == (end - start + 1) for v in exp_counts.values()) 
        # Check total number of exps
        assert len(output) == numIlms

    def setUp(self):
        filepath = os.path.join(os.path.dirname(__file__), 'template.json')
        with open(filepath) as fp:
            context = json.loads(fp.read())
        self.context = context

    def test_ilm_serializer_cos_v4(self):
        for i in range(1, 257):
            params = (
                self.context[self.testCase],
                4,
                self.context['paths'],
                self.context['nexthops'],
                )
            params[0]['batch_size'] = i
            self.ilm_op_stub(params)


class CosIlmSerializerTestCase2(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_2'

class CosIlmSerializerTestCase3(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_3'

class CosIlmSerializerTestCase4(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_4'

class CosIlmSerializerTestCase5(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_pop_and_lookup'

class CosIlmSerializerTestCase6(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_v4_v6'

class CosIlmSerializerTestCase7(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_update_1'

class CosIlmSerializerTestCase8(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_update_2'

class CosIlmSerializerTestCase9(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_update_3'

class CosIlmSerializerTestCase10(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_update_4'

class CosIlmSerializerTestCase11(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_update_pop_and_lookup'

class CosIlmSerializerTestCase12(CosIlmSerializerTestCase1):
    testCase = 'scale_cos_ilm_update_v4_v6'


if __name__ == '__main__':
    unittest.main()
