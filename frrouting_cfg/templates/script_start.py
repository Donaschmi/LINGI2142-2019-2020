#! /usr/bin/env python3

import sys
import json
from mako.template import Template
from argparse import FileType, ArgumentParser


def main(args):
    nb_router = 5

    routers = []

    for i in range(1, nb_router+1):
        router = {}
        routers.append(router)
        router["id"] = i
        router["name"] = 'P'+str(i)
        interfaces = []
        router["interfaces"] = interfaces
        for j in range(nb_router):
            interface = {}
            interfaces.append(interface)
            interface["name"] = "eth"+str(j)
            interface["ipv6"] = "fde4:8:"+str(i)+str(j)+"::"+str(i)+str(i)+"/64"

    routers_json = json.dumps(routers)
    print(routers_json)

    for index in range(len(routers)):
        data = routers[index]
        template = Template(filename=args.template)
        with open(router['name']+"_start", 'w') as f:
            f.write(template.render(data))







'''
    data = json.load(args.input)
    template = Template(filename=args.template)
    if not args.multiple:
        args.output.write(template.render(data=data))
    else:
        if not args.output:
            args.output.close()
        for conf in data:
            with open("%s.conf" % conf['name'], 'w') as f:
                f.write(template.render(data=conf))
'''

if __name__ == '__main__':
    parser = ArgumentParser(description="Simple script that will generate a configuration file "
                                        "according to the template and the JSON file given at arguments")
    parser.add_argument('-i', '--input', type=FileType('r'), default=sys.stdin,
                        help='JSON formatted file path containing data for the template')
    parser.add_argument('-t', '--template', type=str, required=True, help='Path to the Mako based template')
    parser.add_argument('-o', '--output', type=FileType('w'), default=sys.stdout,
                        help='File path where to write the final file. Variables of the JSON file will be applied to '
                             'the template given with the "-t" argument')
    parser.add_argument('-m', '--multiple', action='store_true', required=False,
                        help="If set, the JSON is a list of file to generate. "
                             "If not set, it is a configuration for a single file.")

    main(parser.parse_args())
