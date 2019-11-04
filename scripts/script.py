#! /usr/bin/env python3
import sys
import json
from mako.template import Template
from argparse import FileType, ArgumentParser

def json_start():
    nb_router = 11
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
    with open("_start.json", 'w+') as f:
        json.dump(routers,f, ensure_ascii=False, indent=4)


def create_start(jsonrouters,makostart, makoboot):
    with open(jsonrouters) as f:
        data = json.load(f)
    template_start = Template(filename=makostart)
    template_boot = Template(filename=makoboot)
    for conf in data:
        with open("tmp/%s_start" % conf['name'], 'w+') as f:
            f.write(template_start.render(data=conf))
        with open("tmp/%s_boot" % conf['name'], 'w+') as f:
            f.write(template_boot.render(data=conf))

if __name__ == "__main__":
    json_start()
    create_start('_start.json','_start.mako', '_boot.mako')
