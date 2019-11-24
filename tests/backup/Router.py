#!/usr/bin/env python3

import pexpect
import json

class Router():

    def __init__(self, json_config):
        self.name = json_config["name"]
        self.id = json_config["id"]
        self.namemin = json_config["namemin"]
        self.interfaces = json_config["interfaces"]
        self.lo = ""

    def set_loopback(self, addr):
       self.lo = addr

    def retrieve_neigh_addr(self):
        for interface in self.interfaces:
            yield interface["ipv6"]

    def __str__(self):
        return self.name + " - " + str(self.interfaces)

    def __repr__(self):
        return str(self)
