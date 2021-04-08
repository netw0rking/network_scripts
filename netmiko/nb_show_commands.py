from netmiko import ConnectHandler
import pynetbox
import sys
from pprint import pprint

def netmiko_connect(host):
    net_conn = ConnectHandler(device_type='cisco_ios', host=host, username='wquizhpi', password='cisco') 
    return net_conn

def active_int(host):
    new_int_list = []
    host_int = nb.dcim.interfaces.filter(device=host)
    for intf in host_int:
        if intf.connected_endpoint_reachable == True:
            new_int_list.append(intf)
    return new_int_list

nb = pynetbox.api(url='http://100.64.1.226:8000', token='a11c6850a273edcdaccbab6d71f9fc0c2786e900')
host = sys.argv[1]

intf_list = active_int(host)

port_dict = {}
for i in range(len(intf_list)):
    group = intf_list[i].name
    port_dict[group] = {}
    port_dict[group]['a-host'] = host
    port_dict[group]['a-port'] = intf_list[i].name
    port_dict[group]['z-host'] = intf_list[i].cable_peer.device.display_name
    port_dict[group]['z-port'] = intf_list[i].cable_peer.name

cmd_list = []
for ports in port_dict.keys():
    cmd = 'show interface ' + ports 
    cmd_list.append(cmd)

for command in cmd_list:
    net_conn = netmiko_connect(host)
    output = net_conn.send_command(command,use_textfsm=True)
    pprint(output)
    net_conn.disconnect()
