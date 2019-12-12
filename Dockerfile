FROM ubuntu:16.04

ARG WS=/

ARG GO_VER=1.9.1
ARG GRPC_VER=v1.9.1
ARG PROTOBUF_VER=v3.2.0
ARG GENPROTO_VER=4eb30f4
ARG GO_PROTOBUF_VER=v1.0.0

RUN apt-get update && \
    apt-get install -y git vim doxygen autoconf automake libtool \
                       curl make g++ unzip python3 python3-pip wget

# grpc
RUN git clone -b ${GRPC_VER} https://github.com/grpc/grpc.git ${WS}/grpc && \
    cd ${WS}/grpc && \
    git submodule update --init && \
    make && \
    make install

# protobuf
RUN cd ${WS}/grpc/third_party/protobuf && \
    git checkout -b ${PROTOBUF_VER} ${PROTOBUF_VER} && \
    make && \
    make install && \
    ldconfig

# python
RUN pip3 install 2to3

# go
RUN wget -qO- https://dl.google.com/go/go${GO_VER}.linux-amd64.tar.gz | tar xzvf - -C /usr/local

# environment
ENV SLAPI_ROOT="${WS}/slapi"
ENV GOROOT="/usr/local/go"
ENV GOPATH="${WS}/go"
ENV PATH="${WS}/bin:${GOPATH}/bin:${GOROOT}/bin:${PATH}:."

RUN mkdir -p ${WS}/go

# grpc
RUN go get -d google.golang.org/grpc && \
    git -C ${GOPATH}/src/google.golang.org/grpc checkout \
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

# make install
RUN make -C ${GOPATH}/src/github.com/golang/protobuf install

ENV GOPATH="${GOPATH}:${SLAPI_ROOT}/grpc/go"
