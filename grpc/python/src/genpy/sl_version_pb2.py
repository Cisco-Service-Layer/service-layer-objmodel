# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl_version.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='sl_version.proto',
  package='service_layer',
  syntax='proto3',
  serialized_options=b'ZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layer',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10sl_version.proto\x12\rservice_layer*f\n\tSLVersion\x12\x15\n\x11SL_VERSION_UNUSED\x10\x00\x12\x14\n\x10SL_MAJOR_VERSION\x10\x00\x12\x14\n\x10SL_MINOR_VERSION\x10\x07\x12\x12\n\x0eSL_SUB_VERSION\x10\x00\x1a\x02\x10\x01\x42QZOgithub.com/Cisco-service-layer/service-layer-objmodel/grpc/protos;service_layerb\x06proto3'
)

_SLVERSION = _descriptor.EnumDescriptor(
  name='SLVersion',
  full_name='service_layer.SLVersion',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SL_VERSION_UNUSED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SL_MAJOR_VERSION', index=1, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SL_MINOR_VERSION', index=2, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SL_SUB_VERSION', index=3, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=b'\020\001',
  serialized_start=35,
  serialized_end=137,
)
_sym_db.RegisterEnumDescriptor(_SLVERSION)

SLVersion = enum_type_wrapper.EnumTypeWrapper(_SLVERSION)
SL_VERSION_UNUSED = 0
SL_MAJOR_VERSION = 0
SL_MINOR_VERSION = 7
SL_SUB_VERSION = 0


DESCRIPTOR.enum_types_by_name['SLVersion'] = _SLVERSION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
_SLVERSION._options = None
# @@protoc_insertion_point(module_scope)
