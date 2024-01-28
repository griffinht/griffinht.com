todo locking down racknerd? does setting a root password protect against vnc access? vnc bruteforce?


https://guix.gnu.org/cookbook/en/html_node/Running-Guix-on-a-Linode-Server.html
https://stumbles.id.au/getting-started-with-guix-deploy.html

todo we vs I, `ssh` vs SSH
# Installing Guix without Guix on a cheap RackNerd VPS
# todo install Guix on envy-laptop or rpi
# Installing a custom operating system on a cheap Racknerd VPS

(Guix)[https://guix.gnu.org/] is a fascinating operating system which I have been experimenting with in various forms on my laptop and home servers. Today I wanted to try installing Guix on a virtual private server I had laying around. Previously I had been semi-automatically managing this server with a [collection of shell scripts and an Ansible playbook](https://griffinht.com/git/hot.git/tree/infrastructure/vps?id=f42fb6ad0315d956ed657c609d8d2052f810198e). However, after 8 months of managing my Arch Linux laptop with [Guix home](https://guix.gnu.org/en/blog/2022/keeping-ones-home-tidy/), I was ready to try a whole system.

The challenge today will be installing `guix` without the normal method of plugging in a removable ISO, then booting to an installation screen, then having the system install itself to the host. Instead, we will be installing to a RackNerd machine.

Racknerd is a provider of various cloud services, including a very affordable virtual private server offering. I am personally using their $10.28/year special offer as advertised by [a blog post by LowEndBox](https://lowendbox.com/blog/black-friday-recap-racknerd-kvm-vps-offers-in-multiple-locations-from-10-28-year/). So far the service has been working well - I get 10 GB of SSD storage, 768 MB of RAM, and a dedicated IPv4 address with 1000GB of monthly network bandwidth at 1 Gbps. The only caveat I have found is Racknerd does not provide a method to install a custom operating system, unless you contact their support. I thought it would be fun to see if I could install my Guix system without pestering support using the built-in "Rescue Mode" found within the control panel.

Let's start by selecting a random starting operating system for our VPS from the RackNerd control panel. I chose Debian, but we don't actually even have to `ssh` in to this system. Instead, log in to the control panel and select the Rescue button. Then, enable "Rescue Mode". This will shut down the Debian VPS and boot a rescue machine, accessible via `ssh` at the same address as the regular system. The new `ssh` server is secured by a password, which is shown on the control panel.

TODO show reset button

Let's `ssh` in to the new rescue machine. If you have already logged in to the VPS, then make sure to delete any old entries in your `~/.ssh/known_hosts` file. Otherwise, `ssh` will complain about a possible man-in-the-middle attack. This is because the new machine shares the same address as the old server, but has a completely different `ssh` fingerprint.

```
$ ssh root@my-vps
Warning: Permanently added 'my-vps' (RSA) to the list of known hosts.
root@my-vps's password: 
Linux rescue 4.9.0-4-amd64 #1 SMP Debian 4.9.65-3 (2017-12-03) x86_64

rescue # 
```

Poking around we find what appears to be a rather old Debian 9.3 system with a few special utilities installed.

```
rescue # hostnamectl
   Static hostname: rescue
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 67ecf2e2253a4d5d860f86b543faafc7
           Boot ID: bee21dc2ea4a417981adea2c7ca30645
    Virtualization: kvm
  Operating System: Debian GNU/Linux 9 (stretch)
            Kernel: Linux 4.9.0-4-amd64
      Architecture: x86-64
rescue # lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sr0     11:0    1  1024M  0 rom  
vda    254:0    0    10G  0 disk 
├─vda1 254:1    0 501.6M  0 part 
└─vda2 254:2    0   2.8M  0 part 
vdb    254:16   0   1.1G  0 disk 
└─vdb1 254:17   0   1.1G  0 part /
```

Checking the results of `lsblk`, we see the rescue system is mounted on `/dev/vdb` with a paltry `1.1G` of storage. My old VPS is still on `/dev/vda`. If I wanted, I could `mkdir mnt && mount /dev/vda1 mnt` to poke around the existing Debian system from the rescue machine. However, today I plan on wiping the whole thing to install Guix.

First, let's generate our system image, which will be installed to the VPS. The fully declarative nature of Guix means I can define a fully bit-for-bit reproducible operating system with a few lines of Guile code.
[12.2 `operating-system` reference](https://guix.gnu.org/manual/en/html_node/operating_002dsystem-Reference.html)

`bootstrap.scm`
```
(use-modules (gnu))
(use-service-modules networking ssh desktop)
(use-package-modules bootloaders ssh)

(operating-system
 (host-name "my-vps")
 (timezone "Etc/UTC")
 (bootloader (bootloader-configuration
              (bootloader grub-bootloader)))
 (file-systems %base-file-systems)
 (services
  (append (list (service dhcp-client-service-type)
                (service openssh-service-type
                         (openssh-configuration
                          (openssh openssh-sans-x)
                          ;; allow root login (disabled by default) but not with a password
                          (permit-root-login `prohibit-password)
                          (authorized-keys
                           ;; authorize our public ssh key with the root user
                           `(("root" ,(local-file "id_ed25519.pub"))))))
               ; make shutdown and reboot work
               (service elogind-service-type)) 
          %base-services)))
```

Make sure you place your public ssh key in the same directory as `bootstrap.scm`. This will allow you to log in to the root user without setting a password.

Let's create our image file with the following command, as documented in [the manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-system.html#index-image_002c-creating-disk-images).

```
$ guix system image --image-type=efi-raw bootstrap.scm
...
building /gnu/store/8c38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv...
\builder for `/gnu/store/8c38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv' failed with exit code 1
build of /gnu/store/8c38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv failed
View build log at '/var/log/guix/drvs/8c/38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv.gz'.
guix system: error: build of `/gnu/store/8c38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv' failed
```

Unfortunately this yields a weird build error:

```
$ gunzip < /var/log/guix/drvs/8c/38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv.gz
/gnu/store/q83biigb6w16j2a0yw6qv65h3il6ckmz-grub-2.06/sbin/grub-bios-setup: error: failed to get canonical path of `tmpfs'.
Backtrace:
           2 (primitive-load "/gnu/store/vzcrkrbwwzxsp4pkj9f13zfjc2f?")
In ice-9/eval.scm:
    619:8  1 (_ #(#<directory (guile-user) 7ffff77f7c80> ("/gn?" ?) ?))
In ./guix/build/utils.scm:
    812:6  0 (invoke "/gnu/store/q83biigb6w16j2a0yw6qv65h3il6ckmz-g?" ?)

./guix/build/utils.scm:812:6: In procedure invoke:
ERROR:
  1. &invoke-error:
      program: "/gnu/store/q83biigb6w16j2a0yw6qv65h3il6ckmz-grub-2.06/sbin/grub-bios-setup"
      arguments: ("-m" "device.map" "-r" "hd0,msdos2" "-d" "." "images/image")
      exit-status: 1
      term-signal: #f
      stop-signal: #f
environment variable `PATH' set to `/gnu/store/rvgps5qd5l1b6j6pvw4m93f1ip5y53zl-genimage-15-1.ec44ae0/bin:/gnu/store/yr39rh6wihd1wv6gzf7w4w687dwzf3vb-coreutils-9.1/bin:/gnu/store/016lrymzc8a1rpx2p1app1awp2w2wlpk-findutils-4.9.0/bin:/gnu/store/bvbv5ra6x4gpiqlqi36iw8ii7qrrvpcn-qemu-minimal-7.2.4/bin'
```

Trying again with `--image-type=qcow2` seems to work. Note that I also discovered I could build with `--image-type=efi-raw` on my VPS without any issues, but I'm not exactly sure why. todo

```
$ guix system image --image-type=qcow2 bootstrap.scm
...
/gnu/store/z39g0vfbsdzyzi1x2n6my0qvfpc25ilw-image.qcow2
```

Our `qcow2` image is now available at `/gnu/store/z39g0vfbsdzyzi1x2n6my0qvfpc25ilw-image.qcow2`. We still need an `efi-raw` image for installation, so let's convert using `qemu-img` [source](https://docs.openstack.org/image-guide/convert-images.html).

```
$ qemu-img convert -f qcow2 -O raw /gnu/store/z39g0vfbsdzyzi1x2n6my0qvfpc25ilw-image.qcow2 image.img
$ fdisk -l image.img
Disk image.img: 1.58 GiB, 1692733440 bytes, 3306120 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x00000000

Device     Boot Start     End Sectors  Size Id Type
image.img1       2048   83967   81920   40M ef EFI (FAT-12/16/32)
image.img2 *    83968 3306119 3222152  1.5G 83 Linux
```

It worked! We can see our image has a small EFI partition at the beginning of the disk, as well as a primary bootable Linux partition which contains our system. I'm not 

todo mispell or dont define base file system what happens?
todo ext4 vs btrfs and how to do that from operating system?
todo efi vs no efi, mention different guix --image-type

qcow2
hybrid
efi only
bios only
iso9660 (no resize)

```
building /gnu/store/8c38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv...
\builder for `/gnu/store/8c38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv' failed with exit code 1
build of /gnu/store/8c38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv failed
View build log at '/var/log/guix/drvs/8c/38wdkr9pfs5mrdgi4p6k4pzg8g9kcy-disk-image.drv.gz'.
```

```
$ guix system image --save-provenance --image-type=qcow2
(outputs path to image)
$ qemu-img convert -f qcow2 -O raw my-image.qcow2 my-image.img
```

> I did try to install an iso9660 file and was successfully able to boot to the operating system. However, I wasn't able to expand the partition thanks the way the iso9660 specification works. Instead, my partition was stuck at whatever size the installation image, about 1.5G out of the 10G on my VPs. This does not make for a very usuably system. Normally installing with an iso9660 image is fine when the image is mounted to some kind of removable media, such as a flash drive. This is how many install their operating systems to physical machines - they take a thumb drive loaded with an iso9660 image and plug it in to their machine. Then, the installation disk installs itself to the main system's drive. However, we are writing directly to the drive which also removes the installation step we are already doing it

# Copying the disk image to the remote system

Armed with our disk image, let's copy it to the VPS via the rescue system with a clever invocation of `ssh`:

```
rescue # logout
$ ssh root@my-vps 'cat > /dev/vda' < my-image.img
```

This command will `ssh` in to the rescue machine, then run `cat > /dev/vda`. This has `ssh` send our `my-image.img` file to the remote server, outputting to `cat`, which writes to `/dev/vda`.

Once this completes we are ready to boot in to the system! However, let's first resize the disk partition to take up the entire disk.

# Expanding the partition and filesystem

The disk image only takes around 1.5GB of space initially. The system won't be able to use any more space unless the partition (and underlying filesystem) is resized. This must be done while the disk is not mounted, which means we should do this while in rescue mode before booting the new system.

## Expanding the partition

I like using `cfdisk`, but `fdisk` or anything else works fine here. `cfdisk` has a neat little "Resize" button which makes this process painless.

I found that the rescue system had an ancient version of `cfdisk` from util-linux 2.29.2. This version doesn't have the "Resize" button, which meant I had to manually delete the old partition, then create a new larger partition. Make sure the new partition is a primary partition with the same start sector, sector size, and [partition ID](https://en.wikipedia.org/wiki/Partition_type) (ID 83 for Linux). Don't forget to set the bootable flag (attribute 80), and if prompted, say yes to changing the existing ext4 signature.

```sh
rescue # cfdisk
...
Syncing disks.
```

## Expanding the filesystem

> if you used a non resizable file system (like `iso9660`), then this will not work!

The last step is to resize the actual filesystem contained within the partition. I will be using the `resize2fs` tool to resize my `ext4` filesystem, which Guix created from my operating declaration.

todo if i make btrfs then will guix make it btrfs???

```sh
rescue # resize2fs /dev/vda2
resize2fs 1.43.4 (31-Jan-2017)
Resizing the filesystem on /dev/vda2 to 2610944 (4k) blocks.
The filesystem on /dev/vda2 is now 2610944 (4k) blocks long.
```

Success! If I wanted to ensure everything worked from the rescue machine, then I could have tried mounting the `/dev/vda2` partition, then checked the size with something like `df -Th`.

# Booting the new system

From the RackNerd control panel I disabled "Rescue Mode" and the system booted to my new system without a hitch.

# Managing the system from the control panel

Why doesn't the shut down button work? This is we forget the `elogind-service`
                                
(use-service-modules desktop)
(service elogind-service-type)

# Managing the Guix system

Guix allows us to do a bunch of neat things with the new system.

introduce guix deploy briefly here, then link to a full blog post somewhere idk or just the manual refernce not everything needs a blog post lol
Let's redeploy 

```
$ guix deploy deploy.scm
...
guix deploy: successfully deployed my-vps
```

It's also a good idea to make sure the system is still able to boot. Let's reboot now:

```
$ herd reboot shepherd
You must be kidding.
```

Just kidding, the (manual)[https://www.gnu.org/software/shepherd/manual/html_node/Invoking-reboot.html] clearly states the correct command to use:

```
$ herd stop shepherd
root@my-vps ~# Connection to my-vps closed by remote host.
Connection to my-vps closed by remote host.
Connection to my-vps closed.
```

The system should come back online momentarily. We can also shut down the system ((manual)[https://www.gnu.org/software/shepherd/manual/html_node/Invoking-halt.html]) with the following command:

```
$ herd power-off shepherd
Connection to my-vps closed by remote host.
Connection to my-vps closed.
```

To get our system back online, we will have to boot from the RackNerd control panel. Also note that RackNerd still thinks we are running Debian, and the reboot button doesn't seem to work anymore. The boot button does still work without any problems.




https://stumbles.id.au/getting-started-with-guix-deploy.html
https://guix.gnu.org/cookbook/en/html_node/Running-Guix-on-a-Linode-Server.html
