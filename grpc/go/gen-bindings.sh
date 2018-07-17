#!/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
cd ../protos
printf "Generating GO bindings..."
protoc -I ./ *.proto --plugin=$GOPATH/bin/protoc-gen-go --go_out=plugins=grpc:../go/src/gengo/
echo "Done"
