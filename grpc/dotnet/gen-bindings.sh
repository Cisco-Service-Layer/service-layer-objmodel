#!/bin/bash
#
# Copyright (c) 2023 by cisco Systems, Inc.
# All rights reserved.
#
DOTNET_ROOT=$(pwd)
printf "Generating dotnet bindings for ServiceLayer..."
mkdir -p ${DOTNET_ROOT}/src/gencs
cd ${DOTNET_ROOT}/src/gencs
FILE=./ServiceLayer.csproj
if [ -f "$FILE" ]; then
  echo "$FILE exists."
else
  echo "$FILE does not exist."
  dotnet new classlib --output . --name ServiceLayer
  sed -i "/<\/TargetFramework>/a \
    \ \ \ \ <OutputType>Library<\/OutputType>\n\
    <Version>1.0.0<\/Version>\n\
    <Copyright>Copyright (c) $(date +%Y) by cisco Systems, Inc.<\/Copyright> \
    " $FILE
fi
dotnet add package Grpc
dotnet add package Grpc.Tools
dotnet add package Google.Protobuf
cd ${DOTNET_ROOT}/../protos
protoc -I . --csharp_out ${DOTNET_ROOT}/src/gencs --grpc_out ${DOTNET_ROOT}/src/gencs --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` *.proto
if [ -f "../dotnet/src/gencs/Class1.cs" ]; then
  rm ../dotnet/src/gencs/Class1.cs
fi
rm -rf ../dotnet/src/gencs/obj/
cd ${DOTNET_ROOT}/tutorial/Quickstart
# Restore packages needed by Quickstart
dotnet restore
echo "Done"
