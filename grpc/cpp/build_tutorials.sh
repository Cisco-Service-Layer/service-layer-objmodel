#!/bin/bash


usage="
$(basename "$0") [-h] [-g/--grpc-version -p/--protobuf-version -v/--verbose] -- script to install desired versions of grpc, protobuf and build the libiosxrsl.a library 
where:
    -h  show this help text
    -g/--grpc-version  bring up the libvirt topology, wait for ssh access and then set up ssh tunnels
    -p/--protobuf-version  bring down the libvirt topology
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



SCRIPT_DIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

./build_libiosxrsl.sh -g $GRPC_VERSION -p $PROTOBUF_VERSION

mkdir -p ~/tempdir

# Install glog

if ! ldconfig -p | grep -q glog; then
    git clone https://github.com/google/glog.git ~/tempdir/glog
    cd ~/tempdir/glog
    ./autogen.sh && ./configure && make && make install && ldconfig
fi
# Clean up
cd ~/ && rm -rf ~/tempdir

# Clean up first
$SCRIPT_DIR/clean.sh

# Drop into the tutorial directory to build quickstart that links to libiosxrsl.a
cd $SCRIPT_DIR/src/tutorial
make

cd $SCRIPT_DIR/src/tutorial/rshuttle
make

