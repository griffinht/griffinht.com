https://mike42.me/blog/2019-08-how-to-use-the-qemu-bridge-helper-on-debian-10#Setting-up-th

# Setting up `qemu-bridge-helper`

    fix /usr/libexec/qemu-bridge-helper
        can qemu be used without this?
    setuid deprecated
    /etc/qemu/bridge.conf typo + incorrect lol
        see how /etc/passwd and stuff do it!

## tldr

Import these two modules:

```scm
(gnu packages virtualization) ; qemu
(gnu system setuid) ; setuid
```

Add these two services and the to your `operating-system` declaration.

todo make this a shepherd service???

```scm
(operating-system
 (services
  (append (list ...
                (extra-special-file "/usr/libexec/qemu-bridge-helper" "/run/setuid-programs/qemu-bridge-helper")
                (extra-special-file "/etc/qemu/bridge.conf" (plain-file "" "allow br0"))
                ...)
           %base-services))
 ...
 (setuid-programs
   (append
     (list (setuid-program
             (program (file-append qemu "/libexec/qemu-bridge-helper"))))
     %setuid-programs))
```
Per the qemu documentation todo link, we need to create a `/usr/libexec/qemu-bridge-helper` binary with setuid priviliges, and configuring it by allowing our bridge with `/etc/qemu/bridge.conf` `allow br0` todo




This error is caused by not setting up `qemu-bridge-helper`, which is necessary to allowing us to access the bridge network without root privileges.

See [qemu wiki](https://wiki.qemu.org/Features/HelperNetworking), [helpful blog post](https://apiraino.github.io/qemu-bridge-networking/) and [other helpful blog post](https://mike42.me/blog/2019-08-how-to-use-the-qemu-bridge-helper-on-debian-10) for more information.


## setuid setup

If `qemu-bridge-helper` does not have setuid permissions, then the following error will occur:

```
Error starting domain: /usr/libexec/qemu-bridge-helper --br=br0 --fd=30: failed to communicate with bridge helper: stderr=failed to create tun device: Operation not permitted
: Transport endpoint is not connected
```

```scm
                 (services
                  (append (list ...
                                (extra-special-file "/usr/libexec/qemu-bridge-helper" "/run/setuid-programs/qemu-bridge-helper")
                                ...
                 (setuid-programs
                   (append
                     (list (setuid-program
                             (program (file-append qemu "/libexec/qemu-bridge-helper"))))
                     %setuid-programs))
```
todo is sysctl forward required???
Per [the manual](https://guix.gnu.org/cookbook/en/html_node/Network-bridge-for-QEMU.html), I will start by adding the following to my `operating-system` declaration

```scheme
(setuid-programs
 (append
   (list (file-append qemu "/libexec/qemu-bridge-helper")
   %setuid-programs))
```

This yields an error, which I investigated with `guix repl` and `(load "system.scm")`: todo

```
error: qemu: unbound variable
```

Based on the [gexp section](https://guix.gnu.org/manual/en/html_node/G_002dExpressions.html) of the manual, I can see that the `file-append` procedure takes an object and a suffix. The object here is `qemu`, which I figure must be referring to the `qemu` package, which is defined in `(gnu packages virtualization)`. Let's import this module:

```scheme
(define-module (system)
               ...
               #:use-module (gnu packages virtualization) ; qemu
               ...
```

Trying again fixes the error, but I get a new deprecation warning:

```
warning: representing setuid programs with file-like objects is deprecated; use 'setuid-program' instead
```

This led me to the very helpful manual section on [setuid programs](https://guix.gnu.org/manual/en/html_node/Setuid-Programs.html).

```scheme
(setuid-programs
  (append
    (list (setuid-program
            (program (file-append qemu "/libexec/qemu-bridge-helper"))))
    %setuid-programs))
```

This also requires importing `(gnu system setuid)` - todo how can i get the hint thing?

```scheme
(define-module (system)
               ...
               #:use-module (gnu packages virtualization) ; qemu
               #:use-module (gnu system setuid) ; setuid
               ...
```

Let's make sure it worked:

```sh
libvirt@hypervisor ~$ ls -l $(which qemu-bridge-helper)
-r-sr-xr-x 1 root root 539512 Jan 30 13:56 /run/setuid-programs/qemu-bridge-helper
```

Looks good to me! Let's try starting the VM again:

```
Error starting domain: '/usr/libexec/qemu-bridge-helper' is not a suitable bridge helper: No such file or directory
```

```sh
libvirt@hot-desktop ~$ ls /usr/libexec/qemu-bridge-helper
ls: cannot access '/usr/libexec/qemu-bridge-helper': No such file or directory
libvirt@hot-desktop ~$ which qemu-bridge-helper
/run/setuid-programs/qemu-bridge-helper
```


```scheme

                 (services
                  (append (list ...
                                (extra-special-file "/usr/libexec/qemu-bridge-helper"
                                                    (file-append qemu "/libexec/qemu-bridge-helper"))
                                ...
```

After deploying my changes I was left with this:

```sh
libvirt@hot-desktop ~$ ls /usr/libexec/qemu-bridge-helper
/usr/libexec/qemu-bridge-helper
libvirt@hot-desktop ~$ readlink /usr/libexec/qemu-bridge-helper 
/gnu/store/ggid1sfwrvq2zjfjwbk64wjyi8h8cvsb-qemu-8.1.3/libexec/qemu-bridge-helper
libvirt@hot-desktop ~$ ls -l $(readlink /usr/libexec/qemu-bridge-helper)
-r-xr-xr-x 2 root root 539512 Jan  1  1970 /gnu/store/ggid1sfwrvq2zjfjwbk64wjyi8h8cvsb-qemu-8.1.3/libexec/qemu-bridge-helper
```

todo move this up!



The qemu-bridge-helper trick worked, but now we need to configure

## ACL setup with `/etc/qemu/bridge.conf`

Per the [Setup](https://wiki.qemu.org/Features/HelperNetworking#Setup) section of the Qemu wiki, we need to configure `qemu-bridge-helper` to allow unprivileged users to use the bridge interface by creating a special configuration file:

`/etc/qemu/bridge.conf`
```
allow br0
```

We could create this file manually, or we could let Guix handle things. This can be accomplished by using the `extra-special-file` procedure ([manual](https://guix.gnu.org/manual/en/html_node/Base-Services.html)) to create a service which creates our special configuration file. Add the following to the services list in the `operating-system` declaration:

```scm
                 (services
                  (append (list ...
                                (extra-special-file "/etc/qemu/bridge.conf" (plain-file "" "allow br0"))
                                ...
```

The `plain-file` procedure ([manual](https://guix.gnu.org/manual/en/html_node/G_002dExpressions.html)) returns a "file-like object" with an empty name and the contents `allow br0`. When we deploy our system, Guix will internally create this file in [the store](https://guix.gnu.org/manual/en/html_node/The-Store.html), and then create a symlink at `/etc/qemu/bridge.conf` pointing to the store file.

Here is what this looks like on the resulting system:

```sh
$ ls -l /etc/qemu/bridge.conf 
lrwxrwxrwx 1 root root 44 Jan 30 17:19 /etc/qemu/bridge.conf -> /gnu/store/qsg9gci1pjvdpchs1qp98nzc56m36fsm-
$ cat /etc/qemu/bridge.conf 
allow br0
```

Note that there is no newline at the end of the file, which isn't an issue for our purposes.

### Common errors

If this file does not exist, then the following error occurs:

```
Error starting domain: /usr/libexec/qemu-bridge-helper --br=br0 --fd=30: failed to communicate with bridge helper: stderr=failed to parse default acl file `/etc/qemu/bridge.conf'
: Transport endpoint is not connected
```


