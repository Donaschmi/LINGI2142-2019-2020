#!/usr/bin/env python3

__author__ = 'Donatien Schmitz'
__license__ = 'MIT License'
__version__ = '1.0.1'
__maintainer__ = 'Donatien Schmitz'
__email__ = 'donatien.schmitz@student.uclouvain.be'
__status__ = 'Production'

import argparse
import pexpect
import json
from Network import Network
from utils import *

def main(network):
    print('Network created, beginning tests.')

    print('Beginning OSPF test')
    ospf_test = test_ospf(network)
    print('OSPF test completed \n')
    if ospf_test:
        print(bcolors.OKGREEN + 'OSPF test succeed' + bcolors.ENDC)
    else:
        print(bcolors.FAIL + 'OSPF test failed' + bcolors.ENDC)

    print('Beginning eBGP test')
    ebgp_test = test_ping_google(network)
    print('eBGP test completed \n')
    if ebgp_test:
        print(bcolors.OKGREEN + 'eBGP test succeed' + bcolors.ENDC)
    else:
        print(bcolors.FAIL + 'eBGP test failed' + bcolors.ENDC)

    print('Beginning BGP neighbours test (should be neighbour with 65004 65009 65010)')
    neigh_test = test_bgp_neigh(network)
    print('BGP neighborhood test completed \n')
    if neigh_test:
        print(bcolors.OKGREEN + 'BGP neighborhood test succeed' + bcolors.ENDC)
    else:
        print(bcolors.FAIL + 'BGP neighborhood test failed' + bcolors.ENDC)

    print('End of tests')
    if not ebgp_test or not ospf_test or not neigh_test:
        print(bcolors.FAIL + 'At least one test failed : Network not operationnal' + bcolors.ENDC)
    else:
        print(bcolors.OKGREEN + 'All tests passed : Network operationnal' + bcolors.ENDC)

def test_ping_google(network):
    '''
        Test the reaching of outstide world of the network

        Connects to each router and try to ping google DNS
        The network has been initialised before

        :param network: a Network instance
        :return: The number of failed test
        :rtype: int
    '''
    failed = 0
    succeed = 0
    for r in network.routers:
        router = network.routers[r]
        r_name = router.name
        print('Connecting to '+ r_name)
        child = pexpect.spawn('sudo ../connect_to.sh ' + network.topo + ' ' + r_name)

        child.sendline('ping6 2001:4860:4860::8888 -c 1')
        idx = child.expect(['0% packet loss', r'\d+% packet loss', 'connect: Network is unreachable'])
        if idx == 0:
            print(r_name + ' - Ping of Google successfull')
            succeed += 1
        else:
            print(r_name + ' - Ping of Google failed')
            failed += 1
        child.sendline('exit')
    print_results(succeed, failed, str(len(network.routers)))
    return failed == 0

def test_ospf(network):
    '''
        Test the reaching of routers inside the network

        Connects to each router and try to reach every other routers
        by pinging their loopback address.

        :param network: a Network instance
        :return: The number of failed test
        :rtype: int
    '''
    failed = 0
    succeed = 0
    for r in network.routers:
        router = network.routers[r]
        r_name = router.name
        print('Connecting to '+ r_name)
        child = pexpect.spawn('sudo ../connect_to.sh ' + network.topo + ' ' + r_name)
        child.expect('bash-4.3#')
        for n in network.routers:
            neigh = network.routers[n]
            if r_name == neigh.name:
                continue
            child.sendline('ping6 ' + neigh.lo + ' -c 1')
            idx = child.expect(['0% packet loss', r'\d+% packet loss', 'connect: Network is unreachable'], timeout=5)
            if idx == 0:
                print(r_name + ' - Success pinging ' + neigh.name)
                succeed += 1
            else:
                print(r_name + ' - Fail pinging ' + neigh.name)
                failed += 1
    print_results(succeed, failed, str(len(network.routers)))
    return failed == 0

def test_bgp_neigh(network):
    '''
        Test the reaching of other AS by the network

        Connects to each router and then launch a vtysh instance.
        Then show the json version of the bgp infos and fetch the connected AS
        Fails if an AS it is not supposed to be connected is
        Fails if not connected to an AS it is supposed to

        :param network: a Network instance
        :return: The number of failed test
        :rtype: int
    '''
    failed = 0
    succeed = 0
    addr = 'fde4:'
    prefix = '::/32'
    for r in network.routers:
        router = network.routers[r]
        r_name = router.name
        print('Connecting to '+ r_name)
        child = pexpect.spawn('sudo ../connect_to.sh ' + network.topo + ' ' + r_name)
        child.expect('bash-4.3#')
        child.sendline('LD_LIBRARY_PATH=/usr/local/lib vtysh')
        child.expect('group8#')
        child.sendline('show bgp json')
        child.expect('group8#')
        # Retieve output
        output = child.before.decode('utf-8')
        # Don't need the ssh connections so close them
        child.sendline('exit')
        child.expect('bash-4.3#')
        child.sendline('exit')
        # Remove junks
        if 'bgpd is not running' in output:
            failed += 1
            continue
        output = trim_from_start(output, '{')
        routes = json.loads(output)['routes']
        # Should have eBGP connections with AS9, AS10 and
        for i in range(10):
            if i == 8:
                continue
            full_addr = addr + str(i) + prefix
            if full_addr in route:
                succeed += 1
            else:
                failed += 1

    print_results(succeed, failed, str(len(network.routers)))
    return failed == 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='path to the json config file')
    parser.add_argument('-t', help='path to the topo folder')
    args = parser.parse_args()
    if not args.c:
        print('No config file specified')
        exit(1)
    if not args.t:
        print('No topo folder specified')
        exit(1)
    network = Network(args.c, args.t)
    main(network)
    exit(1)
