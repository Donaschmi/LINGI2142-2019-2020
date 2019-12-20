#! /usr/bin/env python3
import sys
import os
import json
import csv
from mako.template import Template
from argparse import FileType, ArgumentParser

GROUP = 8
CONFIGS = 'configs.json'
TMPDIR = 'tmp/'
TEMPLATEDIR = 'template/'
MAKO_START = '_start.mako'
MAKO_BOOT = '_boot.mako'
MAKO_OSPF = '_ospf.mako'
MAKO_ZEBRA = '_zebra.mako'
MAKO_LDSO = '_ld.so.mako'
MAKO_BGPD = '_bgpd.mako'
MAKO_TOPO ='_topo.mako'
ADDR_32 = 'fde4:'+str(GROUP)+':'
ROUTER_ID = '100.251.23.'
AS = 65000 + GROUP

routers_csv = []
bgpd_csv = []
ospf_csv = []
policies_csv = []

def read_csv():
    global routers_csv
    global bgpd_csv
    global ospf_csv
    global policies_csv

    with open('routers.csv') as f:
        routers_csv = [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    #print(routers_csv)

    with open('bgpd.csv') as f:
        bgpd_csv = [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f,       skipinitialspace=True)]
    #print(bgpd_csv)

    with open('ospf.csv') as f:
        ospf_csv = [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f,       skipinitialspace=True)]

    with open('policies.csv') as f:
        policies_csv = [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f,       skipinitialspace=True)]

def json_csv_configs():
    routers = []
    for r in routers_csv:
        router = {}
        routers.append(router)
        router["id"] = r["id"]
        router["name"] = r["name"]
        router["namemin"] = router["name"].lower()
        router["router-id"] = r["router-id"]
        router["area"] = r["area"]
        router["AS"] = str(AS)
        router["next-hop"] = r["next-hop"]

        loopback = {}
        router["loopback"] = loopback
        loopback["name"] = "lo"
        loopback["ipv6"] = r["lo"]
        interfaces = []
        router["interfaces"] = interfaces
        for link in ospf_csv:
            flag = False
            addr = "addr1"
            inter = "interface1"
            other = "id2"
            if ( link["id1"] == router["id"] ):
                flag = True
            elif ( link["id2"] == router["id"] ):
                flag = True
                addr = "addr2"
                inter = "interface2"
                other = "id1"

            if (flag):
               interface = {}
               interfaces.append(interface)
               interface["interface"] = str(router["name"]+"-"+link[inter])
               interface["ipv6"] = link[addr]
               interface["virtual"] = "False"
               interface["name"] = [r["name"] for r in routers_csv if r["id"] == link[other]][0]
               interface["id"] = [r["id"] for r in routers_csv if r["id"] == link[other]][0]

        neighbors = []
        router["neighbors"] = neighbors
        for link in bgpd_csv:
            flag = False
            strid = "id1"
            other = "id2"
            if ( link["id1"] == router["id"] ):
                flag = True
            elif ( link["id2"] == router["id"] ):
                flag = True
                strid = "id2"
                other = "id1"
            #eBGP
            if (flag and link["external"] == "yes" ):
                interface = {}
                interfaces.append(interface)
                interface["interface"] = link["interface"]
                interface["ipv6"] = link["addr1"]
                interface["virtual"] = "True"
                interface["bridge"] = link["bridge"]

                neighbor = {}
                neighbors.append(neighbor)
                neighbor["external"] = "True"
                neighbor["AS"] = link["as2"]
                neighbor["ipv6"] = link["addr2"]
                neighbor["interface"] = link["interface"]
                neighbor["rr"] = "False"
                neighbor["password"] = link["password"]
                if ( strid == "id1" ):
                    neighbor["send-community"] = link["send-community1"]
                else:
                    eighbor["send-community"] = link["send-community2"]
            if link["route-map-in"] != "none":
                neighbor["route-map-in"] = link["route-map-in"]
            if link["route-map-out"] != "none":
                neighbor["route-map-out"] = link["route-map-out"]
            if link["prefix-list-in"] != "none":
                neighbor["prefix-list-in"] = link["prefix-list-in"]
            if link["prefix-list-out"] != "none":
                neighbor["prefix-list-out"] = link["prefix-list-out"]
            #iBGP
            elif ( flag and link["external"] == "no" ):
                neighbor = {}
                neighbors.append(neighbor)
                neighbor["external"] = "False"
                neighbor["AS"] = router["AS"]
                neighbor["ipv6"] = [r["lo"] for r in routers_csv if r["id"] == link[other]][0]
                if ( link["rr"] == "True" and link["id1"] == router["id"]):
                    neighbor["rr"] = "True"
                else:
                    neighbor["rr"] = "False"
                neighbor["password"] = link["password"]

        policies = []
        router["policies"] = policies
        for p in policies_csv:
            list_routers = p["routers"].replace("[","").replace("]","").split(";")
            for p_id in list_routers:
                if p_id == router["id"]:
                    #COMMUNITY
                    if p["name"] == "COMMUNITY-LIST":
                        policy = {}
                        policies.append(policy)
                        policy["type"] = p["name"]
                        policy["setting"] = p["param1"]
                        policy["name"] = p["param2"]
                        policy["value"] = p["param3"]
                    #EXPORT-FILTER
                    if p["name"] == "EXPORT-FILTER":
                        policy = {}
                        policies.append(policy)
                        policy["type"] = p["name"]
                        policy["name"] = p["param1"]
                        policy["ipv6"] = p["param2"]
                    #ROUTE-MAP
                    if p["name"] == "ROUTE-MAP":
                        policy = {}
                        policies.append(policy)
                        policy["type"] = p["name"]
                        policy["name"] = p["param1"]
                        if p["param2"] != "none":
                            policy["first"] = p["param2"]
                        if p["param3"] != "none":
                            policy["second"] = p["param3"]
                        if p["param4"] != "none":
                            policy["third"] = p["param4"]
                        if p["param5"] != "none":
                            list_policy = p["param5"].replace("[","").replace("]","").split(";")
                            policy["first_pol"] = list_policy
                        if p["param6"] != "none":
                            list_policy2 = p["param6"].replace("[","").replace("]","").split(";")
                            policy["second_pol"] = list_policy2

    #print(routers)
    with open(CONFIGS, 'w+') as f:
        json.dump(routers,f, ensure_ascii=False, indent=4)


def create_start():
    with open(CONFIGS) as f:
        data = json.load(f)
    directory = TMPDIR + "routers/"
    os.makedirs(directory, exist_ok=True)
    template_start = Template(filename=TEMPLATEDIR+MAKO_START)
    template_boot = Template(filename=TEMPLATEDIR+MAKO_BOOT)
    for conf in data:
        with open(directory + "%s_start" % conf['name'], 'w+') as f:
            f.write(template_start.render(data=conf))
        with open(directory + "%s_boot" % conf['name'], 'w+') as f:
            f.write(template_boot.render(data=conf))

def create_files():
    with open(CONFIGS) as f:
        data = json.load(f)
    template_ldso = Template(filename=TEMPLATEDIR+MAKO_LDSO)
    template_zebra = Template(filename=TEMPLATEDIR+MAKO_ZEBRA)
    template_ospf = Template(filename=TEMPLATEDIR+MAKO_OSPF)
    template_bgpd = Template(filename=TEMPLATEDIR+MAKO_BGPD)
    for conf in data:
        directory = TMPDIR+"routers/"+conf['name']+'/'
        os.makedirs(directory, exist_ok=True)
        with open(directory+'ld.so.conf', 'w+') as f:
            f.write(template_ldso.render(data=conf))
        with open(directory+conf['namemin']+'_zebra.conf', 'w+' ) as f:
            f.write(template_zebra.render(data=conf))
        with open(directory+conf['namemin']+'_ospf.conf', 'w+' ) as f:
            f.write(template_ospf.render(data=conf))
        with open(directory+conf['namemin']+'_bgpd.conf', 'w+' ) as f:
            f.write(template_bgpd.render(data=conf))

def create_topo():
    with open(CONFIGS) as f:
        conf = json.load(f)
    template_topo = Template(filename=TEMPLATEDIR+MAKO_TOPO)
    directory = TMPDIR
    os.makedirs(directory,exist_ok=True)

    with open(directory+"my_auto_conf", 'w+') as f:
        f.write(template_topo.render(data=conf))


if __name__ == "__main__":
    read_csv()
    json_csv_configs()
    create_start()
    create_files()
    create_topo()
