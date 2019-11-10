#!/usr/bin/env python3

import argparse
import pexpect
import json
from Network import Network

def main(network):
    test_ping_google(network)


def test_ping_google(network):
    failed = 0
    succeed = 0
    for r in network.routers:
        router = network.routers[r]
        r_name = router.name
        print("Connecting to "+ r_name)
        child = pexpect.spawn('sudo ../connect_to.sh ' + network.topo + ' ' + r_name)

        child.sendline('ping6 2001:4860:4860::8888 -c 1')
        idx = child.expect(['0% packet loss', r'\d+% packet loss', 'connect: Network is unreachable'])
        if idx == 0:
            print(r_name + " - Ping of Google successfull")
            succeed += 1
        else:
            print(r_name + " - Ping of Google failed")
            failed += 1
        child.sendline('exit')
    ratio = (succeed / (succeed + failed)) * 100
    print("Ran ping test for", str(len(network.routers)), "routers :")
    print("Success : " , succeed)
    print("Fail : " , failed)
    print("Ratio : " , ratio , "%")

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
