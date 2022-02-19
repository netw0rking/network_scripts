import pynetbox
import os
from pprint import pprint

nb_url = os.getenv('nb_url')
nb_token = os.getenv('nb_token')
nb = pynetbox.api(
    url=nb_url, token=nb_token
)

host_list = nb.dcim.devices.all()

with open("hosts.yml", "w") as f:
    f.write("---\n")
    for host in host_list:
        if host.primary_ip:
            f.write(f"{host.name.upper()}:\n")
            f.write(f"  hostname: {host.primary_ip.address[:-3]}\n")
            f.write(
                    f"  groups:\n    - {host.device_type.manufacturer.name.lower()}\n    - {host.site.name.lower().replace('-','_')}\n"
            )
