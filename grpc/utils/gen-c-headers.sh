#!/bin/bash
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#

HEADER_FILE=genc/sl_api_err.h
TEST_FILE=test.c
TEST_BIN=test

#
# Header file
#
printf "Generating $HEADER_FILE..."
echo "/*
 *------------------------------------------------------------------
 * This file is AUTO-GENERATED. DO NOT EDIT.
 *
 * Copyright (c) 2016-2019,2025 by cisco Systems, Inc.
 * All rights reserved.
 *------------------------------------------------------------------
 */

#ifndef __SL_API_ERR_H__
#define __SL_API_ERR_H__
" > $HEADER_FILE

# Create a C header file from the error codes
awk '/enum SLErrno {/,/}/' ../protos/sl_common_types.proto |
    # Replace enum with a macro '#define SL_GENERATED_ERR_CODES'
    sed "s/enum SLErrno {/#define SL_GENERATED_ERR_CODES /g" |
    # Replace C++ comments with C comments (C++ comments dont work in Macros)
    sed "s#//\(.*\)#/*\1 */#" |
    # Remove empty lines
    sed "/^\s*$/d" |
    # De-indent by 4
    cut -c 5- |
    # Replace ';' with ','
    sed "s/;/,/g" |
    # Terminate lines with a \
    sed "s/.*/&\\\/g" |
    # Replace enum terminating bracket and trailing \ with a comment
    sed "s/}\\\/    \/*End of Generated error codes*\//g" >> $HEADER_FILE

# some spaces
echo "" >> $HEADER_FILE
echo "" >> $HEADER_FILE
echo "" >> $HEADER_FILE

echo "#define SL_GENERATED_ERR_STRINGS \\" >> $HEADER_FILE
# Add an array of {codes, <text_string>} pairs
awk '/enum SLErrno {/,/}/' ../protos/sl_common_types.proto |
    # Remove enum
    sed "s/enum SLErrno {/ /g" |
    # Remove closing bracket
    sed "s#}##g" |
    # Remove empty lines
    sed "/^\s*$/d" |
    # Remove "!!!" lines to be able to build strings
    grep -v "!!!" |
    # Pick up "=;" and remove the =0x
    sed "s#=\(.*\)#;#g" |
    # Pick up "// .* ;" patterns and re-arrange the line
    awk -v RS=';' -v FS='SL_' '{print "    {" "SL_"$2 "," $1 "},"}' |
    # Pick up "0x" and remove
    sed "s#0x\(.*\)##g" |
    # Replace lines starting with // with ""
    sed 's#//\(.*\)#"\1 "#' |
    # Replace any empty matches
    sed -e '/{SL_,/,/},/c\ ' |
    # Terminate lines with a \
    sed "s/.*/&\\\/g" >> $HEADER_FILE
echo "    /*End of Generated Error strings*/" >> $HEADER_FILE 

echo "
#endif
" >> $HEADER_FILE
echo "Done"





#
# Test .c file
#
printf "Generating $TEST_FILE..."
echo "/*
 *------------------------------------------------------------------
 * This file is AUTO-GENERATED. DO NOT EDIT.
 *
 * Copyright (c) 2016 by cisco Systems, Inc.
 * All rights reserved.
 *------------------------------------------------------------------
 */

#include <stdio.h>
#include \"$HEADER_FILE\"

enum SLError {
    SL_GENERATED_ERR_CODES
    
    SL_EINIT                               = SL_INTERNAL_START_OFFSET + 0x1,
};


typedef struct errcode2str_t {
    enum SLError errcode;
    const char *str;
} errcode2str_t;

static 
errcode2str_t errcode2str[] = {
    SL_GENERATED_ERR_STRINGS
    
    {SL_EINIT, \"Error Init\"},
};

int main(int argc, const char* argv[]) {
    int i;
    printf (\"Value of 'SL_OP_SOME_ERR' is 0x%x\n\", SL_SOME_ERR);
    
    for (i=0;i<sizeof(errcode2str)/sizeof(errcode2str_t);i++) {
        printf(\"0x%x\t\t%s\n\", errcode2str[i].errcode, errcode2str[i].str);
    }
    return (0);
}" > $TEST_FILE
echo "Done"

#
# Make sure it compiles
#
echo "Compiling/Running $TEST_BIN:"
rm -f $TEST_BIN
gcc $TEST_FILE -o $TEST_BIN
if [ -f $TEST_BIN ]; then
    ./$TEST_BIN
fi

#
# Cleanup
#
printf "Cleaning up test files..."
rm -f $TEST_BIN $TEST_FILE
echo "Done"
