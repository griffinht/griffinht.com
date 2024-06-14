# Getting Started

I'm going to use Guix to install Syncthing in a temporary shell environment.

```sh
$ guix shell syncthing
$ syncthing
```

Done! Syncthing is now running, and starts the admin UI at [localhost:34599](http://localhost:34599). From here I can configure my remote devices and sync folders.

[syncthing.png](syncthing.png)

What if I wanted to start Syncthing automatically?

# `syncthing-service-type`

Guix provides a `syncthing-service-type` as part of the `(gnu services syncthing)`. This is a system service, which I think restricts it to only being able to run on a full blown Guix system.

I am running Guix on my laptop (which runs Debian), and want to be able to run Syncthing automatically after I log in. Fortunately, this is the exact use case for [Guix Home](https://guix.gnu.org/en/blog/2022/keeping-ones-home-tidy/), which I already use to manage my dotfiles.

# Guix Home configuration

`home.scm`
```
(use-modules ...
             (gnu home services syncthing)
             ...)

(home-environment
  (services
    (list
      (service home-syncthing-service-type
         (for-home
           (syncthing-configuration
             (arguments '("--help")))))
           )))
```

[manual](https://guix.gnu.org/manual/en/manual/devel/en/html_node/Networking-Home-Services.html)

The `(gnu home services syncthing)` module was newly added in August of last year in [this patch](https://issues.guix.gnu.org/62401), and can be used on the latest development version of Guix.

https://guix.gnu.org/en/blog/2020/gnu-shepherd-user-services/

# Logs

How can I view the logs of the Syncthing service? I have no idea.
