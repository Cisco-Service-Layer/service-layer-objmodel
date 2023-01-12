// @file
// @brief Server RPC proto file. Client invokes to init the session
// on server.
//
// ----------------------------------------------------------------
//  Copyright (c) 2019, 2023 by Cisco Systems, Inc.
//  All rights reserved.
// -----------------------------------------------------------------
//
//

// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.28.1
// 	protoc        v3.18.3
// source: sl_global.proto

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

// Global Event Notification types.
type SLGlobalNotifType int32

const (
	// Reserved. 0x0
	SLGlobalNotifType_SL_GLOBAL_EVENT_TYPE_RESERVED SLGlobalNotifType = 0
	// Error. ErrStatus field elaborates on the message. 0x1
	SLGlobalNotifType_SL_GLOBAL_EVENT_TYPE_ERROR SLGlobalNotifType = 1
	// HeartBeat. 0x2
	SLGlobalNotifType_SL_GLOBAL_EVENT_TYPE_HEARTBEAT SLGlobalNotifType = 2
	// Version. SLInitMsgRsp field elaborates on the server version. 0x3
	SLGlobalNotifType_SL_GLOBAL_EVENT_TYPE_VERSION SLGlobalNotifType = 3
)

// Enum value maps for SLGlobalNotifType.
var (
	SLGlobalNotifType_name = map[int32]string{
		0: "SL_GLOBAL_EVENT_TYPE_RESERVED",
		1: "SL_GLOBAL_EVENT_TYPE_ERROR",
		2: "SL_GLOBAL_EVENT_TYPE_HEARTBEAT",
		3: "SL_GLOBAL_EVENT_TYPE_VERSION",
	}
	SLGlobalNotifType_value = map[string]int32{
		"SL_GLOBAL_EVENT_TYPE_RESERVED":  0,
		"SL_GLOBAL_EVENT_TYPE_ERROR":     1,
		"SL_GLOBAL_EVENT_TYPE_HEARTBEAT": 2,
		"SL_GLOBAL_EVENT_TYPE_VERSION":   3,
	}
)

func (x SLGlobalNotifType) Enum() *SLGlobalNotifType {
	p := new(SLGlobalNotifType)
	*p = x
	return p
}

func (x SLGlobalNotifType) String() string {
	return protoimpl.X.EnumStringOf(x.Descriptor(), protoreflect.EnumNumber(x))
}

func (SLGlobalNotifType) Descriptor() protoreflect.EnumDescriptor {
	return file_sl_global_proto_enumTypes[0].Descriptor()
}

func (SLGlobalNotifType) Type() protoreflect.EnumType {
	return &file_sl_global_proto_enumTypes[0]
}

func (x SLGlobalNotifType) Number() protoreflect.EnumNumber {
	return protoreflect.EnumNumber(x)
}

// Deprecated: Use SLGlobalNotifType.Descriptor instead.
func (SLGlobalNotifType) EnumDescriptor() ([]byte, []int) {
	return file_sl_global_proto_rawDescGZIP(), []int{0}
}

// Initialization message sent to the server.
// If the client and server are running compatible version numbers, a
// connection will be made and the server response will be received
// with a successful status code.
type SLInitMsg struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Client's Major version of service-layer API (refer to sl_version.proto)
	MajorVer uint32 `protobuf:"varint,1,opt,name=MajorVer,proto3" json:"MajorVer,omitempty"`
	// Minor Version
	MinorVer uint32 `protobuf:"varint,2,opt,name=MinorVer,proto3" json:"MinorVer,omitempty"`
	// Sub-Version
	SubVer uint32 `protobuf:"varint,3,opt,name=SubVer,proto3" json:"SubVer,omitempty"`
}

func (x *SLInitMsg) Reset() {
	*x = SLInitMsg{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_global_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLInitMsg) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLInitMsg) ProtoMessage() {}

func (x *SLInitMsg) ProtoReflect() protoreflect.Message {
	mi := &file_sl_global_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLInitMsg.ProtoReflect.Descriptor instead.
func (*SLInitMsg) Descriptor() ([]byte, []int) {
	return file_sl_global_proto_rawDescGZIP(), []int{0}
}

func (x *SLInitMsg) GetMajorVer() uint32 {
	if x != nil {
		return x.MajorVer
	}
	return 0
}

func (x *SLInitMsg) GetMinorVer() uint32 {
	if x != nil {
		return x.MinorVer
	}
	return 0
}

func (x *SLInitMsg) GetSubVer() uint32 {
	if x != nil {
		return x.SubVer
	}
	return 0
}

// Server's response to the SLInitMsg.
// On Success (ErrStatus), the session with the server is established
// and the client is allowed to proceed.
type SLInitMsgRsp struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Server's version of service-layer API (refer to sl_version.proto)
	// Major-number revisions are NOT backwards compatible,
	// unless otherwise specified. The Server may reject a session if there
	// is a version number mismatch or non-backwards compatibility.
	MajorVer uint32 `protobuf:"varint,1,opt,name=MajorVer,proto3" json:"MajorVer,omitempty"`
	// Minor Version
	MinorVer uint32 `protobuf:"varint,2,opt,name=MinorVer,proto3" json:"MinorVer,omitempty"`
	// Sub-Version
	SubVer uint32 `protobuf:"varint,3,opt,name=SubVer,proto3" json:"SubVer,omitempty"`
}

func (x *SLInitMsgRsp) Reset() {
	*x = SLInitMsgRsp{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_global_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLInitMsgRsp) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLInitMsgRsp) ProtoMessage() {}

func (x *SLInitMsgRsp) ProtoReflect() protoreflect.Message {
	mi := &file_sl_global_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLInitMsgRsp.ProtoReflect.Descriptor instead.
func (*SLInitMsgRsp) Descriptor() ([]byte, []int) {
	return file_sl_global_proto_rawDescGZIP(), []int{1}
}

func (x *SLInitMsgRsp) GetMajorVer() uint32 {
	if x != nil {
		return x.MajorVer
	}
	return 0
}

func (x *SLInitMsgRsp) GetMinorVer() uint32 {
	if x != nil {
		return x.MinorVer
	}
	return 0
}

func (x *SLInitMsgRsp) GetSubVer() uint32 {
	if x != nil {
		return x.SubVer
	}
	return 0
}

// Routes replay error notification.
type SLVrfRouteReplayErrorNotif struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// VRF Name.
	VrfName string `protobuf:"bytes,1,opt,name=VrfName,proto3" json:"VrfName,omitempty"`
}

func (x *SLVrfRouteReplayErrorNotif) Reset() {
	*x = SLVrfRouteReplayErrorNotif{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_global_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLVrfRouteReplayErrorNotif) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLVrfRouteReplayErrorNotif) ProtoMessage() {}

func (x *SLVrfRouteReplayErrorNotif) ProtoReflect() protoreflect.Message {
	mi := &file_sl_global_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLVrfRouteReplayErrorNotif.ProtoReflect.Descriptor instead.
func (*SLVrfRouteReplayErrorNotif) Descriptor() ([]byte, []int) {
	return file_sl_global_proto_rawDescGZIP(), []int{2}
}

func (x *SLVrfRouteReplayErrorNotif) GetVrfName() string {
	if x != nil {
		return x.VrfName
	}
	return ""
}

// Globals query message.
type SLGlobalNotif struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Event Type.
	EventType SLGlobalNotifType `protobuf:"varint,1,opt,name=EventType,proto3,enum=service_layer.SLGlobalNotifType" json:"EventType,omitempty"`
	// Status code, interpreted based on the Event Type.
	//
	//	case EventType == SL_GLOBAL_EVENT_TYPE_ERROR:
	//	    case ErrStatus == SL_NOTIF_TERM:
	//	       => Another client is attempting to take over the session.
	//	          This session will be closed.
	//	    case ErrStatus == SL_VRF_V4_ROUTE_REPLAY_FATAL_ERROR:
	//	       => IPv4 Routes replay failed for a VRF.
	//	          See VrfReplayErrorNotif for details.
	//	    case ErrStatus == SL_VRF_V6_ROUTE_REPLAY_FATAL_ERROR:
	//	       => IPv6 Routes replay failed for a VRF.
	//	          See VrfReplayErrorNotif for details.
	//	    case ErrStatus == SL_ILM_REPLAY_FATAL_ERROR:
	//	       => ILM replay failed.
	//	    case ErrStatus == SL_VRF_V4_ROUTE_REPLAY_OK:
	//	       => IPv4 Routes replay succeeded for a VRF.
	//	          See VrfReplayErrorNotif for details.
	//	          This notification is sent only if a
	//	          SL_VRF_V4_ROUTE_REPLAY_FATAL_ERROR was sent earlier
	//	          on the identified VRF.
	//	    case ErrStatus == SL_VRF_V6_ROUTE_REPLAY_OK:
	//	       => IPv6 Routes replay succeeded for a VRF.
	//	          See VrfReplayErrorNotif for details.
	//	          This notification is sent only if a
	//	          SL_VRF_V6_ROUTE_REPLAY_FATAL_ERROR was sent earlier
	//	          on the identified VRF.
	//	    case ErrStatus == SL_ILM_REPLAY_OK:
	//	       => ILM replay succeeded.
	//	          This notification is sent only if a
	//	          SL_ILM_REPLAY_FATAL_ERROR was sent earlier.
	//	    case ErrStatus == (some error from SLErrorStatus)
	//	       => Client must look into the specific error message returned.
	//
	//	case EventType == SL_GLOBAL_EVENT_TYPE_HEARTBEAT:
	//	    case ErrStatus == SL_SUCCESS
	//	       => Client can safely ignore this heartbeat message.
	//
	//	case EventType == SL_GLOBAL_EVENT_TYPE_VERSION:
	//	    case ErrStatus == SL_SUCCESS
	//	       => Client version accepted.
	//	    case ErrStatus == SL_INIT_STATE_READY
	//	       => Client version accepted.
	//	          Any previous state was sucessfully recovered.
	//	    case ErrStatus == SL_INIT_STATE_CLEAR
	//	       => Client version accepted. Any previous state was lost.
	//	          Client must replay all previous objects to server.
	//	    case ErrStatus == SL_UNSUPPORTED_VER
	//	       => Client and Server version mismatch. The client is not
	//	          allowed to proceed, and the channel will be closed.
	//	    case ErrStatus == (some error from SLErrorStatus)
	//	       => Client must either try again, or look into the specific
	//	          error message returned.
	ErrStatus *SLErrorStatus `protobuf:"bytes,2,opt,name=ErrStatus,proto3" json:"ErrStatus,omitempty"`
	// Further info based on EventType.
	//
	// Types that are assignable to Event:
	//
	//	*SLGlobalNotif_InitRspMsg
	//	*SLGlobalNotif_VrfReplayErrorNotif
	Event isSLGlobalNotif_Event `protobuf_oneof:"Event"`
}

func (x *SLGlobalNotif) Reset() {
	*x = SLGlobalNotif{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_global_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLGlobalNotif) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLGlobalNotif) ProtoMessage() {}

func (x *SLGlobalNotif) ProtoReflect() protoreflect.Message {
	mi := &file_sl_global_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLGlobalNotif.ProtoReflect.Descriptor instead.
func (*SLGlobalNotif) Descriptor() ([]byte, []int) {
	return file_sl_global_proto_rawDescGZIP(), []int{3}
}

func (x *SLGlobalNotif) GetEventType() SLGlobalNotifType {
	if x != nil {
		return x.EventType
	}
	return SLGlobalNotifType_SL_GLOBAL_EVENT_TYPE_RESERVED
}

func (x *SLGlobalNotif) GetErrStatus() *SLErrorStatus {
	if x != nil {
		return x.ErrStatus
	}
	return nil
}

func (m *SLGlobalNotif) GetEvent() isSLGlobalNotif_Event {
	if m != nil {
		return m.Event
	}
	return nil
}

func (x *SLGlobalNotif) GetInitRspMsg() *SLInitMsgRsp {
	if x, ok := x.GetEvent().(*SLGlobalNotif_InitRspMsg); ok {
		return x.InitRspMsg
	}
	return nil
}

func (x *SLGlobalNotif) GetVrfReplayErrorNotif() *SLVrfRouteReplayErrorNotif {
	if x, ok := x.GetEvent().(*SLGlobalNotif_VrfReplayErrorNotif); ok {
		return x.VrfReplayErrorNotif
	}
	return nil
}

type isSLGlobalNotif_Event interface {
	isSLGlobalNotif_Event()
}

type SLGlobalNotif_InitRspMsg struct {
	// case EventType == SL_GLOBAL_EVENT_TYPE_VERSION:
	//
	//	=> this field carries the Server version number.
	InitRspMsg *SLInitMsgRsp `protobuf:"bytes,3,opt,name=InitRspMsg,proto3,oneof"`
}

type SLGlobalNotif_VrfReplayErrorNotif struct {
	// case EventType == SL_GLOBAL_EVENT_TYPE_ERROR:
	//
	//	case ErrStatus == SL_VRF_V4_ROUTE_REPLAY_FATAL_ERROR:
	//	case ErrStatus == SL_VRF_V6_ROUTE_REPLAY_FATAL_ERROR:
	//	case ErrStatus == SL_VRF_V4_ROUTE_REPLAY_OK:
	//	case ErrStatus == SL_VRF_V6_ROUTE_REPLAY_OK:
	//	=> this field carries the failed VRF information.
	VrfReplayErrorNotif *SLVrfRouteReplayErrorNotif `protobuf:"bytes,4,opt,name=VrfReplayErrorNotif,proto3,oneof"`
}

func (*SLGlobalNotif_InitRspMsg) isSLGlobalNotif_Event() {}

func (*SLGlobalNotif_VrfReplayErrorNotif) isSLGlobalNotif_Event() {}

// Globals query message.
type SLGlobalsGetMsg struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields
}

func (x *SLGlobalsGetMsg) Reset() {
	*x = SLGlobalsGetMsg{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_global_proto_msgTypes[4]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLGlobalsGetMsg) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLGlobalsGetMsg) ProtoMessage() {}

func (x *SLGlobalsGetMsg) ProtoReflect() protoreflect.Message {
	mi := &file_sl_global_proto_msgTypes[4]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLGlobalsGetMsg.ProtoReflect.Descriptor instead.
func (*SLGlobalsGetMsg) Descriptor() ([]byte, []int) {
	return file_sl_global_proto_rawDescGZIP(), []int{4}
}

// Platform specific globals Response.
type SLGlobalsGetMsgRsp struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	// Corresponding error code
	ErrStatus *SLErrorStatus `protobuf:"bytes,1,opt,name=ErrStatus,proto3" json:"ErrStatus,omitempty"`
	// Maximum vrf name length.
	MaxVrfNameLength uint32 `protobuf:"varint,2,opt,name=MaxVrfNameLength,proto3" json:"MaxVrfNameLength,omitempty"`
	// Maximum interface name length.
	MaxInterfaceNameLength uint32 `protobuf:"varint,3,opt,name=MaxInterfaceNameLength,proto3" json:"MaxInterfaceNameLength,omitempty"`
	// Maximum paths per Route/ILM Entry.
	MaxPathsPerEntry uint32 `protobuf:"varint,4,opt,name=MaxPathsPerEntry,proto3" json:"MaxPathsPerEntry,omitempty"`
	// Maximum primary paths per Route/ILM Entry.
	MaxPrimaryPathPerEntry uint32 `protobuf:"varint,5,opt,name=MaxPrimaryPathPerEntry,proto3" json:"MaxPrimaryPathPerEntry,omitempty"`
	// Maximum backup paths per Route/ILM Entry.
	MaxBackupPathPerEntry uint32 `protobuf:"varint,6,opt,name=MaxBackupPathPerEntry,proto3" json:"MaxBackupPathPerEntry,omitempty"`
	// Maximum MPLS labels per Route/ILM Entry.
	MaxMplsLabelsPerPath uint32 `protobuf:"varint,7,opt,name=MaxMplsLabelsPerPath,proto3" json:"MaxMplsLabelsPerPath,omitempty"`
	// Minimum Primary path id number.
	MinPrimaryPathIdNum uint32 `protobuf:"varint,8,opt,name=MinPrimaryPathIdNum,proto3" json:"MinPrimaryPathIdNum,omitempty"`
	// Maximum Primary path id number.
	MaxPrimaryPathIdNum uint32 `protobuf:"varint,9,opt,name=MaxPrimaryPathIdNum,proto3" json:"MaxPrimaryPathIdNum,omitempty"`
	// Minimum Pure Backup path id number.
	MinBackupPathIdNum uint32 `protobuf:"varint,10,opt,name=MinBackupPathIdNum,proto3" json:"MinBackupPathIdNum,omitempty"`
	// Maximum Pure Backup path id number.
	MaxBackupPathIdNum uint32 `protobuf:"varint,11,opt,name=MaxBackupPathIdNum,proto3" json:"MaxBackupPathIdNum,omitempty"`
	// Maximum number of remote addresses
	MaxRemoteAddressNum uint32 `protobuf:"varint,12,opt,name=MaxRemoteAddressNum,proto3" json:"MaxRemoteAddressNum,omitempty"`
	// Maximum Bridge Domain name length - used for L2 routes.
	MaxL2BdNameLength uint32 `protobuf:"varint,13,opt,name=MaxL2BdNameLength,proto3" json:"MaxL2BdNameLength,omitempty"`
	// Maximum Provider Multicast Service Interface (PMSI) tunnel ID length.
	// Used for L2 Inclusive Multicast Ethernet Tag (IMET) routes.
	MaxL2PmsiTunnelIdLength uint32 `protobuf:"varint,14,opt,name=MaxL2PmsiTunnelIdLength,proto3" json:"MaxL2PmsiTunnelIdLength,omitempty"`
	// Maximum label block client name length.
	MaxLabelBlockClientNameLength uint32 `protobuf:"varint,15,opt,name=MaxLabelBlockClientNameLength,proto3" json:"MaxLabelBlockClientNameLength,omitempty"`
}

func (x *SLGlobalsGetMsgRsp) Reset() {
	*x = SLGlobalsGetMsgRsp{}
	if protoimpl.UnsafeEnabled {
		mi := &file_sl_global_proto_msgTypes[5]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *SLGlobalsGetMsgRsp) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*SLGlobalsGetMsgRsp) ProtoMessage() {}

func (x *SLGlobalsGetMsgRsp) ProtoReflect() protoreflect.Message {
	mi := &file_sl_global_proto_msgTypes[5]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use SLGlobalsGetMsgRsp.ProtoReflect.Descriptor instead.
func (*SLGlobalsGetMsgRsp) Descriptor() ([]byte, []int) {
	return file_sl_global_proto_rawDescGZIP(), []int{5}
}

func (x *SLGlobalsGetMsgRsp) GetErrStatus() *SLErrorStatus {
	if x != nil {
		return x.ErrStatus
	}
	return nil
}

func (x *SLGlobalsGetMsgRsp) GetMaxVrfNameLength() uint32 {
	if x != nil {
		return x.MaxVrfNameLength
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxInterfaceNameLength() uint32 {
	if x != nil {
		return x.MaxInterfaceNameLength
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxPathsPerEntry() uint32 {
	if x != nil {
		return x.MaxPathsPerEntry
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxPrimaryPathPerEntry() uint32 {
	if x != nil {
		return x.MaxPrimaryPathPerEntry
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxBackupPathPerEntry() uint32 {
	if x != nil {
		return x.MaxBackupPathPerEntry
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxMplsLabelsPerPath() uint32 {
	if x != nil {
		return x.MaxMplsLabelsPerPath
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMinPrimaryPathIdNum() uint32 {
	if x != nil {
		return x.MinPrimaryPathIdNum
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxPrimaryPathIdNum() uint32 {
	if x != nil {
		return x.MaxPrimaryPathIdNum
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMinBackupPathIdNum() uint32 {
	if x != nil {
		return x.MinBackupPathIdNum
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxBackupPathIdNum() uint32 {
	if x != nil {
		return x.MaxBackupPathIdNum
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxRemoteAddressNum() uint32 {
	if x != nil {
		return x.MaxRemoteAddressNum
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxL2BdNameLength() uint32 {
	if x != nil {
		return x.MaxL2BdNameLength
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxL2PmsiTunnelIdLength() uint32 {
	if x != nil {
		return x.MaxL2PmsiTunnelIdLength
	}
	return 0
}

func (x *SLGlobalsGetMsgRsp) GetMaxLabelBlockClientNameLength() uint32 {
	if x != nil {
		return x.MaxLabelBlockClientNameLength
	}
	return 0
}

var File_sl_global_proto protoreflect.FileDescriptor

var file_sl_global_proto_rawDesc = []byte{
	0x0a, 0x0f, 0x73, 0x6c, 0x5f, 0x67, 0x6c, 0x6f, 0x62, 0x61, 0x6c, 0x2e, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x12, 0x0d, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72,
	0x1a, 0x15, 0x73, 0x6c, 0x5f, 0x63, 0x6f, 0x6d, 0x6d, 0x6f, 0x6e, 0x5f, 0x74, 0x79, 0x70, 0x65,
	0x73, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22, 0x5b, 0x0a, 0x09, 0x53, 0x4c, 0x49, 0x6e, 0x69,
	0x74, 0x4d, 0x73, 0x67, 0x12, 0x1a, 0x0a, 0x08, 0x4d, 0x61, 0x6a, 0x6f, 0x72, 0x56, 0x65, 0x72,
	0x18, 0x01, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x08, 0x4d, 0x61, 0x6a, 0x6f, 0x72, 0x56, 0x65, 0x72,
	0x12, 0x1a, 0x0a, 0x08, 0x4d, 0x69, 0x6e, 0x6f, 0x72, 0x56, 0x65, 0x72, 0x18, 0x02, 0x20, 0x01,
	0x28, 0x0d, 0x52, 0x08, 0x4d, 0x69, 0x6e, 0x6f, 0x72, 0x56, 0x65, 0x72, 0x12, 0x16, 0x0a, 0x06,
	0x53, 0x75, 0x62, 0x56, 0x65, 0x72, 0x18, 0x03, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x06, 0x53, 0x75,
	0x62, 0x56, 0x65, 0x72, 0x22, 0x5e, 0x0a, 0x0c, 0x53, 0x4c, 0x49, 0x6e, 0x69, 0x74, 0x4d, 0x73,
	0x67, 0x52, 0x73, 0x70, 0x12, 0x1a, 0x0a, 0x08, 0x4d, 0x61, 0x6a, 0x6f, 0x72, 0x56, 0x65, 0x72,
	0x18, 0x01, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x08, 0x4d, 0x61, 0x6a, 0x6f, 0x72, 0x56, 0x65, 0x72,
	0x12, 0x1a, 0x0a, 0x08, 0x4d, 0x69, 0x6e, 0x6f, 0x72, 0x56, 0x65, 0x72, 0x18, 0x02, 0x20, 0x01,
	0x28, 0x0d, 0x52, 0x08, 0x4d, 0x69, 0x6e, 0x6f, 0x72, 0x56, 0x65, 0x72, 0x12, 0x16, 0x0a, 0x06,
	0x53, 0x75, 0x62, 0x56, 0x65, 0x72, 0x18, 0x03, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x06, 0x53, 0x75,
	0x62, 0x56, 0x65, 0x72, 0x22, 0x36, 0x0a, 0x1a, 0x53, 0x4c, 0x56, 0x72, 0x66, 0x52, 0x6f, 0x75,
	0x74, 0x65, 0x52, 0x65, 0x70, 0x6c, 0x61, 0x79, 0x45, 0x72, 0x72, 0x6f, 0x72, 0x4e, 0x6f, 0x74,
	0x69, 0x66, 0x12, 0x18, 0x0a, 0x07, 0x56, 0x72, 0x66, 0x4e, 0x61, 0x6d, 0x65, 0x18, 0x01, 0x20,
	0x01, 0x28, 0x09, 0x52, 0x07, 0x56, 0x72, 0x66, 0x4e, 0x61, 0x6d, 0x65, 0x22, 0xb2, 0x02, 0x0a,
	0x0d, 0x53, 0x4c, 0x47, 0x6c, 0x6f, 0x62, 0x61, 0x6c, 0x4e, 0x6f, 0x74, 0x69, 0x66, 0x12, 0x3e,
	0x0a, 0x09, 0x45, 0x76, 0x65, 0x6e, 0x74, 0x54, 0x79, 0x70, 0x65, 0x18, 0x01, 0x20, 0x01, 0x28,
	0x0e, 0x32, 0x20, 0x2e, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65,
	0x72, 0x2e, 0x53, 0x4c, 0x47, 0x6c, 0x6f, 0x62, 0x61, 0x6c, 0x4e, 0x6f, 0x74, 0x69, 0x66, 0x54,
	0x79, 0x70, 0x65, 0x52, 0x09, 0x45, 0x76, 0x65, 0x6e, 0x74, 0x54, 0x79, 0x70, 0x65, 0x12, 0x3a,
	0x0a, 0x09, 0x45, 0x72, 0x72, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x18, 0x02, 0x20, 0x01, 0x28,
	0x0b, 0x32, 0x1c, 0x2e, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65,
	0x72, 0x2e, 0x53, 0x4c, 0x45, 0x72, 0x72, 0x6f, 0x72, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52,
	0x09, 0x45, 0x72, 0x72, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x12, 0x3d, 0x0a, 0x0a, 0x49, 0x6e,
	0x69, 0x74, 0x52, 0x73, 0x70, 0x4d, 0x73, 0x67, 0x18, 0x03, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1b,
	0x2e, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53,
	0x4c, 0x49, 0x6e, 0x69, 0x74, 0x4d, 0x73, 0x67, 0x52, 0x73, 0x70, 0x48, 0x00, 0x52, 0x0a, 0x49,
	0x6e, 0x69, 0x74, 0x52, 0x73, 0x70, 0x4d, 0x73, 0x67, 0x12, 0x5d, 0x0a, 0x13, 0x56, 0x72, 0x66,
	0x52, 0x65, 0x70, 0x6c, 0x61, 0x79, 0x45, 0x72, 0x72, 0x6f, 0x72, 0x4e, 0x6f, 0x74, 0x69, 0x66,
	0x18, 0x04, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x29, 0x2e, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65,
	0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x56, 0x72, 0x66, 0x52, 0x6f, 0x75, 0x74,
	0x65, 0x52, 0x65, 0x70, 0x6c, 0x61, 0x79, 0x45, 0x72, 0x72, 0x6f, 0x72, 0x4e, 0x6f, 0x74, 0x69,
	0x66, 0x48, 0x00, 0x52, 0x13, 0x56, 0x72, 0x66, 0x52, 0x65, 0x70, 0x6c, 0x61, 0x79, 0x45, 0x72,
	0x72, 0x6f, 0x72, 0x4e, 0x6f, 0x74, 0x69, 0x66, 0x42, 0x07, 0x0a, 0x05, 0x45, 0x76, 0x65, 0x6e,
	0x74, 0x22, 0x11, 0x0a, 0x0f, 0x53, 0x4c, 0x47, 0x6c, 0x6f, 0x62, 0x61, 0x6c, 0x73, 0x47, 0x65,
	0x74, 0x4d, 0x73, 0x67, 0x22, 0xa6, 0x06, 0x0a, 0x12, 0x53, 0x4c, 0x47, 0x6c, 0x6f, 0x62, 0x61,
	0x6c, 0x73, 0x47, 0x65, 0x74, 0x4d, 0x73, 0x67, 0x52, 0x73, 0x70, 0x12, 0x3a, 0x0a, 0x09, 0x45,
	0x72, 0x72, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x18, 0x01, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1c,
	0x2e, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53,
	0x4c, 0x45, 0x72, 0x72, 0x6f, 0x72, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x52, 0x09, 0x45, 0x72,
	0x72, 0x53, 0x74, 0x61, 0x74, 0x75, 0x73, 0x12, 0x2a, 0x0a, 0x10, 0x4d, 0x61, 0x78, 0x56, 0x72,
	0x66, 0x4e, 0x61, 0x6d, 0x65, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x18, 0x02, 0x20, 0x01, 0x28,
	0x0d, 0x52, 0x10, 0x4d, 0x61, 0x78, 0x56, 0x72, 0x66, 0x4e, 0x61, 0x6d, 0x65, 0x4c, 0x65, 0x6e,
	0x67, 0x74, 0x68, 0x12, 0x36, 0x0a, 0x16, 0x4d, 0x61, 0x78, 0x49, 0x6e, 0x74, 0x65, 0x72, 0x66,
	0x61, 0x63, 0x65, 0x4e, 0x61, 0x6d, 0x65, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x18, 0x03, 0x20,
	0x01, 0x28, 0x0d, 0x52, 0x16, 0x4d, 0x61, 0x78, 0x49, 0x6e, 0x74, 0x65, 0x72, 0x66, 0x61, 0x63,
	0x65, 0x4e, 0x61, 0x6d, 0x65, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x12, 0x2a, 0x0a, 0x10, 0x4d,
	0x61, 0x78, 0x50, 0x61, 0x74, 0x68, 0x73, 0x50, 0x65, 0x72, 0x45, 0x6e, 0x74, 0x72, 0x79, 0x18,
	0x04, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x10, 0x4d, 0x61, 0x78, 0x50, 0x61, 0x74, 0x68, 0x73, 0x50,
	0x65, 0x72, 0x45, 0x6e, 0x74, 0x72, 0x79, 0x12, 0x36, 0x0a, 0x16, 0x4d, 0x61, 0x78, 0x50, 0x72,
	0x69, 0x6d, 0x61, 0x72, 0x79, 0x50, 0x61, 0x74, 0x68, 0x50, 0x65, 0x72, 0x45, 0x6e, 0x74, 0x72,
	0x79, 0x18, 0x05, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x16, 0x4d, 0x61, 0x78, 0x50, 0x72, 0x69, 0x6d,
	0x61, 0x72, 0x79, 0x50, 0x61, 0x74, 0x68, 0x50, 0x65, 0x72, 0x45, 0x6e, 0x74, 0x72, 0x79, 0x12,
	0x34, 0x0a, 0x15, 0x4d, 0x61, 0x78, 0x42, 0x61, 0x63, 0x6b, 0x75, 0x70, 0x50, 0x61, 0x74, 0x68,
	0x50, 0x65, 0x72, 0x45, 0x6e, 0x74, 0x72, 0x79, 0x18, 0x06, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x15,
	0x4d, 0x61, 0x78, 0x42, 0x61, 0x63, 0x6b, 0x75, 0x70, 0x50, 0x61, 0x74, 0x68, 0x50, 0x65, 0x72,
	0x45, 0x6e, 0x74, 0x72, 0x79, 0x12, 0x32, 0x0a, 0x14, 0x4d, 0x61, 0x78, 0x4d, 0x70, 0x6c, 0x73,
	0x4c, 0x61, 0x62, 0x65, 0x6c, 0x73, 0x50, 0x65, 0x72, 0x50, 0x61, 0x74, 0x68, 0x18, 0x07, 0x20,
	0x01, 0x28, 0x0d, 0x52, 0x14, 0x4d, 0x61, 0x78, 0x4d, 0x70, 0x6c, 0x73, 0x4c, 0x61, 0x62, 0x65,
	0x6c, 0x73, 0x50, 0x65, 0x72, 0x50, 0x61, 0x74, 0x68, 0x12, 0x30, 0x0a, 0x13, 0x4d, 0x69, 0x6e,
	0x50, 0x72, 0x69, 0x6d, 0x61, 0x72, 0x79, 0x50, 0x61, 0x74, 0x68, 0x49, 0x64, 0x4e, 0x75, 0x6d,
	0x18, 0x08, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x13, 0x4d, 0x69, 0x6e, 0x50, 0x72, 0x69, 0x6d, 0x61,
	0x72, 0x79, 0x50, 0x61, 0x74, 0x68, 0x49, 0x64, 0x4e, 0x75, 0x6d, 0x12, 0x30, 0x0a, 0x13, 0x4d,
	0x61, 0x78, 0x50, 0x72, 0x69, 0x6d, 0x61, 0x72, 0x79, 0x50, 0x61, 0x74, 0x68, 0x49, 0x64, 0x4e,
	0x75, 0x6d, 0x18, 0x09, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x13, 0x4d, 0x61, 0x78, 0x50, 0x72, 0x69,
	0x6d, 0x61, 0x72, 0x79, 0x50, 0x61, 0x74, 0x68, 0x49, 0x64, 0x4e, 0x75, 0x6d, 0x12, 0x2e, 0x0a,
	0x12, 0x4d, 0x69, 0x6e, 0x42, 0x61, 0x63, 0x6b, 0x75, 0x70, 0x50, 0x61, 0x74, 0x68, 0x49, 0x64,
	0x4e, 0x75, 0x6d, 0x18, 0x0a, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x12, 0x4d, 0x69, 0x6e, 0x42, 0x61,
	0x63, 0x6b, 0x75, 0x70, 0x50, 0x61, 0x74, 0x68, 0x49, 0x64, 0x4e, 0x75, 0x6d, 0x12, 0x2e, 0x0a,
	0x12, 0x4d, 0x61, 0x78, 0x42, 0x61, 0x63, 0x6b, 0x75, 0x70, 0x50, 0x61, 0x74, 0x68, 0x49, 0x64,
	0x4e, 0x75, 0x6d, 0x18, 0x0b, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x12, 0x4d, 0x61, 0x78, 0x42, 0x61,
	0x63, 0x6b, 0x75, 0x70, 0x50, 0x61, 0x74, 0x68, 0x49, 0x64, 0x4e, 0x75, 0x6d, 0x12, 0x30, 0x0a,
	0x13, 0x4d, 0x61, 0x78, 0x52, 0x65, 0x6d, 0x6f, 0x74, 0x65, 0x41, 0x64, 0x64, 0x72, 0x65, 0x73,
	0x73, 0x4e, 0x75, 0x6d, 0x18, 0x0c, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x13, 0x4d, 0x61, 0x78, 0x52,
	0x65, 0x6d, 0x6f, 0x74, 0x65, 0x41, 0x64, 0x64, 0x72, 0x65, 0x73, 0x73, 0x4e, 0x75, 0x6d, 0x12,
	0x2c, 0x0a, 0x11, 0x4d, 0x61, 0x78, 0x4c, 0x32, 0x42, 0x64, 0x4e, 0x61, 0x6d, 0x65, 0x4c, 0x65,
	0x6e, 0x67, 0x74, 0x68, 0x18, 0x0d, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x11, 0x4d, 0x61, 0x78, 0x4c,
	0x32, 0x42, 0x64, 0x4e, 0x61, 0x6d, 0x65, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x12, 0x38, 0x0a,
	0x17, 0x4d, 0x61, 0x78, 0x4c, 0x32, 0x50, 0x6d, 0x73, 0x69, 0x54, 0x75, 0x6e, 0x6e, 0x65, 0x6c,
	0x49, 0x64, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x18, 0x0e, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x17,
	0x4d, 0x61, 0x78, 0x4c, 0x32, 0x50, 0x6d, 0x73, 0x69, 0x54, 0x75, 0x6e, 0x6e, 0x65, 0x6c, 0x49,
	0x64, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x12, 0x44, 0x0a, 0x1d, 0x4d, 0x61, 0x78, 0x4c, 0x61,
	0x62, 0x65, 0x6c, 0x42, 0x6c, 0x6f, 0x63, 0x6b, 0x43, 0x6c, 0x69, 0x65, 0x6e, 0x74, 0x4e, 0x61,
	0x6d, 0x65, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x18, 0x0f, 0x20, 0x01, 0x28, 0x0d, 0x52, 0x1d,
	0x4d, 0x61, 0x78, 0x4c, 0x61, 0x62, 0x65, 0x6c, 0x42, 0x6c, 0x6f, 0x63, 0x6b, 0x43, 0x6c, 0x69,
	0x65, 0x6e, 0x74, 0x4e, 0x61, 0x6d, 0x65, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x2a, 0x9c, 0x01,
	0x0a, 0x11, 0x53, 0x4c, 0x47, 0x6c, 0x6f, 0x62, 0x61, 0x6c, 0x4e, 0x6f, 0x74, 0x69, 0x66, 0x54,
	0x79, 0x70, 0x65, 0x12, 0x21, 0x0a, 0x1d, 0x53, 0x4c, 0x5f, 0x47, 0x4c, 0x4f, 0x42, 0x41, 0x4c,
	0x5f, 0x45, 0x56, 0x45, 0x4e, 0x54, 0x5f, 0x54, 0x59, 0x50, 0x45, 0x5f, 0x52, 0x45, 0x53, 0x45,
	0x52, 0x56, 0x45, 0x44, 0x10, 0x00, 0x12, 0x1e, 0x0a, 0x1a, 0x53, 0x4c, 0x5f, 0x47, 0x4c, 0x4f,
	0x42, 0x41, 0x4c, 0x5f, 0x45, 0x56, 0x45, 0x4e, 0x54, 0x5f, 0x54, 0x59, 0x50, 0x45, 0x5f, 0x45,
	0x52, 0x52, 0x4f, 0x52, 0x10, 0x01, 0x12, 0x22, 0x0a, 0x1e, 0x53, 0x4c, 0x5f, 0x47, 0x4c, 0x4f,
	0x42, 0x41, 0x4c, 0x5f, 0x45, 0x56, 0x45, 0x4e, 0x54, 0x5f, 0x54, 0x59, 0x50, 0x45, 0x5f, 0x48,
	0x45, 0x41, 0x52, 0x54, 0x42, 0x45, 0x41, 0x54, 0x10, 0x02, 0x12, 0x20, 0x0a, 0x1c, 0x53, 0x4c,
	0x5f, 0x47, 0x4c, 0x4f, 0x42, 0x41, 0x4c, 0x5f, 0x45, 0x56, 0x45, 0x4e, 0x54, 0x5f, 0x54, 0x59,
	0x50, 0x45, 0x5f, 0x56, 0x45, 0x52, 0x53, 0x49, 0x4f, 0x4e, 0x10, 0x03, 0x32, 0xac, 0x01, 0x0a,
	0x08, 0x53, 0x4c, 0x47, 0x6c, 0x6f, 0x62, 0x61, 0x6c, 0x12, 0x4d, 0x0a, 0x11, 0x53, 0x4c, 0x47,
	0x6c, 0x6f, 0x62, 0x61, 0x6c, 0x49, 0x6e, 0x69, 0x74, 0x4e, 0x6f, 0x74, 0x69, 0x66, 0x12, 0x18,
	0x2e, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53,
	0x4c, 0x49, 0x6e, 0x69, 0x74, 0x4d, 0x73, 0x67, 0x1a, 0x1c, 0x2e, 0x73, 0x65, 0x72, 0x76, 0x69,
	0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x47, 0x6c, 0x6f, 0x62, 0x61,
	0x6c, 0x4e, 0x6f, 0x74, 0x69, 0x66, 0x30, 0x01, 0x12, 0x51, 0x0a, 0x0c, 0x53, 0x4c, 0x47, 0x6c,
	0x6f, 0x62, 0x61, 0x6c, 0x73, 0x47, 0x65, 0x74, 0x12, 0x1e, 0x2e, 0x73, 0x65, 0x72, 0x76, 0x69,
	0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x47, 0x6c, 0x6f, 0x62, 0x61,
	0x6c, 0x73, 0x47, 0x65, 0x74, 0x4d, 0x73, 0x67, 0x1a, 0x21, 0x2e, 0x73, 0x65, 0x72, 0x76, 0x69,
	0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2e, 0x53, 0x4c, 0x47, 0x6c, 0x6f, 0x62, 0x61,
	0x6c, 0x73, 0x47, 0x65, 0x74, 0x4d, 0x73, 0x67, 0x52, 0x73, 0x70, 0x42, 0x51, 0x5a, 0x4f, 0x67,
	0x69, 0x74, 0x68, 0x75, 0x62, 0x2e, 0x63, 0x6f, 0x6d, 0x2f, 0x43, 0x69, 0x73, 0x63, 0x6f, 0x2d,
	0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x2d, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2f, 0x73, 0x65,
	0x72, 0x76, 0x69, 0x63, 0x65, 0x2d, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x2d, 0x6f, 0x62, 0x6a, 0x6d,
	0x6f, 0x64, 0x65, 0x6c, 0x2f, 0x67, 0x72, 0x70, 0x63, 0x2f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x73,
	0x3b, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x5f, 0x6c, 0x61, 0x79, 0x65, 0x72, 0x62, 0x06,
	0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_sl_global_proto_rawDescOnce sync.Once
	file_sl_global_proto_rawDescData = file_sl_global_proto_rawDesc
)

func file_sl_global_proto_rawDescGZIP() []byte {
	file_sl_global_proto_rawDescOnce.Do(func() {
		file_sl_global_proto_rawDescData = protoimpl.X.CompressGZIP(file_sl_global_proto_rawDescData)
	})
	return file_sl_global_proto_rawDescData
}

var file_sl_global_proto_enumTypes = make([]protoimpl.EnumInfo, 1)
var file_sl_global_proto_msgTypes = make([]protoimpl.MessageInfo, 6)
var file_sl_global_proto_goTypes = []interface{}{
	(SLGlobalNotifType)(0),             // 0: service_layer.SLGlobalNotifType
	(*SLInitMsg)(nil),                  // 1: service_layer.SLInitMsg
	(*SLInitMsgRsp)(nil),               // 2: service_layer.SLInitMsgRsp
	(*SLVrfRouteReplayErrorNotif)(nil), // 3: service_layer.SLVrfRouteReplayErrorNotif
	(*SLGlobalNotif)(nil),              // 4: service_layer.SLGlobalNotif
	(*SLGlobalsGetMsg)(nil),            // 5: service_layer.SLGlobalsGetMsg
	(*SLGlobalsGetMsgRsp)(nil),         // 6: service_layer.SLGlobalsGetMsgRsp
	(*SLErrorStatus)(nil),              // 7: service_layer.SLErrorStatus
}
var file_sl_global_proto_depIdxs = []int32{
	0, // 0: service_layer.SLGlobalNotif.EventType:type_name -> service_layer.SLGlobalNotifType
	7, // 1: service_layer.SLGlobalNotif.ErrStatus:type_name -> service_layer.SLErrorStatus
	2, // 2: service_layer.SLGlobalNotif.InitRspMsg:type_name -> service_layer.SLInitMsgRsp
	3, // 3: service_layer.SLGlobalNotif.VrfReplayErrorNotif:type_name -> service_layer.SLVrfRouteReplayErrorNotif
	7, // 4: service_layer.SLGlobalsGetMsgRsp.ErrStatus:type_name -> service_layer.SLErrorStatus
	1, // 5: service_layer.SLGlobal.SLGlobalInitNotif:input_type -> service_layer.SLInitMsg
	5, // 6: service_layer.SLGlobal.SLGlobalsGet:input_type -> service_layer.SLGlobalsGetMsg
	4, // 7: service_layer.SLGlobal.SLGlobalInitNotif:output_type -> service_layer.SLGlobalNotif
	6, // 8: service_layer.SLGlobal.SLGlobalsGet:output_type -> service_layer.SLGlobalsGetMsgRsp
	7, // [7:9] is the sub-list for method output_type
	5, // [5:7] is the sub-list for method input_type
	5, // [5:5] is the sub-list for extension type_name
	5, // [5:5] is the sub-list for extension extendee
	0, // [0:5] is the sub-list for field type_name
}

func init() { file_sl_global_proto_init() }
func file_sl_global_proto_init() {
	if File_sl_global_proto != nil {
		return
	}
	file_sl_common_types_proto_init()
	if !protoimpl.UnsafeEnabled {
		file_sl_global_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLInitMsg); i {
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
		file_sl_global_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLInitMsgRsp); i {
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
		file_sl_global_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLVrfRouteReplayErrorNotif); i {
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
		file_sl_global_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLGlobalNotif); i {
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
		file_sl_global_proto_msgTypes[4].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLGlobalsGetMsg); i {
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
		file_sl_global_proto_msgTypes[5].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*SLGlobalsGetMsgRsp); i {
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
	file_sl_global_proto_msgTypes[3].OneofWrappers = []interface{}{
		(*SLGlobalNotif_InitRspMsg)(nil),
		(*SLGlobalNotif_VrfReplayErrorNotif)(nil),
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_sl_global_proto_rawDesc,
			NumEnums:      1,
			NumMessages:   6,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_sl_global_proto_goTypes,
		DependencyIndexes: file_sl_global_proto_depIdxs,
		EnumInfos:         file_sl_global_proto_enumTypes,
		MessageInfos:      file_sl_global_proto_msgTypes,
	}.Build()
	File_sl_global_proto = out.File
	file_sl_global_proto_rawDesc = nil
	file_sl_global_proto_goTypes = nil
	file_sl_global_proto_depIdxs = nil
}
