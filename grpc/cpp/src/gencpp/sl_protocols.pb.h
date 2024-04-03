// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: sl_protocols.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_sl_5fprotocols_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_sl_5fprotocols_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3019000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3019004 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/generated_enum_reflection.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_sl_5fprotocols_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_sl_5fprotocols_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxiliaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[1]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_sl_5fprotocols_2eproto;
PROTOBUF_NAMESPACE_OPEN
PROTOBUF_NAMESPACE_CLOSE
namespace service_layer {

enum SLBgplsTopoNlriType : int {
  SL_BGPLS_TOPO_NLRI_TYPE_RESERVED = 0,
  SL_BGPLS_TOPO_NLRI_TYPE_NODE = 1,
  SL_BGPLS_TOPO_NLRI_TYPE_LINK = 2,
  SL_BGPLS_TOPO_NLRI_TYPE_IPV4_PREFIX = 3,
  SL_BGPLS_TOPO_NLRI_TYPE_IPV6_PREFIX = 4,
  SL_BGPLS_TOPO_NLRI_TYPE_SR_POLICY_CANDIDATE_PATH = 5,
  SL_BGPLS_TOPO_NLRI_TYPE_SRV6_SID = 6,
  SLBgplsTopoNlriType_INT_MIN_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::min(),
  SLBgplsTopoNlriType_INT_MAX_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::max()
};
bool SLBgplsTopoNlriType_IsValid(int value);
constexpr SLBgplsTopoNlriType SLBgplsTopoNlriType_MIN = SL_BGPLS_TOPO_NLRI_TYPE_RESERVED;
constexpr SLBgplsTopoNlriType SLBgplsTopoNlriType_MAX = SL_BGPLS_TOPO_NLRI_TYPE_SRV6_SID;
constexpr int SLBgplsTopoNlriType_ARRAYSIZE = SLBgplsTopoNlriType_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* SLBgplsTopoNlriType_descriptor();
template<typename T>
inline const std::string& SLBgplsTopoNlriType_Name(T enum_t_value) {
  static_assert(::std::is_same<T, SLBgplsTopoNlriType>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function SLBgplsTopoNlriType_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    SLBgplsTopoNlriType_descriptor(), enum_t_value);
}
inline bool SLBgplsTopoNlriType_Parse(
    ::PROTOBUF_NAMESPACE_ID::ConstStringParam name, SLBgplsTopoNlriType* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<SLBgplsTopoNlriType>(
    SLBgplsTopoNlriType_descriptor(), name, value);
}
enum SLBgplsTopoProtocol : int {
  SL_BGPLS_TOPO_PROTOCOL_RESERVED = 0,
  SL_BGPLS_TOPO_PROTOCOL_ISIS_L1 = 1,
  SL_BGPLS_TOPO_PROTOCOL_ISIS_L2 = 2,
  SL_BGPLS_TOPO_PROTOCOL_OSPFv2 = 3,
  SL_BGPLS_TOPO_PROTOCOL_DIRECT = 4,
  SL_BGPLS_TOPO_PROTOCOL_STATIC = 5,
  SL_BGPLS_TOPO_PROTOCOL_OSPFv3 = 6,
  SL_BGPLS_TOPO_PROTOCOL_BGP = 7,
  SL_BGPLS_TOPO_PROTOCOL_RSVP_TE = 8,
  SL_BGPLS_TOPO_PROTOCOL_SR = 9,
  SLBgplsTopoProtocol_INT_MIN_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::min(),
  SLBgplsTopoProtocol_INT_MAX_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::max()
};
bool SLBgplsTopoProtocol_IsValid(int value);
constexpr SLBgplsTopoProtocol SLBgplsTopoProtocol_MIN = SL_BGPLS_TOPO_PROTOCOL_RESERVED;
constexpr SLBgplsTopoProtocol SLBgplsTopoProtocol_MAX = SL_BGPLS_TOPO_PROTOCOL_SR;
constexpr int SLBgplsTopoProtocol_ARRAYSIZE = SLBgplsTopoProtocol_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* SLBgplsTopoProtocol_descriptor();
template<typename T>
inline const std::string& SLBgplsTopoProtocol_Name(T enum_t_value) {
  static_assert(::std::is_same<T, SLBgplsTopoProtocol>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function SLBgplsTopoProtocol_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    SLBgplsTopoProtocol_descriptor(), enum_t_value);
}
inline bool SLBgplsTopoProtocol_Parse(
    ::PROTOBUF_NAMESPACE_ID::ConstStringParam name, SLBgplsTopoProtocol* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<SLBgplsTopoProtocol>(
    SLBgplsTopoProtocol_descriptor(), name, value);
}
enum SLBgplsTopoOspfRouteType : int {
  SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_RESERVED = 0,
  SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_INTRA_AREA = 1,
  SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_INTER_AREA = 2,
  SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_EXTERN_1 = 3,
  SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_EXTERN_2 = 4,
  SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_NSSA_1 = 5,
  SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_NSSA_2 = 6,
  SLBgplsTopoOspfRouteType_INT_MIN_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::min(),
  SLBgplsTopoOspfRouteType_INT_MAX_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::max()
};
bool SLBgplsTopoOspfRouteType_IsValid(int value);
constexpr SLBgplsTopoOspfRouteType SLBgplsTopoOspfRouteType_MIN = SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_RESERVED;
constexpr SLBgplsTopoOspfRouteType SLBgplsTopoOspfRouteType_MAX = SL_BGPLS_TOPO_OSPF_ROUTE_TYPE_NSSA_2;
constexpr int SLBgplsTopoOspfRouteType_ARRAYSIZE = SLBgplsTopoOspfRouteType_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* SLBgplsTopoOspfRouteType_descriptor();
template<typename T>
inline const std::string& SLBgplsTopoOspfRouteType_Name(T enum_t_value) {
  static_assert(::std::is_same<T, SLBgplsTopoOspfRouteType>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function SLBgplsTopoOspfRouteType_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    SLBgplsTopoOspfRouteType_descriptor(), enum_t_value);
}
inline bool SLBgplsTopoOspfRouteType_Parse(
    ::PROTOBUF_NAMESPACE_ID::ConstStringParam name, SLBgplsTopoOspfRouteType* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<SLBgplsTopoOspfRouteType>(
    SLBgplsTopoOspfRouteType_descriptor(), name, value);
}
enum SLBgplsTopoSrPolicyProtocolOrigin : int {
  SL_BGPLS_TOPO_SR_POLICY_PROTOCOL_ORIGIN_RESERVED = 0,
  SL_BGPLS_TOPO_SR_POLICY_PROTOCOL_ORIGIN_PCEP = 1,
  SL_BGPLS_TOPO_SR_POLICY_PROTOCOL_ORIGIN_BGP_SR_POLICY = 2,
  SL_BGPLS_TOPO_SR_POLICY_PROTOCOL_ORIGIN_CONFIG = 3,
  SL_BGPLS_TOPO_SR_POLICY_PROTOCOL_ORIGIN_PCEP_VIA_PCE = 10,
  SL_BGPLS_TOPO_SR_POLICY_PROTOCOL_ORIGIN_BGP_SR_POLICY_VIA_PCE = 20,
  SL_BGPLS_TOPO_SR_POLICY_PROTOCOL_ORIGIN_CONFIG_VIA_PCE = 30,
  SLBgplsTopoSrPolicyProtocolOrigin_INT_MIN_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::min(),
  SLBgplsTopoSrPolicyProtocolOrigin_INT_MAX_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::max()
};
bool SLBgplsTopoSrPolicyProtocolOrigin_IsValid(int value);
constexpr SLBgplsTopoSrPolicyProtocolOrigin SLBgplsTopoSrPolicyProtocolOrigin_MIN = SL_BGPLS_TOPO_SR_POLICY_PROTOCOL_ORIGIN_RESERVED;
constexpr SLBgplsTopoSrPolicyProtocolOrigin SLBgplsTopoSrPolicyProtocolOrigin_MAX = SL_BGPLS_TOPO_SR_POLICY_PROTOCOL_ORIGIN_CONFIG_VIA_PCE;
constexpr int SLBgplsTopoSrPolicyProtocolOrigin_ARRAYSIZE = SLBgplsTopoSrPolicyProtocolOrigin_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* SLBgplsTopoSrPolicyProtocolOrigin_descriptor();
template<typename T>
inline const std::string& SLBgplsTopoSrPolicyProtocolOrigin_Name(T enum_t_value) {
  static_assert(::std::is_same<T, SLBgplsTopoSrPolicyProtocolOrigin>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function SLBgplsTopoSrPolicyProtocolOrigin_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    SLBgplsTopoSrPolicyProtocolOrigin_descriptor(), enum_t_value);
}
inline bool SLBgplsTopoSrPolicyProtocolOrigin_Parse(
    ::PROTOBUF_NAMESPACE_ID::ConstStringParam name, SLBgplsTopoSrPolicyProtocolOrigin* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<SLBgplsTopoSrPolicyProtocolOrigin>(
    SLBgplsTopoSrPolicyProtocolOrigin_descriptor(), name, value);
}
// ===================================================================


// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace service_layer

PROTOBUF_NAMESPACE_OPEN

template <> struct is_proto_enum< ::service_layer::SLBgplsTopoNlriType> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::service_layer::SLBgplsTopoNlriType>() {
  return ::service_layer::SLBgplsTopoNlriType_descriptor();
}
template <> struct is_proto_enum< ::service_layer::SLBgplsTopoProtocol> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::service_layer::SLBgplsTopoProtocol>() {
  return ::service_layer::SLBgplsTopoProtocol_descriptor();
}
template <> struct is_proto_enum< ::service_layer::SLBgplsTopoOspfRouteType> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::service_layer::SLBgplsTopoOspfRouteType>() {
  return ::service_layer::SLBgplsTopoOspfRouteType_descriptor();
}
template <> struct is_proto_enum< ::service_layer::SLBgplsTopoSrPolicyProtocolOrigin> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::service_layer::SLBgplsTopoSrPolicyProtocolOrigin>() {
  return ::service_layer::SLBgplsTopoSrPolicyProtocolOrigin_descriptor();
}

PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_sl_5fprotocols_2eproto
