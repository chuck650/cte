from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from subprocess import Popen, PIPE
import yaml, os

DOCUMENTATION = r'''
    name: multipass
    plugin_type: inventory
    short_description: Returns Ansible inventory from multipass
    description: Queries Multipass to build a set of QEMU virtual machines managed by Multipass and returns the information as Ansible inventory
    options:
      plugin:
        description: Name of the plugin
        required: true
        choices: ['multipass']
      sources:
        description: List of multipass host nodes. Defaults to 'localhost'
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
           #TODO: Reade user defined sources from multipass.yaml
           self.sources = ['localhost']
           #self.get_option('sources')
       except Exception as e:
           raise AnsibleParserError(
               'All correct options required: {}'.format(e))
       # Call our internal helper to populate the dynamic inventory
       self._populate()

    def _get_structured_multipass_inventory(self, source):
        if not os.path.isfile("/snap/bin/multipass"):
            return {}
        else:
            return {}
        try:
            process = Popen(['multipass','list', '--format','yaml'], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            inventory_data = yaml.safe_load(stdout)
            return inventory_data
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)

    def _populate(self):
        '''Return the hosts and groups'''
        self.inventory.add_group("multipass")
        #import pdb; pdb.set_trace()
        for src in self.sources:
            src_grp = "mp_" + src
            self.inventory.add_group(src_grp)
            mp_inventory = {}
            if src is 'localhost':
                src_ip = "127.0.0.1"
            else:
                pass
            mp_inventory = self._get_structured_multipass_inventory(src)
            for vm, config in mp_inventory.items():
                self.inventory.add_host(vm)
                self.inventory.add_host(host=vm, group="multipass")
                self.inventory.add_host(host=vm, group=src_grp)
                self.inventory.set_variable(vm, 'ansible_host', config[0]['ipv4'][0])
                self.inventory.set_variable(vm, 'state', config[0]['state'])
                self.inventory.set_variable(vm, 'release', config[0]['release'])
