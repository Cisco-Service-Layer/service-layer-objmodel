#!/bin/bash

# install grpc and protobuf
# grpc version = 0.13.1
# protobuf version = 3.5.0

set -x

SCRIPT_DIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

./build_libiosxrsl.sh

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

