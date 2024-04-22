#/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#

cd ../gen-docs/html/
find *.html -type f -exec sed -i 's/struct /message /g;s/Struct /Message /g;s/Class Documentation/Message Documentation/g;s/Public Attributes/Attributes/;s/union /oneof /g' {} \;
