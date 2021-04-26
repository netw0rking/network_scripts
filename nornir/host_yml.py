from jinja2 import Environment, FileSystemLoader
import pynetbox
import sys

if len(sys.argv) <= 1:
    print('Use: host_yml.py {site code}')

def host_dict(site_hosts):
    host_dict = {'cisco':{},'juniper':{}}
    for hostname in site_hosts:
        host = nb.dcim.devices.get(name=hostname)
        ip = str(host.primary_ip)
        host_plat = host['platform']['name']
        if host_plat == 'ios':
            host_dict['cisco']['name'] = hostname
            host_dict['cisco']['loopback'] = ip[:-3]
        elif host_plat == 'junos':
            host_dict['juniper']['name'] = hostname
            host_dict['juniper']['loopback'] = ip[:-3]
    return(host_dict)

nb = pynetbox.api(url='http://100.64.1.226:8000',
                  token='a11c6850a273edcdaccbab6d71f9fc0c2786e900')

site_hosts = nb.dcim.devices.filter(site=sys.argv[1])

hosts = host_dict(site_hosts)
#import pdb; pdb.set_trace()

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('nornir_host_file')
output = template.render(host_list=hosts)