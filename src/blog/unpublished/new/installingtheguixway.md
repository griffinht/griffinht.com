uefi vs bios! absoluetlye lovely article! lovely blog!
https://joonas.fi/2021/02/uefi-pc-boot-process-and-uefi-with-qemu/

    https://guix.gnu.org/blog/2017/porting-guixsd-to-armv7/
    https://guix.gnu.org/cookbook/en/html_node/Guix-System-Image-API.html
    https://othacehe.org/the-guix-system-image-api.html
    https://www.mail-archive.com/help-guix@gnu.org/msg10916.html
https://github.com/techenthusiastsorg/awesome-guix
https://discourse.nixos.org/t/the-guix-system-image-api/9597/2
    https://guix.gnu.org/cookbook/en/html_node/Guix-System-Image-API.html
https://numtide.com/blog/we-dont-need-nixos-cloud-images-anymore-2/
link stumbles??
link that guix digital ocean blog article?
    https://guix.gnu.org/en/blog/2020/running-guix-system-on-a-linode-server/
todo reinstall racknerd

focus on highlighting how guix has solved your real problems! :)
# Installing Linux the Guix way
# Then talk about managing
# Managing my home server the Guix way
# Installing and updating my home server with Guix

# Installing with the guix installer

This can be done on any machine - no Guix installation needed (not host nor binary).

This approach is no fun! Especially when 

Guix allows 

```scheme
(operating-system
  (host-name "my-system")
  (bootloader (bootloader-configuration
                (bootloader grub-bootloader)))
```
# Installing to a vm

Also note you can often yank a drive with an operating installed, plug in in to a different computer, and boot the system with qemu /dev/sda - cool!

# Installing my server! add btrfs with a disk image

- create the image
- cp image /dev/sda
- cfdisk extend partition
- resize2fs ...

uefi may be different!

# Installing with `guix system init`

This what the Guix installer does (link docs) (link installer). In fact, you may see the installer source code at `` - it is nothing more than a highly specialized `operating-system` declaration.

# Installing on the target system with installation media



# Installing remotely

create installatino media
    give guix example
    use some other random distro

pipe image via ssh
or guix system init with sshfs???????????????????

# Updating

Now that we have installed our system, how can we update it? What if we want to change the `operating-system` declaration to change the timezone? add a disk? run docker? change the networking setup? add a user via ssh?

There are two ways
- from the live system manually with guix reconfigure
- guix deploy!
- or just manually tweaking things 
    - examples: /etc/fstab, ssh keys, docker herd services?

What if we wanted to simply reinstall the whole vm image? todo ci!
- actually this is a whole new article i think

`guix deploy`

But wait! What if we wanted to add docker? I know a friend who can do this
Before we `guix deploy`, why not test our changes?
Write a test which checks if docker is running on an ssh server at root@localhost:2222
launch the vm with qemu

# todo uefi with envy-laptop?




use chatgpt to create image definitions????



# what if i want to use guix but all i have is docker?
just guix pack lmao!


# vms
    probably a separate article

I'd like to create a virtual machine which I can use as a Docker host to run my containers. This would allow me to build and run my containers remotely via SSH. For example:

```sh
$ DOCKER_HOST=ssh://server docker run --rm -it hello-world
...
```
https://rendaw.gitlab.io/blog/172c58ea07ae.html#mainstream-technologies

https://rendaw.gitlab.io/blog/3c38052a1eb3.html#a-brief-guix-review

I plan on deploying this VM to a `VM server in my home lab` (link to setting up guix home lab vm host) which uses `libvirtd` to allow me to deploy my VMs to my home lab. You may consider `deploying a vm image to the cloud` (link to deploying images to cloud via guix deploy? or just general).

The old fashioned method would be starting with a pre-built image of Debian or Ubuntu, then SSHing in. From there, I would add my SSH key, disable SSH password login, update the system, install Docker, 
vagrantfile? terraform?

Nowadays there are shiny new tools like `cloud-init` to automate this drudgery. Infrastructure as code tools like Ansible, ..., exist to automate this drudgery. I've also briefly tried Fedora's CoreOS - an immutable distribution of Fedora which acts as a Docker container host, with automatic updates and more uhhh. CoreOs is distributed as an image, and can even be customized with Butane, a domain specific language (DSL). Unfortunately and I remember becoming frustrated when I attempted to configure a static IP address. It involved several lines of akward and brittle YAML to configured the underlying systemd networking stack - a rather leaky abstraction. I was also frustrated at how long it took to build and test my changes.

However, all these shiny new tools seem like mere patches over the original problem. Why can't I just make my own operating system image with all the bells and whistles I want, without any extras?

I'd like to create my own guest VM to use as a Docker host server to run my containers. I'd also like to be able to access it via SSH with my personal SSH key.

the old way
https://earlruby.org/2023/02/quickly-create-guest-vms-using-virsh-cloud-image-files-and-cloud-init/

`cloud-init` appears to be an antiquated hack for when creating a custom image is too difficult. 

As of [this patch](https://issues.guix.gnu.org/65842), the default image type appears to be `--image-type=mbr-hybrid-raw`, which uses the `mbr-hybrid-disk-image` defined in the `(gnu system image)` module [source](todo). I believe that means the following two code segments are basically the same.

Using [`guix system image`](https://guix.gnu.org/manual/en/html_node/Invoking-guix-system.html#index-image_002c-creating-disk-images):

```shell
$ guix system image --image-type=mbr-hybrid-raw my-os.scm
```

Internally, this is line 229 of image.scm todo link
Could this be documented better?
Reading the source code shows how qcow2 is merely an `mbr-hybrid-disk-image` but using the `compressed-qcow2` format instead of `disk-image`, the default for `mbr-hybrid-disk-image`.

Or with an [image declaration](https://guix.gnu.org/manual/en/html_node/image-Reference.html):

`my-image.scm`

```scheme
(use-modules (gnu)
             (gnu image)
             (gnu system image))
(image
  (format 'disk-image)
  (operating-system %my-system)
  (partitions (image-partitions mbr-hybrid-disk-image)))
```

Build the image like this:

```bash
$ guix system image my-image.scm
```

The image can also be inspected like this:

```bash
$ fdisk -l "$(guix system image my-image.scm)"
Disk /gnu/store/5vxmd3xqj3gzwzgwdzgia1jlpdw6211y-disk-image: 4 GiB, 4292415488 bytes, 8383624 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x00000000

Device                                                  Boot Start     End Sectors Size Id Type
/gnu/store/5vxmd3xqj3gzwzgwdzgia1jlpdw6211y-disk-image1       2048   83967   81920  40M ef EFI (FAT-12/16/32)
/gnu/store/5vxmd3xqj3gzwzgwdzgia1jlpdw6211y-disk-image2 *    83968 8383623 8299656   4G 83 Linux
```

# Customizing the image
How can the image be customized? Let's add a swap partition.

I'd like to add a swap partition to my VM. While I don't think this can be accomplished via [`guix system image`](guix system image doc), it can 
I think this is mostly the same as this:

```scheme
(use-modules (gnu)
             (gnu image)
             (gnu system image))
(image
  (format 'disk-image)
  (operating-system %my-system)
  (partitions (image-partitions mbr-hybrid-disk-image)))
```

```bash
$ guix system image my-image.scm
```

An aside:
blockquite?
Can I make a `qcow2` image? Is it better than this?
[this](https://serverfault.com/questions/677639/which-is-better-image-format-raw-or-qcow2-to-use-as-a-baseimage-for-other-vms)






Here is the definition of the `mbr-hybrid-disk-image`. I'd like to add a swap partition to that `partitions` list we see defined here.

[`gnu/system/image.scm`](todo link)
```scheme
(define mbr-hybrid-disk-image
  (image-without-os
   (format 'disk-image)
   (partition-table-type 'mbr)
   (partitions
    (list esp-partition root-partition))))
```

I have very limited knowledge of Scheme and Guile, so I think my first approach is to simply copy this declaration, then add the swap partition to the `partitions` list. This shouldn't be too difficult, especially since `esp-partition` and `root-partition` are both defined (and exported) in `(gnu system image)`. That means I should be able to copy this declaration to `my-image.scm` without any trouble.

`my-image.scm`
```scheme
(image
  (format 'disk-image)
  (operating-system %system)
  (partitions (image-partitions 
                (image-without-os
                 (format 'disk-image)
                 (partition-table-type 'mbr)
                 (partitions
                  (list esp-partition root-partition))))))
```

This works. It was at this time that I realized that there is no way to currently define a swap partition with the Guix image API - per the [`partition` reference](https://guix.gnu.org/manual/en/html_node/partition-Reference.html) the only supported file systems are "vfat", "fat16", "fat32" and "ext4". This means I will have to create my swap partition with


how to add a swap partition - guix currently doesn't support
can do with regular fdisk/parted/mount/mkswap
partition initializer -> maybe with initialize-root-partition????? gnu/build/image.scm <- cool!








Wow we did it!:

todo
```bash
$ fdisk -l "$(guix system image my-image.scm)"
todo
```


todo link to the blog of the person who implemented this
https://guix.gnu.org/cookbook/en/guix-cookbook.html
https://guix.gnu.org/cookbook/en/html_node/Guix-System-Image-API.html



todo guix system image has no docs on --image-type
https://issues.guix.gnu.org/65842
https://othacehe.org/
