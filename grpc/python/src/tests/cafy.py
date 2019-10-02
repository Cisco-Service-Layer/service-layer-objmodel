import time, os, paramiko, datetime, re
import configparser
import sys
import json

# Cafy
from logger.cafylog import CafyLog
from framework.ap_base import ApBase
from topology.zap.zap import Zap
from utils.helper import Helper
from utils.cafyexception import CafyException
from topology.connection.connexceptions import DialogError
from feature_lib.ifmgr import IfMgr
from feature_lib.lldp import Lldp
from feature_lib.config import Config
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException, PatternNotFoundException
from feature_lib.gRPC import Grpc

class Cafy(ApBase):
    execMode = 'cli'
    bootConfig = os.environ.get('PWD')
    log = CafyLog(name='SL Test')

    def __init__(self):
        self.zap = Zap(test_input_file='inputfile.json', topo_file='topology.json')
        deviceName = self.zap.get_feature_configuration("uut_name")
        self.device = self.zap.get_device(deviceName)
        self.ifmgr = IfMgr(device=self.device, mode=self.execMode)
        self.lldp = Lldp(device=self.device, mode=self.execMode)
        self.grpc = Grpc(device=self.device, mode=self.execMode)
        self.verifyCli = self.zap.get_feature_configuration("verify_cli")

        self.configDevice = Config(device=self.device,
                                 mode=self.execMode,
                                 name='Config')
        self.device.connect(handle='vty', over_write_default=True)


    def setup(self):
        pass

    def parseBashCommandOutput(self, output):
        # Remove first, last, and empty lines of output
        """ Output looks like this
        ls /disk0:/ztp/

        auto_breakout  customer ...

        [ios:~]$
        """
        return [line for line in output.split("\n") if line][1:-1]

    def teardown(self):
        for x in self.device.access_info:
            if x['interface'] == 'virtual':
                fixed_address = [
                    y['address'] for y in x['address_info'] if y['name'] == 'ai'
                ]

        self.device.disconnect()
