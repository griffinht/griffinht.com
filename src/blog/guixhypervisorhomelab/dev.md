guix system vm
    mention acpi elogind
guix image
    docker
    qcow2
    raw?
guix container
    todo
    https://guix.gnu.org/cookbook/en/html_node/Container-Networking.html



# ssh setup

Testing locally means we will often be using `ssh` to connect to the system from our host machine. This means we will be encountering many new SSH host keys, which are generated randomly for each system (citation needed). By default, `ssh` will warn us when connected to an unknown SSH host. `ssh` will then become very upset if the SSH host key changes - for example, if we connected to a virtual machine, then destroyed it and replaced it with another virtual machine

todo show mitm

`ssh config todo`
```
```
