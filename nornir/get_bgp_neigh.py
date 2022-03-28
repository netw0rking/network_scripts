from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from pprint import pprint

nr = InitNornir(config_file='./config.yml', dry_run=True)

sw_output = nr.run(task=napalm_get, getters=['facts', 'get_bgp_neighbors'])

output= {}
for switch in sw_output:
    try:
        bgp_neigh_dict= sw_output[switch][0].result
        #import pdb; pdb.set_trace()
        bgp_peers = bgp_neigh_dict['get_bgp_neighbors']['global']['peers'].keys()
        for peers in bgp_peers:
            peer_state = bgp_neigh_dict['get_bgp_neighbors']['global']['peers'][peers]['is_up']
            if peer_state == True:
                print(switch + ' has BGP peering with ' + peers + ' Up/Established')
            elif peer_state == False:
                print(switch + ' has BGP peering down with ' + peers)
    except:
        print('Script on ' + switch + ' was not successful')
        continue
