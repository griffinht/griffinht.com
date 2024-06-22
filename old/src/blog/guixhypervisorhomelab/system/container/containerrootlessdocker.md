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


# operating system

todo lol


guix shell iptables

root@dockerrootless ~# modprobe ip_tables
root@dockerrootless ~# echo "docker:100000:65536" >> /etc/subuid
root@dockerrootless ~# echo "docker:100000:65536" >> /etc/subgid



guix shell shadow # newuidmap
operation not permitted, obviosuly needs setuid
https://github.com/docker-library/docker/blob/8b8d62e7eb791b060cc75cb2956724a1bdc5484b/20.10/dind-rootless/Dockerfile

https://github.com/kubernetes-sigs/kind/issues/3363
https://www.redhat.com/sysadmin/compose-podman-pods
