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
