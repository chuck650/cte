# Developer Notes

## File and directory permissions

Use this command to set file and directory permissions on files before pushing to github.

```bash
find . -type d -exec chmod 0750 {} \; && find . -type f -exec chmod 0640 {} \;
```

Use this command to rsync project files from host to guest for QA testing

```bash
rsync -avzh --exclude '__pycache__' ~/ansible/cte/ cte:~/ansible/cte/
```

## Strip escape sequences from terminal output

An example that gets the ip address of the interface that connects localhost to the first default gateway.  The relevant regex to strip ansi color codes is `s/[[:cntrl:]]\[[0-9]{1,3}m//g`.

```bash
ip route \
| awk 'NR==1 && $1=="default"{print "addr show dev " $5}' \
| sed -r "s/[[:cntrl:]]\[[0-9]{1,3}m//g" \
| ip -b - \
| awk '$1=="inet"{print $2}'
```

To strip all escape sequences and control codes, try this one.

```bash
ip -c addr | sed 's/\x1B[@A-Z\\\]^_]\|\x1B\[[0-9:;<=>?]*[-!"#$%&'"'"'()*+,.\/]*[][\\@A-Z^_`a-z{|}~]//g'
```

## Things to do

1. Make an lxd inventory plugin for containers
2. Make a libvirt inventory plugin for virtual machines
3. Make a lxc_network plugin for managing networks in lxd
4. Make a libvirt plugin for managing libvirt networks


## dnsmasq info

Location of each lxc network's dnsmasq file

```bash
sudo ls -l /var/snap/lxd/common/lxd/networks/cte-netsec
drwxr-xr-x 2 root root 4096 Apr 17 23:14 dnsmasq.hosts
-rw-r--r-- 1 root root  222 Apr 21 07:50 dnsmasq.leases
-rw-r--r-- 1 root root  641 Apr 17 23:14 dnsmasq.pid
-rw-r--r-- 1 root root    1 Apr 17 23:14 dnsmasq.raw
```
