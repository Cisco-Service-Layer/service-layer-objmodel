// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v3.18.3
// source: sl_bfd_ipv4.proto

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

// SLBfdv4OperClient is the client API for SLBfdv4Oper service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type SLBfdv4OperClient interface {
	// SLBfdRegMsg.Oper = SL_REGOP_REGISTER:
	//
	//	Global BFD registration.
	//	A client Must Register BEFORE BFD sessions can be added/modified.
	//
	// SLBfdRegMsg.Oper = SL_REGOP_UNREGISTER:
	//
	//	Global BFD un-registration.
	//	This call is used to end all BFD notifications and unregister any
	//	interest in BFD session configuration.
	//	This call cleans up all BFD sessions previously requested.
	//
	// SLBfdRegMsg.Oper = SL_REGOP_EOF:
	//
	//	BFD End Of File.
	//	After Registration, the client is expected to send an EOF
	//	message to convey the end of replay of the client's known objects.
	//	This is especially useful under certain restart scenarios when the
	//	client and the server are trying to synchronize their BFD sessions.
	SLBfdv4RegOp(ctx context.Context, in *SLBfdRegMsg, opts ...grpc.CallOption) (*SLBfdRegMsgRsp, error)
	// Used to retrieve global BFD info from the server.
	SLBfdv4Get(ctx context.Context, in *SLBfdGetMsg, opts ...grpc.CallOption) (*SLBfdGetMsgRsp, error)
	// Used to retrieve global BFD stats from the server.
	SLBfdv4GetStats(ctx context.Context, in *SLBfdGetMsg, opts ...grpc.CallOption) (*SLBfdGetStatsMsgRsp, error)
	// This call is used to get a stream of session state notifications.
	// The caller must maintain the GRPC channel as long as
	// there is interest in BFD session notifications. Only sessions that were
	// created through this API will be notified to caller.
	// This call can be used to get "push" notifications for session states.
	// It is advised that the caller register for notifications before any
	// sessions are created to avoid any loss of notifications.
	SLBfdv4GetNotifStream(ctx context.Context, in *SLBfdGetNotifMsg, opts ...grpc.CallOption) (SLBfdv4Oper_SLBfdv4GetNotifStreamClient, error)
	// SLBfdv4Msg.Oper = SL_OBJOP_ADD:
	//
	//	Add one or multiple BFD sessions.
	//
	// SLBfdv4Msg.Oper = SL_OBJOP_UPDATE:
	//
	//	Update one or multiple BFD sessions.
	//
	// SLBfdv4Msg.Oper = SL_OBJOP_DELETE:
	//
	//	Delete one or multiple BFD sessions.
	SLBfdv4SessionOp(ctx context.Context, in *SLBfdv4Msg, opts ...grpc.CallOption) (*SLBfdv4MsgRsp, error)
	// Retrieve BFD session attributes and state.
	// This call can be used to "poll" the current state of a session.
	SLBfdv4SessionGet(ctx context.Context, in *SLBfdv4GetMsg, opts ...grpc.CallOption) (*SLBfdv4GetMsgRsp, error)
}

type sLBfdv4OperClient struct {
	cc grpc.ClientConnInterface
}

func NewSLBfdv4OperClient(cc grpc.ClientConnInterface) SLBfdv4OperClient {
	return &sLBfdv4OperClient{cc}
}

func (c *sLBfdv4OperClient) SLBfdv4RegOp(ctx context.Context, in *SLBfdRegMsg, opts ...grpc.CallOption) (*SLBfdRegMsgRsp, error) {
	out := new(SLBfdRegMsgRsp)
	err := c.cc.Invoke(ctx, "/service_layer.SLBfdv4Oper/SLBfdv4RegOp", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *sLBfdv4OperClient) SLBfdv4Get(ctx context.Context, in *SLBfdGetMsg, opts ...grpc.CallOption) (*SLBfdGetMsgRsp, error) {
	out := new(SLBfdGetMsgRsp)
	err := c.cc.Invoke(ctx, "/service_layer.SLBfdv4Oper/SLBfdv4Get", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *sLBfdv4OperClient) SLBfdv4GetStats(ctx context.Context, in *SLBfdGetMsg, opts ...grpc.CallOption) (*SLBfdGetStatsMsgRsp, error) {
	out := new(SLBfdGetStatsMsgRsp)
	err := c.cc.Invoke(ctx, "/service_layer.SLBfdv4Oper/SLBfdv4GetStats", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *sLBfdv4OperClient) SLBfdv4GetNotifStream(ctx context.Context, in *SLBfdGetNotifMsg, opts ...grpc.CallOption) (SLBfdv4Oper_SLBfdv4GetNotifStreamClient, error) {
	stream, err := c.cc.NewStream(ctx, &SLBfdv4Oper_ServiceDesc.Streams[0], "/service_layer.SLBfdv4Oper/SLBfdv4GetNotifStream", opts...)
	if err != nil {
		return nil, err
	}
	x := &sLBfdv4OperSLBfdv4GetNotifStreamClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type SLBfdv4Oper_SLBfdv4GetNotifStreamClient interface {
	Recv() (*SLBfdv4Notif, error)
	grpc.ClientStream
}

type sLBfdv4OperSLBfdv4GetNotifStreamClient struct {
	grpc.ClientStream
}

func (x *sLBfdv4OperSLBfdv4GetNotifStreamClient) Recv() (*SLBfdv4Notif, error) {
	m := new(SLBfdv4Notif)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *sLBfdv4OperClient) SLBfdv4SessionOp(ctx context.Context, in *SLBfdv4Msg, opts ...grpc.CallOption) (*SLBfdv4MsgRsp, error) {
	out := new(SLBfdv4MsgRsp)
	err := c.cc.Invoke(ctx, "/service_layer.SLBfdv4Oper/SLBfdv4SessionOp", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *sLBfdv4OperClient) SLBfdv4SessionGet(ctx context.Context, in *SLBfdv4GetMsg, opts ...grpc.CallOption) (*SLBfdv4GetMsgRsp, error) {
	out := new(SLBfdv4GetMsgRsp)
	err := c.cc.Invoke(ctx, "/service_layer.SLBfdv4Oper/SLBfdv4SessionGet", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// SLBfdv4OperServer is the server API for SLBfdv4Oper service.
// All implementations must embed UnimplementedSLBfdv4OperServer
// for forward compatibility
type SLBfdv4OperServer interface {
	// SLBfdRegMsg.Oper = SL_REGOP_REGISTER:
	//
	//	Global BFD registration.
	//	A client Must Register BEFORE BFD sessions can be added/modified.
	//
	// SLBfdRegMsg.Oper = SL_REGOP_UNREGISTER:
	//
	//	Global BFD un-registration.
	//	This call is used to end all BFD notifications and unregister any
	//	interest in BFD session configuration.
	//	This call cleans up all BFD sessions previously requested.
	//
	// SLBfdRegMsg.Oper = SL_REGOP_EOF:
	//
	//	BFD End Of File.
	//	After Registration, the client is expected to send an EOF
	//	message to convey the end of replay of the client's known objects.
	//	This is especially useful under certain restart scenarios when the
	//	client and the server are trying to synchronize their BFD sessions.
	SLBfdv4RegOp(context.Context, *SLBfdRegMsg) (*SLBfdRegMsgRsp, error)
	// Used to retrieve global BFD info from the server.
	SLBfdv4Get(context.Context, *SLBfdGetMsg) (*SLBfdGetMsgRsp, error)
	// Used to retrieve global BFD stats from the server.
	SLBfdv4GetStats(context.Context, *SLBfdGetMsg) (*SLBfdGetStatsMsgRsp, error)
	// This call is used to get a stream of session state notifications.
	// The caller must maintain the GRPC channel as long as
	// there is interest in BFD session notifications. Only sessions that were
	// created through this API will be notified to caller.
	// This call can be used to get "push" notifications for session states.
	// It is advised that the caller register for notifications before any
	// sessions are created to avoid any loss of notifications.
	SLBfdv4GetNotifStream(*SLBfdGetNotifMsg, SLBfdv4Oper_SLBfdv4GetNotifStreamServer) error
	// SLBfdv4Msg.Oper = SL_OBJOP_ADD:
	//
	//	Add one or multiple BFD sessions.
	//
	// SLBfdv4Msg.Oper = SL_OBJOP_UPDATE:
	//
	//	Update one or multiple BFD sessions.
	//
	// SLBfdv4Msg.Oper = SL_OBJOP_DELETE:
	//
	//	Delete one or multiple BFD sessions.
	SLBfdv4SessionOp(context.Context, *SLBfdv4Msg) (*SLBfdv4MsgRsp, error)
	// Retrieve BFD session attributes and state.
	// This call can be used to "poll" the current state of a session.
	SLBfdv4SessionGet(context.Context, *SLBfdv4GetMsg) (*SLBfdv4GetMsgRsp, error)
	mustEmbedUnimplementedSLBfdv4OperServer()
}

// UnimplementedSLBfdv4OperServer must be embedded to have forward compatible implementations.
type UnimplementedSLBfdv4OperServer struct {
}

func (UnimplementedSLBfdv4OperServer) SLBfdv4RegOp(context.Context, *SLBfdRegMsg) (*SLBfdRegMsgRsp, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SLBfdv4RegOp not implemented")
}
func (UnimplementedSLBfdv4OperServer) SLBfdv4Get(context.Context, *SLBfdGetMsg) (*SLBfdGetMsgRsp, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SLBfdv4Get not implemented")
}
func (UnimplementedSLBfdv4OperServer) SLBfdv4GetStats(context.Context, *SLBfdGetMsg) (*SLBfdGetStatsMsgRsp, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SLBfdv4GetStats not implemented")
}
func (UnimplementedSLBfdv4OperServer) SLBfdv4GetNotifStream(*SLBfdGetNotifMsg, SLBfdv4Oper_SLBfdv4GetNotifStreamServer) error {
	return status.Errorf(codes.Unimplemented, "method SLBfdv4GetNotifStream not implemented")
}
func (UnimplementedSLBfdv4OperServer) SLBfdv4SessionOp(context.Context, *SLBfdv4Msg) (*SLBfdv4MsgRsp, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SLBfdv4SessionOp not implemented")
}
func (UnimplementedSLBfdv4OperServer) SLBfdv4SessionGet(context.Context, *SLBfdv4GetMsg) (*SLBfdv4GetMsgRsp, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SLBfdv4SessionGet not implemented")
}
func (UnimplementedSLBfdv4OperServer) mustEmbedUnimplementedSLBfdv4OperServer() {}

// UnsafeSLBfdv4OperServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to SLBfdv4OperServer will
// result in compilation errors.
type UnsafeSLBfdv4OperServer interface {
	mustEmbedUnimplementedSLBfdv4OperServer()
}

func RegisterSLBfdv4OperServer(s grpc.ServiceRegistrar, srv SLBfdv4OperServer) {
	s.RegisterService(&SLBfdv4Oper_ServiceDesc, srv)
}

func _SLBfdv4Oper_SLBfdv4RegOp_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SLBfdRegMsg)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SLBfdv4OperServer).SLBfdv4RegOp(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/service_layer.SLBfdv4Oper/SLBfdv4RegOp",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SLBfdv4OperServer).SLBfdv4RegOp(ctx, req.(*SLBfdRegMsg))
	}
	return interceptor(ctx, in, info, handler)
}

func _SLBfdv4Oper_SLBfdv4Get_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SLBfdGetMsg)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SLBfdv4OperServer).SLBfdv4Get(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/service_layer.SLBfdv4Oper/SLBfdv4Get",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SLBfdv4OperServer).SLBfdv4Get(ctx, req.(*SLBfdGetMsg))
	}
	return interceptor(ctx, in, info, handler)
}

func _SLBfdv4Oper_SLBfdv4GetStats_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SLBfdGetMsg)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SLBfdv4OperServer).SLBfdv4GetStats(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/service_layer.SLBfdv4Oper/SLBfdv4GetStats",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SLBfdv4OperServer).SLBfdv4GetStats(ctx, req.(*SLBfdGetMsg))
	}
	return interceptor(ctx, in, info, handler)
}

func _SLBfdv4Oper_SLBfdv4GetNotifStream_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(SLBfdGetNotifMsg)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(SLBfdv4OperServer).SLBfdv4GetNotifStream(m, &sLBfdv4OperSLBfdv4GetNotifStreamServer{stream})
}

type SLBfdv4Oper_SLBfdv4GetNotifStreamServer interface {
	Send(*SLBfdv4Notif) error
	grpc.ServerStream
}

type sLBfdv4OperSLBfdv4GetNotifStreamServer struct {
	grpc.ServerStream
}

func (x *sLBfdv4OperSLBfdv4GetNotifStreamServer) Send(m *SLBfdv4Notif) error {
	return x.ServerStream.SendMsg(m)
}

func _SLBfdv4Oper_SLBfdv4SessionOp_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SLBfdv4Msg)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SLBfdv4OperServer).SLBfdv4SessionOp(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/service_layer.SLBfdv4Oper/SLBfdv4SessionOp",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SLBfdv4OperServer).SLBfdv4SessionOp(ctx, req.(*SLBfdv4Msg))
	}
	return interceptor(ctx, in, info, handler)
}

func _SLBfdv4Oper_SLBfdv4SessionGet_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SLBfdv4GetMsg)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SLBfdv4OperServer).SLBfdv4SessionGet(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/service_layer.SLBfdv4Oper/SLBfdv4SessionGet",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SLBfdv4OperServer).SLBfdv4SessionGet(ctx, req.(*SLBfdv4GetMsg))
	}
	return interceptor(ctx, in, info, handler)
}

// SLBfdv4Oper_ServiceDesc is the grpc.ServiceDesc for SLBfdv4Oper service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var SLBfdv4Oper_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "service_layer.SLBfdv4Oper",
	HandlerType: (*SLBfdv4OperServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "SLBfdv4RegOp",
			Handler:    _SLBfdv4Oper_SLBfdv4RegOp_Handler,
		},
		{
			MethodName: "SLBfdv4Get",
			Handler:    _SLBfdv4Oper_SLBfdv4Get_Handler,
		},
		{
			MethodName: "SLBfdv4GetStats",
			Handler:    _SLBfdv4Oper_SLBfdv4GetStats_Handler,
		},
		{
			MethodName: "SLBfdv4SessionOp",
			Handler:    _SLBfdv4Oper_SLBfdv4SessionOp_Handler,
		},
		{
			MethodName: "SLBfdv4SessionGet",
			Handler:    _SLBfdv4Oper_SLBfdv4SessionGet_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "SLBfdv4GetNotifStream",
			Handler:       _SLBfdv4Oper_SLBfdv4GetNotifStream_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "sl_bfd_ipv4.proto",
}
