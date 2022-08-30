FROM ubuntu:bionic

RUN apt-get update && \
    apt-get install -y git vim doxygen autoconf automake libtool \
                       build-essential pkg-config curl make \
                       unzip python3 python3-pip python3-venv wget

# python
RUN python3 -m venv /opt/venv
RUN . /opt/venv/bin/activate
COPY grpc/python/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

ARG GO_VER=1.19
ARG WS=/slapi
RUN mkdir -p ${WS} 
WORKDIR ${WS}

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

# Above were installed in $HOME/go, since this is running as root
# in container. FIXME, how to use $HOME ?
ENV PATH="${PATH}:/root/go/bin"

####################

## CPP grpc build and install
## reference https://grpc.io/docs/languages/cpp/quickstart
## FIXME should use $HOME instead
#ARG MY_INSTALL_DIR=/root/.local
#RUN mkdir -p ${MY_INSTALL_DIR}
#
#ENV PATH="${PATH}:${MY_INSTALL_DIR}/bin"
#
##get cmake
#RUN wget -q -O cmake-linux.sh https://github.com/Kitware/CMake/releases/download/v3.19.6/cmake-3.19.6-Linux-x86_64.sh
#RUN sh cmake-linux.sh -- --skip-license --prefix=${MY_INSTALL_DIR}
#
## Clone GRPC repo
#RUN git clone --recurse-submodules -b v1.46.3 --depth 1 --shallow-submodules https://github.com/grpc/grpc
#WORKDIR ${WS}/grpc
#
#RUN mkdir -p cmake/build
#WORKDIR ${WS}/grpc/cmake/build
#RUN cmake -DgRPC_INSTALL=ON -DgRPC_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=${MY_INSTALL_DIR} ../..
#RUN make -j
#RUN make install
