#!/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
cd ../protos
printf "Generating GO bindings..."
go_opt=

#protoc -I ./ --plugin=protoc-gen-go=`which protoc-gen-go` $go_opt *.proto \
#	--go-grpc_out=../go/src/gengo/

protoc -I ./ \
	sl_bfd_ipv4.proto \
	sl_bfd_ipv6.proto \
	sl_global.proto \
	sl_interface.proto \
	sl_l2_route.proto \
	sl_mpls.proto \
	sl_route_ipv4.proto \
	sl_route_ipv6.proto \
	--go-grpc_out=../go/src/gengo/ \
	--go_out=../go/src/gengo

protoc -I ./ \
	sl_route_common.proto \
	sl_common_types.proto \
	sl_version.proto \
	sl_bfd_common.proto \
	--go_out=../go/src/gengo/

# copy out to original path where .pb.go are archived, protoc-gen-go 1.26 generates
# bindings in the package directory. After generation, just copy them over to wherever
# the go bindings are SCM'ed.
cd ../go/src/gengo
cp github.com/Cisco-service-layer/service-layer-objmodel/grpc/protos/* .
rm -rf github.com
echo "Done"
