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

Setting upstream servers in dnsmasq.raw

```bash
cat << EOF >> /var/snap/lxd/common/lxd/networks/cte-tpd/dnsmasq.raw
server=/netsec.cte/10.223.79.1
server=/243.240.10.in-addr.arpa/10.240.243.1
EOF

cat << EOF >> /var/snap/lxd/common/lxd/networks/cte-netsec/dnsmasq.raw
server=/tpd.cte/10.223.79.1
server=/223.220.10.in-addr.arpa/10.220.223.1
EOF
```

## Linux find any changed files in directory

Finds any file modified or changed in last 7 days.

```bash
find /var/lib/openvas/plugins/ -mindepth 1 -mtime -7 -or -ctime -7 -printf 'yes\n' -quit
```

## Regex Samples

Convert a timestamp from an openvas log to iso8601 format using perl.

```bash
sudo grep -oP '(?<=INFO:).*(?=utc:\d{4}: update_or_rebuild_nvt_cache)' /var/log/openvas/openvasmd.log | tail -n 1 | perl -nle 'print "$1-$2-$3T$4:$5.$6" if /(\d{4})-(\d{2})-(\d{2}) (\d{1,2})h(\d{2})\.(\d{2})/'
```

Again, but using sed.

```bash
sudo grep -oP '(?<=INFO:).*(?=utc:\d{4}: update_or_rebuild_nvt_cache)' /var/log/openvas/openvasmd.log | tail -n 1 | sed -E 's/([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{1,2})h([0-9]{2})\.([0-9]{2})/\1-\2-\3T\4:\5.\6/'
```

## Ansible datetime comparisons

```
- block:
  - name: Show last nvt update timestamp
    debug:
      msg:
        - "Current time:    {{now}}"
        - "Last NVT Update: {{log.nvt.last_update}}"
        - "Difference:      {{ ((now | to_datetime('%Y-%m-%d %H:%M:%S%z')) - (log.nvt.last_update | to_datetime('%Y-%m-%d %H:%M:%S%z'))) }}"
        - "Hours:           {{ ((now | to_datetime('%Y-%m-%d %H:%M:%S%z')) - (log.nvt.last_update | to_datetime('%Y-%m-%d %H:%M:%S%z'))).days }}"
        - "Seconds:         {{ ((now | to_datetime('%Y-%m-%d %H:%M:%S%z')) - (log.nvt.last_update | to_datetime('%Y-%m-%d %H:%M:%S%z'))).seconds }}"
```
