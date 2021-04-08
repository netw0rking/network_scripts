#!/usr/bin/env python3

import paramiko
import sys

host = sys.argv[1]
cmd = input('Type the command to send: ')

def initConn(x):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(x,username='wquizhpi',password='cisco',look_for_keys=False)
    return ssh_client

def sendcmd(sshHost,command):
    stdin,stdout,stderr=sshHost.exec_command(command)
    return stdout

ssh_conn = initConn(host)

output = sendcmd(ssh_conn,cmd)

for items in output:
    items = items.strip("\r\n")
    print(items)

ssh_conn.close()
del ssh_conn
