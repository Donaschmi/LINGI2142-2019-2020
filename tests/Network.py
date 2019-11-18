#!/usr/bin/env python3

__author__ = "Donatien Schmitz"
__license__ = "MIT License"
__version__ = "1.0.1"
__maintainer__ = "Donatien Schmitz"
__email__ = "donatien.schmitz@student.uclouvain.be"
__status__ = "Production"

import pexpect
import json
from Router import Router

class Network():
    """
        The Network containing each routers

        From the json config file, retrieve informations about the routers and create a
        topology of the network

        :param config_file: json file containing routers infos
        :param topo_folder: folder where the routers folder will be created
    """
    def __init__(self, config_file, topo_folder):
        self.routers = {}
        self.config = config_file
        self.topo = topo_folder
        self.build_routers()

    def build_routers(self):
        with open(self.config) as config:
            topo = json.load(config)
            for router in topo:
                r = Router(router)
                self.routers[r.id] = r
                r_name = r.name
                child = pexpect.spawn('sudo ../connect_to.sh ' + self.topo + ' ' + r_name)
                child.expect("bash-4.3#")
                child.sendline('ifconfig lo')
                child.expect("bash-4.3#")
                output = child.before.decode("utf-8")
                child.sendline('exit')
                # Split the result to filter the loopback address
                splited = output.split()
                for s in splited:
                    if "fde4:8" in s:
                        r.set_loopback(s.replace('/128', ''))
                        break
