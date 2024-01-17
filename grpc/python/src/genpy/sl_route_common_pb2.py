# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl_route_common.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import sl_common_types_pb2 as sl__common__types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15sl_route_common.proto\x12\rservice_layer\x1a\x15sl_common_types.proto\"\x16\n\x14SLRouteGlobalsGetMsg\"\x86\x01\n\x17SLRouteGlobalsGetMsgRsp\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x1d\n\x15MaxVrfregPerVrfregmsg\x18\x02 \x01(\r\x12\x1b\n\x13MaxRoutePerRoutemsg\x18\x03 \x01(\r\"\x1a\n\x18SLRouteGlobalStatsGetMsg\"t\n\x1bSLRouteGlobalStatsGetMsgRsp\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x10\n\x08VrfCount\x18\x02 \x01(\r\x12\x12\n\nRouteCount\x18\x03 \x01(\r\"S\n\x08SLVrfReg\x12\x0f\n\x07VrfName\x18\x01 \x01(\t\x12\x15\n\rAdminDistance\x18\x02 \x01(\r\x12\x1f\n\x17VrfPurgeIntervalSeconds\x18\x03 \x01(\r\"`\n\x0bSLVrfRegMsg\x12$\n\x04Oper\x18\x01 \x01(\x0e\x32\x16.service_layer.SLRegOp\x12+\n\nVrfRegMsgs\x18\x02 \x03(\x0b\x32\x17.service_layer.SLVrfReg\"R\n\x0eSLVrfRegMsgRes\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x0f\n\x07VrfName\x18\x02 \x01(\t\"u\n\x0eSLVrfRegMsgRsp\x12\x33\n\rStatusSummary\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12.\n\x07Results\x18\x02 \x03(\x0b\x32\x1d.service_layer.SLVrfRegMsgRes\"H\n\x0eSLVrfRegGetMsg\x12\x0f\n\x07VrfName\x18\x01 \x01(\t\x12\x14\n\x0c\x45ntriesCount\x18\x02 \x01(\r\x12\x0f\n\x07GetNext\x18\x03 \x01(\x08\"{\n\x11SLVrfRegGetMsgRsp\x12\x0b\n\x03\x45of\x18\x01 \x01(\x08\x12/\n\tErrStatus\x18\x02 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12(\n\x07\x45ntries\x18\x03 \x03(\x0b\x32\x17.service_layer.SLVrfReg\":\n\x13SLVRFGetStatsMsgRes\x12\x0f\n\x07VrfName\x18\x01 \x01(\t\x12\x12\n\nRouteCount\x18\x02 \x01(\r\"\x88\x01\n\x13SLVRFGetStatsMsgRsp\x12\x0b\n\x03\x45of\x18\x01 \x01(\x08\x12/\n\tErrStatus\x18\x02 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x33\n\x07\x45ntries\x18\x03 \x03(\x0b\x32\".service_layer.SLVRFGetStatsMsgRes\"\x88\x01\n\x12SLRouteGetNotifMsg\x12&\n\x04Oper\x18\x01 \x01(\x0e\x32\x18.service_layer.SLNotifOp\x12\x12\n\nCorrelator\x18\x02 \x01(\x04\x12\x0f\n\x07VrfName\x18\x03 \x01(\t\x12\x10\n\x08SrcProto\x18\x04 \x01(\t\x12\x13\n\x0bSrcProtoTag\x18\x05 \x01(\t\"l\n\x12SLRouteNotifStatus\x12\x12\n\nCorrelator\x18\x01 \x01(\x04\x12\x0f\n\x07VrfName\x18\x02 \x01(\t\x12\x31\n\x0bNotifStatus\x18\x03 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\"%\n\x12SLRouteNotifMarker\x12\x0f\n\x07VrfName\x18\x01 \x01(\t\"H\n\nSLVrfNotif\x12\x0f\n\x07VrfName\x18\x01 \x01(\t\x12)\n\x06Status\x18\x02 \x01(\x0e\x32\x19.service_layer.SLObjectOp\"}\n\rSLRouteCommon\x12\x15\n\rAdminDistance\x18\x01 \x01(\r\x12\x12\n\nLocalLabel\x18\x02 \x01(\r\x12\x0b\n\x03Tag\x18\x03 \x01(\r\x12\x10\n\x08SrcProto\x18\x04 \x01(\t\x12\x13\n\x0bSrcProtoTag\x18\x05 \x01(\t\x12\r\n\x05\x46lags\x18\x06 \x01(\r\"\xb1\x01\n\x0bSLVxLANPath\x12\x0b\n\x03VNI\x18\x01 \x01(\r\x12\x18\n\x10SourceMacAddress\x18\x02 \x01(\x0c\x12\x16\n\x0e\x44\x65stMacAddress\x18\x03 \x01(\x0c\x12\x30\n\x0cSrcIpAddress\x18\x04 \x01(\x0b\x32\x1a.service_layer.SLIpAddress\x12\x31\n\rDestIpAddress\x18\x05 \x01(\x0b\x32\x1a.service_layer.SLIpAddress\"\xab\x03\n\x0bSLRoutePath\x12\x32\n\x0eNexthopAddress\x18\x01 \x01(\x0b\x32\x1a.service_layer.SLIpAddress\x12\x34\n\x10NexthopInterface\x18\x02 \x01(\x0b\x32\x1a.service_layer.SLInterface\x12\x12\n\nLoadMetric\x18\x03 \x01(\r\x12\x0f\n\x07VrfName\x18\x04 \x01(\t\x12\x0e\n\x06Metric\x18\x05 \x01(\r\x12\x0e\n\x06PathId\x18\x06 \x01(\r\x12\x1b\n\x13ProtectedPathBitmap\x18\x07 \x03(\x04\x12\x12\n\nLabelStack\x18\x08 \x03(\r\x12\x31\n\rRemoteAddress\x18\t \x03(\x0b\x32\x1a.service_layer.SLIpAddress\x12-\n\tEncapType\x18\n \x01(\x0e\x32\x1a.service_layer.SLEncapType\x12\x1c\n\x14VtepRouterMacAddress\x18\x0b \x01(\x0c\x12-\n\tVxLANPath\x18\x0c \x01(\x0b\x32\x1a.service_layer.SLVxLANPath\x12\r\n\x05\x46lags\x18\r \x01(\r*\xca\x01\n\x0bSLNotifType\x12\x1a\n\x16SL_EVENT_TYPE_RESERVED\x10\x00\x12\x17\n\x13SL_EVENT_TYPE_ERROR\x10\x01\x12\x18\n\x14SL_EVENT_TYPE_STATUS\x10\x02\x12\x17\n\x13SL_EVENT_TYPE_ROUTE\x10\x03\x12\x1e\n\x1aSL_EVENT_TYPE_START_MARKER\x10\x04\x12\x1c\n\x18SL_EVENT_TYPE_END_MARKER\x10\x05\x12\x15\n\x11SL_EVENT_TYPE_VRF\x10\x06*M\n\x0cSLRouteFlags\x12\x1a\n\x16SL_ROUTE_FLAG_RESERVED\x10\x00\x12!\n\x1dSL_ROUTE_FLAG_PREFER_OVER_LDP\x10\x01*J\n\x0bSLPathFlags\x12\x19\n\x15SL_PATH_FLAG_RESERVED\x10\x00\x12 \n\x1cSL_PATH_FLAG_SINGLE_PATH_OPT\x10\x01\x42QZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sl_route_common_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layer'
  _globals['_SLNOTIFTYPE']._serialized_start=2254
  _globals['_SLNOTIFTYPE']._serialized_end=2456
  _globals['_SLROUTEFLAGS']._serialized_start=2458
  _globals['_SLROUTEFLAGS']._serialized_end=2535
  _globals['_SLPATHFLAGS']._serialized_start=2537
  _globals['_SLPATHFLAGS']._serialized_end=2611
  _globals['_SLROUTEGLOBALSGETMSG']._serialized_start=63
  _globals['_SLROUTEGLOBALSGETMSG']._serialized_end=85
  _globals['_SLROUTEGLOBALSGETMSGRSP']._serialized_start=88
  _globals['_SLROUTEGLOBALSGETMSGRSP']._serialized_end=222
  _globals['_SLROUTEGLOBALSTATSGETMSG']._serialized_start=224
  _globals['_SLROUTEGLOBALSTATSGETMSG']._serialized_end=250
  _globals['_SLROUTEGLOBALSTATSGETMSGRSP']._serialized_start=252
  _globals['_SLROUTEGLOBALSTATSGETMSGRSP']._serialized_end=368
  _globals['_SLVRFREG']._serialized_start=370
  _globals['_SLVRFREG']._serialized_end=453
  _globals['_SLVRFREGMSG']._serialized_start=455
  _globals['_SLVRFREGMSG']._serialized_end=551
  _globals['_SLVRFREGMSGRES']._serialized_start=553
  _globals['_SLVRFREGMSGRES']._serialized_end=635
  _globals['_SLVRFREGMSGRSP']._serialized_start=637
  _globals['_SLVRFREGMSGRSP']._serialized_end=754
  _globals['_SLVRFREGGETMSG']._serialized_start=756
  _globals['_SLVRFREGGETMSG']._serialized_end=828
  _globals['_SLVRFREGGETMSGRSP']._serialized_start=830
  _globals['_SLVRFREGGETMSGRSP']._serialized_end=953
  _globals['_SLVRFGETSTATSMSGRES']._serialized_start=955
  _globals['_SLVRFGETSTATSMSGRES']._serialized_end=1013
  _globals['_SLVRFGETSTATSMSGRSP']._serialized_start=1016
  _globals['_SLVRFGETSTATSMSGRSP']._serialized_end=1152
  _globals['_SLROUTEGETNOTIFMSG']._serialized_start=1155
  _globals['_SLROUTEGETNOTIFMSG']._serialized_end=1291
  _globals['_SLROUTENOTIFSTATUS']._serialized_start=1293
  _globals['_SLROUTENOTIFSTATUS']._serialized_end=1401
  _globals['_SLROUTENOTIFMARKER']._serialized_start=1403
  _globals['_SLROUTENOTIFMARKER']._serialized_end=1440
  _globals['_SLVRFNOTIF']._serialized_start=1442
  _globals['_SLVRFNOTIF']._serialized_end=1514
  _globals['_SLROUTECOMMON']._serialized_start=1516
  _globals['_SLROUTECOMMON']._serialized_end=1641
  _globals['_SLVXLANPATH']._serialized_start=1644
  _globals['_SLVXLANPATH']._serialized_end=1821
  _globals['_SLROUTEPATH']._serialized_start=1824
  _globals['_SLROUTEPATH']._serialized_end=2251
# @@protoc_insertion_point(module_scope)
