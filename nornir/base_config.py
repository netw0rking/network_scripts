from jinja2 import Environment, FileSystemLoader
import pynetbox
import sys

if len(sys.argv) <= 1:
    print('Use: /base_config.py hostname')

def host_dict(hostname):
    host_dict = {}
    host = nb.dcim.devices.get(name=hostname)
    lo0 = str(host.primary_ip)
    host_dict[hostname] ={}
    host_dict[hostname]['name'] = hostname
    host_dict[hostname]['loopback'] = lo0
    return(host_dict)

def intf_dict(hostname):
    intf_dict = {}
    host_intf = nb.dcim.interfaces.filter(device=hostname)
    for intf in host_intf:
        if intf.cable_peer != None:
            addr = nb.ipam.ip_addresses.get(device=hostname, interface=str(intf), family=4)
            intf_dict[intf] = {}
            intf_dict[intf]['name'] = str(intf)
            intf_dict[intf]['z_host'] = str(intf.cable_peer.device)
            intf_dict[intf]['z_port'] = str(intf.cable_peer.name)
            intf_dict[intf]['local_ip'] = str(addr)
    return(intf_dict)

nb = pynetbox.api(url='http://100.64.1.226:8000',
                  token='a11c6850a273edcdaccbab6d71f9fc0c2786e900')

hostname = sys.argv[1]
host_detail = host_dict(hostname)
intf_detail = intf_dict(hostname)

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('nexus_template')
output = template.render(intf=intf_detail,host=host_detail)
print(output)
