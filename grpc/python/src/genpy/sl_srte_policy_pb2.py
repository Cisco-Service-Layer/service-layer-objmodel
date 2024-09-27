# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl_srte_policy.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import sl_common_types_pb2 as sl__common__types__pb2
from . import sl_sr_common_pb2 as sl__sr__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14sl_srte_policy.proto\x12\rservice_layer\x1a\x15sl_common_types.proto\x1a\x12sl_sr_common.proto\"E\n\x0eSLSrExplicitCP\x12\x33\n\x0bsegmentList\x18\x01 \x03(\x0b\x32\x1e.service_layer.SLSrSegmentList\"\xc5\x03\n\x0fSLSrConstraints\x12\x31\n\naffinities\x18\x01 \x01(\x0b\x32\x1d.service_layer.SLSrAffinities\x12\x35\n\x0cmetricBounds\x18\x02 \x01(\x0b\x32\x1f.service_layer.SLSrMetricBounds\x12M\n\x12segmentConstraints\x18\x03 \x01(\x0b\x32\x31.service_layer.SLSrConstraints.SegmentConstraints\x1a\xf8\x01\n\x12SegmentConstraints\x12T\n\nprotection\x18\x01 \x01(\x0e\x32@.service_layer.SLSrConstraints.SegmentConstraints.ProtectionType\x12\x0f\n\x07sidalgo\x18\x02 \x01(\r\x12\x0b\n\x03MSD\x18\x03 \x01(\r\"n\n\x0eProtectionType\x12\x17\n\x13PROTECTED_PREFERRED\x10\x00\x12\x12\n\x0ePROTECTED_ONLY\x10\x01\x12\x19\n\x15UNPROTECTED_PREFERRED\x10\x02\x12\x14\n\x10UNPROTECTED_ONLY\x10\x03\"\xbd\x01\n\rSLSrDynamicCP\x12.\n\x07ometric\x18\x01 \x01(\x0e\x32\x1d.service_layer.SLSrMetricType\x12\x33\n\x0b\x63onstraints\x18\x02 \x01(\x0b\x32\x1e.service_layer.SLSrConstraints\x12\x35\n\x0cmetricMargin\x18\x03 \x01(\x0b\x32\x1f.service_layer.SLSrMetricMargin\x12\x10\n\x08\x64\x65legate\x18\x04 \x01(\x08\"\x82\x02\n\x11SLSrCandidatePath\x12\x30\n\x03key\x18\x01 \x01(\x0b\x32#.service_layer.SLSrCandidatePathKey\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\npreference\x18\x03 \x01(\r\x12/\n\tdataplane\x18\x04 \x01(\x0e\x32\x1c.service_layer.SLSrDataplane\x12/\n\x07\x64ynamic\x18\x05 \x01(\x0b\x32\x1c.service_layer.SLSrDynamicCPH\x00\x12\x31\n\x08\x65xplicit\x18\x06 \x01(\x0b\x32\x1d.service_layer.SLSrExplicitCPH\x00\x42\x04\n\x02\x43P\"d\n\x10SLSrv6BindingSID\x12\x13\n\x0blocatorName\x18\x01 \x01(\t\x12\x10\n\x08\x62\x65havior\x18\x02 \x01(\r\x12)\n\x03SID\x18\x03 \x01(\x0b\x32\x1c.service_layer.SLIpv6Address\"\xac\x01\n\x0eSLSrBindingSID\x12I\n\x14\x62indingSIDAllocation\x18\x01 \x01(\x0e\x32+.service_layer.SLSrBindingSIDAllocationMode\x12\x16\n\x0emplsBindingSID\x18\x02 \x01(\r\x12\x37\n\x0esrv6BindingSID\x18\x03 \x01(\x0b\x32\x1f.service_layer.SLSrv6BindingSID\"\xbf\x01\n\nSLSrPolicy\x12)\n\x03key\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLSrPolicyKey\x12\x17\n\x0ftransitEligible\x18\x02 \x01(\x08\x12-\n\x03\x43Ps\x18\x03 \x03(\x0b\x32 .service_layer.SLSrCandidatePath\x12+\n\x04\x62sid\x18\x04 \x01(\x0b\x32\x1d.service_layer.SLSrBindingSID\x12\x11\n\tprofileID\x18\x05 \x01(\r\"<\n\rSLSrPolicyMsg\x12+\n\x08policies\x18\x01 \x03(\x0b\x32\x19.service_layer.SLSrPolicy\"\xb8\x01\n\x0fSLSrPolicyOpRsp\x12;\n\tresponses\x18\x01 \x03(\x0b\x32(.service_layer.SLSrPolicyOpRsp.PolicyRsp\x1ah\n\tPolicyRsp\x12\x30\n\nreturnCode\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12)\n\x03key\x18\x02 \x01(\x0b\x32\x1c.service_layer.SLSrPolicyKey*C\n\x1cSLSrBindingSIDAllocationMode\x12\x11\n\rBSID_EXPLICIT\x10\x00\x12\x10\n\x0c\x42SID_DYNAMIC\x10\x01\x32\xaf\x01\n\x0cSLSrtePolicy\x12M\n\rSLSrPolicyAdd\x12\x1c.service_layer.SLSrPolicyMsg\x1a\x1e.service_layer.SLSrPolicyOpRsp\x12P\n\x10SLSrPolicyDelete\x12\x1c.service_layer.SLSrPolicyMsg\x1a\x1e.service_layer.SLSrPolicyOpRspBQZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sl_srte_policy_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layer'
  _globals['_SLSRBINDINGSIDALLOCATIONMODE']._serialized_start=1782
  _globals['_SLSRBINDINGSIDALLOCATIONMODE']._serialized_end=1849
  _globals['_SLSREXPLICITCP']._serialized_start=82
  _globals['_SLSREXPLICITCP']._serialized_end=151
  _globals['_SLSRCONSTRAINTS']._serialized_start=154
  _globals['_SLSRCONSTRAINTS']._serialized_end=607
  _globals['_SLSRCONSTRAINTS_SEGMENTCONSTRAINTS']._serialized_start=359
  _globals['_SLSRCONSTRAINTS_SEGMENTCONSTRAINTS']._serialized_end=607
  _globals['_SLSRCONSTRAINTS_SEGMENTCONSTRAINTS_PROTECTIONTYPE']._serialized_start=497
  _globals['_SLSRCONSTRAINTS_SEGMENTCONSTRAINTS_PROTECTIONTYPE']._serialized_end=607
  _globals['_SLSRDYNAMICCP']._serialized_start=610
  _globals['_SLSRDYNAMICCP']._serialized_end=799
  _globals['_SLSRCANDIDATEPATH']._serialized_start=802
  _globals['_SLSRCANDIDATEPATH']._serialized_end=1060
  _globals['_SLSRV6BINDINGSID']._serialized_start=1062
  _globals['_SLSRV6BINDINGSID']._serialized_end=1162
  _globals['_SLSRBINDINGSID']._serialized_start=1165
  _globals['_SLSRBINDINGSID']._serialized_end=1337
  _globals['_SLSRPOLICY']._serialized_start=1340
  _globals['_SLSRPOLICY']._serialized_end=1531
  _globals['_SLSRPOLICYMSG']._serialized_start=1533
  _globals['_SLSRPOLICYMSG']._serialized_end=1593
  _globals['_SLSRPOLICYOPRSP']._serialized_start=1596
  _globals['_SLSRPOLICYOPRSP']._serialized_end=1780
  _globals['_SLSRPOLICYOPRSP_POLICYRSP']._serialized_start=1676
  _globals['_SLSRPOLICYOPRSP_POLICYRSP']._serialized_end=1780
  _globals['_SLSRTEPOLICY']._serialized_start=1852
  _globals['_SLSRTEPOLICY']._serialized_end=2027
# @@protoc_insertion_point(module_scope)
