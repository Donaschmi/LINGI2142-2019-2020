#! /usr/bin/env python3
import sys
import os
import json
from mako.template import Template
from argparse import FileType, ArgumentParser

CONFIGS = 'configs.json'
TMPDIR = 'tmp/'
MAKO_START = '_start.mako'
MAKO_BOOT = '_boot.mako'
MAKO_OSPF = '_ospf.mako'
MAKO_ZEBRA = '_zebra.mako'
MAKO_LDSO = '_ld.so.mako'

def json_configs():
    nb_router = 3
    routers = []
    for i in range(1, nb_router+1):
        router = {}
        routers.append(router)
        router["id"] = i
        router["name"] = 'P'+str(i)
        router["namemin"] = 'p'+str(i)
        interfaces = []
        router["interfaces"] = interfaces
        for j in range(nb_router):
            interface = {}
            interfaces.append(interface)
            interface["name"] = "eth"+str(j)
            interface["ipv6"] = "fde4:8:"+str(i)+str(j)+"::"+str(i)+str(i)+"/64"
        interface = {}
        interfaces.append(interface)
        interface["name"] = "lo"
        interface["ipv6"] = "fde4:8::"+str(i)+str(i)+"/128"

    with open(CONFIGS, 'w+') as f:
        json.dump(routers,f, ensure_ascii=False, indent=4)


def create_start():
    with open(CONFIGS) as f:
        data = json.load(f)
    os.makedirs(TMPDIR, exist_ok=True)
    template_start = Template(filename=MAKO_START)
    template_boot = Template(filename=MAKO_BOOT)
    for conf in data:
        with open(TMPDIR + "%s_start" % conf['name'], 'w+') as f:
            f.write(template_start.render(data=conf))
        with open(TMPDIR + "%s_boot" % conf['name'], 'w+') as f:
            f.write(template_boot.render(data=conf))

def create_files():
    with open(CONFIGS) as f:
        data = json.load(f)
    template_ldso = Template(filename=MAKO_LDSO)
    template_zebra = Template(filename=MAKO_ZEBRA)
    #template_ospf = Template(filename=MAKO_OSPF)
    for conf in data:
        directory = TMPDIR+conf['name']+'/'
        os.makedirs(directory, exist_ok=True)
        with open(directory+conf['namemin']+'_ld.so.conf', 'w+') as f:
            f.write(template_ldso.render(data=conf))
        with open(directory+conf['namemin']+'_zebra.conf', 'w+' ) as f:
            f.write(template_zebra.render(data=conf))
        #with open(directory+conf['namemin']+'_ospf.conf', 'w+' ) as f:
        #    f.write(template_ospf.render(data=conf))

if __name__ == "__main__":
    json_configs()
    create_start()
    create_files()
