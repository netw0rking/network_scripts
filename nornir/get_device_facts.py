#!/usr/bin/env python3
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description='Use arguments to filter by site, host, role')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-site', type=str, help='Filter by site')
group.add_argument('-host', type=str, help='Filter by host')
args = parser.parse_args()

nr = InitNornir(config_file='./config.yml', dry_run=True)

if args.site:
    device = nr.filter(site=args.site)
elif args.host:
    device = nr.filter(host=args.host)


sw_output = device.run(task=napalm_get, getters=['facts'])
#import pdb; pdb.set_trace()

for switch in sw_output:
    pprint(sw_output[switch][0].result)

