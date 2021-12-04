#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
import pynetbox
import sys
import os

if len(sys.argv) < 2:
    print("Use: ./arista_base_config.py {hostname}")
    quit()


def host_dict(hostname):
    host_dict = {}
    host = nb.dcim.devices.get(name=hostname)
    lo0 = str(host.primary_ip)
    host_dict[hostname] = {}
    host_dict[hostname]["name"] = hostname
    host_dict[hostname]["loopback"] = lo0
    return host_dict


def vxlan_loopback(hostname):
    vxlan_ip = nb.ipam.ip_addresses.get(device=hostname, interface="lo1", family=4)
    vxlan_ip = str(vxlan_ip)
    return vxlan_ip


def intf_dict(hostname):
    intf_dict = {}
    host_intf = nb.dcim.interfaces.filter(device=hostname)
    for intf in host_intf:
        if intf.cable_peer != None:
            s_intf = str(intf)
            addr = nb.ipam.ip_addresses.get(
                device=hostname, interface=str(intf), family=4
            )
            neigh_ip = nb.ipam.ip_addresses.get(
                device=str(intf.cable_peer.device),
                interface=str(intf.cable_peer.name),
                family=4,
            )
            intf_dict[s_intf] = {}
            intf_dict[s_intf]["name"] = str(intf)
            intf_dict[s_intf]["z_host"] = str(intf.cable_peer.device)
            intf_dict[s_intf]["z_port"] = str(intf.cable_peer.name)
            intf_dict[s_intf]["z_ip"] = str(neigh_ip)
            intf_dict[s_intf]["local_ip"] = str(addr)
    return intf_dict


def bgp_dict(intf_detail):
    bgp_dict = {}
    intf_keys = intf_detail.keys()
    for intf_name in intf_keys:
        z_host = intf_detail[intf_name]["z_host"]
        host = nb.dcim.devices.get(name=z_host)
        s_host = str(host)
        host_ip = host.primary_ip
        bgp_dict[s_host] = str(host_ip)[:-3]
    return bgp_dict


def mlag_ip(hostname):
    if "leaf" in hostname:
        split_host = hostname.split("-")
        digit = int(split_host[2]) % 2
        if digit == 0:
            ip = "192.168.255.0/31"
            neigh_ip = "192.168.255.1"
        else:
            ip = "192.168.255.1/31"
            neigh_ip = "192.168.255.0"
        return ip, neigh_ip
    else:
        return 0, 1


nb_url = os.environ.get("nb_url")
nb_token = os.environ.get("nb_token")

nb = pynetbox.api(url=nb_url, token=nb_token)

hostname = sys.argv[1]
host_detail = host_dict(hostname)
intf_detail = intf_dict(hostname)
bgp_detail = bgp_dict(intf_detail)
vxlan_ip = vxlan_loopback(hostname)
mlag, mlag_neigh = mlag_ip(hostname)
# print(mlag_neigh)
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
template = env.get_template("arista_template")
output = template.render(
    intf=intf_detail,
    host=host_detail,
    bgp=bgp_detail,
    vxlan_ip=vxlan_ip,
    mlag=mlag,
    mlag_neigh=mlag_neigh,
)
print(output)
