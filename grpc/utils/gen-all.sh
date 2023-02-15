#!/bin/bash
./gen-c-headers.sh
cd ../python
gen-bindings.sh
# no cpp bindings generation in this branch
#cd ../cpp
#gen-bindings.sh
cd ../go
gen-bindings.sh
