#!/bin/bash
#
# Copyright (c) 2016, 2023 by cisco Systems, Inc.
# All rights reserved.
#
cd ../protos
printf "Generating Python bindings..."
mkdir -p ../python/src/genpy
python3 -m grpc_tools.protoc --proto_path=. --python_out=../python/src/genpy --grpc_python_out=../python/src/genpy *.proto

# Convert generated code to a valid package by adding __init__.py and making
# imports relative
touch ../python/src/genpy/__init__.py
sed -i "s/^\(import sl.*\)/from . \1/g" ../python/src/genpy/*.py

echo "Done"
