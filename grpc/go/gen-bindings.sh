#!/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
cd ../protos
printf "Generating GO bindings..."
go_opt=
#If build env is set using Dockerfile, then that pulls protoc-gen-go latest, which
# at version 1.26, requires a -M option to compile protobufs otherwise one needs
# to add go_package directive in each protofile.
for F in $(ls *.proto)
do
   go_opt="$go_opt --go_opt=M$F=service_layer/"
done

protoc -I ./ *.proto --plugin=protoc-gen-go=`which protoc-gen-go` $go_opt --go_out=plugins=grpc:../go/src/gengo/

# copy out to original path where .pb.go are archived, protoc-gen-go 1.26 generates
# bindings in the package directory. After generation, just copy them over to wherever
# the go bindings are SCM'ed.
cd ../go/src/gengo
cp service_layer/* .
rm -rf service_layer
echo "Done"
