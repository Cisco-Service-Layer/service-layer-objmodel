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

class LoggerStub:
    '''
    This simply a logger stub to replace CafyLogger outside of Cafy env
    '''
    def __init__(*args, **kwargs):
        pass

    debug = print
    info = print
    error = print

if __name__ == '__main__':
    server_ip, server_port = get_server_ip_port()
    print("Using GRPC Server IP(%s) Port(%s)" %(server_ip, server_port))
    
