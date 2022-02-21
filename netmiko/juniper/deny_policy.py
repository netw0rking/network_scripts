from netmiko import ConnectHandler
import os
import pynetbox

nb_url = os.getenv('nb_url')
nb_token = os.getenv('nb_token')

def net_conn(host):
    net = ConnectHandler(ip=host,password='Juniper',username=os.environ.get('USER'),device_type='juniper')
    return net

nb = pynetbox.api(url=nb_url, token=nb_token)
host_list = nb.dcim.devices.filter(site='juniper-routing',manufacturer='juniper')

for host in host_list:
    command= 'set policy-options policy-statement DENY then reject'
    print(f'+++{host.name}+++')
    netmiko_conn = net_conn(host.primary_ip.address[:-3])
    output = netmiko_conn.send_config_set(command,exit_config_mode=False)
    print(output)
    commit_output = netmiko_conn.commit()
    print(commit_output)
    netmiko_conn.disconnect()
