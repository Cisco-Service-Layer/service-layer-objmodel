FROM ubuntu:16.04

ARG WS=/root

ARG GRPC_VER=v1.7.0
ARG PROTOBUF_VER=v3.5.1
ARG GIT_TAG="v1.0.0"


RUN apt-get update && \
    apt-get install -y git vim doxygen autoconf automake libtool \
                       curl make g++ unzip python3 python3-pip golang-go

# grpc
RUN git clone -b ${GRPC_VER} https://github.com/grpc/grpc.git ${WS}/grpc && \
    cd ${WS}/grpc && \
    git submodule update --init && \
    make && \
    make install

# protobuf
RUN git clone -b ${PROTOBUF_VER} https://github.com/google/protobuf.git ${WS}/protobuf && \
    cd ${WS}/protobuf && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install && \
    ldconfig

# python
RUN pip3 install 2to3

# environment
ENV GOROOT="/usr/lib/go-1.6"
ENV GOPATH="${WS}/go"
ENV PATH="${GOPATH}/bin:${GOROOT}/bin:${PATH}:."

# go
RUN mkdir -p ${WS}/go
RUN go get -d -u github.com/golang/protobuf/protoc-gen-go
RUN git -C ${GOPATH}/src/github.com/golang/protobuf checkout ${GIT_TAG}
RUN go install github.com/golang/protobuf/protoc-gen-go
