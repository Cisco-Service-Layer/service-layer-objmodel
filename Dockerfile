FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y git vim doxygen autoconf automake libtool \
                       curl make g++ unzip python3 python3-pip wget

# python
RUN pip3 install 2to3

ARG WS=/

ARG GO_VER=1.14.2
ARG GRPC_VER=v1.30.0
ARG PROTOC_VER=3.12.1
ARG GENPROTO_VER=053ba62
ARG GO_PROTOBUF_VER=v1.4.2

# go
RUN wget -qO- https://dl.google.com/go/go${GO_VER}.linux-amd64.tar.gz | tar xzvf - -C /usr/local

# Install protocol buffer compiler https://grpc.io/docs/protoc-installation/
ARG PB_REL=https://github.com/protocolbuffers/protobuf/releases
RUN curl -LO ${PB_REL}/download/v${PROTOC_VER}/protoc-${PROTOC_VER}-linux-x86_64.zip
RUN unzip protoc-${PROTOC_VER}-linux-x86_64.zip -d /usr/local

# grpc
 RUN git clone -b ${GRPC_VER} https://github.com/grpc/grpc.git ${WS}/grpc && \
     cd ${WS}/grpc && \
     git checkout -b ${GRPC_VER} ${GRPC_VER} && \
     git submodule update --init && \
     make grpc_python_plugin && \
     make install

# protobuf
# RUN cd ${WS}/grpc/third_party/protobuf && \
#    git checkout -b ${PROTOBUF_VER} ${PROTOBUF_VER} && \
#    make && \
#    make install && \
#    ldconfig

## environment
ENV SLAPI_ROOT="${WS}/slapi"
ENV GOROOT="/usr/local/go"
ENV GOPATH="${WS}/go"
ENV PATH="${WS}/bin:${GOPATH}/bin:${GOROOT}/bin:${PATH}:."

RUN mkdir -p ${WS}/go

# grpc download. the go get -d with 1.14.2 fails to download google.golang.org/grpc
# successfully. the exit 0 is to ignore the error. the intent here
# is to have an env for bindings generation.
#
# we need to use this version of go as its compatible with emsd at r73x.
RUN go get -d google.golang.org/grpc; exit 0
RUN git -C ${GOPATH}/src/google.golang.org/grpc checkout \
        -b ${GRPC_VER} ${GRPC_VER}

# The previous command also pulls protobuf and genpro so make sure
# we use the proper versions

# genproto: this repository contains the generated Go packages for common
# protocol buffer types, and the generated gRPC code necessary for interacting
# with Google's gRPC APIs.
RUN git -C ${GOPATH}/src/google.golang.org/genproto checkout \
        -b ${GENPROTO_VER} ${GENPROTO_VER}

# protobuf: This package includes the Protoc compiler for generating Go
# bindings for the protocol buffers, and a library that implements run-time 
# support for encoding (marshaling), decoding (unmarshaling), and accessing
# protocol buffers.
RUN git -C ${GOPATH}/src/github.com/golang/protobuf checkout \
        -b ${GO_PROTOBUF_VER} ${GO_PROTOBUF_VER}

# Build protoc-gen-go plugin for protoc
RUN go install github.com/golang/protobuf/protoc-gen-go

ENV GOPATH="${GOPATH}:${SLAPI_ROOT}/grpc/go"
