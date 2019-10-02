#
# Copyright (c) 2016 by cisco Systems, Inc. 
# All rights reserved.
#

# Standard python libs
import os
import ipaddress

#
# Get the GRPC Server IP address and port number
#
def get_server_ip_port():
    # Get GRPC Server's IP from the environment
    if 'SERVER_IP' not in list(os.environ.keys()):
        print("Need to set the SERVER_IP env variable e.g.")
        print("export SERVER_IP='10.30.110.214'")
        os._exit(0)
    
    # Get GRPC Server's Port from the environment
    if 'SERVER_PORT' not in list(os.environ.keys()):
        print("Need to set the SERVER_PORT env variable e.g.")
        print("export SERVER_PORT='57777'")
        os._exit(0)

    return (os.environ['SERVER_IP'], int(os.environ['SERVER_PORT']))

#
# Increment a v4 or v6 prefix
#
def sl_util_inc_prefix(prefix, prefix_len, num=1, af=4):
    if af == 4:
        prefix_max_len = 32
    else:
        prefix_max_len = 128
    
    if prefix_len > prefix_max_len:
        print("prefix_len %d > max %d" %(prefix_len, prefix_max_len))
        os._exit(0)
    
    val = 1<<(prefix_max_len - prefix_len)
    
    return val + prefix

if __name__ == '__main__':
    prefix_len = 24
    prefix4 = int(ipaddress.ip_address("10.0.0.0"))
    prefix6 = int(ipaddress.ip_address("10::"))
    for i in range(4):
        prefix4 = sl_util_inc_prefix(prefix4, prefix_len, 1, 4)
        print("Prefix %s" %(str(ipaddress.ip_address(prefix4))))
        prefix6 = sl_util_inc_prefix(prefix6, prefix_len, 1, 6)
        print("Prefix %s" %(str(ipaddress.ip_address(prefix6))))
    
    server_ip, server_port = get_server_ip_port()
    print("Using GRPC Server IP(%s) Port(%s)" %(server_ip, server_port))
    
