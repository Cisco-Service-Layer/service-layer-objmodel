// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v3.18.3
// source: sl_policy.proto

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

// SLPolicyClient is the client API for SLPolicy service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type SLPolicyClient interface {
	// On client restart or RPC disconnects, the client has the
	// to reconcile its new state with the state on the device
	// by replaying the difference.
	SLPolicyOp(ctx context.Context, in *SLPolicyOpMsg, opts ...grpc.CallOption) (*SLPolicyOpRsp, error)
	// Retrieve all Policies and its rules and the interfaces where the
	// policy is applied from the server
	SLPolicyGet(ctx context.Context, in *SLPolicyGetMsg, opts ...grpc.CallOption) (SLPolicy_SLPolicyGetClient, error)
	// Retrieve Global Policy capabilities
	SLPolicyGlobalGet(ctx context.Context, in *SLPolicyGlobalGetMsg, opts ...grpc.CallOption) (*SLPolicyGlobalGetMsgRsp, error)
}

type sLPolicyClient struct {
	cc grpc.ClientConnInterface
}

func NewSLPolicyClient(cc grpc.ClientConnInterface) SLPolicyClient {
	return &sLPolicyClient{cc}
}

func (c *sLPolicyClient) SLPolicyOp(ctx context.Context, in *SLPolicyOpMsg, opts ...grpc.CallOption) (*SLPolicyOpRsp, error) {
	out := new(SLPolicyOpRsp)
	err := c.cc.Invoke(ctx, "/service_layer.SLPolicy/SLPolicyOp", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *sLPolicyClient) SLPolicyGet(ctx context.Context, in *SLPolicyGetMsg, opts ...grpc.CallOption) (SLPolicy_SLPolicyGetClient, error) {
	stream, err := c.cc.NewStream(ctx, &SLPolicy_ServiceDesc.Streams[0], "/service_layer.SLPolicy/SLPolicyGet", opts...)
	if err != nil {
		return nil, err
	}
	x := &sLPolicySLPolicyGetClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type SLPolicy_SLPolicyGetClient interface {
	Recv() (*SLPolicyGetMsgRsp, error)
	grpc.ClientStream
}

type sLPolicySLPolicyGetClient struct {
	grpc.ClientStream
}

func (x *sLPolicySLPolicyGetClient) Recv() (*SLPolicyGetMsgRsp, error) {
	m := new(SLPolicyGetMsgRsp)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *sLPolicyClient) SLPolicyGlobalGet(ctx context.Context, in *SLPolicyGlobalGetMsg, opts ...grpc.CallOption) (*SLPolicyGlobalGetMsgRsp, error) {
	out := new(SLPolicyGlobalGetMsgRsp)
	err := c.cc.Invoke(ctx, "/service_layer.SLPolicy/SLPolicyGlobalGet", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// SLPolicyServer is the server API for SLPolicy service.
// All implementations must embed UnimplementedSLPolicyServer
// for forward compatibility
type SLPolicyServer interface {
	// On client restart or RPC disconnects, the client has the
	// to reconcile its new state with the state on the device
	// by replaying the difference.
	SLPolicyOp(context.Context, *SLPolicyOpMsg) (*SLPolicyOpRsp, error)
	// Retrieve all Policies and its rules and the interfaces where the
	// policy is applied from the server
	SLPolicyGet(*SLPolicyGetMsg, SLPolicy_SLPolicyGetServer) error
	// Retrieve Global Policy capabilities
	SLPolicyGlobalGet(context.Context, *SLPolicyGlobalGetMsg) (*SLPolicyGlobalGetMsgRsp, error)
	mustEmbedUnimplementedSLPolicyServer()
}

// UnimplementedSLPolicyServer must be embedded to have forward compatible implementations.
type UnimplementedSLPolicyServer struct {
}

func (UnimplementedSLPolicyServer) SLPolicyOp(context.Context, *SLPolicyOpMsg) (*SLPolicyOpRsp, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SLPolicyOp not implemented")
}
func (UnimplementedSLPolicyServer) SLPolicyGet(*SLPolicyGetMsg, SLPolicy_SLPolicyGetServer) error {
	return status.Errorf(codes.Unimplemented, "method SLPolicyGet not implemented")
}
func (UnimplementedSLPolicyServer) SLPolicyGlobalGet(context.Context, *SLPolicyGlobalGetMsg) (*SLPolicyGlobalGetMsgRsp, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SLPolicyGlobalGet not implemented")
}
func (UnimplementedSLPolicyServer) mustEmbedUnimplementedSLPolicyServer() {}

// UnsafeSLPolicyServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to SLPolicyServer will
// result in compilation errors.
type UnsafeSLPolicyServer interface {
	mustEmbedUnimplementedSLPolicyServer()
}

func RegisterSLPolicyServer(s grpc.ServiceRegistrar, srv SLPolicyServer) {
	s.RegisterService(&SLPolicy_ServiceDesc, srv)
}

func _SLPolicy_SLPolicyOp_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SLPolicyOpMsg)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SLPolicyServer).SLPolicyOp(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/service_layer.SLPolicy/SLPolicyOp",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SLPolicyServer).SLPolicyOp(ctx, req.(*SLPolicyOpMsg))
	}
	return interceptor(ctx, in, info, handler)
}

func _SLPolicy_SLPolicyGet_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(SLPolicyGetMsg)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(SLPolicyServer).SLPolicyGet(m, &sLPolicySLPolicyGetServer{stream})
}

type SLPolicy_SLPolicyGetServer interface {
	Send(*SLPolicyGetMsgRsp) error
	grpc.ServerStream
}

type sLPolicySLPolicyGetServer struct {
	grpc.ServerStream
}

func (x *sLPolicySLPolicyGetServer) Send(m *SLPolicyGetMsgRsp) error {
	return x.ServerStream.SendMsg(m)
}

func _SLPolicy_SLPolicyGlobalGet_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SLPolicyGlobalGetMsg)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SLPolicyServer).SLPolicyGlobalGet(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/service_layer.SLPolicy/SLPolicyGlobalGet",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SLPolicyServer).SLPolicyGlobalGet(ctx, req.(*SLPolicyGlobalGetMsg))
	}
	return interceptor(ctx, in, info, handler)
}

// SLPolicy_ServiceDesc is the grpc.ServiceDesc for SLPolicy service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var SLPolicy_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "service_layer.SLPolicy",
	HandlerType: (*SLPolicyServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "SLPolicyOp",
			Handler:    _SLPolicy_SLPolicyOp_Handler,
		},
		{
			MethodName: "SLPolicyGlobalGet",
			Handler:    _SLPolicy_SLPolicyGlobalGet_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "SLPolicyGet",
			Handler:       _SLPolicy_SLPolicyGet_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "sl_policy.proto",
}
