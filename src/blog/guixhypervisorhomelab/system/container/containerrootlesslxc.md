# goals

## docker daemon

set up a docker daemon which I can access remotely via ssh. For example:

```
DOCKER_HOST=shh?/todo
```

## volumes

I'd like to access the volume array on my [hypervisor](todo link), and use it to provide persistent storage for my containers.

## networking

I'd like for my containers to be able to talk to each other, and I'd like to expose my containers to the internet
todo rewrite that

# guix system

I'm going to create a Guix operating system declaration:

```scm
(use-modules (gnu bootloader)
             (gnu bootloader grub)
             (gnu system file-systems)
             (gnu packages ssh)
             (gnu packages certs)
             (gnu services base)
             (gnu services networking)
             (gnu services desktop)
             (gnu services ssh)
             (gnu services docker)
             (guix gexp))

(operating-system
  (host-name "docker")
  (bootloader (bootloader-configuration (bootloader grub-bootloader)))
  (file-systems %base-file-systems)
  (packages
    (append
      (list nss-certs) ; docker requires https
      %base-packages))
  (services
    (append
      (list (service dhcp-client-service-type)
            ; make acpi shutdown work
            (service elogind-service-type)
            (service openssh-service-type
                     (openssh-configuration
                      (openssh openssh-sans-x)
                      (permit-root-login `prohibit-password)
                      (password-authentication? #f)
                      (authorized-keys
                       `(("root" ,(local-file "id_ed25519.pub"))))))
            ; docker!
            (service docker-service-type))
      %base-services)))

```

wablam!

```sh
$ guix system vm blah blah blah
...
$ DOCKER_HOST=ssh://root@localhost:2222 docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
$ DOCKER_HOST=ssh://root@localhost:2222 docker run --rm hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c1ec31eb5944: Pull complete 
Digest: sha256:4bd78111b6914a99dbc560e6a20eab57ff6655aea4a80c50b0c5491968cbc2e6
Status: Downloaded newer image for hello-world:latest

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
