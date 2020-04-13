# CTE Inventory Plugins

The CTE makes use of Ansible custom inventory plugins to query the hosts managed by Multipass and LXD.

## Multipass

Multipass is a virtual machine orchestration tool from Canonical that can automate the creation of virtual machines on Linux, MacOS and Windows.  It uses different hypervisors on each OS depending on the OS environment.  Generally, in addition to the default configurations shown in the table below, each OS can optionally support VirtualBox as a hypervisor.

| OS | Hypervisor |
| :- | :-: |
| Linux | KVM |
| Windows | Hyper-V |
| MacOS | hyperkit |

The multipass inventory plugin uses the following command to extract data from the host in yaml format as shown in the following example.

```bash
$ multipass list --format=yaml
cte:
  - state: Running
    ipv4:
      - 10.223.79.250
    release: 19.10
vm2:
  - state: Running
    ipv4:
      - 10.223.79.30
    release: 18.04
```

The returned yaml data consists of a dictionary using the VM names as keys, and the VM configuration as a list of configuration data.


## LXD

LXD is a daemon that manages infrastructure containers.  Infrastructure containers run a namespaced OS over a shared kernel providing a complete virtualized OS space as opposed to application containers such as Docker containers.

Since LXD containers share the kernel from the host, they run with low system resource requirements and are very suitable for limiting the amount of system resources required by the CTE when running many OS instances across a virtualized network infrastructure.

LXD containers appear in Ansible inventory with `lxd_` prepended to their container names.  This allows the names to be unique within ansible inventory, while allowing name duplication outside of the LXD container name namespace on the localhost LXD daemon.

The lxd inventory plugin uses the following command to extract data from the host in yaml format as shown in the following example.

```bash
$ lxc list --format yaml
- architecture: x86_64
  config:
    image.architecture: amd64
    image.description: ubuntu 19.10 amd64 (release) (20200320)
    image.label: release
    image.os: ubuntu
    image.release: eoan
    image.serial: "20200320"
    image.type: squashfs
    image.version: "19.10"
    volatile.base_image: af17a20658460256e7c4dd3a6b2ce6c2dc595120eeb0df65f5d80f88cc094d76
    volatile.eth0.host_name: veth51128db7
    volatile.eth0.hwaddr: 00:16:3e:72:fb:24
    volatile.idmap.base: "0"
    volatile.idmap.current: '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]'
    volatile.idmap.next: '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]'
    volatile.last_state.idmap: '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]'
    volatile.last_state.power: RUNNING
  devices:
    eth0:
      ipv4.address: 10.240.243.51
      name: eth0
      nictype: bridged
      parent: cte-netsec
      type: nic
  ephemeral: false
  profiles:
  - default
  - cte-user
  stateful: false
  description: ""
  created_at: 2020-03-30T10:30:49.447394929-04:00
  expanded_config:
    image.architecture: amd64
    image.description: ubuntu 19.10 amd64 (release) (20200320)
    image.label: release
    image.os: ubuntu
    image.release: eoan
    image.serial: "20200320"
    image.type: squashfs
    image.version: "19.10"
    user.user-data: |
      #cloud-config
      users:
        - name: chuck
          gecos: Chuck Nelson
          groups: sudo
          passwd: password
          shell: /bin/bash
          sudo: ['ALL=(ALL) NOPASSWD:ALL']
          lock-passwd: false
          ssh-authorized-keys: [ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/W8uMffjV8hwW6KgyHMYzGPoHBHXF2AD1DHzsJ5qbaZdcL73Nw0iBKoXfHdbGbtWRxpIIDTNr9q4mztuKrKURVE4OCuzyHa+ilHdyO9b8S+2H6o8VmNZI3XfijAHxoZ8gy+4QeVRdQRXFv7BuZpK7ab1uSCrutRXyEHIfACZuFcx9vl7/qcuIfRRo10Brbooz8jiIhGogQHePHs8lfmxwiYSsm311Xok1PwxQO8zVAUHb5NtnBIuREMiLZ816kaxv8Lg+cINBlKOTrzIN+uXozZOHMjmEMhey6NYiW8thYnDvlpE2FwoClpqONYpmqaOPq7amcVvTkDrBjcCiqgtr chuck@cte, ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBACS7eJY6wNk78xQyw6RRjzdg/UGaiHTslr+bugc8yriBVsyDqdz1IUg9nqvPRBxBXUoHTgAyEHoVUnF/3ixKsB4JgFQ2nhhLW947u0L0qL8Wh/trLJp7o8t7QEO3e6IdZaaE4lzn7+E2SIFv2VLizrwTjnExkW4hrpXNuvlP2Kr6Mh1UA== chuck@cte]
      packages: [python,htop,tree,tmux]
    volatile.base_image: af17a20658460256e7c4dd3a6b2ce6c2dc595120eeb0df65f5d80f88cc094d76
    volatile.eth0.host_name: veth51128db7
    volatile.eth0.hwaddr: 00:16:3e:72:fb:24
    volatile.idmap.base: "0"
    volatile.idmap.current: '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]'
    volatile.idmap.next: '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]'
    volatile.last_state.idmap: '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]'
    volatile.last_state.power: RUNNING
  expanded_devices:
    eth0:
      ipv4.address: 10.240.243.51
      name: eth0
      nictype: bridged
      parent: cte-netsec
      type: nic
    root:
      path: /
      pool: default
      type: disk
  name: netsec-ca1
  status: Running
  status_code: 103
  last_used_at: 2020-03-30T10:30:53.395484992-04:00
  location: none
  type: container
  backups: []
  state:
    status: Running
    status_code: 103
    disk:
      root:
        usage: 16099328
    memory:
      usage: 221446144
      usage_peak: 0
      swap_usage: 0
      swap_usage_peak: 0
    network:
      eth0:
        addresses:
        - family: inet
          address: 10.240.243.51
          netmask: "24"
          scope: global
        - family: inet6
          address: fe80::216:3eff:fe72:fb24
          netmask: "64"
          scope: link
        counters:
          bytes_received: 212490
          bytes_sent: 594368
          packets_received: 1967
          packets_sent: 7251
        hwaddr: 00:16:3e:72:fb:24
        host_name: veth51128db7
        mtu: 1500
        state: up
        type: broadcast
      lo:
        addresses:
        - family: inet
          address: 127.0.0.1
          netmask: "8"
          scope: local
        - family: inet6
          address: ::1
          netmask: "128"
          scope: local
        counters:
          bytes_received: 125622
          bytes_sent: 125622
          packets_received: 1395
          packets_sent: 1395
        hwaddr: ""
        host_name: ""
        mtu: 65536
        state: up
        type: loopback
    pid: 23376
    processes: 39
    cpu:
      usage: 163713047873
  snapshots: []
```
