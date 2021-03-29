import os
import json


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


class ApData:
    '''
    One time initialization of testbed and paramters
    '''
    host, port = get_server_ip_port()

    filepath = os.path.join(os.path.dirname(__file__), 'template.json')
    with open(filepath) as fp:
        json_params = json.loads(fp.read())

    logger = LoggerStub
    sim_clean = None
    vxr = None

