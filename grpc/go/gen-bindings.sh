#!/bin/bash
#
# Copyright (c) 2016, 2023 by cisco Systems, Inc. 
# All rights reserved.
#
cd ../protos
printf "Generating GO bindings..."
go_opt=

protoc -I ./ *.proto --go-grpc_out=../go/src/gengo/ --go_out=../go/src/gengo

# copy out to original path where .pb.go are archived, protoc-gen-go 1.26 generates
# bindings in the package directory. After generation, just copy them over to wherever
# the go bindings are SCM'ed.
cd ../go/src/gengo
cp github.com/Cisco-service-layer/service-layer-objmodel/grpc/protos/* .
rm -rf github.com
echo "Done"
