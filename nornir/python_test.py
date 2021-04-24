from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from pprint import pprint

nr = InitNornir(config_file='config.yml', dry_run=True)

sw_output = nr.run(task=napalm_get, getters=['facts', 'get_bgp_neighbors'])

for switch in sw_output:
    bgp_dict= sw_output[switch][0].result
    pprint(bgp_dict['get_bgp_neighbors']['global']['peers'])
    #import pdb; pdb.set_trace()
