FROM ubuntu:bionic

RUN apt-get update && \
    apt-get install -y git vim doxygen autoconf automake libtool \
                       build-essential pkg-config curl cmake make g++ unzip python3 python3-pip python3-venv wget

# python
RUN python3 -m venv /opt/venv
RUN . /opt/venv/bin/activate
COPY grpc/python/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

ARG WS=/

ARG C_GRPC_VER=v1.40.0
ARG PROTOBUF_VER=v3.18.0

ARG GO_VER=1.19
ARG GO_PROTOBUF_VER=v1.4.2
ARG GO_GRPC_VER=v1.34.0
ARG GENPROTO_VER=798beca9d670ad2544685973f1b5eebab3c025cb

# Install GO binary https://go.dev/doc/install
RUN wget -qO- https://golang.org/dl/go${GO_VER}.linux-amd64.tar.gz | tar xzvf - -C /usr/local

#Ensure PATH has GO binary path
ENV PATH="${PATH}:/usr/local/go/bin"

# Install protocol buffer compiler https://grpc.io/docs/protoc-installation/
ARG PB_REL=https://github.com/protocolbuffers/protobuf/releases
RUN curl -LO ${PB_REL}/download/v3.15.8/protoc-3.15.8-linux-x86_64.zip
RUN unzip protoc-3.15.8-linux-x86_64.zip -d /usr/local

# Install protoc-gen-go and protoc-gen-go-grpc
# Reference https://grpc.io/docs/languages/go/quickstart

RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
RUN go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
ENV PATH="${PATH}:/root/go/bin"

## grpc
#RUN git clone -b ${C_GRPC_VER} https://github.com/grpc/grpc.git ${WS}/grpc && \
#    cd ${WS}/grpc && \
#    git submodule update --init && \
#    mkdir -p cmake/build && \
#    cd cmake/build && \
#    cmake ../.. && \
#    make
#
## protobuf
#RUN cd ${WS}/grpc/third_party/protobuf && \
#    git checkout -b ${PROTOBUF_VER} ${PROTOBUF_VER} && \
#    ./autogen.sh && \
#    ./configure && \
#    make && \
#    make install && \
#    ldconfig

# environment
ENV SLAPI_ROOT="${WS}/slapi"
ENV GOROOT="/usr/local/go"
ENV PATH="${PATH}:."

## grpc
#RUN go get -d google.golang.org/grpc && \
#    git -C ${GOPATH}/src/google.golang.org/grpc checkout \
#        -b ${GO_GRPC_VER} ${GO_GRPC_VER}
#
## The previous command also pulls protobuf and genpro so make sure
## we use the proper versions
#
## genproto: this repository contains the generated Go packages for common
## protocol buffer types, and the generated gRPC code necessary for interacting
## with Google's gRPC APIs.
#RUN git -C ${GOPATH}/src/google.golang.org/genproto checkout \
#        -b ${GENPROTO_VER} ${GENPROTO_VER}
#
## protobuf: This package includes the Protoc compiler for generating Go
## bindings for the protocol buffers, and a library that implements run-time 
## support for encoding (marshaling), decoding (unmarshaling), and accessing
## protocol buffers.
#RUN git -C ${GOPATH}/src/github.com/golang/protobuf checkout \
#        -b ${GO_PROTOBUF_VER} ${GO_PROTOBUF_VER}
#
## Build protoc-gen-go plugin for protoc
#RUN go install github.com/golang/protobuf/protoc-gen-go
#
#ENV GOPATH="${GOPATH}:${SLAPI_ROOT}/grpc/go"
