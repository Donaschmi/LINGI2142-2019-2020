#!/usr/bin/env python3

import pexpect
import json
from Router import Router

class Network():

    def __init__(self, config_file, topo_folder):
        self.routers = {}
        self.topo = topo_folder
        with open(config_file) as config:
            topo = json.load(config)
            for router in topo:
                r = Router(router)
                self.routers[r.id] = r

