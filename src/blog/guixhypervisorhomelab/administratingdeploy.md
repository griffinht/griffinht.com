don't duplicate existing information!
https://guix.gnu.org/en/blog/2019/managing-servers-with-gnu-guix-a-tutorial/

imagine the pov of someone new to guix!
also adapt for people running as their main guix system!
maybe make this in to a separate repo and start from scratch that way?? or maybe it shouldn't rely on that?




Let's start by declaring a barebones Guix operating system:

`system.scm`
```scm
```


# `guix system reconfigure`

On a remote system, this can be automated with something like `scp` and `ssh`:

todo
guix deploy: error: failed to deploy dockerrootless: missing root file system

```sh
$ scp -P 2222 system.scm root@localhost:
$ ssh -p 2222 root@localhost
~# guix system reconfigure system.scm
gnu/system.scm:866:2: error: missing root file system
```

`guix system reconfigure` will try to update the bootloader, which means we need to actually define a file system with a mount point at the file system root.

We want to mount the main partition at "/". Images created by `guix system image` have this partition labeled as "Guix_image" by default, which we can specify like this:

`system.scm`
```scm
  (file-systems
    (append
      (list
        (file-system
          (mount-point "/")
          (type "ext4")
          (device (file-system-label "Guix_image"))))
      %base-file-systems))
```

```sh
~# guix system reconfigure system.scm
Git error: the SSL certificate is invalid
```

https://tech.toryanderson.com/2021/10/04/guix-pull-error-git-error-the-ssl-certificate-is-invalid/

```sh
guix install nss-certs
export SSL_CERT_DIR="$HOME/.guix-profile/etc/ssl/certs"
export SSL_CERT_FILE="$HOME/.guix-profile/etc/ssl/certs/ca-certificates.crt"
export GIT_SSL_CAINFO="$SSL_CERT_FILE"
guix system reconfigure system.scm 
```

See the manual for more information: [https://guix.gnu.org/manual/en/html_node/X_002e509-Certificates.html](https://guix.gnu.org/manual/en/html_node/X_002e509-Certificates.html)

The real fix would have been to add `nss-certs` to our list of packages of our operating system declaration from the beginning.

Even if we did that however, `guix system reconfigure` would have been very slow.

What if there was a better way?

`guix system reconfigure` can be annoying and slow, especially when used on systems like virtual machines or other short lived Guix machines. What if there was a better way?

exisiting cloud tools? ansible?

# `guix deploy` ([manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-deploy.html))
    administration guidellines
    todo i think i saved a bunch more blogs from here??
    mention nix equivalent!
    mention sources! jakob or whoever who wrote this in one summer?
    https://stumbles.id.au/getting-started-with-guix-deploy.html 
    see links at bottom of page!

Guix deploy todo terminology works by sending something idk todo. This means we don't have to worry about X.509 certificates or even public Internet access on the target systems - we just need SSH connectivity. This approach is also very fast because it shares the software on the host with the target systems, instead of instructing the target systems to download the software from the Internet. citation needed

Guix deploy can build system derivations locally, instead of on the target deployment machine.

This 

todo dont just copy the manual idk
updates? how do i update the whole system? how can i automate?

# todo what does authorize do?

`deploy.scm`
```scm
(list
  (machine
    ; 'managed-host is a machine that is already running the Guix system and available over the network (via ssh)
    (operating-system (load "system.scm"))
    (environment managed-host-environment-type)
    (configuration
      (machine-ssh-configuration 
        ;; this is the domain or ip address of the target machine
        (host-name "127.0.0.1")
        ;; why is system required?
        (system "x86_64-linux")
        ;; what user to login as, default root
        (user "root")
        ;; ssh public key of remote system
        ;; obtain with `ssh-keyscan -p 2222 hostname`
        ; when omitted, uses ~/.ssh/known-hosts
        (host-key "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKJIH8P+wYeiND2cjYbUcjI10CF2OlPOgZUzYmZzHsaF")
        ;; private key of host machine to authenticate with
        ;; leave default its fine i think
        ; todo change to something idk
        ;;(identity "id_ed25519.pub")
        ;; ssh server port of remote system, default 22
        (port 2222)))))
        ;(port 22)))))
```

```sh
$ guix deploy deploy.scm
guix deploy: error: unauthorized public key: (public-key 
 (ecc 
  (curve Ed25519)
  (q #EF1968BD20277FF7DC1528C7B398FB09EE6E762D39E253D056497177903FC994#)
  )
 )
```

[https://stumbles.id.au/getting-started-with-guix-deploy.html](https://stumbles.id.au/getting-started-with-guix-deploy.html)

`system.scm`
```sh
  (services
    (append
      (list ...)
      (modify-services
        %base-services
        ;; The server must trust the Guix packages you build. If you add the signing-key
        ;; manually it will be overridden on next `guix deploy` giving
        ;; "error: unauthorized public key". This automatically adds the signing-key.
        (guix-service-type
          config =>
          (guix-configuration
          (inherit config)
          (authorized-keys
            (append
              (list (local-file "/etc/guix/signing-key.pub"))
              %default-authorized-guix-keys))))))))
```
todo where is guix-service-type documented??? can guix deploy not do this? it has root after all

We also need to create `/etc/guix/signing-key.pub` on the host todo
how to make guix signing key on foreign distro?

This essentially tells the Guix system to trust anything that make todo what are we making? store derivations?

```sh
$ guix deploy deploy.scm
guix deploy: successfully deployed hostname
```
