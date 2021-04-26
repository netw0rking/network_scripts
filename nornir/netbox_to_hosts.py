import pynetbox
from pprint import pprint

nb = pynetbox.api(url='http://100.64.1.226:8000',
                  token='a11c6850a273edcdaccbab6d71f9fc0c2786e900')

host_list = nb.dcim.devices.filter(site='juniper-lab')

host_dict = {'ios': {},'juniper': {}}
for hostname in host_list:
    host = nb.dcim.devices.get(name=hostname)
    host_plat = host['platform']['name']
    if host_plat ==