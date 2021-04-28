from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from pprint import pprint

nr = InitNornir(config_file='./inventory/config.yml', dry_run=True)

sw_output = nr.run(task=napalm_get, getters=['facts', 'get_interfaces_ip'])

output= {}
for switch in sw_output:
    try:
        intf_dict= sw_output[switch][0].result
        pprint(intf_dict['facts']['hostname'])
        pprint(intf_dict['get_interfaces_ip'])
    except:
        print('Script on ' + switch + ' was not successful')
        continue