# Tactical Perimeter Defense
===

## Installation

The cte-tpd training environment depends on the cte-common setup, which will automatically run as a dependency when the cte-tpd playbook is ran.  To install and check the full cte-tpd environment, run the following playbook.

```bash
ansible-playbook -v playbooks/cte-tpd.yaml
```

 If the CTE common environment has already been successfully run, and you just want to run the cte-tpd specific portions, run the cte-tpd playbook with the following options.

 ```bash
 ansible-playbook -v playbooks/cte-tpd.yaml --skip-tags cte-common
 ```

## Checks

You can perform several checks on the environment to ensure it is configured and functioning correctly.

Check the gateway with this comand.

```bash
$ networkctl status cte-tpd
● 8: cte-tpd
       Link File: /usr/lib/systemd/network/99-default.link
    Network File: n/a
            Type: ether
           State: routable (unmanaged)
          Driver: openvswitch
      HW Address: 5e:2c:30:d4:2d:48
         Address: 10.220.223.1
                  fe80::5c2c:30ff:fed4:2d48
```
