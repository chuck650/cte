# OpenvSwitch

## Getting rid on unused ports on all bridges

```bash
sudo ovs-vsctl show | grep -oP 'veth[a-f0-9]{8}(?= \(No such device\))' | xargs -n 1 sudo ovs-vsctl --if-exists del-port
```
