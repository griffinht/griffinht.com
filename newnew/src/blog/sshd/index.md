# sshd

Why is can't I find an easy way to run a tool as useful as `sshd` on my machine? I'm not talking about running a system wide `sshd` daemon - that would be far too complex. Each Linux distribution has a slightly different idea of how `sshd` should be configured, and why should I have to tweak a daemon which runs as the `root` user? I'd like to be able to run `sshd` as an unpriviliged user - in the userland.

# why not a reverse shell

[Entire blog posts](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/) have been written on how to tweak the various reverse shells techniques to support interactive use, and each method comes with their own caveats. I just want a program that is easy to install and can be run by me, not the root user.

# why not `sshd`

Again, several blog posts and StackOverflow questions have been written about the topic:

https://serverfault.com/questions/344295/is-it-possible-to-run-sshd-as-a-normal-user
https://www.codejam.info/2021/11/standalone-userland-ssh-server.html
https://github.com/valeriangalliat/sshd-on-the-go

The last project is promising, but I wanted something more portable and robust - `sshd` on the go is mostly a Makefile with no installation methods other than `git clone ... && make setup...`.

# why not `dropbear`

Again, very complex, not to mention running an alternative SSH server has security implications.

# why not `containerssh`

kind of but nah

# example usage

sshd-userland --password bruh
# options

```
--allow-all
--password=<password>
--authorized-keys='asdasd'
--authorized-keys-file=~/.ssh/authorized_keys
--port=<port> (2222 by default)
--listen=<interface>
```

# use cases

Theoretically this tool could trivially reimplement the ContainerSSH project in one line.

`sshd-userland -- docker run --rm -it alpine sh`
