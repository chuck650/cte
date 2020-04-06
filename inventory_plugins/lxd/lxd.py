from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from subprocess import Popen, PIPE
import yaml, os, operator

DOCUMENTATION = r'''
    name: lxd
    plugin_type: inventory
    short_description: Returns Ansible inventory from lxd
    description: Builds Ansible inventory from lxd managed containers
    options:
      plugin:
        description: Name of the plugin
        required: true
        choices: ['lxd']
      sources:
        description: List of lxd host nodes. Defaults to 'localhost'
        required: false
'''



from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError



class InventoryModule(BaseInventoryPlugin):
    NAME = 'lxd'


    def verify_file(self, path):
        '''Return true/false if this is possibly a valid file for this plugin to consume
        '''
        valid = False
        #import pdb; pdb.set_trace()
        if super(InventoryModule, self).verify_file(path):
            #base class verifies that file exists
            #and is readable by current user
            if path.endswith(('lxd.yaml',
                              'lxd.yml')):
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
           #TODO: Read user defined sources from lxd.yaml
           self.sources = ['localhost']
           #self.get_option('sources')
       except Exception as e:
           raise AnsibleParserError(
               'All correct options required: {}'.format(e))
       # Call our internal helper to populate the dynamic inventory
       self._populate()

    def _get_structured_inventory(self, source):
        #import pdb; pdb.set_trace()
        if not os.path.isfile("/snap/bin/lxd"):
            return {}
        try:
            # lxc list --format yaml
            # Returns: List of Dictionary objects
            process = Popen(['lxc','list', '--format','yaml'], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            inventory_data = yaml.safe_load(stdout)
            return inventory_data
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)
        except FileNotFoundError as e:
            return {}

    def _get_item(self, element, data):
        try:
            return reduce(operator.getitem, element.split('/'), data)
        except:
            return None

    def _populate(self):
        '''Return the hosts and groups'''
        self.inventory.add_group("lxd")
        for src in self.sources:
            src_grp = "lxd_" + src
            self.inventory.add_group(src_grp)
            inventory_data = []
            if src is 'localhost':
                src_ip = "127.0.0.1"
            else:
                pass
            inventory_data = self._get_structured_inventory(src)
            #import pdb; pdb.set_trace()
            for item in inventory_data:
                hostname = 'lxd_' + item['name']
                self.inventory.add_host(hostname)
                self.inventory.add_host(host=hostname, group="lxd")
                self.inventory.add_host(host=hostname, group=src_grp)
                try:
                    self.inventory.set_variable(hostname, 'ansible_host', self._get_item('devices/eth0/ipv4.address',item))
                    self.inventory.set_variable(hostname, 'state', item['status'])
                    self.inventory.set_variable(hostname, 'release', item['config']['image.release'])
                    self.inventory.set_variable(hostname, 'lxd_data', item)
                except Exception as e:
                    continue
            #print('Inventory count: ', len(inventory_data))
            #import pdb; pdb.set_trace()
            return
