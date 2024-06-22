# Modular Libvirt daemons without `systemd`

I transitioned from having one rootful "monolithic" `libvirt` daemon.

Normally this is managed by systemd, but I am running things on a Guix machine [todo link to guix machine].

The original setup had one "monolithic" `libvirtd` daemon running as root, which I could connect to via SSH with `qemu+ssh://root@hot-desktop.lan.hot.griffinht.com/system`

```
(service lbivirt-service-type)
```

I also wanted to experiment running libvirt with the least possible privileges, so I created a completely unprivileged `libvirt` user on the Guix system. The only special privileges this user had was being part of the `KVM` group, which allowed it to take advantage of hardware acceleration with `KVM`. Note that I did not add this user to a `libvirt` group, which would have given the unprivilieged user access to the root `libvirtd` daemon. I now had no daemon to even give access to in the first place!

With the new setup, all I had to do was install the `libvirt` and `qemu` packages to the system, and I could now start and stop VMs via the following [libvirt Connection URI](https://libvirt.org/uri.html): `qemu+ssh://libvirt@hot-desktop.lan.hot.griffinht.com/session`.

This worked, but I found that I would "lose" my VMs after a while. I would log in, start a VM, log out, then log back in later and find that my VM was showing as not started, even though it was running. Trying to start the already running VM would result in an "unable to acquire lockfile" error, which makes sense because the VM was already running. 

The quick fix was to kill the `virtqemud` process (which also kills my VMs) and then log in again. This was annoying, as every time I wanted to check or restart a VM I had to restart every single VM on the hypervisor.

## Problem

todo show top
todo copy paste with colors? then put them here with ansi color?

Connecting via `qemu+ssh://libvirt@hot-desktop.lan.hot.griffinht.com/session`:

If there is no daemon running, some component of `libvirt` will automatically spawn the necessary modular daemons as needed. For example, logging in via `virt-manager` spawns `virtqemud`, `virtstoraged`, `virtnetworkd`, and `virtnodedevd`. Logging in via `virsh` spawns xyz. Starting a VM will spawn `virtsyslogd`. 

### Daemon timeouts

Each of these daemons are spawned with a timeout of 120 seconds, which will stop the daemon if there is no activity for 120 seconds. This is why I only experienced my issue after waiting at least 2 minutes after disconnecting. Before the 2 minute time period the daemons never timed out and everything was fine.

After starting a VM in `virt-manager`, the only daemons the VM needs to run are `virtqemud` and `virtsyslogd`. This means that logging out of `virt-manager` will result in the other 3 modular daemons (`virtstoraged`, `virtnetworkd`, and `virtnodedevd`) to time out and die after 2 minutes. Then, when logging back in to `virt-manager`, I found that it will ignore the already running `virtqemud` and create the 4 modular daemons again, duplicatoing `virtqemud` and causing any running VMs on the system to show as stopped. 

todo what about connecting locally via `libvirt://session` or whatever it is?

## Solution

The solution is to start `virtqemud` myself

todo why doesn't the `virtqemud` started by virt-manager work? whats the diff

```sh
virtqemud --daemon
```

This daemon should be started when the system starts, and it should run as my unprivileged `libvirt` user (no need to run as root!).


### Manual approach

```sh
ssh libvirt@hot-desktop.lan.hot.griffinht.com virtqemud --daemon
```

### systemd

First create a user systemd service to start the virtqemud daemon. Note that system

Then, to start the daemon without requiring the user to log in first, [enable user lingering](todo).

### Guix

We need to start a daemon which runs as the libvirt user when the system starts up. How can we do this on a Guix system?

shepherd todo


# Autostarting

Now that we have the `virtqemud` daemon starting automatically on startup, we should be able to actually start our VMs on startup.

## todo


logging
--daemon
by default libvirt logs to journald which doesn't exist
but journald doesn't exist so we have to redirect to syslog
