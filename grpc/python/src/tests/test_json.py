#!/usr/bin/env python
#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#

import json

#
# Interpret the specified 'filename' .json file
# Returns a dictionary of all .json objects
#
def sl_json_paths_load_file(filename):
    data = None
    with open(filename) as data_file:
        data = json.loads(data_file.read())
    return data

#
# Given a dictionary of objects, save them in .json format
#
def sl_json_paths_save_file(filename, json_dict):
    with open(filename, 'w') as data_file:
        json.dump(json_dict, data_file, indent=4, sort_keys=True)

# Basic tests
if __name__ == '__main__':
    inputfile =  "template.json"
    outputfile = "out.json"
    # Load file
    test = sl_json_paths_load_file(inputfile)
    #
    # Basic usage examples and test cases
    #
    nh_dict = test["nexthops"]
    path_dict = test["path_route_all_attrs"]
    #
    print (nh_dict[path_dict["paths"][0]["nexthop"]]["v4_addr"])
    print (path_dict["paths"][0]["labels"][1])
    # Length of paths
    print (len(path_dict["paths"]))
    print ("v4 batch len: %d" %(len(test["batch_v4_route"]["routes"])))
    #
    # Diff input and output - useful when editing the .json input file
    sl_json_paths_save_file(outputfile, test)
    print("Please diff %s %s" %(inputfile, outputfile))
    print("Replace %s with %s if necessary" %(outputfile, inputfile))
