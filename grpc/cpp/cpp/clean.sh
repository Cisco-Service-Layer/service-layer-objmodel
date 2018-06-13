#!/bin/bash

set -x
SCRIPT_DIR="$(cd "$(dirname "${0}")"; echo "$(pwd)")"

cd $SCRIPT_DIR/src && make clean
cd $SCRIPT_DIR/src/tutorial && make clean
cd $SCRIPT_DIR/src/tutorial/rshuttle && make clean
