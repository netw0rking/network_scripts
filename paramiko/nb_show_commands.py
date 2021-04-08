import pynetbox
import paramiko
import os
import sys

nb = pynetbox.api(url='http://100.64.1.226:8000', token='a11c6850a273edcdaccbab6d71f9fc0c2786e900')
username = os.getenv('USER')
host = sys.argv[1]

def initConn(x,username):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(x,username=username,password='cisco',look_for_keys=False)
    return ssh_client

def sendcmd(sshHost,command):
    stdin,stdout,stderr=sshHost.exec_command(command)
    return stdout

def active_int(host):
    new_int_list = []
    host_int = nb.dcim.interfaces.filter(device=host)
    for intf in host_int:
        if intf.connected_endpoint_reachable == True:
            new_int_list.append(intf)
    return new_int_list

intf_list = active_int(host)
#import pdb; pdb.set_trace()

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
    cmd = 'show interface ' + ports + ' | in crc|err|connected'
    cmd_list.append(cmd)

for command in cmd_list:
    ssh_conn = initConn(host,username)
    output = sendcmd(ssh_conn,command)
    for items in output:
        items = items.strip("\r\n")
        print(items)
    ssh_conn.close()
    del ssh_conn
    print('\n')
