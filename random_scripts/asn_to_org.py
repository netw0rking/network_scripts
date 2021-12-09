#!/usr/bin/env python
import requests

as_number = input('What AS number are you searching for?\n')

def find_as_owner(as_number):
    r = requests.get(f'https://www.peeringdb.com/api/net?asn__in={as_number}')
    as_data = r.json()
    try:
        as_name = as_data['data'][0]['name']
        return as_name
    except:
        return

org = find_as_owner(as_number)
if org:
    print(f'{as_number} belongs to {org}')
else:
    print(f'{as_number} does not exist in PeeringDB')
