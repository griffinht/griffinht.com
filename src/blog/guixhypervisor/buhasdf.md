am i sure i didn't already make a post about this lol
https://news.ycombinator.com/item?id=27006354


# todo find other people doing this with guix or nix


# Overview

why not truenas, freenas? unraid? debian? proxmox? idk there are a bunch of others

I want a machine that can run any operating system as a virtual machine. I want to manage the machine remotely. I also don't want to manage the machine - I want updates and things to happen magically idk. I also want the machine to manage networking (each VM gets a real IP address on my LAN0 and storage (two hard drives in btrfs raid1).

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

# Testing out the system

`guix system vm system.scm`

also add ssh port forwarding
We can see the system is complaining about the missing drives when attempting to mount them. No worries!

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
