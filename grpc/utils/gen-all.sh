#!/bin/bash
./gen-c-headers.sh
cd ../python
gen-bindings.sh
cd ../cpp
gen-bindings.sh
cd ../go
gen-bindings.sh
cd ../dotnet
gen-bindings.sh
