# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl_af.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import sl_common_types_pb2 as sl__common__types__pb2
from . import sl_route_common_pb2 as sl__route__common__pb2
from . import sl_route_ipv4_pb2 as sl__route__ipv4__pb2
from . import sl_route_ipv6_pb2 as sl__route__ipv6__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bsl_af.proto\x12\rservice_layer\x1a\x15sl_common_types.proto\x1a\x15sl_route_common.proto\x1a\x13sl_route_ipv4.proto\x1a\x13sl_route_ipv6.proto\"`\n\nSLAFVrfReg\x12)\n\x05Table\x18\x01 \x01(\x0e\x32\x1a.service_layer.SLTableType\x12\'\n\x06VrfReg\x18\x02 \x01(\x0b\x32\x17.service_layer.SLVrfReg\"d\n\rSLAFVrfRegMsg\x12$\n\x04Oper\x18\x01 \x01(\x0e\x32\x16.service_layer.SLRegOp\x12-\n\nVrfRegMsgs\x18\x02 \x03(\x0b\x32\x19.service_layer.SLAFVrfReg\"\x7f\n\x10SLAFVrfRegMsgRes\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x0f\n\x07VrfName\x18\x02 \x01(\t\x12)\n\x05Table\x18\x03 \x01(\x0e\x32\x1a.service_layer.SLTableType\"y\n\x10SLAFVrfRegMsgRsp\x12\x33\n\rStatusSummary\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x30\n\x07Results\x18\x02 \x03(\x0b\x32\x1f.service_layer.SLAFVrfRegMsgRes\"\"\n\x10SLAFVrfRegGetMsg\x12\x0e\n\x06GetAll\x18\x01 \x01(\x08\"\xad\x01\n\x13SLAFVrfRegGetMsgRsp\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x10\n\x08\x43lientID\x18\x02 \x01(\x04\x12)\n\x05Table\x18\x03 \x01(\x0e\x32\x1a.service_layer.SLTableType\x12(\n\x07\x45ntries\x18\x04 \x03(\x0b\x32\x17.service_layer.SLVrfReg\"\x9b\x02\n\x0bSLPathGroup\x12.\n\x0bPathGroupId\x18\x01 \x01(\x0b\x32\x19.service_layer.SLObjectId\x12\x15\n\rAdminDistance\x18\x02 \x01(\r\x12\x39\n\x08PathList\x18\x03 \x01(\x0b\x32%.service_layer.SLPathGroup.SLPathListH\x00\x12\r\n\x05\x46lags\x18\x04 \x01(\r\x1a\x32\n\x06SLPath\x12(\n\x04Path\x18\x01 \x01(\x0b\x32\x1a.service_layer.SLRoutePath\x1a>\n\nSLPathList\x12\x30\n\x05Paths\x18\x01 \x03(\x0b\x32!.service_layer.SLPathGroup.SLPathB\x07\n\x05\x65ntry\"\xb8\x01\n\x0bSLMplsEntry\x12\x12\n\nLocalLabel\x18\x01 \x01(\r\x12\x15\n\rAdminDistance\x18\x02 \x01(\r\x12,\n\x08PathList\x18\x03 \x03(\x0b\x32\x1a.service_layer.SLRoutePath\x12\x38\n\x0cPathGroupKey\x18\x04 \x01(\x0b\x32 .service_layer.SLPathGroupRefKeyH\x00\x12\r\n\x05\x46lags\x18\x05 \x01(\rB\x07\n\x05\x65ntry\"\xd5\x01\n\nSLAFObject\x12-\n\tIPv4Route\x18\x01 \x01(\x0b\x32\x18.service_layer.SLRoutev4H\x00\x12-\n\tIPv6Route\x18\x02 \x01(\x0b\x32\x18.service_layer.SLRoutev6H\x00\x12/\n\tMplsLabel\x18\x03 \x01(\x0b\x32\x1a.service_layer.SLMplsEntryH\x00\x12/\n\tPathGroup\x18\x04 \x01(\x0b\x32\x1a.service_layer.SLPathGroupH\x00\x42\x07\n\x05\x65ntry\"x\n\x06SLAFOp\x12+\n\x08\x41\x46Object\x18\x01 \x01(\x0b\x32\x19.service_layer.SLAFObject\x12\x13\n\x0bOperationID\x18\x02 \x01(\x04\x12,\n\x07\x41\x63kType\x18\x03 \x01(\x0e\x32\x1b.service_layer.SLRspACKType\"s\n\nSLAFGetMsg\x12\x0f\n\x07VrfName\x18\x01 \x01(\t\x12)\n\x05Table\x18\x02 \x01(\x0e\x32\x1a.service_layer.SLTableType\x12\x15\n\rGetAllClients\x18\x03 \x01(\x08\x12\x12\n\nMatchRegex\x18\x04 \x01(\t\"~\n\x12SLAFGetMsgRspEntry\x12#\n\x04\x41\x46Op\x18\x01 \x01(\x0b\x32\x15.service_layer.SLAFOp\x12/\n\tFIBStatus\x18\x02 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x12\n\nFIBVersion\x18\x03 \x01(\x04\"\x96\x01\n\rSLAFGetMsgRsp\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x0f\n\x07VrfName\x18\x02 \x01(\t\x12\x10\n\x08\x43lientID\x18\x03 \x01(\x04\x12\x31\n\x06\x41\x46List\x18\x04 \x03(\x0b\x32!.service_layer.SLAFGetMsgRspEntry\"j\n\x07SLAFMsg\x12\'\n\x04Oper\x18\x01 \x01(\x0e\x32\x19.service_layer.SLObjectOp\x12\x0f\n\x07VrfName\x18\x02 \x01(\t\x12%\n\x06OpList\x18\x03 \x03(\x0b\x32\x15.service_layer.SLAFOp\"\xf9\x01\n\x07SLAFRes\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x13\n\x0bOperationID\x18\x02 \x01(\x04\x12#\n\x04\x41\x46Op\x18\x03 \x01(\x0b\x32\x15.service_layer.SLAFOp\x12/\n\tFIBStatus\x18\x04 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x12\n\nFIBVersion\x18\x05 \x01(\x04\x12\x13\n\x0b\x45rrorString\x18\x06 \x01(\t\x12)\n\tDepResult\x18\x07 \x03(\x0b\x32\x16.service_layer.SLAFRes\"F\n\nSLAFMsgRsp\x12\x0f\n\x07VrfName\x18\x01 \x01(\t\x12\'\n\x07Results\x18\x02 \x03(\x0b\x32\x16.service_layer.SLAFRes\"d\n\x10SLAFRedistRegMsg\x12\x10\n\x08SrcProto\x18\x01 \x01(\t\x12\x13\n\x0bSrcProtoTag\x18\x02 \x01(\t\x12)\n\x05Table\x18\x03 \x01(\x0e\x32\x1a.service_layer.SLTableType\"g\n\x0fSLAFNotifRegReq\x12\x34\n\tRedistReq\x18\x01 \x01(\x0b\x32\x1f.service_layer.SLAFRedistRegMsgH\x00\x12\x13\n\x0bOperationID\x18\x03 \x01(\x04\x42\t\n\x07request\"y\n\x0cSLAFNotifReq\x12&\n\x04Oper\x18\x01 \x01(\x0e\x32\x18.service_layer.SLNotifOp\x12\x0f\n\x07VrfName\x18\x02 \x01(\t\x12\x30\n\x08NotifReq\x18\x03 \x03(\x0b\x32\x1e.service_layer.SLAFNotifRegReq\"s\n\x0cSLAFNotifRsp\x12\x30\n\x08NotifReq\x18\x01 \x01(\x0b\x32\x1e.service_layer.SLAFNotifRegReq\x12\x31\n\x0bNotifStatus\x18\x02 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\"{\n\tSLAFNotif\x12\x32\n\x0bNotifStatus\x18\x01 \x01(\x0b\x32\x1b.service_layer.SLAFNotifRspH\x00\x12\x31\n\x0cRedistObject\x18\x04 \x01(\x0b\x32\x19.service_layer.SLAFObjectH\x00\x42\x07\n\x05\x45vent\"v\n\x0cSLAFNotifMsg\x12\x0f\n\x07VrfName\x18\x01 \x01(\t\x12)\n\x05Table\x18\x02 \x01(\x0e\x32\x1a.service_layer.SLTableType\x12*\n\x08\x41\x46Notifs\x18\x03 \x03(\x0b\x32\x18.service_layer.SLAFNotif2\xc8\x03\n\x04SLAF\x12M\n\x0cSLAFVrfRegOp\x12\x1c.service_layer.SLAFVrfRegMsg\x1a\x1f.service_layer.SLAFVrfRegMsgRsp\x12V\n\rSLAFVrfRegGet\x12\x1f.service_layer.SLAFVrfRegGetMsg\x1a\".service_layer.SLAFVrfRegGetMsgRsp0\x01\x12;\n\x06SLAFOp\x12\x16.service_layer.SLAFMsg\x1a\x19.service_layer.SLAFMsgRsp\x12\x45\n\x0cSLAFOpStream\x12\x16.service_layer.SLAFMsg\x1a\x19.service_layer.SLAFMsgRsp(\x01\x30\x01\x12\x44\n\x07SLAFGet\x12\x19.service_layer.SLAFGetMsg\x1a\x1c.service_layer.SLAFGetMsgRsp0\x01\x12O\n\x0fSLAFNotifStream\x12\x1b.service_layer.SLAFNotifReq\x1a\x1b.service_layer.SLAFNotifMsg(\x01\x30\x01\x42QZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sl_af_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layer'
  _globals['_SLAFVRFREG']._serialized_start=118
  _globals['_SLAFVRFREG']._serialized_end=214
  _globals['_SLAFVRFREGMSG']._serialized_start=216
  _globals['_SLAFVRFREGMSG']._serialized_end=316
  _globals['_SLAFVRFREGMSGRES']._serialized_start=318
  _globals['_SLAFVRFREGMSGRES']._serialized_end=445
  _globals['_SLAFVRFREGMSGRSP']._serialized_start=447
  _globals['_SLAFVRFREGMSGRSP']._serialized_end=568
  _globals['_SLAFVRFREGGETMSG']._serialized_start=570
  _globals['_SLAFVRFREGGETMSG']._serialized_end=604
  _globals['_SLAFVRFREGGETMSGRSP']._serialized_start=607
  _globals['_SLAFVRFREGGETMSGRSP']._serialized_end=780
  _globals['_SLPATHGROUP']._serialized_start=783
  _globals['_SLPATHGROUP']._serialized_end=1066
  _globals['_SLPATHGROUP_SLPATH']._serialized_start=943
  _globals['_SLPATHGROUP_SLPATH']._serialized_end=993
  _globals['_SLPATHGROUP_SLPATHLIST']._serialized_start=995
  _globals['_SLPATHGROUP_SLPATHLIST']._serialized_end=1057
  _globals['_SLMPLSENTRY']._serialized_start=1069
  _globals['_SLMPLSENTRY']._serialized_end=1253
  _globals['_SLAFOBJECT']._serialized_start=1256
  _globals['_SLAFOBJECT']._serialized_end=1469
  _globals['_SLAFOP']._serialized_start=1471
  _globals['_SLAFOP']._serialized_end=1591
  _globals['_SLAFGETMSG']._serialized_start=1593
  _globals['_SLAFGETMSG']._serialized_end=1708
  _globals['_SLAFGETMSGRSPENTRY']._serialized_start=1710
  _globals['_SLAFGETMSGRSPENTRY']._serialized_end=1836
  _globals['_SLAFGETMSGRSP']._serialized_start=1839
  _globals['_SLAFGETMSGRSP']._serialized_end=1989
  _globals['_SLAFMSG']._serialized_start=1991
  _globals['_SLAFMSG']._serialized_end=2097
  _globals['_SLAFRES']._serialized_start=2100
  _globals['_SLAFRES']._serialized_end=2349
  _globals['_SLAFMSGRSP']._serialized_start=2351
  _globals['_SLAFMSGRSP']._serialized_end=2421
  _globals['_SLAFREDISTREGMSG']._serialized_start=2423
  _globals['_SLAFREDISTREGMSG']._serialized_end=2523
  _globals['_SLAFNOTIFREGREQ']._serialized_start=2525
  _globals['_SLAFNOTIFREGREQ']._serialized_end=2628
  _globals['_SLAFNOTIFREQ']._serialized_start=2630
  _globals['_SLAFNOTIFREQ']._serialized_end=2751
  _globals['_SLAFNOTIFRSP']._serialized_start=2753
  _globals['_SLAFNOTIFRSP']._serialized_end=2868
  _globals['_SLAFNOTIF']._serialized_start=2870
  _globals['_SLAFNOTIF']._serialized_end=2993
  _globals['_SLAFNOTIFMSG']._serialized_start=2995
  _globals['_SLAFNOTIFMSG']._serialized_end=3113
  _globals['_SLAF']._serialized_start=3116
  _globals['_SLAF']._serialized_end=3572
# @@protoc_insertion_point(module_scope)
