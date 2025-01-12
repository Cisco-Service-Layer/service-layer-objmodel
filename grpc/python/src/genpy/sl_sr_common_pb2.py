# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl_sr_common.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12sl_sr_common.proto\x12\rservice_layer\" \n\x0fSLSrPolicyFlags\x12\r\n\x05\x46lags\x18\x01 \x01(\r\"@\n\x08SLSrBsid\x12\x12\n\x08MplsBsid\x18\x01 \x01(\rH\x00\x12\x12\n\x08Srv6Bsid\x18\x02 \x01(\x0cH\x00\x42\x0c\n\nBindingSid\"\x1a\n\nSLSrCpName\x12\x0c\n\x04Name\x18\x01 \x01(\t\"\xd8\x01\n\x0fSLSrSegmentDesc\x12\x11\n\tAlgorithm\x18\x01 \x01(\r\x12\x17\n\rIpv4LocalAddr\x18\x02 \x01(\x0cH\x00\x12\x17\n\rIpv6LocalAddr\x18\x03 \x01(\x0cH\x00\x12\x18\n\x0eIpv4RemoteAddr\x18\x04 \x01(\x0cH\x01\x12\x18\n\x0eIpv6RemoteAddr\x18\x05 \x01(\x0cH\x01\x12\x17\n\x0fLocalNodeIntfId\x18\x06 \x01(\r\x12\x18\n\x10RemoteNodeIntfId\x18\x07 \x01(\rB\x0b\n\tLocalNodeB\x0c\n\nRemoteNode\"\xa2\x02\n\x0bSLSrSegment\x12,\n\x04Type\x18\x01 \x01(\x0e\x32\x1e.service_layer.SLSrSegmentType\x12\r\n\x05\x46lags\x18\x02 \x01(\r\x12\x13\n\tMplsLabel\x18\x03 \x01(\rH\x00\x12\x11\n\x07Srv6Sid\x18\x04 \x01(\x0cH\x00\x12\x33\n\x0bSegmentDesc\x18\x05 \x01(\x0b\x32\x1e.service_layer.SLSrSegmentDesc\x12?\n\x10\x45ndPointBehavior\x18\x06 \x01(\x0b\x32%.service_layer.SLSrv6EndPointBehavior\x12\x31\n\tSidStruct\x18\x07 \x01(\x0b\x32\x1e.service_layer.SLSrv6SidStructB\x05\n\x03Sid\"\xba\x01\n\x10SLSrv6BindingSid\x12\r\n\x05\x46lags\x18\x01 \x01(\r\x12\x0c\n\x04\x42sid\x18\x02 \x01(\x0c\x12\x15\n\rSpecifiedBsid\x18\x03 \x01(\x0c\x12?\n\x10\x45ndPointBehavior\x18\x04 \x01(\x0b\x32%.service_layer.SLSrv6EndPointBehavior\x12\x31\n\tSidStruct\x18\x05 \x01(\x0b\x32\x1e.service_layer.SLSrv6SidStruct\"T\n\x16SLSrv6EndPointBehavior\x12\x18\n\x10\x45ndPointBehavior\x18\x01 \x01(\r\x12\r\n\x05\x46lags\x18\x02 \x01(\r\x12\x11\n\tAlgorithm\x18\x03 \x01(\r\"g\n\x0fSLSrv6SidStruct\x12\x17\n\x0fLocatorBlockLen\x18\x01 \x01(\r\x12\x16\n\x0eLocatorNodeLen\x18\x02 \x01(\r\x12\x13\n\x0b\x46unctionLen\x18\x03 \x01(\r\x12\x0e\n\x06\x41rgLen\x18\x04 \x01(\r*\x90\x03\n\x18SLSrPolicyProtocolOrigin\x12)\n%SL_SR_POLICY_PROTOCOL_ORIGIN_RESERVED\x10\x00\x12%\n!SL_SR_POLICY_PROTOCOL_ORIGIN_PCEP\x10\x01\x12.\n*SL_SR_POLICY_PROTOCOL_ORIGIN_BGP_SR_POLICY\x10\x02\x12\'\n#SL_SR_POLICY_PROTOCOL_ORIGIN_CONFIG\x10\x03\x12-\n)SL_SR_POLICY_PROTOCOL_ORIGIN_PCEP_VIA_PCE\x10\n\x12\x36\n2SL_SR_POLICY_PROTOCOL_ORIGIN_BGP_SR_POLICY_VIA_PCE\x10\x14\x12/\n+SL_SR_POLICY_PROTOCOL_ORIGIN_CONFIG_VIA_PCE\x10\x1e\x12\x31\n,SL_SR_POLICY_PROTOCOL_ORIGIN_CONFIG_VIA_GRPC\x10\xfb\x01*}\n\x12SLSrPolicyFlagsDef\x12\x1e\n\x1aSL_SR_POLICY_FLAG_RESERVED\x10\x00\x12\"\n\x1dSL_SR_POLICY_FLAG_ENDPOINT_V6\x10\x80\x01\x12#\n\x1fSL_SR_POLICY_FLAG_ORIGINATOR_V6\x10@*\x9b\x04\n\x0fSLSrSegmentType\x12\x1b\n\x17SL_SR_SEG_TYPE_RESERVED\x10\x00\x12\x1d\n\x19SL_SR_SEG_TYPE_MPLS_LABEL\x10\x01\x12\x1e\n\x1aSL_SR_SEG_TYPE_SRV6_SID_V6\x10\x02\x12\"\n\x1eSL_SR_SEG_TYPE_MPLS_PFX_SID_V4\x10\x03\x12\"\n\x1eSL_SR_SEG_TYPE_MPLS_PFX_SID_V6\x10\x04\x12\x33\n/SL_SR_SEG_TYPE_MPLS_ADJ_SID_V4_NODE_ADDR_LOC_ID\x10\x05\x12/\n+SL_SR_SEG_TYPE_MPLS_ADJ_SID_V4_LOC_REM_ADDR\x10\x06\x12\x36\n2SL_SR_SEG_TYPE_MPLS_ADJ_SID_V6_LOC_REM_ADDR_AND_ID\x10\x07\x12/\n+SL_SR_SEG_TYPE_MPLS_ADJ_SID_V6_LOC_REM_ADDR\x10\x08\x12,\n(SL_SR_SEG_TYPE_SRV6_END_SID_V6_NODE_ADDR\x10\t\x12\x36\n2SL_SR_SEG_TYPE_SRV6_END_SID_V6_LOC_REM_ADDR_AND_ID\x10\n\x12/\n+SL_SR_SEG_TYPE_SRV6_END_SID_V6_LOC_REM_ADDR\x10\x0b*\x80\x02\n\x10SLSrSegmentFlags\x12\x1f\n\x1bSL_SR_SEGMENT_FLAG_RESERVED\x10\x00\x12$\n\x1eSL_SR_SEGMENT_FLAG_SID_PRESENT\x10\x80\x80\x02\x12\x31\n+SL_SR_SEGMENT_FLAG_SID_EXPLICIT_PROVISIONED\x10\x80\x80\x01\x12$\n\x1fSL_SR_SEGMENT_FLAG_SID_VERIFIED\x10\x80@\x12$\n\x1fSL_SR_SEGMENT_FLAG_SID_RESOLVED\x10\x80 \x12&\n!SL_SR_SEGMENT_FLAG_SID_ALGO_VALID\x10\x80\x10*\x9b\x01\n\x15SLSrv6BindingSidFlags\x12\x1e\n\x1aSL_SRV6_BSID_FLAG_RESERVED\x10\x00\x12!\n\x1bSL_SRV6_BSID_FLAG_ALLOCATED\x10\x80\x80\x02\x12\x1f\n\x19SL_SRV6_BSID_FLAG_UNAVAIL\x10\x80\x80\x01\x12\x1e\n\x19SL_SRV6_BSID_FLAG_DYNAMIC\x10\x80@BQZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sl_sr_common_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layer'
  _globals['_SLSRPOLICYPROTOCOLORIGIN']._serialized_start=1058
  _globals['_SLSRPOLICYPROTOCOLORIGIN']._serialized_end=1458
  _globals['_SLSRPOLICYFLAGSDEF']._serialized_start=1460
  _globals['_SLSRPOLICYFLAGSDEF']._serialized_end=1585
  _globals['_SLSRSEGMENTTYPE']._serialized_start=1588
  _globals['_SLSRSEGMENTTYPE']._serialized_end=2127
  _globals['_SLSRSEGMENTFLAGS']._serialized_start=2130
  _globals['_SLSRSEGMENTFLAGS']._serialized_end=2386
  _globals['_SLSRV6BINDINGSIDFLAGS']._serialized_start=2389
  _globals['_SLSRV6BINDINGSIDFLAGS']._serialized_end=2544
  _globals['_SLSRPOLICYFLAGS']._serialized_start=37
  _globals['_SLSRPOLICYFLAGS']._serialized_end=69
  _globals['_SLSRBSID']._serialized_start=71
  _globals['_SLSRBSID']._serialized_end=135
  _globals['_SLSRCPNAME']._serialized_start=137
  _globals['_SLSRCPNAME']._serialized_end=163
  _globals['_SLSRSEGMENTDESC']._serialized_start=166
  _globals['_SLSRSEGMENTDESC']._serialized_end=382
  _globals['_SLSRSEGMENT']._serialized_start=385
  _globals['_SLSRSEGMENT']._serialized_end=675
  _globals['_SLSRV6BINDINGSID']._serialized_start=678
  _globals['_SLSRV6BINDINGSID']._serialized_end=864
  _globals['_SLSRV6ENDPOINTBEHAVIOR']._serialized_start=866
  _globals['_SLSRV6ENDPOINTBEHAVIOR']._serialized_end=950
  _globals['_SLSRV6SIDSTRUCT']._serialized_start=952
  _globals['_SLSRV6SIDSTRUCT']._serialized_end=1055
# @@protoc_insertion_point(module_scope)
