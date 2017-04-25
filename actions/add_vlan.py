import warnings
import lib.phpipam
import lib.utils

warnings.filterwarnings('ignore')

from st2actions.runners.pythonrunner import Action

class AddVlan(Action):
    """ Stackstorm Python Runner """
    def run(self, name, number, **kwargs):
        """ Stackstorm Run Method  """

        api_uri = self.config.get('api_uri', None)
        api_username = self.config.get('api_username', None)
        api_password = self.config.get('api_password', None)
        api_verify_ssl = self.config.get('api_verify_ssl', True)

        ipam = lib.phpipam.PhpIpamApi(api_uri=api_uri, api_verify_ssl=api_verify_ssl)
        ipam.login(auth=(api_username, api_password))

        if kwargs['l2domain'] is not None:
            l2domains_api = lib.phpipam.controllers.L2DomainsApi(phpipam=ipam)

            l2domain_name = kwargs['l2domain']
            l2domains = (l2domains_api.list_l2domains())['data']
            l2dom = [x for x in l2domains if x['name'] == l2domain_name]
            lib.utils.check_list(t_list=l2dom, t_item=l2domain_name,
                             t_string='layer 2 domain')
            l2dom_id = l2dom[0]['id']
            kwargs['l2domain_id'] = l2dom_id


        vlans_api = lib.phpipam.controllers.VlansApi(phpipam=ipam)

        new_vlan = vlans_api.add_vlan(name=name, number=number, **kwargs)

        ipam.logout()

        return new_vlan
