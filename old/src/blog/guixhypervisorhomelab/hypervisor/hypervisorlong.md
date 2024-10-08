`qemu`
Qemu
libvirt@hypervisor ~$
use hypervisor as host?

https://search.marginalia.nu/search?query=homelab+vm+hypervisor&js=&adtech=&profile=&recent=

sshd vs ssh? libvirtd vs libvirt
am i sure i didn't already make a post about this lol
https://news.ycombinator.com/item?id=27006354


# todo find other people doing this with guix or nix
https://joekarlsson.com/2023/09/how-to-get-started-building-a-homelab-server-in-2024/

# features

Starting with the 10 year old desktop I have, I'd like to:
- run any operating system
    - remote management
        - ssh
        - libvirt
            - virt-manager
            - virsh
    - wireguard
        - why not in a vm?
    - bridge networking
        - one physical device, multiple network interfaces? ips?
        - basically as if i had multiple physical devices attached to my local network
    - KVM
    - disk array

# non feeature
- peristent storage

# principles
i'd like to try to follow the principle of least power. For example, I could run a web server directly from the hypervisor, but I could also run the web server in a VM on the hypervisor. I'd prefer the latter, todo more examples
look at ovirt proxmox and see what they do that i want to offload

# Overview

why not truenas, freenas? unraid? debian? proxmox? ovirt? idk there are a bunch of others

Previously I had been running plain old Debian, and was mostly used it as a Docker container host (runtime? daemon?).

I probably could have followed the [debian wiki](https://wiki.debian.org/KVM) and gotten a very similar setup, but I wanted to use Guix.

I like this new setup much better than the old one

I want a machine that can run any operating system as a virtual machine. I want to manage the machine remotely. I also don't want to manage the machine - I want updates and things to happen magically idk. I also want the machine to manage networking (each VM gets a real IP address on my LAN0 and storage (two hard drives in btrfs raid1).

Instead of having to pick a decent operating system, I could simply have all of them. Installing Debian and CoreOS wouldn't mean I had to physically pick a machine I had laying around and install the operating system - I could do everything from one host and without being physically present! 

## network

I also still wanted to be able to have multiple network addresses on my LAN. This meant that each VM would have its own MAC address and link-local IP address, which I could then manage from my router, just like if the machines were physically connected to the network.

## storage

It would also be nice to centrally manage storage. I have a BTRFS drive array which I store all my persistent data to todo.

# Background

I was looking to improve my home server. Previously I had been running Debian, which was fine. System maintenence was mostly as easy as `apt update && apt upgrade`, and I ran everything in Docker. Debian also seems to support virtualization just fine (link to setting up debian as a hypervisor?)

After about a year of managing my user profile/home with Guix todo link, I figured I might as well do the same with my Debian system. Previously, I had been managing things with a series of shell scripts and a bit of Ansible. This was a pain to maintain, and impossible to test. If I ever wanted to reinstall Debian, then I'd have to take a brittle collection of shell scripts and work my way through the installation process. This would start with me putting the Debian installer on a flash drive, and bootstrapping the headless server by plugging in a display and keyboard. Then I would have to copy my SSH key over, either via the network or a flash drive, then finally start executing a bunch of `apt install` and editing a bunch of random system configuration files idk. This is the imperative way (i think). Guix allows me to do all of the declaratively.

Debian provides a variety of installation options https://www.debian.org/distrib/, but I don't really like any of them

At one point I even went through the trouble of setting up Debian's preseed thing with a bunch of (a soup?) shell scripts and Ansible things and the whole think was just mostly painful. I am all for treating my servers like cattle and not pets, which is why I only back up my application data and not the entire system. todo clarify why this isn't bad. I still dreaded the idea of having to restart from scratch idk

## Bootloader

My motherboard is 10 years old and does not appear to support fancy UEFI booting. Thus, I will be using BIOS? terminlogy?

```scheme
(bootloader (bootloader-configuration (bootloader grub-bootloader)))
```

If curious, here is an example for efi booting, and here is an example of idk

## File systems

The machine I have contains an SSD, as well as two hard drives which I have rurnning a btrfs raid0 thing

I'll be using the SSD as a boot drive and the two drives for storing most other data.

```scheme
 (file-systems (cons*
                 (file-system
                   (mount-point "/")
                   (type "ext4")
                   (device (file-system-label "Guix_image"))) ; the image we will produce later has this label by default
                 (file-system
                   (mount-point "/mnt/btrfs_data")
                   (type "btrfs")
                   (options "compress=zstd")
                   (device (file-system-label "btrfs_data"))) ; i'll be setting this label when I partition the hard drives
```

Here is the `/etc/fstab` which the above will produce:
```
# This file was generated from your Guix configuration.  Any changes
# will be lost upon reboot or reconfiguration.

LABEL=Guix_image	/	ext4	defaults	
LABEL=btrfs_data	/mnt/btrfs_data	btrfs	compress=zstd	
```

todo kind of random
I'll be formatting the two hard drives once I have the system installed and running, in [this section?](#installing-the-system)

## sshd

For remote access, I'll be using ssh.

```scheme
(service openssh-service-type
         (openssh-configuration ; check out the defaults here: https://guix.gnu.org/manual/en/html_node/Networking-Services.html
          (openssh openssh-sans-x) ; the openssh package comes with some x window system things we don't need
          (permit-root-login `prohibit-password)
          (password-authentication? #f)
          (authorized-keys
           `(("root" ,(local-file "id_ed25519.pub"))))))
```

What is `id_ed25519.pub`? It is merely a file in the same directory as this operating system declaration we have been writing. It contains my personal SSH public key.

`id_ed25519.pub`
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILlrXoJEmDX/hi1wvH3M2NNYm2saKxrC+ELNyt3v1pBI griffin@cool-laptop
```

If you don't want a separate file for this, then try (plain-text....

todo find other examples of this?

If you'd like, consider (plain-text guix gexp idk

## Wireguard

I wanted to run WireGuard on the host machine. I could have put it on a guest VM, but figured their might be too many moving pieces with all the networking configuration, and Guix makes it so easy to configure.

```scheme
insert wireguard config
```

Theoretically I could have skipped this and exposed `sshd` on port 22 to the world, but I didn't want to do that. links?


# Final system configuration:

```
dont forget this!
(service elogind-service-type) ; makes things like the power button work
```

# Testing out the system

`guix system vm system.scm`

also add ssh port forwarding
We can see the system is complaining about the missing drives when attempting to mount them. No worries!

# Generating the system image

todo

# Installing the system

I could use any kind of "live cd"/system installer to boot to the system and copy the image to the drive. This is a great approach for some cloud/VPS environments, and is how I installed Guix to a Racknerd VPS (todo link).

I could also install Guix with the Guix installer, then reconfigure the default Guix system installation to ours.

However, it is easiest for me to make a disk image out of our system declaration, then simply plug in in the system's SSD to my laptop with this handy USB sata adapter I shucked from a WD Easystore.
run on lol

### booting the old system for fun

I previously ran Debian on the old system. Just for fun, I can boot this system from my laptop with `qemu`. This also makes me more confident that the new Guix system will boot, todo

With the SSD plugged in, I can make sure the . If the old system 

```
$ cp image /dev/sdx
$ sync
```

Once copied over, don't forget to resize both the partition and the ext4 filesystem. I like `cfdisk` (link?) because it has a nice TUI interface, which is much more friendly than plain old `fdisk`.

```sh
$ cfdisk
```

I chose to use `ext4` when I [configured the file systems](#File-systems). The tool to resize the underlying `ext4` filesystem to fill my newly expanded partition is `resize2fs`.

```sh
$ guix shell?
$ resize2fs
```

# Accessing the system

With the SSD plugged in and the system booted, I can finally `ssh` in:

I can also see which DHCP address my system took. I also took the liberty of assigning a static DHCP lease . Alternatively, one could have configured static networking with network manager or without but then libvirt no work idk

```sh
$ ssh 192.168.0.5
```

Note that if the system was inaccessible via `ssh`, I could plug a display and keyboard in to the physical box and log in as root with an empty password (configure a password here if you want, but this only really protects against local access, but at that point you already have the whole system, but maybe consider disk encryption?)

If I wanted to reboot, I could (unintuitively)

todo link guix reboot manual

```sh
$ herd stop root?
ssh connection closed
```

# Partitioning the disks

Now with the system up and running, I can creaate my btrfs array. I picked btrfs over ext4 because I wanted some redundancy against a hard drive failure, which I think will be the most common form of data loss. Redundancy would save me from restoring from a backup. I picked btrfs over zfs because I think btrfs is great for tiny JBOD (link) setups like mine, where I might want to add an oddly sized disk to the array, which might be difficult with zfs run on lol. zfs also isn't implemented by Guix thanks to some licensing free software issues todo link issue. Not to say Guix can't support zfs, and in fact support has nearly been added by bruh link.

```sh
here is how i partitioned the drives
$ lsblk
...
$ # we will need some btrfs helper programs, which guix provides in the btrfs-progs package
$ guix shell btrfs-progs
...
$ mkfs.btrfs bruh
```

# Updating the system

## `guix deploy`
Say you wanted to update the system, add an SSH or Wireguard key, or add a new system service ([manual](https://guix.gnu.org/manual/en/html_node/Services.html)). Update `system.scm` and use `guix deploy` to (insert what guix deploy does)

```sh
$ guix deploy deploy.scm
```

## old fashioned way

Let's say you don't want to use `guix deploy` (why don't you want to use `guix deploy`?). Maybe the system you are using doesn't have Guix installed (Guix can be installed on top of many Linux systems, like Debian! https://guix.gnu.org/manual/en/html_node/Installation.html )

```sh
$ ssh mysystem
$ guix update???
$ herd restart??
```




# libvirt

Now that everything is set up let's try to spin up a VM.

```
Unable to complete install: 'Failed to connect socket to '/var/run/libvirt/virtlogd-sock': No such file or directory'
```



[manual](https://guix.gnu.org/manual/en/html_node/Virtualization-Services.html)

We forgot virtlogd, which Guix provides with the `virtlog-service-type`.

```scheme
(service virtlog-service-type)
```

One quick `guix deploy deploy.scm` from my laptop and we can try again:

```
Unable to complete install: 'Cannot get interface MTU on 'br0': No such device'
```

I used a nonexistant bridge device. Let's create a bridge. 
NetworkManager makes this whole process very easy. I like using `nmtui` from the terminal. A bridge can be created from the "Edit a connection" menu.

We need a bridge. Also make a bridge slave with the ethernet device todo
https://guix.gnu.org/cookbook/en/html_node/Network-bridge-for-QEMU.html#Configuring-the-QEMU-bridge-helper-script

`hot-desktop`
```sh
root@hot-desktop ~# nmcli con add type bridge con-name br0 ifname br0
root@hot-desktop ~# nmcli con add type bridge-slave ifname enp2s0 master br0
```

Let's try again:

```
Unable to complete install: 'internal error: qemu unexpectedly closed the monitor: qemu-system-x86_64: -no-hpet: warning: -no-hpet is deprecated, use '-machine hpet=off' instead
2024-01-16T00:54:03.810893Z qemu-system-x86_64: -blockdev {"driver":"file","filename":"/root/gkfpsjjw0xps6gvjvw3jpnlb2z5kzhqp-disk-image","node-name":"libvirt-1-storage","auto-read-only":true,"discard":"unmap"}: Could not open '/root/gkfpsjjw0xps6gvjvw3jpnlb2z5kzhqp-disk-image': Permission denied'
```

A quick `ls -l` shows I forgot to mark my disk image as writable.

```
root@hot-desktop ~# ls -l
total 1951812
-r--r--r-- 1 root root 1998647296 Jan 15 22:03 gkfpsjjw0xps6gvjvw3jpnlb2z5kzhqp-disk-image
root@hot-desktop ~# chmod +w gkfpsjjw0xps6gvjvw3jpnlb2z5kzhqp-disk-image 
root@hot-desktop ~# ls -l
total 1951812
-rw-r--r-- 1 root root 1998647296 Jan 15 22:03 gkfpsjjw0xps6gvjvw3jpnlb2z5kzhqp-disk-image
root@hot-desktop ~# 
```

Fixing this I still had the issue, the solution was both ensuring writable and copying to /var/lib/libvirt/images
todo rootless stuff
https://github.com/jedi4ever/veewee/issues/996



```
Viewer was disconnected.
Encountered SPICE error-link

SSH tunnel error output: sh: line 1: nc: command not found
```

The issue here is clear: we need netcat!

```sh
root@hot-desktop ~# guix install netcat
```

I found I had to reconnect libvirt after installing. guix install requires guix profile to be resourced, which is accomplished by reconnecting libvirt 

Also consider how I could have added `netcat` to my operating system declaration, then reconfigured and reconnected.

`system.scm`
```scheme
(packages
  (append (list netcat)
          %base-packages))
```


The "NIC" entry of the "Show virtual hardware details" menu shows a MAC address, but the IP address is "Unknown". What gives?

```sh
root@hot-desktop ~# ip a
...
12: br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 1e:69:53:53:75:8a brd ff:ff:ff:ff:ff:ff
...
root@hot-desktop ~# nmcli
enp3s0: connected to Wired connection 1
        "Realtek RTL8111/8168/8411"
        ethernet (r8169), FC:AA:14:B0:1B:64, hw, mtu 1500
        ip4 default
        inet4 192.168.0.5/24
        route4 192.168.0.0/24 metric 100
        route4 default via 192.168.0.1 metric 100
        inet6 fe80::b1f1:c5fb:924a:718e/64
        route6 fe80::/64 metric 1024

lo: connected (externally) to lo
        "lo"
        loopback (unknown), 00:00:00:00:00:00, sw, mtu 65536
        inet4 127.0.0.1/8
        inet6 ::1/128

wg0: connected (externally) to wg0
        "wg0"
        wireguard, sw, mtu 1420
        inet4 10.0.0.2/32
        route4 10.0.0.9/32 metric 0

br0: connecting (getting IP configuration) to br0
        "br0"
        bridge, 1E:69:53:53:75:8A, sw, mtu 1500

vnet6: unmanaged
        "vnet6"
        tun, FE:54:00:3D:81:FF, sw, mtu 1500

DNS configuration:
        servers: 192.168.0.1 166.102.165.13 207.91.5.20
        interface: enp3s0

Use "nmcli device show" to get complete information about known devices and
"nmcli connection show" to get an overview on active connection profiles.

Consult nmcli(1) and nmcli-examples(7) manual pages for complete usage details.
```

Looks like our bridge isn't quite working.
https://wiki.archlinux.org/title/network_bridge

Rebooting seemed to fix things lol

```sh
root@hot-desktop ~# herd stop root
Connection to hot-desktop.wg.griffinht.com closed by remote host.
Connection to hot-desktop.wg.griffinht.com closed.
```

```sh
root@hot-desktop ~# nmcli
br0: connected to br0
        "br0"
        bridge, FC:AA:14:B0:1B:64, sw, mtu 1500
        ip4 default
        inet4 192.168.0.5/24
        route4 192.168.0.0/24 metric 425
        route4 default via 192.168.0.1 metric 425
        inet6 fe80::970:fd84:ffb7:c66/64
        route6 fe80::/64 metric 1024

lo: connected (externally) to lo
        "lo"
        loopback (unknown), 00:00:00:00:00:00, sw, mtu 65536
        inet4 127.0.0.1/8
        inet6 ::1/128

wg0: connected (externally) to wg0
        "wg0"
        wireguard, sw, mtu 1420
        inet4 10.0.0.2/32
        route4 10.0.0.9/32 metric 0

enp3s0: connected to bridge-slave-enp3s0
        "Realtek RTL8111/8168/8411"
        ethernet (r8169), FC:AA:14:B0:1B:64, hw, mtu 1500
        master br0

DNS configuration:
        servers: 192.168.0.1 166.102.165.13 207.91.5.20
        interface: br0

Use "nmcli device show" to get complete information about known devices and
"nmcli connection show" to get an overview on active connection profiles.

Consult nmcli(1) and nmcli-examples(7) manual pages for complete usage details.
```

I think this is what 
https://wiki.archlinux.org/title/network_bridge#With_NetworkManager
accomplishes without rebooting

Anyways I found that I had to wait ~30 seconds for the VM to get an IPv4 address.
disable stp from nmtui

I found I had to reboot the VM host for the changes to go in to effect.

https://www.happyassassin.net/posts/2014/07/23/bridged-networking-for-libvirt-with-networkmanager-2014-fedora-21/




todo link to iaac

# accessing libvirt remotely via `ssh`

Assuming I can log in to my hypervisor via `ssh` with `ssh root@host`, then I can use the following URI to connect to libvirt:

```
qemu+ssh://root@host/system
```

[reference](https://libvirt.org/uri.html)

This URI can be passed to tools like `virsh`:

```
virsh --connect qemu+ssh://root@host/system
```


I like using [`virt-manager`](https://virt-manager.org/), which is a nice GUI for managing virtual machines with libvirt. All I need to do is `File` > `Add connection...` and I get a prompt to configure the connection URI.

screenshot here

# system vs session

What is that `/system` in the URI? This has the program connect to the `system` hypervisor, as opposed to the `session` hypervisor. What's the difference? Which one do I want?
https://blog.wikichoon.com/2016/01/qemusystem-vs-qemusession.html
https://wiki.libvirt.org/FAQ.html#what-is-the-difference-between-qemu-system-and-qemu-session-which-one-should-i-use

session can't be autostarted

# rootless

All I want is to be able to create and destroy some virtual machines. Do I really need. What if I wanted to have some other system (maybe a continuous deployment server) manage some virtual machines. Do I really need to provide full root access?

This technique is also common on the desktop, where the user may want to run some virtual machines without root access.

[ref](https://blog.wikichoon.com/2016/01/qemusystem-vs-qemusession.html)
[ref](https://wiki.libvirt.org/SSHSetup.html#verify-it-works)


## creating a non root user

Currently, our hypervisor only has the root user. Let's make a user called `` and add my `ssh` key.

`system.scm`

```scheme
 (users
   (append
     (list
       (user-account
         (name "libvirt")
         (group "users")))
         ;(supplementary-groups
         ;  (list "libvirt")))
     %base-user-accounts))
```

```scheme
 (openssh-configuration
  ...
  (authorized-keys
   `(("root" ,ssh-public-key)
     ("libvirt" ,ssh-public-key))))
```

Let's update the hypervisor with the new configuration:

```sh
$ guix deploy deploy.scm
```

> hey! the root user and regular user have the same ssh key! yes, but imagine the regular user having the ssh key of a continuous deployment server or unprivileged developer machine

I can now use something like `virsh` to test out the connection:

```sh
$ virsh --connect qemu+ssh://libvirt@host/system
error: failed to connect to the hypervisor
error: End of file while reading data: virt-ssh-helper: cannot connect to '/var/run/libvirt/libvirt-sock': Failed to connect socket to '/var/run/libvirt/libvirt-sock': Permission denied: Input/output error
```

We tried to connect to the system `libvirtd` as a regular user. I could allow this by adding my `libvirt` user to the `libvirt` group [docs](), but the whole point of this setup is to run with minimal privileges. All we have done so far is create a regular old Linux user called `libvirt` todo use `my-user` instead? I'd rather not expose the privileged system `libvirtd` to this user (why not, what security isses? compare to docker).

```sh
$ virsh --connect qemu+ssh://libvirt@host/session
Welcome to virsh, the virtualization interactive terminal.

Type:  'help' for help with commands
       'quit' to quit

virsh # 
```

# KVM setup

It worked! Let's try making a VM. I'm also going to switch to `virt-manager` at this point because I like the GUI. I got a warning when trying to create a new VM that KVM was not working on the libvirt user session. Let's verify with `virsh`:

```sh
$ virsh --connect qemu+ssh://libvirt@host/session capabilities | grep kvm
$ virsh --connect qemu+ssh://root@host/system capabilities | grep kvm
      <baselabel type='kvm'>+65534:+984</baselabel>
      <domain type='kvm'/>
      <domain type='kvm'/>
```

We can see that the root system connection has KVM access, but the `libvirt` user session does not. We can fix this by adding our `libvirt` user to the `kvm` group:

```scheme
(user-account
 (name "libvirt")
 ...
 (supplementary-groups
   (list "kvm"))))
```

```sh
$ guix deploy deploy.scm
```

I found that after the `guix deploy` I had to restart the hypervisor for the changes to take effect. One reboot later and we have this:

```sh
virsh --connect qemu+ssh://libvirt@host/session capabilities | grep kvm
      <domain type='kvm'/>
      <domain type='kvm'/>
```

It's time to spin up a VM:

# Bridge networking setup

Everything works, but this VM is using usermode networking. This is fine, but I'd like to use the bridge network I created earlier. Tools like `ping` won't work with usermode networking todo blog post idk To accomplish this, I first stopped the VM then changed the configuration to use the bridge network. Starting the VM resulted in this error:

```
Error starting domain: '/usr/libexec/qemu-bridge-helper' is not a suitable bridge helper: No such file or directory
```

Using the bridge network requires root privileges. `qemu` provides a workaround for this in the form of a helper program called `qemu-bridge-helper` ([qemu wiki](https://wiki.qemu.org/Features/HelperNetworking)). This allows us to make use of our bridge network without root privileges, by using a setuid program to set up privileged networking for us.

I wrote a blog post on the process of configuring and troubleshooting `qemu-bridge-helper` on a Guix system todo link, but the final result boils down to the following:

```scm
todo
```

Deploy the changes and it should work todo

# storage

how can my vms access that filesystem from earlier?

# Ditching the system daemon

libvirtd is the monolithic daemon of libvirt. This is being replaced by modular daemons. [](https://libvirt.org/daemons.html)

Remember that all we have done with libvirt is created a QEMU KVM virtual machine with bridge networking. This behaivior can be replicated with the following command:

No root privileges required! Why do we still need the monolithic system libvirt daemon?

[This section](https://libvirt.org/daemons.html#modular-driver-daemons) explains how the QEMU management daemon, `virtqemud`, can run in session mode. This makes sense, as we could run our VM as a simple invocation of `qemu-system-x86_64` with KVM acceleration and bridge networking with `qemu-bridge-helper`. 

so can we disable it??
```sh
$ virsh -c qemu+ssh://libvirt@hot-desktop.wg.griffinht.com/session list
error: failed to connect to the hypervisor
error: End of file while reading data: sh: line 1: virt-ssh-helper: command not found: Input/output error
$ ssh libvirt@host
~$ virsh -c qemu:///session list
virsh: command not found
~$ guix install libvirt
# after a guix install we will need to log out then log back in to get the new environment variables set up
~$ logout
$ ssh libvirt@host
~$ virsh -c qemu:///session list
 Id   Name   State
--------------------

~$ logout
$ virsh -c qemu+ssh://libvirt@hot-desktop.wg.griffinht.com/session list
```

We could also install `libvirt` system wide by adding it to the list of packages in the `operating-system` declaration.

It looks like the VM didn't start, so lets try starting it:

```sh
~$ virsh start myvm
error: Failed to start domain 'mystuff_dockervm'
error: Cannot check QEMU binary /run/current-system/profile/bin/qemu-system-x86_64: No such file or directory
~$ guix install qemu
~$ logout
```

Again, we could also declare `qemu` as a package in the list of the `operating-system` packages if we wanted to.

Anyways this doesn't work and i was getting another weird error and it might have to do with setuid so idk todo maybe



# Autostart

https://libvirt.org/daemons.html#architectural-options

VM autostart won't really work because the session daemon is not autostarted. This means that VMs will not start when the system starts, so a reboot would kill all your precious VMs. The session VMs will be started once the session daemon is started.

## Manually starting the session daemon

I found that merely connecting to the session daemon with something like `virsh -c qemu+ssh://libvirt@host/session` (or `virsh -c qemu:///session` if you were already logged in to the host) would automatically start whatever daemons where needed (`virtqemud` and `virtlogd`). This would also autostart all the VMs.

## Automatically starting the session daemon

https://www.libvirt.org/manpages/libvirtd.html#when-run-as-non-root
https://guix.gnu.org/blog/2020/gnu-shepherd-user-services/
https://guix.gnu.org/manual/en/html_node/Shepherd-Services.html


## securirt 1
how is this more secure than simply allowing root access?
isn't this like creating an unprivileged docker user then exposing the system docker daemon? effectively providing root?
what does this protect against?

https://wiki.libvirt.org/FAQ.html#what-is-the-difference-between-qemu-system-and-qemu-session-which-one-should-i-use
https://libvirt.org/daemons.html

## security
todo irrelevant now lol

https://libvirt.org/auth.html
https://libvirt.org/acl.html
Is this really more secure? For example, if the system Docker daemon was exposed to the user ([docs](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-usera)), then the user effectively has root-level privileges. This is different from "rootless" Docker ([docs](https://docs.docker.com/engine/security/rootless/), which does have security benefits. allow users to create and destroy containers without root access to the system.


https://libvirt.org/acl.html
https://wiki.libvirt.org/SSHSetup.html#verify-it-works

https://libvirt.org/kbase/secureusage.html
https://blog.wikichoon.com/2016/01/qemusystem-vs-qemusession.html


# exposing block devices 

https://wiki.archlinux.org/title/QEMU#Sharing_data_between_host_and_guest
