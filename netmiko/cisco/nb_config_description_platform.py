from netmiko import ConnectHandler
from pprint import pprint
import pynetbox
import sys
import os

def netmiko_connect(host,username,cli):
    if 'ios' == cli:
        cli = 'cisco_ios'
    elif 'nexus' == cli:
        cli = 'cisco_nxos'
    elif 'ios-xr' == cli:
        cli = 'cisco_xr'
    net_conn = ConnectHandler(device_type=cli, host=host, username=username, password='cisco') 
    return net_conn

def active_int(host):
    new_int_list = []
    host_int = nb.dcim.interfaces.filter(device=host)
    for intf in host_int:
        if intf.connected_endpoint_reachable == True:
            new_int_list.append(intf)
    return new_int_list

def platform(host):
    host_plat = nb.dcim.devices.get(name=host)
    cli = host_plat['platform']['name']
    return cli

nb = pynetbox.api(url='http://100.64.1.226:8000', token='a11c6850a273edcdaccbab6d71f9fc0c2786e900')
host = sys.argv[1]
username = os.getenv('USER')

intf_list = active_int(host)
cli = platform(host)

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
    net_conn = netmiko_connect(host,username,cli)
    output = net_conn.send_command(command,use_textfsm=True)
    for items in output:
        if 'BB' not in items['description']:
            intf = (items['interface'])
            config_list = []
            config_list.append('interface ' + intf)
            new_desc = 'description BB: ' + port_dict[intf]['z-host'] + ':' + port_dict[intf]['z-port']
            config_list.append(new_desc)
            if cli == 'ios-xr':
                config_list.append('commit')
            print('Configuring this ' + new_desc +' on ' + host)
            desc_out = net_conn.send_config_set(config_list)
            print(desc_out)
        else:
            print('Interface description is configured on port ' + items['interface'])
    net_conn.disconnect()
