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
        #import pdb; pdb.set_trace()
        valid = False
        if super(InventoryModule, self).verify_file(path):
            #base class verifies that file exists
            #and is readable by current user
            print(path)
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

    def get_yaml():
        return self._get_structured_inventory('localhost')

    def _get_structured_inventory(self, source):
        #import pdb; pdb.set_trace()
        if not os.path.isfile("/snap/bin/multipass"):
            return {}
        try:
            # multipass list --format yaml
            # Returns: Dictionary of key,value pairs
            process = Popen(['multipass','list', '--format','yaml'], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            inventory_data = yaml.safe_load(stdout)
            return inventory_data
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)
        except FileNotFoundError as e:
            return {}

    def _populate(self):
        '''Return the hosts and groups'''
        self.inventory.add_group("multipass")
        for src in self.sources:
            src_grp = "mp_" + src
            self.inventory.add_group(src_grp)
            inventory_data = {}
            if src is 'localhost':
                src_ip = "127.0.0.1"
            else:
                pass
            inventory_data = self._get_structured_inventory(src)
            #import pdb; pdb.set_trace()
            for vm, config in inventory_data.items():
                hostname = 'mp_' + vm
                self.inventory.add_host(hostname)
                self.inventory.add_host(host=hostname, group="multipass")
                self.inventory.add_host(host=hostname, group=src_grp)
                self.inventory.set_variable(hostname, 'ansible_host', config[0]['ipv4'][0])
                self.inventory.set_variable(hostname, 'state', config[0]['state'])
                self.inventory.set_variable(hostname, 'release', config[0]['release'])
                self.inventory.set_variable(hostname, 'mp_data', config)
