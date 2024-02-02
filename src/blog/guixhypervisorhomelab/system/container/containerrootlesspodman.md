https://www.reddit.com/r/GUIX/comments/13tudtn/getting_podman_working_with_rootless_containers/
https://www.reddit.com/r/NixOS/comments/12r4knb/extreme_noob_question_on_getting_podman_to_work/
why not coreos? debian?

# Podman from scratch on a Guix system

# todo kubernetes, cri-o, minikube?

# Docker daemon

# rootless

docker
podman

https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
https://opensource.com/article/19/2/how-does-rootless-podman-work

wireguard in podman rootless?

# guix

literally just guix with a podman user (and ipv4 forward i guess)

# installing and configuring podman



```scm
(operating-system
  (host-name "container-orchestrator")
  ;todo remove timezone not necessary? defaults are fine?
  (timezone "Etc/UTC")
  (bootloader (bootloader-configuration (bootloader grub-bootloader)))
  (file-systems %base-file-systems)
  ; todo add swap
  ;(swap-devices (list (swap-space (target "/swapfile"))))
  (users
    (append
      (list
        (user-account
          (name "podman")
          (group "users")))
      %base-user-accounts))
  (services
   (append
     (list (service dhcp-client-service-type)
           ; make acpi shutdown signal work
           (service elogind-service-type)
           ; ssh
           (service openssh-service-type
                    (openssh-configuration
                     (openssh openssh-sans-x)
                     (permit-root-login `prohibit-password)
                     (password-authentication? #f)
                     (authorized-keys
                      `(("root" ,ssh-public-key)
                        ("podman" ,ssh-public-key)))))))))
```

guix system vm --no-graphic ...

# todo put this in a developing with guix post

```
$ ssh -p 2222 podman@localhost
podman@container-orchestrator ~$ guix shell podman
hint: Consider passing the `--check' option once to make sure your shell does not clobber environment variables.

guix shell: error: changing ownership of path '/gnu/store': Read-only file system
```

`guix system vm` is great, but limits us by sharing the store with the host. This allows for very fast testing, but won't allow us to actually modify the store to install new software. Instead, we can generate an image, copy it somewhere we can write to, then run the image with full read/write everywhere on the system. Check out [the manual](https://guix.gnu.org/manual/en/html_node/Running-Guix-in-a-VM.html) for more info.

```sh
temp="$(mktemp)" \
     && cp "$(guix system image system.scm...todo)" "$temp" \
     && chmod +w "$temp" \
     && qemu-system-x86_64 \
	-enable-kvm \
	-drive "file=$temp,format=raw" \
	-m 512 \
	-nic 'user,model=virtio-net-pci,hostfwd=tcp::2222-:22'
```

Note this does the full boot sequence, where the script produced by `guix system vm` boots straight to the kernel. We could configure that here, but that would be extra work. This means we go through GRUB when booting. I also noticed that GRUB would not boot with the `-nographic`, so I omitted that here.

```sh
$ guix install podman
podman@container-orchestrator ~$ guix shell podman
...
ERROR: In procedure run-hook:
In procedure fport_write: No space left on device
podman@container-orchestrator ~$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
fd0      2:0    1    4K  0 disk 
sda      8:0    0  1.9G  0 disk 
├─sda1   8:1    0   40M  0 part 
└─sda2   8:2    0  1.8G  0 part /gnu/store
                                /
sr0     11:0    1 1024M  0 rom  
```

No space! This makes sense, as our VM image is only as large as it needs to be. Fortunately we can pass `--image-size` to `guix system image` to create a larger image. Note that we could also accomplish this by taking the generated disk image, resizing it with something like `fdisk`, then resizing the filesystem with something like `resize2fs`. The easiest way however is by letting `guix system image` do the work.

https://guix.gnu.org/manual/en/html_node/Invoking-guix-system.html#index-image_002c-creating-disk-images
todo manual is wrong
Also note that the image we are producing is an `efi-raw` image its actually mbr hybrid or something. This image format does not support "sparse partitinoning". This means that if we wanted to create a VM image with 100 gigabytes of space, then it would take exactly 100G of actual disk space on the host, even if the majority of space was empty.

Thankfully, the `qcow` format does support sparse partitioning. Let's create a 20G `qcow2` disk image:

```sh
$ guix system image --image-size=20G --image-format=qcow2 bootstrap.scm
$ ls -lh /gnu/store/g1xmm3fbj3j24yaqm8wxr77n528f4c8d-image.qcow2
-r--r--r-- 2 root root 516M Dec 31  1969 /gnu/store/g1xmm3fbj3j24yaqm8wxr77n528f4c8d-image.qcow2
```

It worked! You can see how the 20G disk image only took around half a gigabyte of space on the host.

Don't forget to set `format=qcow2` in the options passed to `qemu`:

```sh
temp="$(mktemp)" \
     && cp "$(guix system image --image-size=20G --image-type=qcow2 bootstrap.scm)" "$temp" \
     && chmod +w "$temp" \
     && qemu-system-x86_64 \
	-enable-kvm \
	-drive "file=$temp,format=qcow2" \
	-m 512 \
	-nic 'user,model=virtio-net-pci,hostfwd=tcp::2222-:22'
```

## rapid development

You may have noticed how long it took to generate the disk image. What if we wanted to change the `operating-system` declaration? Would we have to regenerate the entire VM? No!

Remember that we have a regular Guix system at this point. This means we are free to `guix system reconfigure` and even `guix deploy` - we won't even need to reboot to see our changes!

## podman

Finally we can continue with Podman.

```sh
guix shell podman
```


```sh
podman@container-orchestrator ~ [env]$ podman run hello-world
WARN[0000] "/" is not a shared mount, this could cause issues or missing mounts with rootless containers 
ERRO[0000] cannot find UID/GID for user podman: open /etc/subuid: no such file or directory - check rootless mode in man pages. 
WARN[0000] Using rootless single mapping into the namespace. This might break some images. Check /etc/subuid and /etc/subgid for adding sub*ids if not using a network user 
Error: short-name "hello-world" did not resolve to an alias and no containers-registries.conf(5) was found
```

warnings todo

Welcome to the world of Podman. 

There are some warnings here that I will be ignoring for now. The first thing we need to do is configure our container registries.

# `container-registries.conf(5)` ([man](https://man.archlinux.org/man/containers-registries.conf.5.en))

If desired, we could create a `~/.config/containers/registries.conf` file to emulate Docker's default behaivor of resolving unqualified names to the [Docker Hub](https://hub.docker.com/) (available at `docker.io`). 

If you'd like to emulate Docker's default pull behavior, then try this:

`~/.config/containers/registries.conf`
```
unqualified-search-registries = ['docker.io']

[[registry]]
prefix="docker.io"
location="docker.io"
```

This will reslolve "unqualified" names to the Docker hub. This means that `podman run hello-world` becomes `podman run docker.io/hello-world`. This also means that this step is unnecessary! The Docker Hub is just another container registry, and you could simply qualify todo idk

For now, I will simply be more explicit:

```sh
podman@container-orchestrator ~ [env]$ podman run docker.io/hello-world
Error: open /etc/containers/policy.json: no such file or directory
```

# `containers-policy.json(5)` ([man](https://man.archlinux.org/man/containers-policy.json.5.en))

We will need to configure a signature verification policy file. This differs from Docker's default behavior of accepting anything. todo learn more about image signing

Essentially we need this:

`~/.config/containers/policy.json`
```json
{
    "default": [
        {
            "type": "insecureAcceptAnything"
        }
    ]
}
```

todo actually do signing and stuff

# CA certificate installation

```sh
podman@container-orchestrator ~$ podman run docker.io/hello-world
Trying to pull docker.io/library/hello-world:latest...
Error: initializing source docker://hello-world:latest: pinging container registry registry-1.docker.io: Get "https://registry-1.docker.io/v2/": x509: certificate signed by unknown authority
```

Our system does not have any X.509 certificates installed by default. This means we will need to install them ourselves. ([manual](https://guix.gnu.org/manual/en/html_node/X_002e509-Certificates.html))

```sh
podman@container-orchestrator ~$ guix install nss-certs
podman@container-orchestrator ~$ logout
$ ssh -p 2222 podman@localhost
podman@container-orchestrator ~$ podman run docker.io/hello-world
Trying to pull docker.io/library/hello-world:latest...
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

It worked!

> why didn't we need X.509 certificates when installing Guix software? This is because Guix does not rely on HTTPS, and will either ignore it or use HTTP (citation needed). Instead, Guix relies entirely on blah blah substitutes challenge blah blah todo

# setuid/subguid

Let's try running the official [`alpine`](https://hub.docker.com/_/alpine/) image. I'm also going to start using `--rm` to remove the image after I run it, and `-it` to give me an interactive shell.

```sh
podman@container-orchestrator ~$ podman run --rm -it docker.io/alpine
Trying to pull docker.io/library/alpine:latest...
Getting image source signatures
Copying blob 4abcf2066143 done  
ERRO[0001] While applying layer: ApplyLayer stdout:  stderr: potentially insufficient UIDs or GIDs available in user namespace (requested 0:42 for /etc/shadow): Check /etc/subuid and /etc/subgid if configured locally and run podman-system-migrate: lchown /etc/shadow: invalid argument exit status 1 
Error: copying system image from manifest list: writing blob: adding layer with blob "sha256:4abcf20661432fb2d719aaf90656f55c287f8ca915dc1c92ec14ff61e67fbaf8": ApplyLayer stdout:  stderr: potentially insufficient UIDs or GIDs available in user namespace (requested 0:42 for /etc/shadow): Check /etc/subuid and /etc/subgid if configured locally and run podman-system-migrate: lchown /etc/shadow: invalid argument exit status 1
```

> why did hello world work but alpine didnt? alpine requires root or something, peep hello world it doesnt

# volumes

host bind mounts

# outbound networking

curl

# inbound networking

http server

# container-container networking/dns

http server reverse proxy idk

# privileged

wireguard

# secrets?

# docker api

DOCKER_HOST=ssh:///podman@localhost



first why not put everything in a package??
i wonder how this integrates with shepherd and local testing?

# declarative with guix package

# declarative user profile with `guix home`


So far we have been installing software and writing our configurations **imperativelty**. This differs from the declarative nature of our operating system - we declared an operating system, then used Guix to create it. Why can't we do the same for all this user configuration?

`guix home import`
Why don't we manage this declaratively with `guix home` - SEPARATE THING

I think this would be similar to using something like Ansible to install packages and create the configuration files.

