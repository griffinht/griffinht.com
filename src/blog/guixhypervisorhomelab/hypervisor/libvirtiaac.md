GUIX DELPOT GUIX DEPLOY

# pipeline
ci somewhere builds and tests vms defined here, then publishes the resulting image to the web? or maybe i should do direct to machine first? hmmm idk


# needs
- iaac (declarative code)
- quick iteration
    test my changes as quickly (or quicker thanks to abstraction!, but **never** slower) as using the underlying tools
- monitoring 
    is my infrastructure deployed?
    
# iaac
todo also do one for network manager config?
like create bridge network that would be neat if i could automate that with a network manager service
terraform also uses BUSL license which seems stinky https://www.hashicorp.com/blog/hashicorp-adopts-business-source-license link hn?
https://sumit-ghosh.com/posts/create-vm-using-libvirt-cloud-images-cloud-init/

now that we have a hypervisor, let's spin up some vms!
`virt-manager` is a lovely GUI frontend for this type of work. what if I wanted to automate this? perhaps integrate with ci?
todo guix shepherd vs libvirt terraform

basically i want to define a set of virtual machines with various resources - storage, cpu, memory, networking (i want to set the mac address of the interface it will use) access to system resources like the disk array, 
the vm images will come from some place idk

https://news.ycombinator.com/item?id=39101828
iaac tools scare me. I think they are the source of the longest developer feedback loops and can quickly turn in to templating hell.
unless I need to practice RDD (resume-driven development todo link), then these tools have no place in my hypervisor. lets get guixy!

also specify kernel boot params???

https://registry.terraform.io/providers/dmacvicar/libvirt/latest/docs/resources/cloudinit

```scm
(virtual-machine
; https://libvirt.org/formatdomain.html
(libvirt-domain
 (cpu 2)
 (memory 2G)
 (storage 10G)
 (networking
  (mac-address ab:cd:ef:gd))
 (mount-points
   (btrfsarray)))
```



`virt-install` seems to be the move



# what we need:

get the disk/filesystem on the vm host
use a 

```sh
virt-install --import --disk/--filesystem
```

can i avoid using virt-install? and stick to virsh?

# getting a repl! my favorite!

```sh
virsh --connect qemu+ssh://root@hot-desktop.wg.griffinht.com/system
```

todo make sure domain is autostarted at boot!



# getting a disk image

## creating
todo link to guix blog post
todo link to others

If the VM image is too small, then consider resizing it. The libvirt storage, partition, and filesystem will all need to be resized. todo how

`guix system image --image-size`

`qcow2` is nice here because the disk format supports "spare partitions". This means a 30G partition will not take up 30G in storage on the hypervisor todo

I suppose this is where `cloud-init`, and OS specific mechanisms such as Debian's preseed (i don't like this todo link?), butane ignite coreos
https://calgaryrhce.ca/posts/2022-07-07-fully-autonomous-containerized-deployment/
todo link other "old way"
https://nbailey.ca/post/kvm-ansible-automation/


## testing
we can test this vm image before we deploy it
there are a bunch of different ways to do this but qemu is nice and quick and easy

# getting a domain configuration xml

## creating
best:
virt-install --disk size=10 --osinfo linux2022 --print-xml

there are a bunch of different ways to do this
virt-install does a lot for us which is nice - its the same that virt-manager does i think

```sh
virt-install --print-xml
```

## testing
the xml can be validated with uhhh
doesn't virt install do this for us? well idk

# sending the disk image to the hypervisor

i think virt-install --disk path=http://example.com does this for me
dont forget to specify the size!

# sending the domain config to the hypervisor

same, i think it is trivial to let virt-install/virsh handle this

# creating "defining" the domain

    this definition will persist across hypervisor restarts

virsh define <domain>

# starting the domain

virsh start <domain>

# stopping the domain

    this is like pressing the power button on a physical machine

virsh shutdown <domain>

# forcefully stopping the domain

    this is like pulling the power plug on a physical machine

virsh destroy <domain>

# deleting the domain

virsh undefine <domain>

# autostart

https://serverfault.com/a/397890

# updating the domain image

many systems are capable of updating themselves (`apt update && apt upgrade`) without interruptions. however, if we want to change the image we can

virsh shutdown <domain>
manually edit the file?
virsh start <domain>

# updating the domain config

We can use `virsh define` again to redefine an updated XML configuration. Per [`virsh(1)`](tdo link), the domain must be restart for changes to go in to effect.

virsh define

If domain is already running, the changes will take effect on the next boot.

# live updating the domain

https://www.libvirt.org/manpages/virsh.html#device-commands

certain characteristics of the domain can be updated without restarting, don't forget to make changes persisten with both --live --config

https://www.libvirt.org/manpages/virsh.html#update-device

virsh update-device

