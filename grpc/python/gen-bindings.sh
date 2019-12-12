#!/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
cd ../protos
printf "Generating Python bindings..."
protoc -I ./ --python_out=../python/src/genpy/ --grpc_out=../python/src/genpy/ --plugin=protoc-gen-grpc=`which grpc_python_plugin` *.proto
cd ../python/src/genpy; 2to3 -wn *
echo "Done"
