from netmiko import ConnectHandler
import os
import pynetbox

nb_url = os.getenv('nb_url')
nb_token = os.getenv('nb_token')

def net_conn(host):
    net = ConnectHandler(ip=host,password='Juniper',username=os.environ.get('USER'),device_type='juniper')
    return net

def neighbor_ip(host):
    z_side={}
    interfaces = nb.dcim.interfaces.filter(device=host)
    for interface in interfaces:
        if interface.connected_endpoint and 'core' in interface.connected_endpoint.device.name:
            z_switch=interface.connected_endpoint.device.name
            z_ip = nb.dcim.devices.get(name=z_switch)
            z_side[z_switch]= z_ip.primary_ip.address
    return z_side

def command_list(switch_ip):
    commands=[]
    for switch,ip in switch_ip.items():
        neighbor_command= f'set protocols bgp group INTERNAL neighbor {ip[:-3]} description {switch}'
        commands.append(neighbor_command)
    commands.append('set protocols bgp group INTERNAL type internal')
    return commands

switch_list= ['junos-core-3','junos-core-4','junos-core-5']
nb = pynetbox.api(url=nb_url, token=nb_token)

for switch in switch_list:
    z_side= neighbor_ip(switch)
    commands= command_list(z_side)
    print(f'+++{switch}+++')
    for command in commands:
        print(command)
    #host_ip= nb.dcim.devices.get(name=switch)
    #netmiko_conn = net_conn(host_ip.primary_ip.address[:-3])
    #output = netmiko_conn.send_config_set(commands,exit_config_mode=False)
    #print(output)
    #commit_output = netmiko_conn.commit()
    #print(commit_output)
