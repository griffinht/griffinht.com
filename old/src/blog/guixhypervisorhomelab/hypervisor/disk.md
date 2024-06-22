## host
share to multiple clients with virtio
    contention?
security:
    great, rootful hypervisor mounts and exposes fs
    BUT how do we manage our btrfs install? uh oh now we need to pollute the hypervisor!
    real solution:
        expose block device to unix user, then only have that user responsible for that one single nas vm
    todo how to get btrfs stats from within 

## guest
dont bother the host
security:
    passing a block device to a guest, requires exposing that block device to unpriv user

todo consider cloud use cases




# mounting a btrfs array from a kvm libvirt qemu vm guest non root

```sh
```

## permissions

## mounting

```sh
$ mkdir mnt
$ mount /dev/disk/by-label/btrfs_data mnt
(fail todo show error)
```

## mounting part 2

## modified permissions persistence

host vm guix config udev rules? see chatgpt
persisting our changes

## mounting persistence

guest vm guix config
