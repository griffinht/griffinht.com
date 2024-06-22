# Deploying and Developing a Guix server

Let's recap what I have done so far


I defined a simple Guix `operating-system` [(ref)](https://guix.gnu.org/manual/en/html_node/operating_002dsystem-Reference.html) in Guile Scheme.

`bootstrap.scm`
```
(use-modules (gnu))
(use-service-modules networking ssh)
(use-package-modules bootloaders ssh)

(operating-system
 (host-name "my-vps")
 (bootloader (bootloader-configuration
              (bootloader grub-bootloader)))
 (file-systems %base-file-systems)
 (services
  (append (list (service dhcp-client-service-type)
                (service openssh-service-type
                         (openssh-configuration
                          (openssh openssh-sans-x)
                          ;; allow root login (disabled by default) but not with a password
                          (permit-root-login `prohibit-password)
                          (authorized-keys
                           ;; authorize our public ssh key with the root user
                           `(("root" ,(local-file "id_ed25519.pub")))))))
          %base-services)))
```

I then created an `efi-raw` disk image from this `operating-system` definition with `guix system image bootstrap.scm`. I took the resulting image and wrote it to the virtual drive `/dev/vda` of my RackNerd VPS. I accomplished this by enabling "Rescue Mode" on my VPS control panel, which creates and boots a special rescue system accessible via `ssh`. This allowed me to write my image to `/dev/vda` with the following command: `ssh root@my-vps 'cat > /dev/vda' < image.img`. After the image finished writing, I `ssh`ed in to the rescue machine and resized the main partition to take the rest the space of my 10Gb drive. I simply recreated the same partition but with an increased size, then used `resize2fs` to properly resize the filesystem. I then disabled "Rescued Mode" and my system booted. Check out my [last blog post](todo) to see a detailed overview of each step.

With my new Guix system up and running, I can begin 

```
(use-modules (gnu))
(use-service-modules networking ssh)
(use-package-modules bootloaders ssh)

(operating-system
 (host-name "my-vps")
 (bootloader (bootloader-configuration
              (bootloader grub-bootloader)))
 (file-systems (cons (file-system
                       (mount-point "/")
                       (device "/dev/vda2")
                       (type "ext4"))
               %base-file-systems))
 (services
  (append (list (service dhcp-client-service-type)
                (service openssh-service-type
                         (openssh-configuration
                          (openssh openssh-sans-x)
                          (permit-root-login `prohibit-password)
                          (password-authentication? #f)
                          (authorized-keys
                           `(("root" ,(local-file "id_ed25519.pub")))))))
          (modify-services %base-services
          ;todo paraphrase
          ;; The server must trust the Guix packages you build. If you add the signing-key
          ;; manually it will be overridden on next `guix deploy` giving
          ;; "error: unauthorized public key". This automatically adds the signing-key.
          (guix-service-type config =>
                             (guix-configuration
                              (inherit config)
                              (authorized-keys
                               (append (list (local-file "/etc/guix/signing-key.pub"))
                                       %default-authorized-guix-keys)))))
                      )))
```

Nothing much has changed, except I do need to define a root filesystem (a file system with `(mount-point "/")`). Otherwise `guix deploy` will return an error. I also defined a `guix-service-type` which adds my own signing key to the server. This allows the server to trust me to send over packages I built on my machine.

Now that my `operating-system` declaration is complete There are a few ways to do this in Guile Scheme, 

```
$ guix deploy deploy.scm
The following 1 machine will be deployed:
  my-vps

guix deploy: deploying to my-vps...
guix deploy: error: failed to deploy nerd-vps: server at 'nerd-vps.griffinht.com' returned host key 'AAAAC3NzaC1lZDI1NTE5AAAAIB7LTlg2Q0cIrY2zDcgH7CWjAxIjvAqRIf5DMkhMRl3P' of type 'ed25519' instead of 'AAAAC3NzaC1lZDI1NTE5AAAAIGEYgDBZArT6Yv22sNHZqXPujGCyeZhAvzq+hRjElGNk' of type 'ed25519'
```

The server has a new SSH host key which I need to add to my `deploy.scm` configuration.

# Local Development

Guix systems allow for extremely short developer feedback loops. An entire system can be created locally on the dev machine in mere seconds with a virtual machine, container, or Docker container. This means testing out new changes will never require a more costly `guix deploy` to a remote system. Instead, I/DEVELOPER todo may spin up a full VM or lightweight container which replicates the entire system.

Each of these machines generate a new SSH host key each time they are started. Consider using the following `ssh` command to avoid messing up your `~/.ssh/known_hosts` file.

```
$ ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 10022 root@localhost
```

https://guix.gnu.org/manual/en/html_node/Invoking-guix-system.html
## with `guix system vm`

Why not make a virtual machine?

[reference](https://guix.gnu.org/manual/en/html_node/Running-Guix-in-a-VM.html)

## with `guix system container`

Why not run a container

## with `guix system image --image-type=docker`

Why not run a Docker image?
Now that we know how to deploy to our remote servers, how can we test out our changes locally?

Why not run a local VM? Or maybe a container? Or a Docker image?
