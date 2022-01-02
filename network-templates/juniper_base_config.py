#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
import pynetbox
import sys
import os


if len(sys.argv) < 2:
    print("Use: ./juniper_base_config.py hostname")
    quit()


def get_interface_description(hostname):
    intf_desc = {}
    intfs = nb.dcim.interfaces.filter(device=hostname)
    for interface in intfs:
        if interface.connected_endpoint:
            intf_desc[interface] = interface.connected_endpoint["device"][
                "display_name"
            ]
    return intf_desc


def get_interfaces_ip(hostname):
    intf_addrs = {}
    host_intfs = nb.dcim.interfaces.filter(device=hostname)
    for intf in host_intfs:
        if intf.connected_endpoint and intf.count_ipaddresses:
            ip = nb.ipam.ip_addresses.get(
                device=hostname, interface=intf.name, family=4
            )
            intf_addrs[intf] = ip.address
        elif "lo0" in intf.name:
            ip = nb.ipam.ip_addresses.get(
                device=hostname, interface=intf.name, family=4
            )
            intf_addrs[intf] = ip.address
    return intf_addrs


def create_iso(hostname):
    ip = nb.ipam.ip_addresses.get(device=hostname, interface="lo0", family=4)
    if ip.address:
        no_dot = ip.address[:-3].replace(".", "")
        if len(no_dot) < 12:
            fill_in = 12 - len(no_dot)
            new_ip = ("0" * fill_in) + no_dot
        else:
            new_ip = no_dot

        iso_list = [new_ip[i : i + 4] for i in range(0, len(new_ip), 4)]
        sys_id = ".".join(iso_list)
        iso_address = f"49.0002.{sys_id}.00"
        return iso_address


nb_url = os.environ.get("nb_url")
nb_token = os.environ.get("nb_token")
nb = pynetbox.api(url=nb_url, token=nb_token)

hostname = sys.argv[1]
int_ip = get_interfaces_ip(hostname)
iso = create_iso(hostname)
username = os.environ.get("USER")
intf_desc = get_interface_description(hostname)
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
template = env.get_template("junos_template")
output = template.render(
    intf=int_ip, hostname=hostname, iso=iso, intf_desc=intf_desc, user=username
)
print(output)
