from ntc_templates.parse import parse_output
from netmiko import ConnectHandler
from pprint import pprint
import pynetbox
import sys
import os

def netmiko_connect(host,username):
    net_conn = ConnectHandler(device_type='juniper', host=host, username=username, password='Juniper') 
    return net_conn

def active_int(host):
    new_int_list = []
    host_int = nb.dcim.interfaces.filter(device=host)
    for intf in host_int:
        if intf.connected_endpoint_reachable == True:
            new_int_list.append(intf)
    return new_int_list

def port_details(intf_list):
    port_dict = {}
    for i in range(len(intf_list)):
        group = intf_list[i].name
        port_dict[group] = {}
        port_dict[group]['a-host'] = host
        port_dict[group]['a-port'] = intf_list[i].name
        port_dict[group]['z-host'] = intf_list[i].cable_peer.device.display_name
        port_dict[group]['z-port'] = intf_list[i].cable_peer.name
    return port_dict

nb = pynetbox.api(url='http://100.64.1.226:8000', token='a11c6850a273edcdaccbab6d71f9fc0c2786e900')
host = sys.argv[1]
username = os.getenv('USER')

intf_list = active_int(host)

port_dict = port_details(intf_list)

for ports in port_dict.keys():
    cmd = 'show interfaces ' + ports + ' descriptions'
    net_conn = netmiko_connect(host,username)
    output = net_conn.send_command(cmd)
    if 'BB' not in output:
        desc = 'set interfaces ' + ports + ' description "BB: ' + port_dict[ports]['z-host'] + ':' + port_dict[ports]['z-port'] + '"'
        print('Configuring this ' + desc +' on ' + host)
        output = net_conn.send_config_set(desc,exit_config_mode=False)
        print(output)
        commit_output = net_conn.commit()
        print(commit_output)
    else:
        print('Interface description is configured on port ' + ports)
    net_conn.disconnect()

print('Script Completed')
