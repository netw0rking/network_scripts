from jinja2 import Environment, FileSystemLoader
import pynetbox
import sys
import os

if len(sys.argv) <= 2:
    print("Use: /vlan_config.py hostname vlan-id")
    quit()

nb_url = os.environ.get("nb_url")
nb_token = os.environ.get("nb_token")

nb = pynetbox.api(url=nb_url, token=nb_token)

def primary_ip(hostname):
    host = nb.dcim.devices.get(name=hostname)
    host_ip = host.primary_ip4
    ip = str(host_ip)[:-3]
    return ip


hostname = sys.argv[1]
vlan_id = sys.argv[2]
leaf_ip = primary_ip(hostname)

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
template = env.get_template("vlan_vni_template")

output = template.render(
    vlan_id = vlan_id,
    leaf_ip = leaf_ip
)
print(output)
