#!/bin/bash

usage="
$(basename "$0") [-h] [-g/--grpc-version -p/--protobuf-version -v/--verbose] -- script to install desired versions of grpc, protobuf and build the libiosxrsl.a library 
where:
    -h  show this help text
    -g/--grpc-version specify the grpc version to be installed (mandatory argument) 
    -p/--protobuf-version specify the protobuf version to be installed (mandatory argument)
    -v  get more verbose information during script execution
"

while true; do
  case "$1" in
    -v | --verbose )     VERBOSE=true; shift ;;
    -h | --help )        echo "$usage"; exit 0 ;;
    -g | --grpc-version )   GRPC_VERSION=$2; shift; shift;;
    -p | --protobuf-version ) PROTOBUF_VERSION=$2; shift; shift;; 
    -- ) shift; break ;;
    * ) break ;;
  esac
done

if ! [[ $GRPC_VERSION ]] || ! [[ $PROTOBUF_VERSION ]]; then
   echo "Must specify both  -g/--grpc--version and -p/--protobuf-version, see usage below"
   echo "$usage"
   exit 0
fi

if [[ $VERBOSE ]];then
    set -x
fi

# Install pkg-config first
apt-get update && apt-get install -y \
         autoconf automake libtool curl make g++ unzip git pkg-config

PROTOBUF_INSTALLED_VERSION=`pkg-config --exists protobuf && pkg-config --modversion protobuf`
GRPC_INSTALLED_VERSION=`pkg-config --exists grpc && pkg-config --modversion grpc++`


SCRIPT_DIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"



if [[ $GRPC_INSTALLED_VERSION != $GRPC_VERSION ]] ||
        [[ $PROTOBUF_INSTALLED_VERSION != $PROTOBUF_VERSION ]]; then 

    rm -rf ~/tempdir
    mkdir -p ~/tempdir/protobuf

    if [[ $PROTOBUF_INSTALLED_VERSION != $PROTOBUF_VERSION ]]; then
        #install protobuf
        cd ~/tempdir/protobuf
        curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOBUF_VERSION}/protobuf-all-${PROTOBUF_VERSION}.tar.gz && \
        tar -zxvf protobuf-all-${PROTOBUF_VERSION}.tar.gz && \
        cd protobuf-${PROTOBUF_VERSION}/ && \
        ./configure && \
        make && \
        make install &&\
        ldconfig 

    fi

    if [[ $GRPC_INSTALLED_VERSION != $GRPC_VERSION ]]; then
        #install grpc
        git clone https://github.com/grpc/grpc.git -b v${GRPC_VERSION} ~/tempdir/grpc && \
        cd ~/tempdir/grpc && \
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
