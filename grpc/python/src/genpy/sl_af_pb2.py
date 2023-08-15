# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl_af.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import sl_common_types_pb2 as sl__common__types__pb2
from . import sl_route_common_pb2 as sl__route__common__pb2
from . import sl_route_ipv4_pb2 as sl__route__ipv4__pb2
from . import sl_route_ipv6_pb2 as sl__route__ipv6__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='sl_af.proto',
  package='service_layer',
  syntax='proto3',
  serialized_options=b'ZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layer',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0bsl_af.proto\x12\rservice_layer\x1a\x15sl_common_types.proto\x1a\x15sl_route_common.proto\x1a\x13sl_route_ipv4.proto\x1a\x13sl_route_ipv6.proto\"`\n\nSLAFVrfReg\x12)\n\x05Table\x18\x01 \x01(\x0e\x32\x1a.service_layer.SLTableType\x12\'\n\x06VrfReg\x18\x02 \x01(\x0b\x32\x17.service_layer.SLVrfReg\"d\n\rSLAFVrfRegMsg\x12$\n\x04Oper\x18\x01 \x01(\x0e\x32\x16.service_layer.SLRegOp\x12-\n\nVrfRegMsgs\x18\x02 \x03(\x0b\x32\x19.service_layer.SLAFVrfReg\"\x7f\n\x10SLAFVrfRegMsgRes\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x0f\n\x07VrfName\x18\x02 \x01(\t\x12)\n\x05Table\x18\x03 \x01(\x0e\x32\x1a.service_layer.SLTableType\"y\n\x10SLAFVrfRegMsgRsp\x12\x33\n\rStatusSummary\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x30\n\x07Results\x18\x02 \x03(\x0b\x32\x1f.service_layer.SLAFVrfRegMsgRes\"\x8c\x02\n\x0bSLPathGroup\x12.\n\x0bPathGroupId\x18\x01 \x01(\x0b\x32\x19.service_layer.SLObjectId\x12\x15\n\rAdminDistance\x18\x02 \x01(\r\x12\x39\n\x08PathList\x18\x03 \x01(\x0b\x32%.service_layer.SLPathGroup.SLPathListH\x00\x1a\x32\n\x06SLPath\x12(\n\x04Path\x18\x01 \x01(\x0b\x32\x1a.service_layer.SLRoutePath\x1a>\n\nSLPathList\x12\x30\n\x05Paths\x18\x01 \x03(\x0b\x32!.service_layer.SLPathGroup.SLPathB\x07\n\x05\x65ntry\"\xa9\x01\n\x0bSLMplsEntry\x12\x12\n\nLocalLabel\x18\x01 \x01(\r\x12\x15\n\rAdminDistance\x18\x02 \x01(\r\x12,\n\x08PathList\x18\x03 \x03(\x0b\x32\x1a.service_layer.SLRoutePath\x12\x38\n\x0cPathGroupKey\x18\x04 \x01(\x0b\x32 .service_layer.SLPathGroupRefKeyH\x00\x42\x07\n\x05\x65ntry\"\xd5\x01\n\nSLAFObject\x12-\n\tIPv4Route\x18\x01 \x01(\x0b\x32\x18.service_layer.SLRoutev4H\x00\x12-\n\tIPv6Route\x18\x02 \x01(\x0b\x32\x18.service_layer.SLRoutev6H\x00\x12/\n\tMplsLabel\x18\x03 \x01(\x0b\x32\x1a.service_layer.SLMplsEntryH\x00\x12/\n\tPathGroup\x18\x04 \x01(\x0b\x32\x1a.service_layer.SLPathGroupH\x00\x42\x07\n\x05\x65ntry\"J\n\x06SLAFOp\x12+\n\x08\x41\x46Object\x18\x01 \x01(\x0b\x32\x19.service_layer.SLAFObject\x12\x13\n\x0bOperationID\x18\x02 \x01(\x04\"\x98\x01\n\x07SLAFMsg\x12\'\n\x04Oper\x18\x01 \x01(\x0e\x32\x19.service_layer.SLObjectOp\x12\x0f\n\x07VrfName\x18\x02 \x01(\t\x12,\n\x07\x41\x63kType\x18\x03 \x01(\x0e\x32\x1b.service_layer.SLRspACKType\x12%\n\x06OpList\x18\x04 \x03(\x0b\x32\x15.service_layer.SLAFOp\"O\n\x07SLAFRes\x12/\n\tErrStatus\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\x13\n\x0bOperationID\x18\x02 \x01(\x04\"j\n\nSLAFMsgRsp\x12\x33\n\rStatusSummary\x18\x01 \x01(\x0b\x32\x1c.service_layer.SLErrorStatus\x12\'\n\x07Results\x18\x02 \x03(\x0b\x32\x16.service_layer.SLAFRes2\xd9\x01\n\x04SLAF\x12M\n\x0cSLAFVrfRegOp\x12\x1c.service_layer.SLAFVrfRegMsg\x1a\x1f.service_layer.SLAFVrfRegMsgRsp\x12;\n\x06SLAFOp\x12\x16.service_layer.SLAFMsg\x1a\x19.service_layer.SLAFMsgRsp\x12\x45\n\x0cSLAFOpStream\x12\x16.service_layer.SLAFMsg\x1a\x19.service_layer.SLAFMsgRsp(\x01\x30\x01\x42QZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layerb\x06proto3'
  ,
  dependencies=[sl__common__types__pb2.DESCRIPTOR,sl__route__common__pb2.DESCRIPTOR,sl__route__ipv4__pb2.DESCRIPTOR,sl__route__ipv6__pb2.DESCRIPTOR,])




_SLAFVRFREG = _descriptor.Descriptor(
  name='SLAFVrfReg',
  full_name='service_layer.SLAFVrfReg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Table', full_name='service_layer.SLAFVrfReg.Table', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='VrfReg', full_name='service_layer.SLAFVrfReg.VrfReg', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=118,
  serialized_end=214,
)


_SLAFVRFREGMSG = _descriptor.Descriptor(
  name='SLAFVrfRegMsg',
  full_name='service_layer.SLAFVrfRegMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Oper', full_name='service_layer.SLAFVrfRegMsg.Oper', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='VrfRegMsgs', full_name='service_layer.SLAFVrfRegMsg.VrfRegMsgs', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=216,
  serialized_end=316,
)


_SLAFVRFREGMSGRES = _descriptor.Descriptor(
  name='SLAFVrfRegMsgRes',
  full_name='service_layer.SLAFVrfRegMsgRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ErrStatus', full_name='service_layer.SLAFVrfRegMsgRes.ErrStatus', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='VrfName', full_name='service_layer.SLAFVrfRegMsgRes.VrfName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Table', full_name='service_layer.SLAFVrfRegMsgRes.Table', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=318,
  serialized_end=445,
)


_SLAFVRFREGMSGRSP = _descriptor.Descriptor(
  name='SLAFVrfRegMsgRsp',
  full_name='service_layer.SLAFVrfRegMsgRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='StatusSummary', full_name='service_layer.SLAFVrfRegMsgRsp.StatusSummary', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Results', full_name='service_layer.SLAFVrfRegMsgRsp.Results', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=447,
  serialized_end=568,
)


_SLPATHGROUP_SLPATH = _descriptor.Descriptor(
  name='SLPath',
  full_name='service_layer.SLPathGroup.SLPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Path', full_name='service_layer.SLPathGroup.SLPath.Path', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=716,
  serialized_end=766,
)

_SLPATHGROUP_SLPATHLIST = _descriptor.Descriptor(
  name='SLPathList',
  full_name='service_layer.SLPathGroup.SLPathList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Paths', full_name='service_layer.SLPathGroup.SLPathList.Paths', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=768,
  serialized_end=830,
)

_SLPATHGROUP = _descriptor.Descriptor(
  name='SLPathGroup',
  full_name='service_layer.SLPathGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='PathGroupId', full_name='service_layer.SLPathGroup.PathGroupId', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='AdminDistance', full_name='service_layer.SLPathGroup.AdminDistance', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='PathList', full_name='service_layer.SLPathGroup.PathList', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_SLPATHGROUP_SLPATH, _SLPATHGROUP_SLPATHLIST, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='entry', full_name='service_layer.SLPathGroup.entry',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=571,
  serialized_end=839,
)


_SLMPLSENTRY = _descriptor.Descriptor(
  name='SLMplsEntry',
  full_name='service_layer.SLMplsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='LocalLabel', full_name='service_layer.SLMplsEntry.LocalLabel', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='AdminDistance', full_name='service_layer.SLMplsEntry.AdminDistance', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='PathList', full_name='service_layer.SLMplsEntry.PathList', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='PathGroupKey', full_name='service_layer.SLMplsEntry.PathGroupKey', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='entry', full_name='service_layer.SLMplsEntry.entry',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=842,
  serialized_end=1011,
)


_SLAFOBJECT = _descriptor.Descriptor(
  name='SLAFObject',
  full_name='service_layer.SLAFObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='IPv4Route', full_name='service_layer.SLAFObject.IPv4Route', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='IPv6Route', full_name='service_layer.SLAFObject.IPv6Route', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='MplsLabel', full_name='service_layer.SLAFObject.MplsLabel', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='PathGroup', full_name='service_layer.SLAFObject.PathGroup', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='entry', full_name='service_layer.SLAFObject.entry',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=1014,
  serialized_end=1227,
)


_SLAFOP = _descriptor.Descriptor(
  name='SLAFOp',
  full_name='service_layer.SLAFOp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='AFObject', full_name='service_layer.SLAFOp.AFObject', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='OperationID', full_name='service_layer.SLAFOp.OperationID', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1229,
  serialized_end=1303,
)


_SLAFMSG = _descriptor.Descriptor(
  name='SLAFMsg',
  full_name='service_layer.SLAFMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Oper', full_name='service_layer.SLAFMsg.Oper', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='VrfName', full_name='service_layer.SLAFMsg.VrfName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='AckType', full_name='service_layer.SLAFMsg.AckType', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='OpList', full_name='service_layer.SLAFMsg.OpList', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1306,
  serialized_end=1458,
)


_SLAFRES = _descriptor.Descriptor(
  name='SLAFRes',
  full_name='service_layer.SLAFRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ErrStatus', full_name='service_layer.SLAFRes.ErrStatus', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='OperationID', full_name='service_layer.SLAFRes.OperationID', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1460,
  serialized_end=1539,
)


_SLAFMSGRSP = _descriptor.Descriptor(
  name='SLAFMsgRsp',
  full_name='service_layer.SLAFMsgRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='StatusSummary', full_name='service_layer.SLAFMsgRsp.StatusSummary', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Results', full_name='service_layer.SLAFMsgRsp.Results', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1541,
  serialized_end=1647,
)

_SLAFVRFREG.fields_by_name['Table'].enum_type = sl__common__types__pb2._SLTABLETYPE
_SLAFVRFREG.fields_by_name['VrfReg'].message_type = sl__route__common__pb2._SLVRFREG
_SLAFVRFREGMSG.fields_by_name['Oper'].enum_type = sl__common__types__pb2._SLREGOP
_SLAFVRFREGMSG.fields_by_name['VrfRegMsgs'].message_type = _SLAFVRFREG
_SLAFVRFREGMSGRES.fields_by_name['ErrStatus'].message_type = sl__common__types__pb2._SLERRORSTATUS
_SLAFVRFREGMSGRES.fields_by_name['Table'].enum_type = sl__common__types__pb2._SLTABLETYPE
_SLAFVRFREGMSGRSP.fields_by_name['StatusSummary'].message_type = sl__common__types__pb2._SLERRORSTATUS
_SLAFVRFREGMSGRSP.fields_by_name['Results'].message_type = _SLAFVRFREGMSGRES
_SLPATHGROUP_SLPATH.fields_by_name['Path'].message_type = sl__route__common__pb2._SLROUTEPATH
_SLPATHGROUP_SLPATH.containing_type = _SLPATHGROUP
_SLPATHGROUP_SLPATHLIST.fields_by_name['Paths'].message_type = _SLPATHGROUP_SLPATH
_SLPATHGROUP_SLPATHLIST.containing_type = _SLPATHGROUP
_SLPATHGROUP.fields_by_name['PathGroupId'].message_type = sl__common__types__pb2._SLOBJECTID
_SLPATHGROUP.fields_by_name['PathList'].message_type = _SLPATHGROUP_SLPATHLIST
_SLPATHGROUP.oneofs_by_name['entry'].fields.append(
  _SLPATHGROUP.fields_by_name['PathList'])
_SLPATHGROUP.fields_by_name['PathList'].containing_oneof = _SLPATHGROUP.oneofs_by_name['entry']
_SLMPLSENTRY.fields_by_name['PathList'].message_type = sl__route__common__pb2._SLROUTEPATH
_SLMPLSENTRY.fields_by_name['PathGroupKey'].message_type = sl__route__common__pb2._SLPATHGROUPREFKEY
_SLMPLSENTRY.oneofs_by_name['entry'].fields.append(
  _SLMPLSENTRY.fields_by_name['PathGroupKey'])
_SLMPLSENTRY.fields_by_name['PathGroupKey'].containing_oneof = _SLMPLSENTRY.oneofs_by_name['entry']
_SLAFOBJECT.fields_by_name['IPv4Route'].message_type = sl__route__ipv4__pb2._SLROUTEV4
_SLAFOBJECT.fields_by_name['IPv6Route'].message_type = sl__route__ipv6__pb2._SLROUTEV6
_SLAFOBJECT.fields_by_name['MplsLabel'].message_type = _SLMPLSENTRY
_SLAFOBJECT.fields_by_name['PathGroup'].message_type = _SLPATHGROUP
_SLAFOBJECT.oneofs_by_name['entry'].fields.append(
  _SLAFOBJECT.fields_by_name['IPv4Route'])
_SLAFOBJECT.fields_by_name['IPv4Route'].containing_oneof = _SLAFOBJECT.oneofs_by_name['entry']
_SLAFOBJECT.oneofs_by_name['entry'].fields.append(
  _SLAFOBJECT.fields_by_name['IPv6Route'])
_SLAFOBJECT.fields_by_name['IPv6Route'].containing_oneof = _SLAFOBJECT.oneofs_by_name['entry']
_SLAFOBJECT.oneofs_by_name['entry'].fields.append(
  _SLAFOBJECT.fields_by_name['MplsLabel'])
_SLAFOBJECT.fields_by_name['MplsLabel'].containing_oneof = _SLAFOBJECT.oneofs_by_name['entry']
_SLAFOBJECT.oneofs_by_name['entry'].fields.append(
  _SLAFOBJECT.fields_by_name['PathGroup'])
_SLAFOBJECT.fields_by_name['PathGroup'].containing_oneof = _SLAFOBJECT.oneofs_by_name['entry']
_SLAFOP.fields_by_name['AFObject'].message_type = _SLAFOBJECT
_SLAFMSG.fields_by_name['Oper'].enum_type = sl__common__types__pb2._SLOBJECTOP
_SLAFMSG.fields_by_name['AckType'].enum_type = sl__common__types__pb2._SLRSPACKTYPE
_SLAFMSG.fields_by_name['OpList'].message_type = _SLAFOP
_SLAFRES.fields_by_name['ErrStatus'].message_type = sl__common__types__pb2._SLERRORSTATUS
_SLAFMSGRSP.fields_by_name['StatusSummary'].message_type = sl__common__types__pb2._SLERRORSTATUS
_SLAFMSGRSP.fields_by_name['Results'].message_type = _SLAFRES
DESCRIPTOR.message_types_by_name['SLAFVrfReg'] = _SLAFVRFREG
DESCRIPTOR.message_types_by_name['SLAFVrfRegMsg'] = _SLAFVRFREGMSG
DESCRIPTOR.message_types_by_name['SLAFVrfRegMsgRes'] = _SLAFVRFREGMSGRES
DESCRIPTOR.message_types_by_name['SLAFVrfRegMsgRsp'] = _SLAFVRFREGMSGRSP
DESCRIPTOR.message_types_by_name['SLPathGroup'] = _SLPATHGROUP
DESCRIPTOR.message_types_by_name['SLMplsEntry'] = _SLMPLSENTRY
DESCRIPTOR.message_types_by_name['SLAFObject'] = _SLAFOBJECT
DESCRIPTOR.message_types_by_name['SLAFOp'] = _SLAFOP
DESCRIPTOR.message_types_by_name['SLAFMsg'] = _SLAFMSG
DESCRIPTOR.message_types_by_name['SLAFRes'] = _SLAFRES
DESCRIPTOR.message_types_by_name['SLAFMsgRsp'] = _SLAFMSGRSP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SLAFVrfReg = _reflection.GeneratedProtocolMessageType('SLAFVrfReg', (_message.Message,), {
  'DESCRIPTOR' : _SLAFVRFREG,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLAFVrfReg)
  })
_sym_db.RegisterMessage(SLAFVrfReg)

SLAFVrfRegMsg = _reflection.GeneratedProtocolMessageType('SLAFVrfRegMsg', (_message.Message,), {
  'DESCRIPTOR' : _SLAFVRFREGMSG,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLAFVrfRegMsg)
  })
_sym_db.RegisterMessage(SLAFVrfRegMsg)

SLAFVrfRegMsgRes = _reflection.GeneratedProtocolMessageType('SLAFVrfRegMsgRes', (_message.Message,), {
  'DESCRIPTOR' : _SLAFVRFREGMSGRES,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLAFVrfRegMsgRes)
  })
_sym_db.RegisterMessage(SLAFVrfRegMsgRes)

SLAFVrfRegMsgRsp = _reflection.GeneratedProtocolMessageType('SLAFVrfRegMsgRsp', (_message.Message,), {
  'DESCRIPTOR' : _SLAFVRFREGMSGRSP,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLAFVrfRegMsgRsp)
  })
_sym_db.RegisterMessage(SLAFVrfRegMsgRsp)

SLPathGroup = _reflection.GeneratedProtocolMessageType('SLPathGroup', (_message.Message,), {

  'SLPath' : _reflection.GeneratedProtocolMessageType('SLPath', (_message.Message,), {
    'DESCRIPTOR' : _SLPATHGROUP_SLPATH,
    '__module__' : 'sl_af_pb2'
    # @@protoc_insertion_point(class_scope:service_layer.SLPathGroup.SLPath)
    })
  ,

  'SLPathList' : _reflection.GeneratedProtocolMessageType('SLPathList', (_message.Message,), {
    'DESCRIPTOR' : _SLPATHGROUP_SLPATHLIST,
    '__module__' : 'sl_af_pb2'
    # @@protoc_insertion_point(class_scope:service_layer.SLPathGroup.SLPathList)
    })
  ,
  'DESCRIPTOR' : _SLPATHGROUP,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLPathGroup)
  })
_sym_db.RegisterMessage(SLPathGroup)
_sym_db.RegisterMessage(SLPathGroup.SLPath)
_sym_db.RegisterMessage(SLPathGroup.SLPathList)

SLMplsEntry = _reflection.GeneratedProtocolMessageType('SLMplsEntry', (_message.Message,), {
  'DESCRIPTOR' : _SLMPLSENTRY,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLMplsEntry)
  })
_sym_db.RegisterMessage(SLMplsEntry)

SLAFObject = _reflection.GeneratedProtocolMessageType('SLAFObject', (_message.Message,), {
  'DESCRIPTOR' : _SLAFOBJECT,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLAFObject)
  })
_sym_db.RegisterMessage(SLAFObject)

SLAFOp = _reflection.GeneratedProtocolMessageType('SLAFOp', (_message.Message,), {
  'DESCRIPTOR' : _SLAFOP,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLAFOp)
  })
_sym_db.RegisterMessage(SLAFOp)

SLAFMsg = _reflection.GeneratedProtocolMessageType('SLAFMsg', (_message.Message,), {
  'DESCRIPTOR' : _SLAFMSG,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLAFMsg)
  })
_sym_db.RegisterMessage(SLAFMsg)

SLAFRes = _reflection.GeneratedProtocolMessageType('SLAFRes', (_message.Message,), {
  'DESCRIPTOR' : _SLAFRES,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLAFRes)
  })
_sym_db.RegisterMessage(SLAFRes)

SLAFMsgRsp = _reflection.GeneratedProtocolMessageType('SLAFMsgRsp', (_message.Message,), {
  'DESCRIPTOR' : _SLAFMSGRSP,
  '__module__' : 'sl_af_pb2'
  # @@protoc_insertion_point(class_scope:service_layer.SLAFMsgRsp)
  })
_sym_db.RegisterMessage(SLAFMsgRsp)


DESCRIPTOR._options = None

_SLAF = _descriptor.ServiceDescriptor(
  name='SLAF',
  full_name='service_layer.SLAF',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1650,
  serialized_end=1867,
  methods=[
  _descriptor.MethodDescriptor(
    name='SLAFVrfRegOp',
    full_name='service_layer.SLAF.SLAFVrfRegOp',
    index=0,
    containing_service=None,
    input_type=_SLAFVRFREGMSG,
    output_type=_SLAFVRFREGMSGRSP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SLAFOp',
    full_name='service_layer.SLAF.SLAFOp',
    index=1,
    containing_service=None,
    input_type=_SLAFMSG,
    output_type=_SLAFMSGRSP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SLAFOpStream',
    full_name='service_layer.SLAF.SLAFOpStream',
    index=2,
    containing_service=None,
    input_type=_SLAFMSG,
    output_type=_SLAFMSGRSP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SLAF)

DESCRIPTOR.services_by_name['SLAF'] = _SLAF

# @@protoc_insertion_point(module_scope)