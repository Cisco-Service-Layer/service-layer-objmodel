// @file
// @brief Specifies the API version number
//
// ----------------------------------------------------------------
//  Copyright (c) 2016 by cisco Systems, Inc.
//  All rights reserved.
// -----------------------------------------------------------------
//
//

// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.31.0-devel
// 	protoc        v3.12.1
// source: sl_version.proto

package service_layer

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

// Service Layer API version.
// This is used in the Global init message exchange to handshake client/server
// Version numbers.
type SLVersion int32

const (
	SLVersion_SL_VERSION_UNUSED SLVersion = 0
	SLVersion_SL_MAJOR_VERSION  SLVersion = 0
	SLVersion_SL_MINOR_VERSION  SLVersion = 5
	SLVersion_SL_SUB_VERSION    SLVersion = 0
)

// Enum value maps for SLVersion.
var (
	SLVersion_name = map[int32]string{
		0: "SL_VERSION_UNUSED",
		// Duplicate value: 0: "SL_MAJOR_VERSION",
		5: "SL_MINOR_VERSION",
		// Duplicate value: 0: "SL_SUB_VERSION",
	}
	SLVersion_value = map[string]int32{
		"SL_VERSION_UNUSED": 0,
		"SL_MAJOR_VERSION":  0,
		"SL_MINOR_VERSION":  5,
		"SL_SUB_VERSION":    0,
	}
)

func (x SLVersion) Enum() *SLVersion {
	p := new(SLVersion)
	*p = x
	return p
}

func (x SLVersion) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (SLVersion) Descriptor() protoreflect.EnumDescriptor {
	return file_sl_version_proto_enumTypes[0].Descriptor()
}

func (SLVersion) Type() protoreflect.EnumType {
	return &file_sl_version_proto_enumTypes[0]
}

func (x SLVersion) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Use SLVersion.Descriptor instead.
func (SLVersion) EnumDescriptor() ([]byte, []int) {
	return file_sl_version_proto_rawDescGZIP(), []int{0}
}

var File_sl_version_proto protoreflect.FileDescriptor

var file_sl_version_proto_rawDesc = []byte{
	0x0a, 0x10, 0x73, 0x6c, 0x5f, 0x76, 0x65, 0x72, 0x73, 0x69, 0x6f, 0x6e, 0x2e, 0x70, 0x72, 0x6f,
	0x74, 0x6f, 0x12, 0x0d, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65,
	0x72, 0x2a, 0x66, 0x0a, 0x09, 0x53, 0x4c, 0x56, 0x65, 0x72, 0x73, 0x69, 0x6f, 0x6e, 0x12, 0x15,
	0x0a, 0x11, 0x53, 0x4c, 0x5f, 0x56, 0x45, 0x52, 0x53, 0x49, 0x4f, 0x4e, 0x5f, 0x55, 0x4e, 0x55,
	0x53, 0x45, 0x44, 0x10, 0x00, 0x12, 0x14, 0x0a, 0x10, 0x53, 0x4c, 0x5f, 0x4d, 0x41, 0x4a, 0x4f,
	0x52, 0x5f, 0x56, 0x45, 0x52, 0x53, 0x49, 0x4f, 0x4e, 0x10, 0x00, 0x12, 0x14, 0x0a, 0x10, 0x53,
	0x4c, 0x5f, 0x4d, 0x49, 0x4e, 0x4f, 0x52, 0x5f, 0x56, 0x45, 0x52, 0x53, 0x49, 0x4f, 0x4e, 0x10,
	0x05, 0x12, 0x12, 0x0a, 0x0e, 0x53, 0x4c, 0x5f, 0x53, 0x55, 0x42, 0x5f, 0x56, 0x45, 0x52, 0x53,
	0x49, 0x4f, 0x4e, 0x10, 0x00, 0x1a, 0x02, 0x10, 0x01, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x33,
}

var (
	file_sl_version_proto_rawDescOnce sync.Once
	file_sl_version_proto_rawDescData = file_sl_version_proto_rawDesc
)

func file_sl_version_proto_rawDescGZIP() []byte {
	file_sl_version_proto_rawDescOnce.Do(func() {
		file_sl_version_proto_rawDescData = protoimpl.X.CompressGZIP(file_sl_version_proto_rawDescData)
	})
	return file_sl_version_proto_rawDescData
}

var file_sl_version_proto_enumTypes = make([]protoimpl.EnumInfo, 1)
var file_sl_version_proto_goTypes = []interface{}{
	(SLVersion)(0), // 0: service_layer.SLVersion
}
var file_sl_version_proto_depIdxs = []int32{
	0, // [0:0] is the sub-list for method output_type
	0, // [0:0] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_sl_version_proto_init() }
func file_sl_version_proto_init() {
	if File_sl_version_proto != nil {
		return
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_sl_version_proto_rawDesc,
			NumEnums:      1,
			NumMessages:   0,
			NumExtensions: 0,
			NumServices:   0,
		},
		GoTypes:           file_sl_version_proto_goTypes,
		DependencyIndexes: file_sl_version_proto_depIdxs,
		EnumInfos:         file_sl_version_proto_enumTypes,
	}.Build()
	File_sl_version_proto = out.File
	file_sl_version_proto_rawDesc = nil
	file_sl_version_proto_goTypes = nil
	file_sl_version_proto_depIdxs = nil
}
