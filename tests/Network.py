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
