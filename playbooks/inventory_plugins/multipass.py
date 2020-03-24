from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: multipass
    plugin_type: inventory
    short_description: Returns Ansible inventory from multipass
    description: Returns Ansible inventory from multipass
    options:
      plugin:
        description: Name of the plugin
        required: true
        choices: ['multipass']
      sources:
        description: Host list of multipass servers
        required: false
'''



from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError



class InventoryModule(BaseInventoryPlugin):
    NAME = 'multipass'


    def verify_file(self, path):
        '''Return true/false if this is possibly a valid file for this plugin to consume
        '''
        valid = False
        if super(InventoryModule, self).verify_file(path):
            #base class verifies that file exists
            #and is readable by current user
            if path.endswith(('multipass.yaml',
                              'multipass.yml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache):
       '''Return dynamic inventory from source '''
       super(InventoryModule, self).parse(inventory, loader, path, cache)
       # Read the inventory YAML file
       self._read_config_data(path)
       try:
           # Store the options from the YAML file
           self.plugin = self.get_option('plugin')
           self.sources = ['localhost']#self.get_option('sources')
       except Exception as e:
           raise AnsibleParserError(
               'All correct options required: {}'.format(e))
       # Call our internal helper to populate the dynamic inventory
       self._populate()

    def _populate(self):
        '''Return the hosts and groups'''
        self.inventory.add_group("multipass")
        #import pdb; pdb.set_trace()
        for src in self.sources:
            src_grp = "mp_" + src
            self.inventory.add_group(src_grp)
            if src is 'localhost':
                src_ip = "127.0.0.1"
                guest_ip = "10.223.79.156"
                guest_name = "tpd-chuck"
            else:
                pass
            self.inventory.add_host(guest_name)
            self.inventory.add_host(host=guest_name, group="multipass")
            self.inventory.add_host(host=guest_name, group=src_grp)
            self.inventory.set_variable(guest_name, 'ansible_host', guest_ip)
