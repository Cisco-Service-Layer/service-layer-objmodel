#!/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
mkdir -p src/gencpp
printf "Generating cplusplus bindings..."
#protoc installed for cpp is newer than one for go/python - based on grpc.io instructions
/$HOME/.local/bin/protoc -I ../protos --grpc_out=./src/gencpp --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ../protos/*.proto
/$HOME/.local/bin/protoc -I ../protos --cpp_out=./src/gencpp ../protos/*.proto
echo "Done"
