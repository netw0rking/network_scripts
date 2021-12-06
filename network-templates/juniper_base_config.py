#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
import pynetbox
import sys
import os


if len(sys.argv) < 2:
    print("Use: ./juniper_base_config.py hostname")
    quit()

def get_interfaces_ip(hostname):
    host_intfs = nb.dcim.interfaces.filter(device=hostname)
    intf_addrs = {}
    for intf in host_intfs:
        if intf.connected_endpoint and intf.count_ipaddresses:
            ip = nb.ipam.ip_addresses.get(device=hostname,interface=intf.name,family=4)
            intf_addrs[intf]=ip.address
        elif 'lo0' in intf.name:
            ip = nb.ipam.ip_addresses.get(device=hostname,interface=intf.name,family=4)
            intf_addrs[intf]=ip.address
    return intf_addrs
 

nb_url = os.environ.get("nb_url")
nb_token = os.environ.get("nb_token")
nb = pynetbox.api(url=nb_url, token=nb_token)

hostname = sys.argv[1]
int_ip = get_interfaces_ip(hostname)
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
template = env.get_template("junos_template")
output = template.render(intf=int_ip,hostname=hostname)
print(output)
