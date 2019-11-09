#!/usr/bin/env python3

import argparse
import pexpect
import json
from Network import Network

def main(network):
    test_ping_google(network)


def test_ping_google(network):
    for r in network.routers:
        router = network.routers[r]
        r_name = router.name
        print("Connecting to "+ r_name)
        child = pexpect.spawn('sudo ../connect_to.sh ' + network.topo + ' ' + r_name)

        child.sendline('ping6 2001:4860:4860::8888 -c 1')
        idx = child.expect(['0% packet loss', r'\d+% packet loss'])
        if idx == 0:
            print(r_name + " - Ping of Google successfull")
        else:
            print(r_name + " - Ping of Google failed")
        child.sendline('exit')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="path to the json config file")
    parser.add_argument("-t", help="path to the topo folder")
    args = parser.parse_args()
    if not args.c:
        print("No config file specified")
        exit(1)
    if not args.t:
        print("No topo folder specified")
        exit(1)
    network = Network(args.c, args.t)
    main(network)
    exit(1)
