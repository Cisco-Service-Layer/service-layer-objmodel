#!/bin/bash

# install grpc and protobuf
# grpc version = 0.13.1
# protobuf version = 3.5.0

set -x

PROTOBUF_INSTALLED_VERSION=`pkg-config --exists protobuf && pkg-config --modversion protobuf`
GRPC_INSTALLED_VERSION=`pkg-config --exists grpc && pkg-config --modversion grpc`

# protobuf 3.5.0 
PROTOBUF_VERSION="3.5.0"
PROTOBUF_HASH=2761122b810fe8861004ae785cc3ab39f384d342
# grpc 0.13.1
GRPC_VERSION="0.13.1"
GRPC_HASH=80893242c1ee929d19e6bec5dc19a1515cd8dd81


SCRIPT_DIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"


# Install pkg-config first
apt-get update && apt-get install -y pkg-config

if [[ $GRPC_INSTALLED_VERSION != $GRPC_VERSION  || \
          $PROTOBUF_INSTALLED_VERSION != $PROTOBUF_VERSION ]]; then 
    apt-get update && apt-get install -y \
         autoconf automake libtool curl make g++ unzip git

    rm -rf ~/tempdir
    mkdir -p ~/tempdir/

    if [[ $PROTOBUF_INSTALLED_VERSION != $PROTOBUF_VERSION ]]; then
        #install protobuf
        git clone https://github.com/google/protobuf.git ~/tempdir/protobuf && \

        cd ~/tempdir/protobuf && \
        git checkout $PROTOBUF_HASH && \
        ./autogen.sh && \
        ./configure && \
        make && \
        make install &&\
        ldconfig 

    fi

    if [[ $GRPC_INSTALLED_VERSION != $GRPC_VERSION ]]; then
        #install grpc
        git clone https://github.com/grpc/grpc.git ~/tempdir/grpc && \
        cd ~/tempdir/grpc && \
        git checkout $GRPC_HASH && \
        git submodule update --init && \
        make && \
        make install 
    fi
 
fi

cd ~/ && rm -rf ~/tempdir

# Clean up first
$SCRIPT_DIR/clean.sh

# Create the c++ bindings from proto files
cd $SCRIPT_DIR
./gen-bindings.sh

# Drop into the src directory to build and install the service layer bindings as a static library libiosxrsl.a
cd $SCRIPT_DIR/src
mkdir -p /usr/local/lib/iosxrsl

if [ ! -f /usr/local/lib/libiosxrsl.a ]; then
    # Create the genobj directory
    mkdir -p genobj
    make
    make install
    ldconfig
fi
