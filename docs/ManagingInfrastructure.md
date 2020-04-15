# Managing CTE Infrastructure

The CTE supports automatic discovery of hosts running in the CTE under control of the lxd daemon.  You can view the status of the daemon using systemd tools.

```bash
$ systemctl status snap.lxd.daemon
● snap.lxd.daemon.service - Service for snap application lxd.daemon
   Loaded: loaded (/etc/systemd/system/snap.lxd.daemon.service; static; vendor preset: enabled)
   Active: active (running) since Wed 2020-04-15 13:49:29 EDT; 2h 43min ago
 Main PID: 19922 (daemon.start)
    Tasks: 0 (limit: 4915)
   Memory: 25.6M
   CGroup: /system.slice/snap.lxd.daemon.service
           ‣ 19922 /bin/sh /snap/lxd/14594/commands/daemon.start
```

## Using Ansible

The Ansible DevOps tool is used to provision lxd containers and also to provision services on hosts within the CTE.  It is also used to perform various tasks to maintain the CTE in working order, report CTE information, and configure the networking environment so that provisioned networks and containers are able to communicate upstream to the host environment and beyond.

The Ansible infrastructure is installed in a directory using `git` to clone the project from *github*.  Once cloned, all ansible commands should be run from the folder where the project was cloned.  As an alternative, you can set an Ansible environment variable in your `.bashrc` file to set Ansible's home to this directory.

### Inventory

The containers within the CTE are tagged with metadata inside the lxd configuration for each container.  This helps Ansible determine the course and CTE groups that each container belong to, and what roles should be provisioned and maintained on each container.  You can use the `ansible-inventory` tool to view container membership in various groups.  Here are a few examples.

#### Viewing the cte group

```bash
~/ansible/cte$ ansible-inventory cte --graph
~/ansible/cte/inventory/inventory.yaml
~/ansible/cte/inventory/lxd.yaml
~/ansible/cte/inventory/multipass.yaml
@cte:
  |--lxd_netsec-ca1
  |--lxd_netsec-www
  |--lxd_pia1
  |--lxd_pia2
  |--lxd_pub1
  |--lxd_tpd-db1
  |--lxd_tpd-mq1
  |--lxd_tpd-www1
```

#### Viewing the tpd group

```bash
$ ansible-inventory cte --graph
~/ansible/cte/inventory/inventory.yaml
~/ansible/cte/inventory/lxd.yaml
~/ansible/cte/inventory/multipass.yaml
@cte:
  |--lxd_pub1
  |--lxd_tpd-db1
  |--lxd_tpd-mq1
  |--lxd_tpd-www1
```

#### Viewing the webservers group

```bash
~/ansible/cte$ ansible-inventory webservers --graph
~/ansible/cte/inventory/inventory.yaml
~/ansible/cte/inventory/lxd.yaml
~/ansible/cte/inventory/multipass.yaml
@cte:
  |--lxd_netsec-www
  |--lxd_tpd-www1
```

### Provisioning a Course

Each course has a different set of networks and hosts associated with the coursework and the tasks to be taught during the course.  To provision the network(s) and host(s) that are required to meet the learning objectives and perform the tasks required in lab work, run the course playbook using the `ansible-playbook` tool.  Each course's playbook is found in the playbooks directory and is prefixed with the word `cte_` before the course name.  e.g, the *Principles of Information Assurance* course playbook is found at **playbooks/cte-pia.yaml**.  Each playbook is a `yaml` data file that describe the tasks to be performed to provision and configure the environment for the course.

#### Example course playbook

```bash
~ansible/cte$ ansible-playbook playbooks/cte-netsec.yaml
```

### Provisioning a service

A service is a configured set of software on a host that provides services to the network or to a logged in user.  Services are determined and configured by group membership.  E.g., a host can provide an http web server service to the network by provisioning and configuring a web server on the host.  You can provision a single system by limiting the inventory item on which the playbook operates.  These playbooks are identified by their role name.

### Provision a single web server service

First verify the hosts that can be operated on by a playbook by using the `--list-hosts` option on the playbook.  Select a valid host inventory name, then run the playbook using the `--limit=` option, specifying the inventory name after the equals sign.

```bash
~/ansible/cte$ ansible-playbook playbooks/cte-webservers.yaml --list-hosts
/home/chuck/ansible/cte/inventory/inventory.yaml
/home/chuck/ansible/cte/inventory/lxd.yaml
/home/chuck/ansible/cte/inventory/multipass.yaml

playbook: playbooks/cte-webservers.yaml

  play #1 (webservers): webservers	TAGS: []
    pattern: ['webservers']
    hosts (2):
      lxd_tpd-www1
      lxd_netsec-www

~/ansible/cte$ ansible-playbook playbooks/webservers.yaml --limit=lxd_tpd-www1
```
