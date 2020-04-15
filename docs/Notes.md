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

## Things to do

1. Make an lxd inventory plugin for containers
2. Make a libvirt inventory plugin for virtual machines
3. Make a lxc_network plugin for managing networks in lxd
4. Make a libvirt plugin for managing libvirt networks
