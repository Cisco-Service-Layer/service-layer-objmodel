// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v3.18.3
// source: sl_af.proto

package service_layer

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// SLAFClient is the client API for SLAF service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type SLAFClient interface {
	// VRF registration operations. By default, The client must register with
	// the corresponding VRF table before programming objects in that table.
	//
	// SLAFVrfRegMsg.Oper = SL_REGOP_REGISTER:
	//
	//	VRF table registration: Sends a list of VRF table registration
	//	messages and expects a list of registration responses.
	//	A client Must Register a VRF table BEFORE objects can be
	//	added/modified in the associated VRF table.
	//
	// SLAFVrfRegMsg.Oper = SL_REGOP_UNREGISTER:
	//
	//	VRF table Un-registration: Sends a list of VRF table un-registration
	//	messages and expects a list of un-registration responses.
	//	This can be used to convey that the client is no longer interested
	//	in these VRF tables. All previously installed objects would be
	//	remove.
	//
	// SLAFVrfRegMsg.Oper = SL_REGOP_EOF:
	//
	//	VRF table End Of File message.
	//	After Registration, the client is expected to send an EOF
	//	message to convey the end of replay of the client's known objects.
	//	This is especially useful under certain restart scenarios when the
	//	client and the server are trying to synchronize their objects.
	//
	// The VRF table registration operations can be used by the client to
	// synchronize objects with the device. When the client re-registers the
	// VRF table with the server using SL_REGOP_REGISTER, server marks
	// objects in that table as stale.
	// Client then MUST reprogram objects it is interested in.
	// When client sends SL_REGOP_EOF, any objects not reprogrammed
	// are removed from the device.
	//
	// The client MUST perform all operations (VRF registration, objects)
	// from a single execution context.
	//
	// The VRF registration requirement and recovery using mark and
	// sweep can be disabled by configuring
	// "grpc service-layer auto-register" on the device. In presence
	// of this configuration, on client restart or RPC disconnects,
	// the client has the responsibility to reconcile its new state
	// with the state on the device by replaying the difference.
	SLAFVrfRegOp(ctx context.Context, in *SLAFVrfRegMsg, opts ...grpc.CallOption) (*SLAFVrfRegMsgRsp, error)
	// VRF get. Used to retrieve VRF attributes from the server.
	SLAFVrfRegGet(ctx context.Context, in *SLAFVrfRegGetMsg, opts ...grpc.CallOption) (SLAF_SLAFVrfRegGetClient, error)
	// SLAFMsg.Oper = SL_OBJOP_ADD:
	//
	//	Object add. Fails if the object already exists and is not stale.
	//	First ADD operation on a stale object is treated as implicit update
	//	and the object is no longer considered stale.
	//
	// SLAFMsg.Oper = SL_OBJOP_UPDATE:
	//
	//	Object update. Create or update the object. The RPC implements
	//	replacement semantics, wherein if the object exists, all its
	//	attributes are replaced with values from the new message.
	//
	// SLAFMsg.Oper = SL_OBJOP_DELETE:
	//
	//	Object delete. The object's key is enough to delete the object;
	//	other attributes if present are ignored.
	//	Delete of a non-existant object is returned as success.
	SLAFOp(ctx context.Context, in *SLAFMsg, opts ...grpc.CallOption) (*SLAFMsgRsp, error)
	// SLAFMsg.Oper = SL_OBJOP_ADD:
	//
	//	Object add. Fails if the objects already exists and is not stale.
	//	First ADD operation on a stale object is allowed and the object
	//	is no longer considered stale.
	//
	// SLAFMsg.Oper = SL_OBJOP_UPDATE:
	//
	//	Object update. Creates or updates the object.
	//
	// SLAFMsg.Oper = SL_OBJOP_DELETE:
	//
	//	Object delete. The object's key is enough to delete the object.
	//	Delete of a non-existant object is returned as success.
	SLAFOpStream(ctx context.Context, opts ...grpc.CallOption) (SLAF_SLAFOpStreamClient, error)
	// Retrieves object attributes.
	SLAFGet(ctx context.Context, in *SLAFGetMsg, opts ...grpc.CallOption) (SLAF_SLAFGetClient, error)
	SLAFNotifStream(ctx context.Context, opts ...grpc.CallOption) (SLAF_SLAFNotifStreamClient, error)
}

type sLAFClient struct {
	cc grpc.ClientConnInterface
}

func NewSLAFClient(cc grpc.ClientConnInterface) SLAFClient {
	return &sLAFClient{cc}
}

func (c *sLAFClient) SLAFVrfRegOp(ctx context.Context, in *SLAFVrfRegMsg, opts ...grpc.CallOption) (*SLAFVrfRegMsgRsp, error) {
	out := new(SLAFVrfRegMsgRsp)
	err := c.cc.Invoke(ctx, "/service_layer.SLAF/SLAFVrfRegOp", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *sLAFClient) SLAFVrfRegGet(ctx context.Context, in *SLAFVrfRegGetMsg, opts ...grpc.CallOption) (SLAF_SLAFVrfRegGetClient, error) {
	stream, err := c.cc.NewStream(ctx, &SLAF_ServiceDesc.Streams[0], "/service_layer.SLAF/SLAFVrfRegGet", opts...)
	if err != nil {
		return nil, err
	}
	x := &sLAFSLAFVrfRegGetClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type SLAF_SLAFVrfRegGetClient interface {
	Recv() (*SLAFVrfRegGetMsgRsp, error)
	grpc.ClientStream
}

type sLAFSLAFVrfRegGetClient struct {
	grpc.ClientStream
}

func (x *sLAFSLAFVrfRegGetClient) Recv() (*SLAFVrfRegGetMsgRsp, error) {
	m := new(SLAFVrfRegGetMsgRsp)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *sLAFClient) SLAFOp(ctx context.Context, in *SLAFMsg, opts ...grpc.CallOption) (*SLAFMsgRsp, error) {
	out := new(SLAFMsgRsp)
	err := c.cc.Invoke(ctx, "/service_layer.SLAF/SLAFOp", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *sLAFClient) SLAFOpStream(ctx context.Context, opts ...grpc.CallOption) (SLAF_SLAFOpStreamClient, error) {
	stream, err := c.cc.NewStream(ctx, &SLAF_ServiceDesc.Streams[1], "/service_layer.SLAF/SLAFOpStream", opts...)
	if err != nil {
		return nil, err
	}
	x := &sLAFSLAFOpStreamClient{stream}
	return x, nil
}

type SLAF_SLAFOpStreamClient interface {
	Send(*SLAFMsg) error
	Recv() (*SLAFMsgRsp, error)
	grpc.ClientStream
}

type sLAFSLAFOpStreamClient struct {
	grpc.ClientStream
}

func (x *sLAFSLAFOpStreamClient) Send(m *SLAFMsg) error {
	return x.ClientStream.SendMsg(m)
}

func (x *sLAFSLAFOpStreamClient) Recv() (*SLAFMsgRsp, error) {
	m := new(SLAFMsgRsp)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *sLAFClient) SLAFGet(ctx context.Context, in *SLAFGetMsg, opts ...grpc.CallOption) (SLAF_SLAFGetClient, error) {
	stream, err := c.cc.NewStream(ctx, &SLAF_ServiceDesc.Streams[2], "/service_layer.SLAF/SLAFGet", opts...)
	if err != nil {
		return nil, err
	}
	x := &sLAFSLAFGetClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type SLAF_SLAFGetClient interface {
	Recv() (*SLAFGetMsgRsp, error)
	grpc.ClientStream
}

type sLAFSLAFGetClient struct {
	grpc.ClientStream
}

func (x *sLAFSLAFGetClient) Recv() (*SLAFGetMsgRsp, error) {
	m := new(SLAFGetMsgRsp)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *sLAFClient) SLAFNotifStream(ctx context.Context, opts ...grpc.CallOption) (SLAF_SLAFNotifStreamClient, error) {
	stream, err := c.cc.NewStream(ctx, &SLAF_ServiceDesc.Streams[3], "/service_layer.SLAF/SLAFNotifStream", opts...)
	if err != nil {
		return nil, err
	}
	x := &sLAFSLAFNotifStreamClient{stream}
	return x, nil
}

type SLAF_SLAFNotifStreamClient interface {
	Send(*SLAFNotifReq) error
	Recv() (*SLAFNotifMsg, error)
	grpc.ClientStream
}

type sLAFSLAFNotifStreamClient struct {
	grpc.ClientStream
}

func (x *sLAFSLAFNotifStreamClient) Send(m *SLAFNotifReq) error {
	return x.ClientStream.SendMsg(m)
}

func (x *sLAFSLAFNotifStreamClient) Recv() (*SLAFNotifMsg, error) {
	m := new(SLAFNotifMsg)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

// SLAFServer is the server API for SLAF service.
// All implementations must embed UnimplementedSLAFServer
// for forward compatibility
type SLAFServer interface {
	// VRF registration operations. By default, The client must register with
	// the corresponding VRF table before programming objects in that table.
	//
	// SLAFVrfRegMsg.Oper = SL_REGOP_REGISTER:
	//
	//	VRF table registration: Sends a list of VRF table registration
	//	messages and expects a list of registration responses.
	//	A client Must Register a VRF table BEFORE objects can be
	//	added/modified in the associated VRF table.
	//
	// SLAFVrfRegMsg.Oper = SL_REGOP_UNREGISTER:
	//
	//	VRF table Un-registration: Sends a list of VRF table un-registration
	//	messages and expects a list of un-registration responses.
	//	This can be used to convey that the client is no longer interested
	//	in these VRF tables. All previously installed objects would be
	//	remove.
	//
	// SLAFVrfRegMsg.Oper = SL_REGOP_EOF:
	//
	//	VRF table End Of File message.
	//	After Registration, the client is expected to send an EOF
	//	message to convey the end of replay of the client's known objects.
	//	This is especially useful under certain restart scenarios when the
	//	client and the server are trying to synchronize their objects.
	//
	// The VRF table registration operations can be used by the client to
	// synchronize objects with the device. When the client re-registers the
	// VRF table with the server using SL_REGOP_REGISTER, server marks
	// objects in that table as stale.
	// Client then MUST reprogram objects it is interested in.
	// When client sends SL_REGOP_EOF, any objects not reprogrammed
	// are removed from the device.
	//
	// The client MUST perform all operations (VRF registration, objects)
	// from a single execution context.
	//
	// The VRF registration requirement and recovery using mark and
	// sweep can be disabled by configuring
	// "grpc service-layer auto-register" on the device. In presence
	// of this configuration, on client restart or RPC disconnects,
	// the client has the responsibility to reconcile its new state
	// with the state on the device by replaying the difference.
	SLAFVrfRegOp(context.Context, *SLAFVrfRegMsg) (*SLAFVrfRegMsgRsp, error)
	// VRF get. Used to retrieve VRF attributes from the server.
	SLAFVrfRegGet(*SLAFVrfRegGetMsg, SLAF_SLAFVrfRegGetServer) error
	// SLAFMsg.Oper = SL_OBJOP_ADD:
	//
	//	Object add. Fails if the object already exists and is not stale.
	//	First ADD operation on a stale object is treated as implicit update
	//	and the object is no longer considered stale.
	//
	// SLAFMsg.Oper = SL_OBJOP_UPDATE:
	//
	//	Object update. Create or update the object. The RPC implements
	//	replacement semantics, wherein if the object exists, all its
	//	attributes are replaced with values from the new message.
	//
	// SLAFMsg.Oper = SL_OBJOP_DELETE:
	//
	//	Object delete. The object's key is enough to delete the object;
	//	other attributes if present are ignored.
	//	Delete of a non-existant object is returned as success.
	SLAFOp(context.Context, *SLAFMsg) (*SLAFMsgRsp, error)
	// SLAFMsg.Oper = SL_OBJOP_ADD:
	//
	//	Object add. Fails if the objects already exists and is not stale.
	//	First ADD operation on a stale object is allowed and the object
	//	is no longer considered stale.
	//
	// SLAFMsg.Oper = SL_OBJOP_UPDATE:
	//
	//	Object update. Creates or updates the object.
	//
	// SLAFMsg.Oper = SL_OBJOP_DELETE:
	//
	//	Object delete. The object's key is enough to delete the object.
	//	Delete of a non-existant object is returned as success.
	SLAFOpStream(SLAF_SLAFOpStreamServer) error
	// Retrieves object attributes.
	SLAFGet(*SLAFGetMsg, SLAF_SLAFGetServer) error
	SLAFNotifStream(SLAF_SLAFNotifStreamServer) error
	mustEmbedUnimplementedSLAFServer()
}

// UnimplementedSLAFServer must be embedded to have forward compatible implementations.
type UnimplementedSLAFServer struct {
}

func (UnimplementedSLAFServer) SLAFVrfRegOp(context.Context, *SLAFVrfRegMsg) (*SLAFVrfRegMsgRsp, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SLAFVrfRegOp not implemented")
}
func (UnimplementedSLAFServer) SLAFVrfRegGet(*SLAFVrfRegGetMsg, SLAF_SLAFVrfRegGetServer) error {
	return status.Errorf(codes.Unimplemented, "method SLAFVrfRegGet not implemented")
}
func (UnimplementedSLAFServer) SLAFOp(context.Context, *SLAFMsg) (*SLAFMsgRsp, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SLAFOp not implemented")
}
func (UnimplementedSLAFServer) SLAFOpStream(SLAF_SLAFOpStreamServer) error {
	return status.Errorf(codes.Unimplemented, "method SLAFOpStream not implemented")
}
func (UnimplementedSLAFServer) SLAFGet(*SLAFGetMsg, SLAF_SLAFGetServer) error {
	return status.Errorf(codes.Unimplemented, "method SLAFGet not implemented")
}
func (UnimplementedSLAFServer) SLAFNotifStream(SLAF_SLAFNotifStreamServer) error {
	return status.Errorf(codes.Unimplemented, "method SLAFNotifStream not implemented")
}
func (UnimplementedSLAFServer) mustEmbedUnimplementedSLAFServer() {}

// UnsafeSLAFServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to SLAFServer will
// result in compilation errors.
type UnsafeSLAFServer interface {
	mustEmbedUnimplementedSLAFServer()
}

func RegisterSLAFServer(s grpc.ServiceRegistrar, srv SLAFServer) {
	s.RegisterService(&SLAF_ServiceDesc, srv)
}

func _SLAF_SLAFVrfRegOp_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SLAFVrfRegMsg)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SLAFServer).SLAFVrfRegOp(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/service_layer.SLAF/SLAFVrfRegOp",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SLAFServer).SLAFVrfRegOp(ctx, req.(*SLAFVrfRegMsg))
	}
	return interceptor(ctx, in, info, handler)
}

func _SLAF_SLAFVrfRegGet_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(SLAFVrfRegGetMsg)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(SLAFServer).SLAFVrfRegGet(m, &sLAFSLAFVrfRegGetServer{stream})
}

type SLAF_SLAFVrfRegGetServer interface {
	Send(*SLAFVrfRegGetMsgRsp) error
	grpc.ServerStream
}

type sLAFSLAFVrfRegGetServer struct {
	grpc.ServerStream
}

func (x *sLAFSLAFVrfRegGetServer) Send(m *SLAFVrfRegGetMsgRsp) error {
	return x.ServerStream.SendMsg(m)
}

func _SLAF_SLAFOp_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SLAFMsg)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SLAFServer).SLAFOp(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/service_layer.SLAF/SLAFOp",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SLAFServer).SLAFOp(ctx, req.(*SLAFMsg))
	}
	return interceptor(ctx, in, info, handler)
}

func _SLAF_SLAFOpStream_Handler(srv interface{}, stream grpc.ServerStream) error {
	return srv.(SLAFServer).SLAFOpStream(&sLAFSLAFOpStreamServer{stream})
}

type SLAF_SLAFOpStreamServer interface {
	Send(*SLAFMsgRsp) error
	Recv() (*SLAFMsg, error)
	grpc.ServerStream
}

type sLAFSLAFOpStreamServer struct {
	grpc.ServerStream
}

func (x *sLAFSLAFOpStreamServer) Send(m *SLAFMsgRsp) error {
	return x.ServerStream.SendMsg(m)
}

func (x *sLAFSLAFOpStreamServer) Recv() (*SLAFMsg, error) {
	m := new(SLAFMsg)
	if err := x.ServerStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func _SLAF_SLAFGet_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(SLAFGetMsg)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(SLAFServer).SLAFGet(m, &sLAFSLAFGetServer{stream})
}

type SLAF_SLAFGetServer interface {
	Send(*SLAFGetMsgRsp) error
	grpc.ServerStream
}

type sLAFSLAFGetServer struct {
	grpc.ServerStream
}

func (x *sLAFSLAFGetServer) Send(m *SLAFGetMsgRsp) error {
	return x.ServerStream.SendMsg(m)
}

func _SLAF_SLAFNotifStream_Handler(srv interface{}, stream grpc.ServerStream) error {
	return srv.(SLAFServer).SLAFNotifStream(&sLAFSLAFNotifStreamServer{stream})
}

type SLAF_SLAFNotifStreamServer interface {
	Send(*SLAFNotifMsg) error
	Recv() (*SLAFNotifReq, error)
	grpc.ServerStream
}

type sLAFSLAFNotifStreamServer struct {
	grpc.ServerStream
}

func (x *sLAFSLAFNotifStreamServer) Send(m *SLAFNotifMsg) error {
	return x.ServerStream.SendMsg(m)
}

func (x *sLAFSLAFNotifStreamServer) Recv() (*SLAFNotifReq, error) {
	m := new(SLAFNotifReq)
	if err := x.ServerStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

// SLAF_ServiceDesc is the grpc.ServiceDesc for SLAF service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var SLAF_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "service_layer.SLAF",
	HandlerType: (*SLAFServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "SLAFVrfRegOp",
			Handler:    _SLAF_SLAFVrfRegOp_Handler,
		},
		{
			MethodName: "SLAFOp",
			Handler:    _SLAF_SLAFOp_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "SLAFVrfRegGet",
			Handler:       _SLAF_SLAFVrfRegGet_Handler,
			ServerStreams: true,
		},
		{
			StreamName:    "SLAFOpStream",
			Handler:       _SLAF_SLAFOpStream_Handler,
			ServerStreams: true,
			ClientStreams: true,
		},
		{
			StreamName:    "SLAFGet",
			Handler:       _SLAF_SLAFGet_Handler,
			ServerStreams: true,
		},
		{
			StreamName:    "SLAFNotifStream",
			Handler:       _SLAF_SLAFNotifStream_Handler,
			ServerStreams: true,
			ClientStreams: true,
		},
	},
	Metadata: "sl_af.proto",
}
