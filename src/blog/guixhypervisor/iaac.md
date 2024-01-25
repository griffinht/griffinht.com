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

```sh
virt-install --import --disk/--filesystem
```

can i avoid using virt-install? and stick to virsh?

