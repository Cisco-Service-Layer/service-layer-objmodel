// @file
// @brief Common definitions for BFD proto files. See RFC 5880 for BFD
// details.
// This file defines basic BFD features, including Tx interval,
// BFD multiplier, BFD state information, and the response status.
//
// ----------------------------------------------------------------
//  Copyright (c) 2016 by Cisco Systems, Inc.
//  All rights reserved.
// -----------------------------------------------------------------
//
//

//@defgroup BFD
//@brief BFD service definitions.

// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.31.0-devel
// 	protoc        v3.12.1
// source: sl_bfd_common.proto

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

type SLBfdType int32

const (
	// Reserved. 0x0
	SLBfdType_SL_BFD_RESERVED SLBfdType = 0
	// Single Hop. 0x1
	SLBfdType_SL_BFD_SINGLE_HOP SLBfdType = 1
	// Multi Hop. 0x2
	SLBfdType_SL_BFD_MULTI_HOP SLBfdType = 2
)

// Enum value maps for SLBfdType.
var (
	SLBfdType_name = map[int32]string{
		0: "SL_BFD_RESERVED",
		1: "SL_BFD_SINGLE_HOP",
		2: "SL_BFD_MULTI_HOP",
	}
	SLBfdType_value = map[string]int32{
		"SL_BFD_RESERVED":   0,
		"SL_BFD_SINGLE_HOP": 1,
		"SL_BFD_MULTI_HOP":  2,
	}
)

func (x SLBfdType) Enum() *SLBfdType {
	p := new(SLBfdType)
	*p = x
	return p
}

func (x SLBfdType) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (SLBfdType) Descriptor() protoreflect.EnumDescriptor {
	return file_sl_bfd_common_proto_enumTypes[0].Descriptor()
}

func (SLBfdType) Type() protoreflect.EnumType {
	return &file_sl_bfd_common_proto_enumTypes[0]
}

func (x SLBfdType) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Use SLBfdType.Descriptor instead.
func (SLBfdType) EnumDescriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{0}
}

// BFD Event Notification types
type SLBfdNotifType int32

const (
	// Reserved. 0x0
	SLBfdNotifType_SL_BFD_EVENT_TYPE_RESERVED SLBfdNotifType = 0
	// Error - ErrStatus field elaborates on the error. 0x1
	SLBfdNotifType_SL_BFD_EVENT_TYPE_ERROR SLBfdNotifType = 1
	// BFD Session state event. 0x2
	SLBfdNotifType_SL_BFD_EVENT_TYPE_SESSION_STATE SLBfdNotifType = 2
)

// Enum value maps for SLBfdNotifType.
var (
	SLBfdNotifType_name = map[int32]string{
		0: "SL_BFD_EVENT_TYPE_RESERVED",
		1: "SL_BFD_EVENT_TYPE_ERROR",
		2: "SL_BFD_EVENT_TYPE_SESSION_STATE",
	}
	SLBfdNotifType_value = map[string]int32{
		"SL_BFD_EVENT_TYPE_RESERVED":      0,
		"SL_BFD_EVENT_TYPE_ERROR":         1,
		"SL_BFD_EVENT_TYPE_SESSION_STATE": 2,
	}
)

func (x SLBfdNotifType) Enum() *SLBfdNotifType {
	p := new(SLBfdNotifType)
	*p = x
	return p
}

func (x SLBfdNotifType) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (SLBfdNotifType) Descriptor() protoreflect.EnumDescriptor {
	return file_sl_bfd_common_proto_enumTypes[1].Descriptor()
}

func (SLBfdNotifType) Type() protoreflect.EnumType {
	return &file_sl_bfd_common_proto_enumTypes[1]
}

func (x SLBfdNotifType) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Use SLBfdNotifType.Descriptor instead.
func (SLBfdNotifType) EnumDescriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{1}
}

// BFD state information.
type SLBfdCommonState_SLBfdStateEnum int32

const (
	// Session never established
	SLBfdCommonState_SL_BFD_SESSION_STATE_UNKNOWN SLBfdCommonState_SLBfdStateEnum = 0
	// Session state UP
	SLBfdCommonState_SL_BFD_SESSION_UP SLBfdCommonState_SLBfdStateEnum = 1
	// Session state is down
	SLBfdCommonState_SL_BFD_SESSION_DOWN SLBfdCommonState_SLBfdStateEnum = 2
	// Neighbor's config was removed
	SLBfdCommonState_SL_BFD_NEIGHBOR_UNCONFIG SLBfdCommonState_SLBfdStateEnum = 3
)

// Enum value maps for SLBfdCommonState_SLBfdStateEnum.
var (
	SLBfdCommonState_SLBfdStateEnum_name = map[int32]string{
		0: "SL_BFD_SESSION_STATE_UNKNOWN",
		1: "SL_BFD_SESSION_UP",
		2: "SL_BFD_SESSION_DOWN",
		3: "SL_BFD_NEIGHBOR_UNCONFIG",
	}
	SLBfdCommonState_SLBfdStateEnum_value = map[string]int32{
		"SL_BFD_SESSION_STATE_UNKNOWN": 0,
		"SL_BFD_SESSION_UP":            1,
		"SL_BFD_SESSION_DOWN":          2,
		"SL_BFD_NEIGHBOR_UNCONFIG":     3,
	}
)

func (x SLBfdCommonState_SLBfdStateEnum) Enum() *SLBfdCommonState_SLBfdStateEnum {
	p := new(SLBfdCommonState_SLBfdStateEnum)
	*p = x
	return p
}

func (x SLBfdCommonState_SLBfdStateEnum) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (SLBfdCommonState_SLBfdStateEnum) Descriptor() protoreflect.EnumDescriptor {
	return file_sl_bfd_common_proto_enumTypes[2].Descriptor()
}

func (SLBfdCommonState_SLBfdStateEnum) Type() protoreflect.EnumType {
	return &file_sl_bfd_common_proto_enumTypes[2]
}

func (x SLBfdCommonState_SLBfdStateEnum) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Use SLBfdCommonState_SLBfdStateEnum.Descriptor instead.
func (SLBfdCommonState_SLBfdStateEnum) EnumDescriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{7, 0}
}

// BFD diagnostic indicates the reason for the last transition of
// the local protocol from up to some other state.
type SLBfdCommonState_SLBfdDiagStateEnum int32

const (
	// Diag Value -- Value Meaning
	// No diagnostic
	SLBfdCommonState_SL_BFD_DIAG_NONE SLBfdCommonState_SLBfdDiagStateEnum = 0
	// Control detection time expired
	SLBfdCommonState_SL_BFD_DIAG_DETECT_EXPIRED SLBfdCommonState_SLBfdDiagStateEnum = 1
	// Neighbor signaled session down
	SLBfdCommonState_SL_BFD_DIAG_NBR_DOWN SLBfdCommonState_SLBfdDiagStateEnum = 2
	// Path down
	SLBfdCommonState_SL_BFD_DIAG_PATH_DOWN SLBfdCommonState_SLBfdDiagStateEnum = 3
	// Forwarding plane reset
	SLBfdCommonState_SL_BFD_DIAG_FWDING_PLANE_RESET SLBfdCommonState_SLBfdDiagStateEnum = 4
	// Administratively down
	SLBfdCommonState_SL_BFD_DIAG_ADMIN_DOWN SLBfdCommonState_SLBfdDiagStateEnum = 5
	// Reverse Concatenated Path Down
	SLBfdCommonState_SL_BFD_DIAG_REV_CONC_PATH_DOWN SLBfdCommonState_SLBfdDiagStateEnum = 6
	// Echo Function Failed
	SLBfdCommonState_SL_BFD_DIAG_ECHO_FUNCTION_FAILED SLBfdCommonState_SLBfdDiagStateEnum = 7
	// Concatenated Path Down
	SLBfdCommonState_SL_BFD_DIAG_CONC_PATH_DOWN SLBfdCommonState_SLBfdDiagStateEnum = 8
)

// Enum value maps for SLBfdCommonState_SLBfdDiagStateEnum.
var (
	SLBfdCommonState_SLBfdDiagStateEnum_name = map[int32]string{
		0: "SL_BFD_DIAG_NONE",
		1: "SL_BFD_DIAG_DETECT_EXPIRED",
		2: "SL_BFD_DIAG_NBR_DOWN",
		3: "SL_BFD_DIAG_PATH_DOWN",
		4: "SL_BFD_DIAG_FWDING_PLANE_RESET",
		5: "SL_BFD_DIAG_ADMIN_DOWN",
		6: "SL_BFD_DIAG_REV_CONC_PATH_DOWN",
		7: "SL_BFD_DIAG_ECHO_FUNCTION_FAILED",
		8: "SL_BFD_DIAG_CONC_PATH_DOWN",
	}
	SLBfdCommonState_SLBfdDiagStateEnum_value = map[string]int32{
		"SL_BFD_DIAG_NONE":                 0,
		"SL_BFD_DIAG_DETECT_EXPIRED":       1,
		"SL_BFD_DIAG_NBR_DOWN":             2,
		"SL_BFD_DIAG_PATH_DOWN":            3,
		"SL_BFD_DIAG_FWDING_PLANE_RESET":   4,
		"SL_BFD_DIAG_ADMIN_DOWN":           5,
		"SL_BFD_DIAG_REV_CONC_PATH_DOWN":   6,
		"SL_BFD_DIAG_ECHO_FUNCTION_FAILED": 7,
		"SL_BFD_DIAG_CONC_PATH_DOWN":       8,
	}
)

func (x SLBfdCommonState_SLBfdDiagStateEnum) Enum() *SLBfdCommonState_SLBfdDiagStateEnum {
	p := new(SLBfdCommonState_SLBfdDiagStateEnum)
	*p = x
	return p
}

func (x SLBfdCommonState_SLBfdDiagStateEnum) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (SLBfdCommonState_SLBfdDiagStateEnum) Descriptor() protoreflect.EnumDescriptor {
	return file_sl_bfd_common_proto_enumTypes[3].Descriptor()
}

func (SLBfdCommonState_SLBfdDiagStateEnum) Type() protoreflect.EnumType {
	return &file_sl_bfd_common_proto_enumTypes[3]
}

func (x SLBfdCommonState_SLBfdDiagStateEnum) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Use SLBfdCommonState_SLBfdDiagStateEnum.Descriptor instead.
func (SLBfdCommonState_SLBfdDiagStateEnum) EnumDescriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{7, 1}
}

// BFD Registration message.
type SLBfdRegMsg struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Registration Operation
	Oper SLRegOp `protobuf:"varint,1,opt,name=Oper,proto3,enum=service_layer.SLRegOp" json:"Oper,omitempty"`
}

func (x *SLBfdRegMsg) Reset() {
	*x = SLBfdRegMsg{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_bfd_common_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLBfdRegMsg) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLBfdRegMsg) ProtoMessage() {}

func (x *SLBfdRegMsg) ProtoReflect() protoreflect.Message {
	mi := &file_sl_bfd_common_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLBfdRegMsg.ProtoReflect.Descriptor instead.
func (*SLBfdRegMsg) Descriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{0}
}

func (x *SLBfdRegMsg) GetOper() SLRegOp {
	if x != nil {
		return x.Oper
	}
	return SLRegOp_SL_REGOP_RESERVED
}

// BFD Registration response message.
type SLBfdRegMsgRsp struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Error code
	ErrStatus *SLErrorStatus `protobuf:"bytes,1,opt,name=ErrStatus,proto3" json:"ErrStatus,omitempty"`
}

func (x *SLBfdRegMsgRsp) Reset() {
	*x = SLBfdRegMsgRsp{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_bfd_common_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLBfdRegMsgRsp) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLBfdRegMsgRsp) ProtoMessage() {}

func (x *SLBfdRegMsgRsp) ProtoReflect() protoreflect.Message {
	mi := &file_sl_bfd_common_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLBfdRegMsgRsp.ProtoReflect.Descriptor instead.
func (*SLBfdRegMsgRsp) Descriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{1}
}

func (x *SLBfdRegMsgRsp) GetErrStatus() *SLErrorStatus {
	if x != nil {
		return x.ErrStatus
	}
	return nil
}

// BFD Globals Get message.
type SLBfdGetMsg struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields
}

func (x *SLBfdGetMsg) Reset() {
	*x = SLBfdGetMsg{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_bfd_common_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLBfdGetMsg) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLBfdGetMsg) ProtoMessage() {}

func (x *SLBfdGetMsg) ProtoReflect() protoreflect.Message {
	mi := &file_sl_bfd_common_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLBfdGetMsg.ProtoReflect.Descriptor instead.
func (*SLBfdGetMsg) Descriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{2}
}

// BFD Get Global info response message.
type SLBfdGetMsgRsp struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Error code
	ErrStatus *SLErrorStatus `protobuf:"bytes,1,opt,name=ErrStatus,proto3" json:"ErrStatus,omitempty"`
	// Max BFD objects within a single BfdMsg message.
	MaxBfdSessionCfgPerSLBfdMsg uint32 `protobuf:"varint,2,opt,name=MaxBfdSessionCfgPerSLBfdMsg,proto3" json:"MaxBfdSessionCfgPerSLBfdMsg,omitempty"`
	// Min BFD Transmit Interval for single hop sessions.
	MinBfdTxIntervalSingleHop uint32 `protobuf:"varint,3,opt,name=MinBfdTxIntervalSingleHop,proto3" json:"MinBfdTxIntervalSingleHop,omitempty"`
	// Min BFD session Transmit Interval for multi hop sessions.
	MinBfdTxIntervalMultiHop uint32 `protobuf:"varint,4,opt,name=MinBfdTxIntervalMultiHop,proto3" json:"MinBfdTxIntervalMultiHop,omitempty"`
	// Min BFD detection multiplier for single hop sessions.
	MinBfdDetectMultiplierSingleHop uint32 `protobuf:"varint,5,opt,name=MinBfdDetectMultiplierSingleHop,proto3" json:"MinBfdDetectMultiplierSingleHop,omitempty"`
	// Min BFD detection multiplier for multi hop sessions.
	MinBfdDetectMultiplierMultiHop uint32 `protobuf:"varint,6,opt,name=MinBfdDetectMultiplierMultiHop,proto3" json:"MinBfdDetectMultiplierMultiHop,omitempty"`
}

func (x *SLBfdGetMsgRsp) Reset() {
	*x = SLBfdGetMsgRsp{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_bfd_common_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLBfdGetMsgRsp) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLBfdGetMsgRsp) ProtoMessage() {}

func (x *SLBfdGetMsgRsp) ProtoReflect() protoreflect.Message {
	mi := &file_sl_bfd_common_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLBfdGetMsgRsp.ProtoReflect.Descriptor instead.
func (*SLBfdGetMsgRsp) Descriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{3}
}

func (x *SLBfdGetMsgRsp) GetErrStatus() *SLErrorStatus {
	if x != nil {
		return x.ErrStatus
	}
	return nil
}

func (x *SLBfdGetMsgRsp) GetMaxBfdSessionCfgPerSLBfdMsg() uint32 {
	if x != nil {
		return x.MaxBfdSessionCfgPerSLBfdMsg
	}
	return 0
}

func (x *SLBfdGetMsgRsp) GetMinBfdTxIntervalSingleHop() uint32 {
	if x != nil {
		return x.MinBfdTxIntervalSingleHop
	}
	return 0
}

func (x *SLBfdGetMsgRsp) GetMinBfdTxIntervalMultiHop() uint32 {
	if x != nil {
		return x.MinBfdTxIntervalMultiHop
	}
	return 0
}

func (x *SLBfdGetMsgRsp) GetMinBfdDetectMultiplierSingleHop() uint32 {
	if x != nil {
		return x.MinBfdDetectMultiplierSingleHop
	}
	return 0
}

func (x *SLBfdGetMsgRsp) GetMinBfdDetectMultiplierMultiHop() uint32 {
	if x != nil {
		return x.MinBfdDetectMultiplierMultiHop
	}
	return 0
}

// BFD Get Global Stats response message.
type SLBfdGetStatsMsgRsp struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Error code
	ErrStatus *SLErrorStatus `protobuf:"bytes,1,opt,name=ErrStatus,proto3" json:"ErrStatus,omitempty"`
	// Global BFD event sequence number. This is used to order various events
	// The sequence number is equivalent to a timestamp
	// This field contains the latest global BFD event sequence number
	SeqNum uint64 `protobuf:"varint,2,opt,name=SeqNum,proto3" json:"SeqNum,omitempty"`
	// Num BFD sessions added through the service layer.
	BfdCount uint32 `protobuf:"varint,3,opt,name=BfdCount,proto3" json:"BfdCount,omitempty"`
}

func (x *SLBfdGetStatsMsgRsp) Reset() {
	*x = SLBfdGetStatsMsgRsp{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_bfd_common_proto_msgTypes[4]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLBfdGetStatsMsgRsp) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLBfdGetStatsMsgRsp) ProtoMessage() {}

func (x *SLBfdGetStatsMsgRsp) ProtoReflect() protoreflect.Message {
	mi := &file_sl_bfd_common_proto_msgTypes[4]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLBfdGetStatsMsgRsp.ProtoReflect.Descriptor instead.
func (*SLBfdGetStatsMsgRsp) Descriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{4}
}

func (x *SLBfdGetStatsMsgRsp) GetErrStatus() *SLErrorStatus {
	if x != nil {
		return x.ErrStatus
	}
	return nil
}

func (x *SLBfdGetStatsMsgRsp) GetSeqNum() uint64 {
	if x != nil {
		return x.SeqNum
	}
	return 0
}

func (x *SLBfdGetStatsMsgRsp) GetBfdCount() uint32 {
	if x != nil {
		return x.BfdCount
	}
	return 0
}

// BFD Get Notifications message.
type SLBfdGetNotifMsg struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields
}

func (x *SLBfdGetNotifMsg) Reset() {
	*x = SLBfdGetNotifMsg{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_bfd_common_proto_msgTypes[5]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLBfdGetNotifMsg) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLBfdGetNotifMsg) ProtoMessage() {}

func (x *SLBfdGetNotifMsg) ProtoReflect() protoreflect.Message {
	mi := &file_sl_bfd_common_proto_msgTypes[5]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLBfdGetNotifMsg.ProtoReflect.Descriptor instead.
func (*SLBfdGetNotifMsg) Descriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{5}
}

// Common bidirectional forwarding detection attributes.
type SLBfdConfigCommon struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Desired Tx interval in micro seconds.
	// This is the minimum interval that the local system would like to
	// use when transmitting BFD control packets.
	// The value zero is reserved.
	// This can be changed at anytime.
	DesiredTxIntUsec uint32 `protobuf:"varint,1,opt,name=DesiredTxIntUsec,proto3" json:"DesiredTxIntUsec,omitempty"`
	// Detection time = DesiredTxIntUsec *
	//                  DetectMultiplier
	// Detection time is the period of time without receiving BFD
	// packets after which the session is determined to have failed.
	// Note: there may be a different detection time in each direction.
	DetectMultiplier uint32 `protobuf:"varint,2,opt,name=DetectMultiplier,proto3" json:"DetectMultiplier,omitempty"`
}

func (x *SLBfdConfigCommon) Reset() {
	*x = SLBfdConfigCommon{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_bfd_common_proto_msgTypes[6]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLBfdConfigCommon) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLBfdConfigCommon) ProtoMessage() {}

func (x *SLBfdConfigCommon) ProtoReflect() protoreflect.Message {
	mi := &file_sl_bfd_common_proto_msgTypes[6]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLBfdConfigCommon.ProtoReflect.Descriptor instead.
func (*SLBfdConfigCommon) Descriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{6}
}

func (x *SLBfdConfigCommon) GetDesiredTxIntUsec() uint32 {
	if x != nil {
		return x.DesiredTxIntUsec
	}
	return 0
}

func (x *SLBfdConfigCommon) GetDetectMultiplier() uint32 {
	if x != nil {
		return x.DetectMultiplier
	}
	return 0
}

// BFD state information.
type SLBfdCommonState struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Global BFD event sequence number. This is used to order various events
	// The sequence number is equivalent to a timestamp
	SeqNum uint64                              `protobuf:"varint,1,opt,name=SeqNum,proto3" json:"SeqNum,omitempty"`
	Status SLBfdCommonState_SLBfdStateEnum     `protobuf:"varint,2,opt,name=Status,proto3,enum=service_layer.SLBfdCommonState_SLBfdStateEnum" json:"Status,omitempty"`
	Diag   SLBfdCommonState_SLBfdDiagStateEnum `protobuf:"varint,3,opt,name=Diag,proto3,enum=service_layer.SLBfdCommonState_SLBfdDiagStateEnum" json:"Diag,omitempty"`
}

func (x *SLBfdCommonState) Reset() {
	*x = SLBfdCommonState{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_bfd_common_proto_msgTypes[7]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLBfdCommonState) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLBfdCommonState) ProtoMessage() {}

func (x *SLBfdCommonState) ProtoReflect() protoreflect.Message {
	mi := &file_sl_bfd_common_proto_msgTypes[7]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLBfdCommonState.ProtoReflect.Descriptor instead.
func (*SLBfdCommonState) Descriptor() ([]byte, []int) {
	return file_sl_bfd_common_proto_rawDescGZIP(), []int{7}
}

func (x *SLBfdCommonState) GetSeqNum() uint64 {
	if x != nil {
		return x.SeqNum
	}
	return 0
}

func (x *SLBfdCommonState) GetStatus() SLBfdCommonState_SLBfdStateEnum {
	if x != nil {
		return x.Status
	}
	return SLBfdCommonState_SL_BFD_SESSION_STATE_UNKNOWN
}

func (x *SLBfdCommonState) GetDiag() SLBfdCommonState_SLBfdDiagStateEnum {
	if x != nil {
		return x.Diag
	}
	return SLBfdCommonState_SL_BFD_DIAG_NONE
}

var File_sl_bfd_common_proto protoreflect.FileDescriptor

var file_sl_bfd_common_proto_rawDesc = []byte{
	0x0a, 0x13, 0x73, 0x6c, 0x5f, 0x62, 0x66, 0x64, 0x5f, 0x63, 0x6f, 0x6d, 0x6d, 0x6f, 0x6e, 0x2e,
	0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x0d, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c,
	0x61, 0x79, 0x65, 0x72, 0x1a, 0x15, 0x73, 0x6c, 0x5f, 0x63, 0x6f, 0x6d, 0x6d, 0x6f, 0x6e, 0x5f,
	0x74, 0x79, 0x70, 0x65, 0x73, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22, 0x39, 0x0a, 0x0b, 0x53,
	0x4c, 0x42, 0x66, 0x64, 0x52, 0x65, 0x67, 0x4d, 0x73, 0x67, 0x12, 0x2a, 0x0a, 0x04, 0x4f, 0x70,
	0x65, 0x72, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0e, 0x32, 0x16, 0x2e, 0x73, 0x65, 0x72, 0x76, 0x69,
	0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x52, 0x65, 0x67, 0x4f, 0x70,
	0x52, 0x04, 0x4f, 0x70, 0x65, 0x72, 0x22, 0x4c, 0x0a, 0x0e, 0x53, 0x4c, 0x42, 0x66, 0x64, 0x52,
	0x65, 0x67, 0x4d, 0x73, 0x67, 0x52, 0x73, 0x70, 0x12, 0x3a, 0x0a, 0x09, 0x45, 0x72, 0x72, 0x53,
	0x74, 0x61, 0x74, 0x75, 0x73, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1c, 0x2e, 0x73, 0x65,
	0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x45, 0x72,
	0x72, 0x6f, 0x72, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x09, 0x45, 0x72, 0x72, 0x53, 0x74,
	0x61, 0x74, 0x75, 0x73, 0x22, 0x0d, 0x0a, 0x0b, 0x53, 0x4c, 0x42, 0x66, 0x64, 0x47, 0x65, 0x74,
	0x4d, 0x73, 0x67, 0x22, 0x9a, 0x03, 0x0a, 0x0e, 0x53, 0x4c, 0x42, 0x66, 0x64, 0x47, 0x65, 0x74,
	0x4d, 0x73, 0x67, 0x52, 0x73, 0x70, 0x12, 0x3a, 0x0a, 0x09, 0x45, 0x72, 0x72, 0x53, 0x74, 0x61,
	0x74, 0x75, 0x73, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1c, 0x2e, 0x73, 0x65, 0x72, 0x76,
	0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x45, 0x72, 0x72, 0x6f,
	0x72, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x09, 0x45, 0x72, 0x72, 0x53, 0x74, 0x61, 0x74,
	0x75, 0x73, 0x12, 0x40, 0x0a, 0x1b, 0x4d, 0x61, 0x78, 0x42, 0x66, 0x64, 0x53, 0x65, 0x73, 0x73,
	0x69, 0x6f, 0x6e, 0x43, 0x66, 0x67, 0x50, 0x65, 0x72, 0x53, 0x4c, 0x42, 0x66, 0x64, 0x4d, 0x73,
	0x67, 0x18, 0x02, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x1b, 0x4d, 0x61, 0x78, 0x42, 0x66, 0x64, 0x53,
	0x65, 0x73, 0x73, 0x69, 0x6f, 0x6e, 0x43, 0x66, 0x67, 0x50, 0x65, 0x72, 0x53, 0x4c, 0x42, 0x66,
	0x64, 0x4d, 0x73, 0x67, 0x12, 0x3c, 0x0a, 0x19, 0x4d, 0x69, 0x6e, 0x42, 0x66, 0x64, 0x54, 0x78,
	0x49, 0x6e, 0x74, 0x65, 0x72, 0x76, 0x61, 0x6c, 0x53, 0x69, 0x6e, 0x67, 0x6c, 0x65, 0x48, 0x6f,
	0x70, 0x18, 0x03, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x19, 0x4d, 0x69, 0x6e, 0x42, 0x66, 0x64, 0x54,
	0x78, 0x49, 0x6e, 0x74, 0x65, 0x72, 0x76, 0x61, 0x6c, 0x53, 0x69, 0x6e, 0x67, 0x6c, 0x65, 0x48,
	0x6f, 0x70, 0x12, 0x3a, 0x0a, 0x18, 0x4d, 0x69, 0x6e, 0x42, 0x66, 0x64, 0x54, 0x78, 0x49, 0x6e,
	0x74, 0x65, 0x72, 0x76, 0x61, 0x6c, 0x4d, 0x75, 0x6c, 0x74, 0x69, 0x48, 0x6f, 0x70, 0x18, 0x04,
	0x20, 0x01, 0x28, 0x0d, 0x52, 0x18, 0x4d, 0x69, 0x6e, 0x42, 0x66, 0x64, 0x54, 0x78, 0x49, 0x6e,
	0x74, 0x65, 0x72, 0x76, 0x61, 0x6c, 0x4d, 0x75, 0x6c, 0x74, 0x69, 0x48, 0x6f, 0x70, 0x12, 0x48,
	0x0a, 0x1f, 0x4d, 0x69, 0x6e, 0x42, 0x66, 0x64, 0x44, 0x65, 0x74, 0x65, 0x63, 0x74, 0x4d, 0x75,
	0x6c, 0x74, 0x69, 0x70, 0x6c, 0x69, 0x65, 0x72, 0x53, 0x69, 0x6e, 0x67, 0x6c, 0x65, 0x48, 0x6f,
	0x70, 0x18, 0x05, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x1f, 0x4d, 0x69, 0x6e, 0x42, 0x66, 0x64, 0x44,
	0x65, 0x74, 0x65, 0x63, 0x74, 0x4d, 0x75, 0x6c, 0x74, 0x69, 0x70, 0x6c, 0x69, 0x65, 0x72, 0x53,
	0x69, 0x6e, 0x67, 0x6c, 0x65, 0x48, 0x6f, 0x70, 0x12, 0x46, 0x0a, 0x1e, 0x4d, 0x69, 0x6e, 0x42,
	0x66, 0x64, 0x44, 0x65, 0x74, 0x65, 0x63, 0x74, 0x4d, 0x75, 0x6c, 0x74, 0x69, 0x70, 0x6c, 0x69,
	0x65, 0x72, 0x4d, 0x75, 0x6c, 0x74, 0x69, 0x48, 0x6f, 0x70, 0x18, 0x06, 0x20, 0x01, 0x28, 0x0d,
	0x52, 0x1e, 0x4d, 0x69, 0x6e, 0x42, 0x66, 0x64, 0x44, 0x65, 0x74, 0x65, 0x63, 0x74, 0x4d, 0x75,
	0x6c, 0x74, 0x69, 0x70, 0x6c, 0x69, 0x65, 0x72, 0x4d, 0x75, 0x6c, 0x74, 0x69, 0x48, 0x6f, 0x70,
	0x22, 0x85, 0x01, 0x0a, 0x13, 0x53, 0x4c, 0x42, 0x66, 0x64, 0x47, 0x65, 0x74, 0x53, 0x74, 0x61,
	0x74, 0x73, 0x4d, 0x73, 0x67, 0x52, 0x73, 0x70, 0x12, 0x3a, 0x0a, 0x09, 0x45, 0x72, 0x72, 0x53,
	0x74, 0x61, 0x74, 0x75, 0x73, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1c, 0x2e, 0x73, 0x65,
	0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x45, 0x72,
	0x72, 0x6f, 0x72, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x09, 0x45, 0x72, 0x72, 0x53, 0x74,
	0x61, 0x74, 0x75, 0x73, 0x12, 0x16, 0x0a, 0x06, 0x53, 0x65, 0x71, 0x4e, 0x75, 0x6d, 0x18, 0x02,
	0x20, 0x01, 0x28, 0x04, 0x52, 0x06, 0x53, 0x65, 0x71, 0x4e, 0x75, 0x6d, 0x12, 0x1a, 0x0a, 0x08,
	0x42, 0x66, 0x64, 0x43, 0x6f, 0x75, 0x6e, 0x74, 0x18, 0x03, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x08,
	0x42, 0x66, 0x64, 0x43, 0x6f, 0x75, 0x6e, 0x74, 0x22, 0x12, 0x0a, 0x10, 0x53, 0x4c, 0x42, 0x66,
	0x64, 0x47, 0x65, 0x74, 0x4e, 0x6f, 0x74, 0x69, 0x66, 0x4d, 0x73, 0x67, 0x22, 0x6b, 0x0a, 0x11,
	0x53, 0x4c, 0x42, 0x66, 0x64, 0x43, 0x6f, 0x6e, 0x66, 0x69, 0x67, 0x43, 0x6f, 0x6d, 0x6d, 0x6f,
	0x6e, 0x12, 0x2a, 0x0a, 0x10, 0x44, 0x65, 0x73, 0x69, 0x72, 0x65, 0x64, 0x54, 0x78, 0x49, 0x6e,
	0x74, 0x55, 0x73, 0x65, 0x63, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x10, 0x44, 0x65, 0x73,
	0x69, 0x72, 0x65, 0x64, 0x54, 0x78, 0x49, 0x6e, 0x74, 0x55, 0x73, 0x65, 0x63, 0x12, 0x2a, 0x0a,
	0x10, 0x44, 0x65, 0x74, 0x65, 0x63, 0x74, 0x4d, 0x75, 0x6c, 0x74, 0x69, 0x70, 0x6c, 0x69, 0x65,
	0x72, 0x18, 0x02, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x10, 0x44, 0x65, 0x74, 0x65, 0x63, 0x74, 0x4d,
	0x75, 0x6c, 0x74, 0x69, 0x70, 0x6c, 0x69, 0x65, 0x72, 0x22, 0xe9, 0x04, 0x0a, 0x10, 0x53, 0x4c,
	0x42, 0x66, 0x64, 0x43, 0x6f, 0x6d, 0x6d, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x65, 0x12, 0x16,
	0x0a, 0x06, 0x53, 0x65, 0x71, 0x4e, 0x75, 0x6d, 0x18, 0x01, 0x20, 0x01, 0x28, 0x04, 0x52, 0x06,
	0x53, 0x65, 0x71, 0x4e, 0x75, 0x6d, 0x12, 0x46, 0x0a, 0x06, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73,
	0x18, 0x02, 0x20, 0x01, 0x28, 0x0e, 0x32, 0x2e, 0x2e, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65,
	0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x42, 0x66, 0x64, 0x43, 0x6f, 0x6d, 0x6d,
	0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x65, 0x2e, 0x53, 0x4c, 0x42, 0x66, 0x64, 0x53, 0x74, 0x61,
	0x74, 0x65, 0x45, 0x6e, 0x75, 0x6d, 0x52, 0x06, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x12, 0x46,
	0x0a, 0x04, 0x44, 0x69, 0x61, 0x67, 0x18, 0x03, 0x20, 0x01, 0x28, 0x0e, 0x32, 0x32, 0x2e, 0x73,
	0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x42,
	0x66, 0x64, 0x43, 0x6f, 0x6d, 0x6d, 0x6f, 0x6e, 0x53, 0x74, 0x61, 0x74, 0x65, 0x2e, 0x53, 0x4c,
	0x42, 0x66, 0x64, 0x44, 0x69, 0x61, 0x67, 0x53, 0x74, 0x61, 0x74, 0x65, 0x45, 0x6e, 0x75, 0x6d,
	0x52, 0x04, 0x44, 0x69, 0x61, 0x67, 0x22, 0x80, 0x01, 0x0a, 0x0e, 0x53, 0x4c, 0x42, 0x66, 0x64,
	0x53, 0x74, 0x61, 0x74, 0x65, 0x45, 0x6e, 0x75, 0x6d, 0x12, 0x20, 0x0a, 0x1c, 0x53, 0x4c, 0x5f,
	0x42, 0x46, 0x44, 0x5f, 0x53, 0x45, 0x53, 0x53, 0x49, 0x4f, 0x4e, 0x5f, 0x53, 0x54, 0x41, 0x54,
	0x45, 0x5f, 0x55, 0x4e, 0x4b, 0x4e, 0x4f, 0x57, 0x4e, 0x10, 0x00, 0x12, 0x15, 0x0a, 0x11, 0x53,
	0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x53, 0x45, 0x53, 0x53, 0x49, 0x4f, 0x4e, 0x5f, 0x55, 0x50,
	0x10, 0x01, 0x12, 0x17, 0x0a, 0x13, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x53, 0x45, 0x53,
	0x53, 0x49, 0x4f, 0x4e, 0x5f, 0x44, 0x4f, 0x57, 0x4e, 0x10, 0x02, 0x12, 0x1c, 0x0a, 0x18, 0x53,
	0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x4e, 0x45, 0x49, 0x47, 0x48, 0x42, 0x4f, 0x52, 0x5f, 0x55,
	0x4e, 0x43, 0x4f, 0x4e, 0x46, 0x49, 0x47, 0x10, 0x03, 0x22, 0xa9, 0x02, 0x0a, 0x12, 0x53, 0x4c,
	0x42, 0x66, 0x64, 0x44, 0x69, 0x61, 0x67, 0x53, 0x74, 0x61, 0x74, 0x65, 0x45, 0x6e, 0x75, 0x6d,
	0x12, 0x14, 0x0a, 0x10, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x44, 0x49, 0x41, 0x47, 0x5f,
	0x4e, 0x4f, 0x4e, 0x45, 0x10, 0x00, 0x12, 0x1e, 0x0a, 0x1a, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44,
	0x5f, 0x44, 0x49, 0x41, 0x47, 0x5f, 0x44, 0x45, 0x54, 0x45, 0x43, 0x54, 0x5f, 0x45, 0x58, 0x50,
	0x49, 0x52, 0x45, 0x44, 0x10, 0x01, 0x12, 0x18, 0x0a, 0x14, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44,
	0x5f, 0x44, 0x49, 0x41, 0x47, 0x5f, 0x4e, 0x42, 0x52, 0x5f, 0x44, 0x4f, 0x57, 0x4e, 0x10, 0x02,
	0x12, 0x19, 0x0a, 0x15, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x44, 0x49, 0x41, 0x47, 0x5f,
	0x50, 0x41, 0x54, 0x48, 0x5f, 0x44, 0x4f, 0x57, 0x4e, 0x10, 0x03, 0x12, 0x22, 0x0a, 0x1e, 0x53,
	0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x44, 0x49, 0x41, 0x47, 0x5f, 0x46, 0x57, 0x44, 0x49, 0x4e,
	0x47, 0x5f, 0x50, 0x4c, 0x41, 0x4e, 0x45, 0x5f, 0x52, 0x45, 0x53, 0x45, 0x54, 0x10, 0x04, 0x12,
	0x1a, 0x0a, 0x16, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x44, 0x49, 0x41, 0x47, 0x5f, 0x41,
	0x44, 0x4d, 0x49, 0x4e, 0x5f, 0x44, 0x4f, 0x57, 0x4e, 0x10, 0x05, 0x12, 0x22, 0x0a, 0x1e, 0x53,
	0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x44, 0x49, 0x41, 0x47, 0x5f, 0x52, 0x45, 0x56, 0x5f, 0x43,
	0x4f, 0x4e, 0x43, 0x5f, 0x50, 0x41, 0x54, 0x48, 0x5f, 0x44, 0x4f, 0x57, 0x4e, 0x10, 0x06, 0x12,
	0x24, 0x0a, 0x20, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x44, 0x49, 0x41, 0x47, 0x5f, 0x45,
	0x43, 0x48, 0x4f, 0x5f, 0x46, 0x55, 0x4e, 0x43, 0x54, 0x49, 0x4f, 0x4e, 0x5f, 0x46, 0x41, 0x49,
	0x4c, 0x45, 0x44, 0x10, 0x07, 0x12, 0x1e, 0x0a, 0x1a, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f,
	0x44, 0x49, 0x41, 0x47, 0x5f, 0x43, 0x4f, 0x4e, 0x43, 0x5f, 0x50, 0x41, 0x54, 0x48, 0x5f, 0x44,
	0x4f, 0x57, 0x4e, 0x10, 0x08, 0x2a, 0x4d, 0x0a, 0x09, 0x53, 0x4c, 0x42, 0x66, 0x64, 0x54, 0x79,
	0x70, 0x65, 0x12, 0x13, 0x0a, 0x0f, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x52, 0x45, 0x53,
	0x45, 0x52, 0x56, 0x45, 0x44, 0x10, 0x00, 0x12, 0x15, 0x0a, 0x11, 0x53, 0x4c, 0x5f, 0x42, 0x46,
	0x44, 0x5f, 0x53, 0x49, 0x4e, 0x47, 0x4c, 0x45, 0x5f, 0x48, 0x4f, 0x50, 0x10, 0x01, 0x12, 0x14,
	0x0a, 0x10, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x4d, 0x55, 0x4c, 0x54, 0x49, 0x5f, 0x48,
	0x4f, 0x50, 0x10, 0x02, 0x2a, 0x72, 0x0a, 0x0e, 0x53, 0x4c, 0x42, 0x66, 0x64, 0x4e, 0x6f, 0x74,
	0x69, 0x66, 0x54, 0x79, 0x70, 0x65, 0x12, 0x1e, 0x0a, 0x1a, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44,
	0x5f, 0x45, 0x56, 0x45, 0x4e, 0x54, 0x5f, 0x54, 0x59, 0x50, 0x45, 0x5f, 0x52, 0x45, 0x53, 0x45,
	0x52, 0x56, 0x45, 0x44, 0x10, 0x00, 0x12, 0x1b, 0x0a, 0x17, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44,
	0x5f, 0x45, 0x56, 0x45, 0x4e, 0x54, 0x5f, 0x54, 0x59, 0x50, 0x45, 0x5f, 0x45, 0x52, 0x52, 0x4f,
	0x52, 0x10, 0x01, 0x12, 0x23, 0x0a, 0x1f, 0x53, 0x4c, 0x5f, 0x42, 0x46, 0x44, 0x5f, 0x45, 0x56,
	0x45, 0x4e, 0x54, 0x5f, 0x54, 0x59, 0x50, 0x45, 0x5f, 0x53, 0x45, 0x53, 0x53, 0x49, 0x4f, 0x4e,
	0x5f, 0x53, 0x54, 0x41, 0x54, 0x45, 0x10, 0x02, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_sl_bfd_common_proto_rawDescOnce sync.Once
	file_sl_bfd_common_proto_rawDescData = file_sl_bfd_common_proto_rawDesc
)

func file_sl_bfd_common_proto_rawDescGZIP() []byte {
	file_sl_bfd_common_proto_rawDescOnce.Do(func() {
		file_sl_bfd_common_proto_rawDescData = protoimpl.X.CompressGZIP(file_sl_bfd_common_proto_rawDescData)
	})
	return file_sl_bfd_common_proto_rawDescData
}

var file_sl_bfd_common_proto_enumTypes = make([]protoimpl.EnumInfo, 4)
var file_sl_bfd_common_proto_msgTypes = make([]protoimpl.MessageInfo, 8)
var file_sl_bfd_common_proto_goTypes = []interface{}{
	(SLBfdType)(0),                           // 0: service_layer.SLBfdType
	(SLBfdNotifType)(0),                      // 1: service_layer.SLBfdNotifType
	(SLBfdCommonState_SLBfdStateEnum)(0),     // 2: service_layer.SLBfdCommonState.SLBfdStateEnum
	(SLBfdCommonState_SLBfdDiagStateEnum)(0), // 3: service_layer.SLBfdCommonState.SLBfdDiagStateEnum
	(*SLBfdRegMsg)(nil),                      // 4: service_layer.SLBfdRegMsg
	(*SLBfdRegMsgRsp)(nil),                   // 5: service_layer.SLBfdRegMsgRsp
	(*SLBfdGetMsg)(nil),                      // 6: service_layer.SLBfdGetMsg
	(*SLBfdGetMsgRsp)(nil),                   // 7: service_layer.SLBfdGetMsgRsp
	(*SLBfdGetStatsMsgRsp)(nil),              // 8: service_layer.SLBfdGetStatsMsgRsp
	(*SLBfdGetNotifMsg)(nil),                 // 9: service_layer.SLBfdGetNotifMsg
	(*SLBfdConfigCommon)(nil),                // 10: service_layer.SLBfdConfigCommon
	(*SLBfdCommonState)(nil),                 // 11: service_layer.SLBfdCommonState
	(SLRegOp)(0),                             // 12: service_layer.SLRegOp
	(*SLErrorStatus)(nil),                    // 13: service_layer.SLErrorStatus
}
var file_sl_bfd_common_proto_depIdxs = []int32{
	12, // 0: service_layer.SLBfdRegMsg.Oper:type_name -> service_layer.SLRegOp
	13, // 1: service_layer.SLBfdRegMsgRsp.ErrStatus:type_name -> service_layer.SLErrorStatus
	13, // 2: service_layer.SLBfdGetMsgRsp.ErrStatus:type_name -> service_layer.SLErrorStatus
	13, // 3: service_layer.SLBfdGetStatsMsgRsp.ErrStatus:type_name -> service_layer.SLErrorStatus
	2,  // 4: service_layer.SLBfdCommonState.Status:type_name -> service_layer.SLBfdCommonState.SLBfdStateEnum
	3,  // 5: service_layer.SLBfdCommonState.Diag:type_name -> service_layer.SLBfdCommonState.SLBfdDiagStateEnum
	6,  // [6:6] is the sub-list for method output_type
	6,  // [6:6] is the sub-list for method input_type
	6,  // [6:6] is the sub-list for extension type_name
	6,  // [6:6] is the sub-list for extension extendee
	0,  // [0:6] is the sub-list for field type_name
}

func init() { file_sl_bfd_common_proto_init() }
func file_sl_bfd_common_proto_init() {
	if File_sl_bfd_common_proto != nil {
		return
	}
	file_sl_common_types_proto_init()
	if !protoimpl.UnsafeEnabled {
		file_sl_bfd_common_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLBfdRegMsg); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_sl_bfd_common_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLBfdRegMsgRsp); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_sl_bfd_common_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLBfdGetMsg); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_sl_bfd_common_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLBfdGetMsgRsp); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_sl_bfd_common_proto_msgTypes[4].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLBfdGetStatsMsgRsp); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_sl_bfd_common_proto_msgTypes[5].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLBfdGetNotifMsg); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_sl_bfd_common_proto_msgTypes[6].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLBfdConfigCommon); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_sl_bfd_common_proto_msgTypes[7].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLBfdCommonState); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_sl_bfd_common_proto_rawDesc,
			NumEnums:      4,
			NumMessages:   8,
			NumExtensions: 0,
			NumServices:   0,
		},
		GoTypes:           file_sl_bfd_common_proto_goTypes,
		DependencyIndexes: file_sl_bfd_common_proto_depIdxs,
		EnumInfos:         file_sl_bfd_common_proto_enumTypes,
		MessageInfos:      file_sl_bfd_common_proto_msgTypes,
	}.Build()
	File_sl_bfd_common_proto = out.File
	file_sl_bfd_common_proto_rawDesc = nil
	file_sl_bfd_common_proto_goTypes = nil
	file_sl_bfd_common_proto_depIdxs = nil
}
