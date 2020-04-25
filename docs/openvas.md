# OpenVAS Security Vulnerability Scanner

Generally followed this guide to create the Ansible role for openvas.  It's a little out of date, so not all the steps are correct anymore.

[OpenVAS install HowTo](https://www.fosslinux.com/7320/how-to-install-and-configure-openvas-9-on-ubuntu.htm "How to install and configure openvas security scanner")

[Greenbone Security Assistant docs](https://docs.greenbone.net/src/gsa/7.0/index.html)

## Getting the server ready

*Note: the quotes around the limit list are __required__ to prevent bash from interpreting the `&` and launching `ansible-playbook` as a background task.*

```bash
ansible-playbook playbooks/cte-openvas.yaml --list-hosts
ansible-playbook playbooks/cte-openvas.yaml --limit "pia:&openvas"
```

## First steps

Sync the data feeds.

```bash
greenbone-nvt-sync
greenbone-scapdata-sync
greenbone-certdata-sync
```

Start the services.

```bash
systemctl restart openvas-scanner
systemctl restart openvas-manager
systemctl restart greenbone-security-assistant
```

Enable services to run at boot.

```bash
systemctl enable openvas-scanner
systemctl enable openvas-manager
systemctl enable greenbone-security-assistant
```

Check the listening ports and rebuild the feed cache.

```bash
sudo ss -plnt4 | grep openvas
openvasmd --rebuild --progress
```

## Verify the installation

Here we are going to use openvas-check-setup tool for checking the state of OpenVAS installation.

Download and copy it to your path:

```bash
wget --no-check-certificate https://svn.wald.intevation.org/svn/openvas/branches/tools-attic/openvas-check-setup -P /usr/local/bin/
```

Give execute permission.

```bash
chmod +x /usr/local/bin/openvas-check-setup
```

Now verify installation.

```bash
openvas-check-setup --v9
```

https://docs.greenbone.net/GSM-Manual/gos-6/en/web-interface.html#login-web-interface

wget --no-check-certificate https://svn.wald.intevation.org/svn/openvas/branches/tools-attic/openvas-check-setup -P /usr/local/bin/

ruby -run -e httpd . -p 5000
