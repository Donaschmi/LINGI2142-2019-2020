#!/usr/bin/env python3

import argparse
import pexpect
import json
from Network import Network

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main(network):
    print("Network created, beginning tests.")

    print("Beginning OSPF test")
    ospf_test = test_ospf(network)
    print("OSPF test completed \n")
    if ospf_test:
        print(bcolors.OKGREEN + "OSPF test succeed" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "OSPF test failed" + bcolors.ENDC)

    print("Beginning eBGP test")
    ebgp_test = test_ping_google(network)
    print("eBGP test completed \n")
    if ebgp_test:
        print(bcolors.OKGREEN + "eBGP test succeed" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "eBGP test failed" + bcolors.ENDC)

    print("End of tests")
    if not ebgp_test or not ospf_test:
        print(bcolors.FAIL + "At least one test failed : Network not operationnal" + bcolors.ENDC)
    else:
        print(bcolors.OKGREEN + "All tests passed : Network operationnal" + bcolors.ENDC)

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

    return failed == 0

def test_ospf(network):
    failed = 0
    succeed = 0
    for r in network.routers:
        router = network.routers[r]
        r_name = router.name
        print("Connecting to "+ r_name)
        child = pexpect.spawn('sudo ../connect_to.sh ' + network.topo + ' ' + r_name)
        child.expect("bash-4.3#")
        for n in network.routers:
            neigh = network.routers[n]
            if r_name == neigh.name:
                continue
            child.sendline('ping6 ' + neigh.lo + ' -c 1')
            idx = child.expect(['0% packet loss', r'\d+% packet loss', 'connect: Network is unreachable'], timeout=5)
            if idx == 0:
                print(r_name + " - Success pinging " + neigh.name)
                succeed += 1
            else:
                print(r_name + " - Fail pinging " + neigh.name)
                failed += 1
    ratio = (succeed / (succeed + failed)) * 100
    print("Ran ping test for", str(len(network.routers)), "routers :")
    print("Success : " , succeed)
    print("Fail : " , failed)
    print("Ratio : " , ratio , "%")

    return failed == 0

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
