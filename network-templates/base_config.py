from jinja2 import Environment, FileSystemLoader
import pynetbox
import sys

if len(sys.argv) <= 1:
    print('Use: /base_config.py hostname')
    quit()

def host_dict(hostname):
    host_dict = {}
    host = nb.dcim.devices.get(name=hostname)
    lo0 = str(host.primary_ip)

    host_dict[hostname] ={}
    host_dict[hostname]['name'] = hostname
    host_dict[hostname]['loopback'] = lo0
    return(host_dict)

def vxlan_loopback(hostname):
    vxlan_ip = nb.ipam.ip_addresses.get(device=hostname,interface='lo1',family=4)
    vxlan_ip = str(vxlan_ip)
    return(vxlan_ip)

def intf_dict(hostname):
    intf_dict = {}
    host_intf = nb.dcim.interfaces.filter(device=hostname)
    for intf in host_intf:
        if intf.cable_peer != None:
            s_intf = str(intf)
            addr = nb.ipam.ip_addresses.get(device=hostname, interface=str(intf), family=4)
            intf_dict[s_intf] = {}
            intf_dict[s_intf]['name'] = str(intf)
            intf_dict[s_intf]['z_host'] = str(intf.cable_peer.device)
            intf_dict[s_intf]['z_port'] = str(intf.cable_peer.name)
            intf_dict[s_intf]['local_ip'] = str(addr)
    return(intf_dict)

def bgp_dict(intf_detail):
    bgp_dict = {}
    intf_keys = intf_detail.keys()
    for intf_name in intf_keys:
        z_host = intf_detail[intf_name]['z_host']
        host = nb.dcim.devices.get(name=z_host)
        s_host = str(host)
        host_ip = host.primary_ip
        bgp_dict[s_host] = str(host_ip)[:-3]
    return(bgp_dict)

nb = pynetbox.api(url='http://100.64.1.226:8000',
                  token='a11c6850a273edcdaccbab6d71f9fc0c2786e900')

hostname = sys.argv[1]
host_detail = host_dict(hostname)
intf_detail = intf_dict(hostname)
bgp_detail = bgp_dict(intf_detail)
vxlan_ip = vxlan_loopback(hostname)
#print(bgp_detail)
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('arista_template')
output = template.render(intf=intf_detail, host=host_detail, bgp=bgp_detail,
                         vxlan_ip=vxlan_ip)
print(output)