#/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#
cp tab_h_2.png ../gen-docs/html/tab_h_2.png
cp search_m.png ../gen-docs/html/search_m.png
cp tab_a_3.png ../gen-docs/html/tab_a_3.png
cp tab_s_2.png ../gen-docs/html/tab_s_2.png

cd ../gen-docs/html/
find *.html -type f -exec sed -i 's/struct /message /g;s/Struct /Message /g;s/Class Documentation/Message Documentation/g;s/Public Attributes/Attributes/' {} \;


sed -i.bak -e "82,305d" index.html

