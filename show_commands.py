#!/usr/bin/env python3

import paramiko
import sys
from pprint import pprint

host = sys.argv[1]
cmd = input('Type the command to send: ')

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host,username='wquizhpi',password='cisco',look_for_keys=False)

stdin,stdout,stderr=ssh_client.exec_command(cmd)

output = stdout.readlines()
pprint(output)

ssh_client.close()

del ssh_client, stdin, stdout, stderr
