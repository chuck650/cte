# Virtual Machines

This document provides instructions for using a virtual machine to host the CTE.  The CTE can be run on a variety of hypervisors hosted on Linux, MacOS or Windows.  A VM is not required however, if the host machine is running a Debian based distribution of Linux.  The CTE will run directly on a host running an up to date Debian based Linux distribution, such as Ubuntu.

The VM can run a full desktop version, a server version or a cloud image version of a Debian based Linux distribution.  Cloud images and server iso installers do not provide the X11 graphical environment by default, therefore GUI applications are not usable since there is no display for the applications.  Using the capabilities of X11 or Wayland, GUI applications can be installed and configured to use remote displays on Linux and MacOS.

## Running VM GUI applications on Linux Host using X11 Forwarding

There are many ways to get a remote display of a GUI or single application on a remote server.  This example uses X11 native capabilities to run Firefox on a headless multipass VM without a display and show the GUI on the display of a host running X11.  The host can be Linux (`X11`), MacOS (`XQuartz`), or Windows (`vcxsrv`) running one of the fore mentioned X-servers.

The simplest, and by far easiest method, is to use X11Forwarding via ssh.  The CTE VM must have X11Forwarding enabled in `/etc/ssh/sshd_config` with the configuration line `X11Forwarding yes`.

You can check this from the host.

```bash
@host:~$ ssh cte "grep '^X11Forwarding' /etc/ssh/sshd_config"
X11Forwarding yes
```
You can also check this from the CTE VM.

```bash
@cte:~$ grep '^X11Forwarding' /etc/ssh/sshd_config
X11Forwarding yes
```

First connect via ssh with X11Forwarding, then run the GUI application.  The GUI will open on the host's X11 server.  Redirecting stderr to `/dev/null` keeps the session quiet on the CTE VM and pushing the process to a job releases the CTE terminal for additional input.

```bash
@host:~$ ssh -X cte
@cte:~$ firefox 2>/dev/null &
```

## Running VM GUI applications without X11 Forwarding

**⮦ ⮦ ⮦ ⮦ ⮦**    *Below section incomplete*    **⮧ ⮧ ⮧ ⮧ ⮧**

---

It is possible that the UID of the user account on the Host and the CTE VM is different.  Make sure to generate or use an `.Xauthority` file for the appropriate user when logged in the each shell.

Determine the location of the `Xauthority` file on the host system.

```bash
user@host:~$ echo ${XAUTHORITY}
/run/user/1000/gdm/Xauthority
```
Determine your user account effective id in the CTE virtual machine.

```bash
user@host:~$ ssh cte "id -u"
1000
```

Map the host `Xauthority` file to the CTE virtual machine using a multipass directory mount.

```bash
user@host:~$ multipass mount /tmp/.X11-unix cte:/tmp/.X11-unix
```

Determine the host display number and IPv4 address to the virtual machine's multipass network.

```bash
user@host:~$ echo ${DISPLAY}
:1
user@host:~$ ip -c -br -4 addr show dev mpqemubr0 | awk '{print $3}' | cut -d/ -f1
10.223.79.1
```

---

**⮤ ⮤ ⮤ ⮤ ⮤**    *Above section incomplete*    **⮥ ⮥ ⮥ ⮥ ⮥**


## Multipass Orchestration

Multipass is an orchestration tool that stores vm instance configuration data in a json file regardless of underlying hypervisor.

- Linux - `/var/snap/multipass/common/data/multipassd/multipassd-vm-instances.json`
- Windows - `C:\Windows\System32\config\systemprofile\AppData\Roaming\multipassd\multipassd-vm-instances.json`
- MacOS - `/var/root/Library/Application Support/multipassd/multipassd-vm-instances.json`

There are a couple of environment variables you can set to control default configuration settings for vm creation under multipass.

```bash
SNAPCRAFT_BUILD_ENVIRONMENT_CPU=4
SNAPCRAFT_BUILD_ENVIRONMENT_MEMORY=8G
```

### Multipass on Windows using VirtualBox

You can still get access to the underlying virtualbox manager.

```dos
C:\> psexec.exe -s -i VirtualBox
```
