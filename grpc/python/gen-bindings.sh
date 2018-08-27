#!/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
cd ../protos
printf "Generating Python bindings..."

for proto_file in *.proto
do
  python -m grpc_tools.protoc -I ./ --python_out=../python/src/genpy/ --grpc_python_out=../python/src/genpy/ $proto_file
done
echo "Done"
