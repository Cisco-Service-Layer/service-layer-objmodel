#!/bin/bash
#
# Copyright (c) 2023 by cisco Systems, Inc.
# All rights reserved.
#
printf "Generating dotnet bindings for ServiceLayer..."
mkdir -p ./src/gencs
cd ./src/gencs
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
# replace end of line chars
sed -i 's/\r$//' "$FILE"
cd ../../../protos
protoc -I . --csharp_out ../dotnet/src/gencs --grpc_out ../dotnet/src/gencs --plugin=protoc-gen-grpc=`which grpc_csharp_plugin` *.proto
if [ -f "../dotnet/src/gencs/Class1.cs" ]; then
  rm ../dotnet/src/gencs/Class1.cs
fi
rm -rf ../dotnet/src/gencs/obj/
for file in $(find ../dotnet/src/gencs/ -name "*.cs")
  do
    echo -e "/*\n * Copyright (c) $(date +%Y) by cisco Systems, Inc. All rights reserved.\n */\n$(cat $file)" > $file
  done
echo "Done"
