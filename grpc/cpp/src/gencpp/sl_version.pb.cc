// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: sl_version.proto

#include "sl_version.pb.h"

#include <algorithm>

#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/wire_format_lite.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/reflection_ops.h>
#include <google/protobuf/wire_format.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>

PROTOBUF_PRAGMA_INIT_SEG
namespace service_layer {
}  // namespace service_layer
static constexpr ::PROTOBUF_NAMESPACE_ID::Metadata* file_level_metadata_sl_5fversion_2eproto = nullptr;
static const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* file_level_enum_descriptors_sl_5fversion_2eproto[1];
static constexpr ::PROTOBUF_NAMESPACE_ID::ServiceDescriptor const** file_level_service_descriptors_sl_5fversion_2eproto = nullptr;
const ::PROTOBUF_NAMESPACE_ID::uint32 TableStruct_sl_5fversion_2eproto::offsets[1] = {};
static constexpr ::PROTOBUF_NAMESPACE_ID::internal::MigrationSchema* schemas = nullptr;
static constexpr ::PROTOBUF_NAMESPACE_ID::Message* const* file_default_instances = nullptr;

const char descriptor_table_protodef_sl_5fversion_2eproto[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) =
  "\n\020sl_version.proto\022\rservice_layer*f\n\tSLV"
  "ersion\022\025\n\021SL_VERSION_UNUSED\020\000\022\024\n\020SL_MAJO"
  "R_VERSION\020\000\022\024\n\020SL_MINOR_VERSION\020\004\022\022\n\016SL_"
  "SUB_VERSION\020\000\032\002\020\001BCZAgithub.com/Cisco-se"
  "rvice-layer/service-layer-objmodel/grpc/"
  "protosb\006proto3"
  ;
static ::PROTOBUF_NAMESPACE_ID::internal::once_flag descriptor_table_sl_5fversion_2eproto_once;
const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_sl_5fversion_2eproto = {
  false, false, 214, descriptor_table_protodef_sl_5fversion_2eproto, "sl_version.proto", 
  &descriptor_table_sl_5fversion_2eproto_once, nullptr, 0, 0,
  schemas, file_default_instances, TableStruct_sl_5fversion_2eproto::offsets,
  file_level_metadata_sl_5fversion_2eproto, file_level_enum_descriptors_sl_5fversion_2eproto, file_level_service_descriptors_sl_5fversion_2eproto,
};
PROTOBUF_ATTRIBUTE_WEAK ::PROTOBUF_NAMESPACE_ID::Metadata
descriptor_table_sl_5fversion_2eproto_metadata_getter(int index) {
  ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&descriptor_table_sl_5fversion_2eproto);
  return descriptor_table_sl_5fversion_2eproto.file_level_metadata[index];
}

// Force running AddDescriptors() at dynamic initialization time.
PROTOBUF_ATTRIBUTE_INIT_PRIORITY static ::PROTOBUF_NAMESPACE_ID::internal::AddDescriptorsRunner dynamic_init_dummy_sl_5fversion_2eproto(&descriptor_table_sl_5fversion_2eproto);
namespace service_layer {
const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* SLVersion_descriptor() {
  ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&descriptor_table_sl_5fversion_2eproto);
  return file_level_enum_descriptors_sl_5fversion_2eproto[0];
}
bool SLVersion_IsValid(int value) {
  switch (value) {
    case 0:
    case 4:
      return true;
    default:
      return false;
  }
}


// @@protoc_insertion_point(namespace_scope)
}  // namespace service_layer
PROTOBUF_NAMESPACE_OPEN
PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)
#include <google/protobuf/port_undef.inc>
