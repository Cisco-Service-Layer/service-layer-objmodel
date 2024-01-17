# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl_bfd_ipv6.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import sl_common_types_pb2 as sl__common__types__pb2
from . import sl_bfd_common_pb2 as sl__bfd__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11sl_bfd_ipv6.proto\x12\rservice_layer\x1a\x15sl_common_types.proto\x1a\x13sl_bfd_common.proto\"\x99\x01\n\nSLBfdv6Key\x12&\n\x04Type\x18\x01 \x01(\x0e\x32\x18.service_layer.SLBfdType\x12\x0f\n\x07VrfName\x18\x02 \x01(\t\x12\x0f\n\x07NbrAddr\x18\x03 \x01(\x0c\x12-\n\tInterface\x18\x04 \x01(\x0b\x32\x1a.service_layer.SLInterface\x12\x12\n\nSourceAddr\x18\x05 \x01(\x0c\"m\n\x11SLBfdv6SessionCfg\x12&\n\x03Key\x18\x01 \x01(\x0b\x32\x19.service_layer.SLBfdv6Key\x12\x30\n\x06\x43onfig\x18\x02 \x01(\x0b\x32 .service_layer.SLBfdConfigCommon\"i\n\nSLBfdv6Msg\x12\'\n\x04Oper\x18\x01 \x01(\x0e\x32\x19.service_layer.SLObjectOp\x12\x32\n\x08Sessions\x18\x02 \x03(\x0b\x32 .service_layer.SLBfdv6SessionCfg\"e\n\nSLBfdv6Res\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12&\n\x03Key\x18\x02 \x01(\x0b\x32\x19.service_layer.SLBfdv6Key\"p\n\rSLBfdv6MsgRsp\x12\x33\n\rStatusSummary\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12*\n\x07Results\x18\x02 \x03(\x0b\x32\x19.service_layer.SLBfdv6Res\"n\n\rSLBfdv6GetMsg\x12&\n\x03Key\x18\x01 \x01(\x0b\x32\x19.service_layer.SLBfdv6Key\x12\x0e\n\x06SeqNum\x18\x02 \x01(\x04\x12\x14\n\x0c\x45ntriesCount\x18\x03 \x01(\r\x12\x0f\n\x07GetNext\x18\x04 \x01(\x08\"\xa2\x01\n\x16SLBfdv6SessionCfgState\x12&\n\x03Key\x18\x01 \x01(\x0b\x32\x19.service_layer.SLBfdv6Key\x12\x30\n\x06\x43onfig\x18\x02 \x01(\x0b\x32 .service_layer.SLBfdConfigCommon\x12.\n\x05State\x18\x03 \x01(\x0b\x32\x1f.service_layer.SLBfdCommonState\"\x88\x01\n\x10SLBfdv6GetMsgRsp\x12\x0b\n\x03\x45of\x18\x01 \x01(\x08\x12/\n\tErrStatus\x18\x02 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x36\n\x07\x45ntries\x18\x03 \x03(\x0b\x32%.service_layer.SLBfdv6SessionCfgState\"m\n\x13SLBfdv6SessionState\x12&\n\x03Key\x18\x01 \x01(\x0b\x32\x19.service_layer.SLBfdv6Key\x12.\n\x05State\x18\x02 \x01(\x0b\x32\x1f.service_layer.SLBfdCommonState\"\xb3\x01\n\x0cSLBfdv6Notif\x12\x30\n\tEventType\x18\x01 \x01(\x0e\x32\x1d.service_layer.SLBfdNotifType\x12\x31\n\tErrStatus\x18\x02 \x01(\x0b\x32\x1c.service_layer.SLErrorStatusH\x00\x12\x35\n\x07Session\x18\x03 \x01(\x0b\x32\".service_layer.SLBfdv6SessionStateH\x00\x42\x07\n\x05\x45vent2\xee\x03\n\x0bSLBfdv6Oper\x12I\n\x0cSLBfdv6RegOp\x12\x1a.service_layer.SLBfdRegMsg\x1a\x1d.service_layer.SLBfdRegMsgRsp\x12G\n\nSLBfdv6Get\x12\x1a.service_layer.SLBfdGetMsg\x1a\x1d.service_layer.SLBfdGetMsgRsp\x12Q\n\x0fSLBfdv6GetStats\x12\x1a.service_layer.SLBfdGetMsg\x1a\".service_layer.SLBfdGetStatsMsgRsp\x12W\n\x15SLBfdv6GetNotifStream\x12\x1f.service_layer.SLBfdGetNotifMsg\x1a\x1b.service_layer.SLBfdv6Notif0\x01\x12K\n\x10SLBfdv6SessionOp\x12\x19.service_layer.SLBfdv6Msg\x1a\x1c.service_layer.SLBfdv6MsgRsp\x12R\n\x11SLBfdv6SessionGet\x12\x1c.service_layer.SLBfdv6GetMsg\x1a\x1f.service_layer.SLBfdv6GetMsgRspBQZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sl_bfd_ipv6_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layer'
  _globals['_SLBFDV6KEY']._serialized_start=81
  _globals['_SLBFDV6KEY']._serialized_end=234
  _globals['_SLBFDV6SESSIONCFG']._serialized_start=236
  _globals['_SLBFDV6SESSIONCFG']._serialized_end=345
  _globals['_SLBFDV6MSG']._serialized_start=347
  _globals['_SLBFDV6MSG']._serialized_end=452
  _globals['_SLBFDV6RES']._serialized_start=454
  _globals['_SLBFDV6RES']._serialized_end=555
  _globals['_SLBFDV6MSGRSP']._serialized_start=557
  _globals['_SLBFDV6MSGRSP']._serialized_end=669
  _globals['_SLBFDV6GETMSG']._serialized_start=671
  _globals['_SLBFDV6GETMSG']._serialized_end=781
  _globals['_SLBFDV6SESSIONCFGSTATE']._serialized_start=784
  _globals['_SLBFDV6SESSIONCFGSTATE']._serialized_end=946
  _globals['_SLBFDV6GETMSGRSP']._serialized_start=949
  _globals['_SLBFDV6GETMSGRSP']._serialized_end=1085
  _globals['_SLBFDV6SESSIONSTATE']._serialized_start=1087
  _globals['_SLBFDV6SESSIONSTATE']._serialized_end=1196
  _globals['_SLBFDV6NOTIF']._serialized_start=1199
  _globals['_SLBFDV6NOTIF']._serialized_end=1378
  _globals['_SLBFDV6OPER']._serialized_start=1381
  _globals['_SLBFDV6OPER']._serialized_end=1875
# @@protoc_insertion_point(module_scope)
