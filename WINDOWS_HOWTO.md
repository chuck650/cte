# Microsoft Windows HowTo

This HowTo will help you prepare Microsoft Windows for CTE.

---

## Requirements

Ansible control nodes can only run on Linux or MacOS computers, Windows is not supported as control node, but Windows can be managed by an Ansible control node.  Adiitionally, the CTE runs in a Linux environment, therefore you must have a running instance of Linux in order to install the CTE.

## Linux Options

You generally have three options for getting a running instance of Linux.

1. Run Linux as the primary OS on a physical platform.
2. Run Linux in a hypervisor that is running on a physical platform
3. Run Linux as a secondary OS on a physical platform where another OS the primary in a multi-boot configuration on a physical platform.

Multi-boot environments where Windows is the primary OS is not recommended due to the troubles often encountered with Windows not recognizing the secondary OS.

Running Linux as the primary OS is the easiest and often least troublesome option, but may not be an option for those that have a single system and require Windows for other tasks.  My preferred method when running Windows is to run Linux as my primary OS on the physical platform, and run Windows in a hypervisor as a virtual machine.

Most of you will probably opt for keeping Windows as your primary OS and run a Linux virtual machine in a hypervisor.  Here are your options in order of preference.

1. Use *Microsoft Hyper-V* and install Ubuntu Linux in a VM.
2. Use *Oracle Virtualbox* and install Ubuntu Linux in a VM.
3. Use *VMWare Player* and install Ubuntu Linux in a VM.

By far, Using Microsoft Hyper-V is the most efficient as Hyper-V is integrated into the Windows Kernel and will result in the best use of system resources and better stability of the running VM's.  Hyper-V is only available when you run the Pro or Enterprise editions of Windows, it will **not** run on Windows Home edition.

## Virtual Machine Requirements

Here are the requirements for the virtual machine that need to be configured within you hypervisor.  Your physical system needs to have sufficient resources to allocate these requirements to the hypervisor.

* 16 GiB of RAM
* 80 GiB of Storage
* One Internet accessible network interface that uses NAT

You may find your hypervisor has additional requirements to get Linux functioning, such as special device drivers.  Consult you hypervisor documentation and the Internet for help with these.

It may be possible to allocate as little at 8 GiB of RAM to the Linux virtual machine, but performance will likely suffer under some conditions when running multiple parts of the CTE simultaneously, as resource demand can be higher under certain scenarios.  Windows 10 **will** require a minimum of 8 GiB of RAM to maintain the stability of the system and the hypervisor.  Allocating less then 8 GiB of RAM will likely result in hypervisor instability, Windows instability, Windows locking up or a complete system crash.  **You have been warned!**

## Installing Linux with Multipass

One option is to download and install Multipass on windows, along with virtualbox, and use the multipass command line tool to install an Ubuntu cloud image on your Windows system.  Multipass will make most of the choices for you and setup a new Linux environment in a rather short amount of time.

[Multipass for Windows](https://multipass.run/docs/installing-on-windows "How to intall Multipass on Windows")

To configure Multipass to use the VirtualBox hypervisor and launch an instance of Ubuntu Eoan, enter the following commands.

```cmd
C:\WINDOWS\system32> multipass set local.driver=virtualbox
C:\WINDOWS\system32> multipass launch --name cte eoan
```
