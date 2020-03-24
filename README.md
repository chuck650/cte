
# Cyber Training Environment (CTE)

Ansible playbooks and supporting plugins for building a home lab for PSCC cyber defense students.

---
# Installation

Create a  directory to install the CTE ansible environment.

``` bash
~$ mkdir ~/ansible
~$ cd ~/ansible
~/ansible$ git clone https://github.com/chuck650/cte.git
```

## Initialize and setup the CTE using the CTE initialization playbook

``` bash
~$ cd ~/ansible/cte
~/ansible/cte$ ansible
```

## Conduct a basic system inventory

Run the ansible setup module against the localhost and tee the output into a file for future reference.

``` bash
$ ansible -i localhost -m setup | tee ~/config-${USER}.txt
```
---
# Examples of Usage

## Override default ansible configuration

The CTE provides a sample Ansible environment variable configuration that can be sourced into the current user environment to set Ansible environment variables.

``` bash
~/ansible/cte$ . ansible.env
```

## Show ansible running configuration
``` bash
$ ansible-config dump
```

## Ping the localhost implicit inventory item
``` bash
$ ansible -m ping localhost
```

## Run a playbook
``` bash
~/ansible/cte$ ansible-playbook  disable-network-manager
```

---
# CTE Example Directory Structure

```
production                # inventory file for production servers
staging                   # inventory file for staging environment

group_vars/
   group1.yml             # here we assign variables to particular groups
   group2.yml
host_vars/
   hostname1.yml          # here we assign variables to particular systems
   hostname2.yml

library/                  # if any custom modules, put them here (optional)
module_utils/             # if any custom module_utils to support modules, put them here (optional)
filter_plugins/           # if any custom filter plugins, put them here (optional)

site.yml                  # master playbook
webservers.yml            # playbook for webserver tier
dbservers.yml             # playbook for dbserver tier

roles/
    common/               # this hierarchy represents a "role"
        tasks/            #
            main.yml      #  <-- tasks file can include smaller files if warranted
        handlers/         #
            main.yml      #  <-- handlers file
        templates/        #  <-- files for use with the template resource
            ntp.conf.j2   #  <------- templates end in .j2
        files/            #
            bar.txt       #  <-- files for use with the copy resource
            foo.sh        #  <-- script files for use with the script resource
        vars/             #
            main.yml      #  <-- variables associated with this role
        defaults/         #
            main.yml      #  <-- default lower priority variables for this role
        meta/             #
            main.yml      #  <-- role dependencies
        library/          # roles can also include custom modules
        module_utils/     # roles can also include custom module_utils
        lookup_plugins/   # or other types of plugins, like lookup in this case

    webtier/              # same kind of structure as "common" was above, done for the webtier role
    monitoring/           # ""
    fooapp/               # ""
```
