#!/usr/bin/env python3

__author__ = 'Donatien Schmitz'
__license__ = 'MIT License'
__version__ = '1.0.1'
__maintainer__ = 'Donatien Schmitz'
__email__ = 'donatien.schmitz@student.uclouvain.be'
__status__ = 'Production'

import pexpect
import json

class Router():
    '''
        A Router

        Has an ID, name, namemin, and addresses of its interfaces
        It's the network job to fecth the router's lo address

        :param json_config: json containing the Router infos
    '''

    def __init__(self, json_config):
        self.name = json_config['name']
        self.id = json_config['id']
        self.namemin = json_config['namemin']
        self.interfaces = json_config['interfaces']
        self.lo = ''

    def set_loopback(self, addr):
       self.lo = addr

    def retrieve_neigh_addr(self):
        for interface in self.interfaces:
            yield interface['ipv6']

    def __str__(self):
        return self.name + ' - ' + str(self.interfaces)

    def __repr__(self):
        return str(self)
