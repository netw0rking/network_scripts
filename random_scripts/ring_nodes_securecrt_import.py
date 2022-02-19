#!/usr/bin/env python3
import requests
import pycountry
import os

username = os.getenv('USER')
# Change root_folder var if different
root_folder = 'ring-nodes'
top_line = 'hostname,username,folder,protocol,session_name\n'
user = input('What is the ringnode login name?\n')

while True:
    with open('ringnodes.csv', 'wt') as f:
        f.write(top_line)
        r = requests.get('https://api.ring.nlnog.net/1.0/nodes')
        host_list = r.json()['results']['nodes']
        for host in host_list:
            hostname = host['hostname']
            country = pycountry.countries.get(alpha_2=host['countrycode'])
            folder = f'{root_folder}/{country.name}/'
            protocol = 'SSH2'
            session_name = host['hostname'].replace('.ring.nlnog.net','')
            #import pdb; pdb.set_trace()
            next_line = f'{hostname},{user},{folder},{protocol},{session_name}\n'
            f.write(next_line)
    f.close()
    break

print(f'Created ringnodes.csv')
