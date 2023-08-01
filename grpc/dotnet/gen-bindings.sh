#!/bin/bash
#
# Copyright (c) 2023 by cisco Systems, Inc.
# All rights reserved.
#
printf "Generating dotnet bindings for ServiceLayer..."
DOTNET_ROOT=$(pwd)
cd ${DOTNET_ROOT}/src/gencs
# Restore packages needed by gencs
dotnet restore
cd ${DOTNET_ROOT}/../protos
protoc -I . --csharp_out ${DOTNET_ROOT}/src/gencs --grpc_out ${DOTNET_ROOT}/src/gencs --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` *.proto
#Remove unwanted files
files=("Class1.cs" "SlHello.cs")
for file in "${DOTNET_ROOT}/src/gencs/${files[@]}"
do
  if [ -f "$file" ]
  then
    rm "$file"
    echo "Deleted $file"
  fi
done
cd ${DOTNET_ROOT}/src/tutorial/Quickstart
# Restore packages needed by Quickstart
dotnet restore
cd ${DOTNET_ROOT}
# Generating documentation with DocFX
printf "Generating documentation with DocFX..."
#Remove unwanted directories
rm -rf ${DOTNET_ROOT}/api/
rm -rf ${DOTNET_ROOT}/docs/
docfx docfx.json
#Remove unwanted directories
rm -rf ${DOTNET_ROOT}/src/gencs/obj/
rm -rf ${DOTNET_ROOT}/src/gencs/bin/
rm -rf ${DOTNET_ROOT}/api/
echo "Done"
