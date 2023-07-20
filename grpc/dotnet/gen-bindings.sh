#!/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc.
# All rights reserved.
#
printf "Generating dotnet bindings..."
mkdir -p ./src/gencs
cd ./src/gencs
dotnet new console --force
dotnet add package Grpc
dotnet add package Grpc.Tools
dotnet add package Google.Protobuf
cd ../../../protos
protoc -I . --csharp_out ../dotnet/src/gencs --grpc_out ../dotnet/src/gencs --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` *.proto
rm ../dotnet/src/gencs/Program.cs
rm -rf ../dotnet/src/gencs/obj/
echo "Done"
