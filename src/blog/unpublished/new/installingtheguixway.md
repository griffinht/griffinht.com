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

Nowadays there are shiny new tools like `cloud-init` to automate this drudgery. Infrastructure as code tools like Ansible, ..., exist to automate this drudgery. I've also briefly tried Fedora's CoreOS - an immutable distribution of Fedora which acts as a Docker container host, with automatic updates and more uhhh. CoreOs is distributed as an image, and can even be customized with Butane, a domain specific language (DSL). Unfortunately and I remember becoming frustrated when I attempted to configure a static IP address. It involved several lines of akward and brittle YAML to configured the underlying systemd networking stack - a rather leaky abstraction. I was also frustrated at how long it took to build and test my changes.

However, all these shiny new tools seem like mere patches over the original problem. Why can't I just make my own operating system image with all the bells and whistles I want, without any extras?

I'd like to create my own guest VM to use as a Docker host server to run my containers. I'd also like to be able to access it via SSH with my personal SSH key.

the old way
https://earlruby.org/2023/02/quickly-create-guest-vms-using-virsh-cloud-image-files-and-cloud-init/

`cloud-init` appears to be an antiquated hack for when creating a custom image is too difficult. 

```shell
guix system image --image-type=efi-raw my-os.scm
```

```scheme
(add-to-load-path (string-append (dirname (current-filename)) "/"))

(use-modules (my-bruh)
             (gnu)
             (gnu image)
             (gnu system image))
(image
  (format 'disk-image)
  (operating-system %my-system)
  (partitions (image-partitions efi-disk-image)))
```

# Customizing the image
I'd like to add a swap partition to my VM
I think this is mostly the same as this:

```shell
guix system image my-image.scm
```

```scheme
(add-to-load-path (string-append (dirname (current-filename)) "/"))

(use-modules (system)
             (gnu)
             (gnu image)
             (gnu system image))
(image
  (format 'disk-image)
  (operating-system %my-system)
  (partitions (image-partitions efi-disk-image)))
```

I have no idea what `image-partitions` is. It is only referenced in the [Instantiante an image](https://guix.gnu.org/manual/en/html_node/Instantiate-an-Image.html) documentation, but the only definition I could find were two lines in the source code. It is notably absent from the [Image reference](https://guix.gnu.org/manual/en/html_node/image-Reference.html) documentation, which only mentions.

todo link to the blog of the person who implemented this
https://guix.gnu.org/cookbook/en/guix-cookbook.html

The 

##### bad

```(scheme)
(partitions (list efi-disk-image))
```

##### good

```(scheme)
(partitions (image-partitions efi-disk-image))
```
