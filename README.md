
# Cyber Training Environment (CTE)

Ansible playbooks and supporting plugins for building a home lab for PSCC cyber defense students.

---

## Prerequisites

You'll need a Debian based Linux environment to run the CTE.  If you are running Microsoft Windows as your primary OS, see the [WINDOWS_HOWTO](../master/WINDOWS_HOWTO.md) file in this repository for further guidance on how to get a Linux instance running.

### Preparing for Installation

There are a few tasks you need to perform to get your CTE VM ready. If you created your VM using multipass and the cloud-init file generated from the [cte-multipass](https://github.com/chuck650/cte-multipass "Generate a user-data.yaml cloud-init file for multipass") project, then this part has already been done for you when the VM initialized.

Ensure the system is up to date with all packages.

```bash
$ sudo apt update
$ sudo apt -y full-upgrade
```

Ensure you have a basic Python execution environment.

```bash
$ sudo apt install python python3
```

**Recommended:** Create a user account for yourself in addition to the local administrator account.  Add the new user to the `sudo` group, then login with the new user's account.

```bash
$ sudo adduser ${NEW_USER}
$ sudo adduser ${NEW_USER} sudo
$ sudo login ${NEW_USER}
```

Generate RSA and ECDA ssh keys and add the public keys to the authorized keys file.

```bash
~$ ssh-keygen -t rsa -b 2048
~$ ssh-keygen -t ecdsa -b 521
~$ cat .ssh/id_{ecd,r}sa.pub >> .ssh/authorized_keys
```

> If you are going to use ssh to connect to this VM from outside the CTE, also copy any other public keys necessary to the `~/.ssh/authorized_keys` file.



Install Ansible.

```bash
$ sudo apt install software-properties-common
$ sudo apt-add-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible
```

[Ansible user guide](https://docs.ansible.com/ansible/latest/user_guide/index.html "Covers how to work with Ansible")

[Ansible tutorial](http://riptutorial.com/ebook/ansible "Free ebook written by many hardworking individuals at Stack Overflow")


## Installation

Create a  directory to install the CTE ansible environment.

```bash
~$ mkdir ~/ansible
~$ cd ~/ansible
~/ansible$ git clone https://github.com/chuck650/cte.git
```

To update the installation of the CTE with the most recent changes, use `git` to pull in updates to the CTE.

```bash
~$ cd ansible/cte
~/ansible/cte$ git pull
```

### Conduct a basic system inventory

Run the ansible setup module against the localhost and tee the output into a file for future reference.

```bash
~/ansible/cte$ ansible -m setup localhost | tee ~/config-${USER}.txt
```

### Conduct a more in-depth system inventory

Ansible provides the DevOps tool that manages the CTE. Much of the power of the tool comes from using Ansible playbooks to group many DevOps tasks together.  

[About playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#about-playbooks "Provides the basis for really simple configuration management")

Run the cte-config playbook and tee the output into a file for future reference.

```bash
~/ansible/cte$ ansible-playbook playbooks/cte-config.yaml | tee ~/cte-config-${USER}.txt
```

### Initialize and setup the CTE using the CTE initialization playbook

```bash
~$ cd ~/ansible/cte
~/ansible/cte$ ansible-playbook playbooks/cte-common.yaml
```

## Setting up a class

Depending on the classes you are taking, you may need to build one or more learning environments.  Each class has a separate skills development area (SDA), usually divided by a different network and infrastructure container.  There are two ways to build a skills development area using the CTE.  First, you can call the SDA's playbook with ansible, or you can call the CTE playbook with a parameter for the class name.

Here's how to call a playbook directly for the network security class

```bash
$ ansible-playbook -v playbooks/cte-netsec.yaml
```

Here's how to call the CTE playbook with a class name for network security.

```bash
$ ansible-playbook -v playbooks/cte.yaml -e 'class=netsec'
```



---

## Examples of Usage

Here are some examples of using the CTE Ansible DevOps tool to manage the CTE.  These are meant as examples, and should only be run when you need to perform the tasks described in the example.

## Override default ansible configuration

The CTE provides a sample Ansible environment variable configuration that can be sourced into the current user environment to set Ansible environment variables.

```bash
~/ansible/cte$ . ansible.env
```

## Show ansible running configuration
```bash
$ ansible-config dump
```

## Ping the localhost implicit inventory item
```bash
$ ansible -m ping localhost
```

## Run a playbook
```bash
~/ansible/cte$ ansible-playbook  playbooks/${playbook_name}
```

---
# CTE Example Directory Structure

Here is an example directory structure for an Ansible DevOps project.  This will give you some familiarity with how an Ansible project is structured and where the different Ansible components can be found.

[Ansible best practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html "Tips for making the most of Ansible and Ansible playbooks")

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

---
# Configuration

The Cyber Training Environment is established using a set of Ansible playbooks that execute a set of tasks organized by the role and location of the target system.  These tasks are supported by Ansible modules and plugins written in Python.  Custom plugins are also written in Python and extend the core capabilities of Ansible.

CTE uses a custom inventory plugin to discover and report on virtual machines managed by Canonical's Multipass VM controller.

## Multipass Inventory plugin

You can view the documentation on the plugin using this command.

```bash
~/ansible/cte$ ansible-doc -t inventory multipass
```

You can get a list of the Ansible attributes of all your Multipass VM instances in YAML using this command.

```bash
~/ansible/cte$ ansible-inventory -i inventory/multipass.yaml --list
```

you can see all found inventory, using this command.

```bash
~/ansible/cte$ ansible-inventory --list
```

And as a graph, using this command.

```bash
~/ansible/cte$ ansible-inventory --graph
```
