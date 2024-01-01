
# From Debian to Docker to Guix
# From Docker to Guix
# From Host to Docker to Guix

emphasize docker feature parity and more!
Let's say I want to 



todo website example!

https://guix.gnu.org/manual/en/html_node/Invoking-guix-pack.html

(time command?)
Why is `guix pack` taking so long to run? The answer is that guix is using `gzip` compression by default. Passing the `--compression=none` flag makes `guix pack` run nearly instantly, which is great for development.





Where is the `laminarc` command?

`ls gnu/store`

```
056s5mikk0dsiq9sqvggv8mhj4mj1xqx-sqlite-3.39.3
1fjm5sqgiwl2rcy9fwn69abaahx6z3sq-ncurses-6.2.20210619
2nk6zligq2l16wqjl1mp87x0h9xkl7ak-laminar-1.2
6ncav55lbk5kqvwwflrzcr41hp5jbq0c-gcc-11.3.0-lib
8ak4r4sz1ajza5vckn7mb6vw1wk54agn-info-dir
8sinf2f2am0w88d9j2gkss6lbcw0dh65-readline-8.1.2
dlhbpjx28m3jddficjhnsy60h5hrfz2q-emacs-subdirs
ggbfxc0xsb4mv3dgfc3al68c7nqq8lw2-capnproto-1.0
hl6lb3irs8wrfv49fnirxshsq590pi9v-zlib-1.2.13
ln6hxqjvz6m9gdd9s97pivlqck7hzs99-glibc-2.35
vmc20r1iqvxvxdsix5xf4llan86i65yn-profile
zzyywykw7kriln18rxqd82f0k5kidla7-bash-static-5.1.16
```

`ls ./gnu/store/2nk6zligq2l16wqjl1mp87x0h9xkl7ak-laminar-1.2/`

```
bin
etc
sbin
share
```

`--symlink=/bin=bin`

`--symlink=/sbin=sbin`

###

```
docker run --rm \
    laminar
```

```
guix shell --container \
    nginx
```
# running

# enabling networking

# exposing ports to host

# inter container networking - ???

# mounting files to volume

Now let's run the Laminar daemon, `laminard`:
```
$ ./sbin/laminard
terminate called after throwing an instance of 'kj::ExceptionImpl'
  what():  kj/filesystem.c++:612: failed: directory does not exist; path = var/lib/laminar
```

Laminar is looking for some configuration files, but there are none. How can we add our own?
Now that we have `laminar` nicely packaged, how can we add our own files? Like html nginx todo or config files

option b: guix shell --container with --share
This is similar to running a docker container with host bind mounts `-v ./config:/var/lib/laminar`

https://guix.gnu.org/en/cookbook/en/html_node/Guix-Containers.html

todo be mindful of --no-cwd
```
guix shell --container \
    --share=./config=/var/lib/laminar \
    laminar \
    -- laminard
```

```
docker run --rm 
    --volumesss? ./config:/var/lib/lamianr
```


# custom image

```
FROM nginx

COPY config /etc/config
```

# a whole guix system
https://guix.gnu.org/en/cookbook/en/html_node/Guix-System-Containers.html

# Summary
Notice how none of the Guix commands required `sudo`. Unlike Docker, there is no magical rootful daemon and there is no clunky rootless docker setup, nor hafl supported podman setup ro something idk


























# From Docker to Guix

Docker is great, but I think Guix is much more powerful. Here is how I migrated `griffinht.com` from a haphazard set of Docker images to a powerful uhh Guix.

# tldr

## migrating my static website generator from Docker to Guix
are we doing this or a guix overview???? uhhhhh
just do it all and split later :)

[`inline-website`](source) is a static website generator I wrote to create this website.

`Dockerfile`
```Dockerfile
FROM python:alpine

RUN pip install chevron markdown pyyaml 

COPY src/ /usr/local/bin/

ENTRYPOINT ["inline-website.py"]
```

Run in a Docker container:

```bash
$ docker run --rm inline-website --help
```

becomes

`manifest.scm`
```scheme
```

Run:

```bash
$ guix shell -- src/inline-website --help
```

Run in a container:

```bash
$ guix shell --container -- src/inline-website --help
```

Run in a Docker container:
```bash
$ docker load "$()"
```

Run as a semi cross platform tarball: guix made a good blog abt this

Try it!

RUn as an actually portable executable https://justine.lol/ape.html

Try it!

## No `guix`? No problem!

guix pack or something?

## How do I get this fancy `guix` command?

https://guix.gnu.org/manual/en/html_node/Binary-Installation.html

## migrating my static website from Docker to Guix

## migrating my website from Docker to Guix



Docker is a great tool which allows nearly any software to be packaged and deployed to nearly any environment. It allows me to run my home lab

Today I will be migrating away from Docker

This is the `Dockerfile` for a static site generator I wrote (source code)[https://griffinht.com/git/inline-website.git].


`inline-website.py` is nothing more than a single file python script which can be run from the command line.

Let's try running it

```bash
$ src/inline-website.py --help
Traceback (most recent call last):
  File "/home/griffin/git/inline-website/src/inline-website.py", line 11, in <module>
    import chevron
ModuleNotFoundError: No module named 'chevron'
```

We are missing some dependencies - `inline-website.py` uses the `chevron`, `yaml`, `markdown`, and `asyncinotify` Python libraries. They are all available on [PyPI](https://pypi.org/), Python's package repository.

I can use [`pip`](https://pypi.org/project/pip/), a package installer for Python, to install packages from PyPI.

Debian
```bash
```

Arch (via the AUR with paru)
```bash
paru -S python-chevron
```

```Dockerfile
FROM python

RUN pip install chevron pyyaml markdown asyncinotify
```

`pip`
```bash
pip install chevron pyyaml markdown asyncinotify
```

nix
```
```

### Installing packages to a profile
    `guix install`

### Guix Manifests
https://guix.gnu.org/en/manual/devel/en/html_node/Writing-Manifests.html
introduce the manifest here!
https://www.futurile.net/2022/12/12/guix-managing-apps-with-manifests/


[`guix shell` documentation](https://guix.gnu.org/manual/en/html_node/Invoking-guix-shell.html#Invoking-guix-shell)
Thankfully, GNU Guix
```bash
$ guix shell python python-chevron python-pyyaml python-markdown
...
$ src/inline-website.py --help
usage: inline-website.py [-h] [-v] [-o OUTPUT] [-w] ...

positional arguments:
  REMAINDER

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
  -w, --watch
```

However, this approach is kind of unwieldy. I could place the `guix shell ...` command in a one line shell script for easy reference, but Guix has a better idea. I'm going to instead put these packages in a *manifest*. The ([manual](https://guix.gnu.org/en/manual/devel/en/html_node/Writing-Manifests.html)) describes manifests as *a “bill of materials” that defines a package set*.

```bash
$ guix shell python python-chevron python-pyyaml python-markdown --export-manifest > manifest.scm
```

`manifest.scm`
```scheme
;; What follows is a "manifest" equivalent to the command line you gave.
;; You can store it in a file that you may then pass to any 'guix' command
;; that accepts a '--manifest' (or '-m') option.

(specifications->manifest
  (list "python"
        "python-chevron"
        "python-pyyaml"
        "python-markdown"))
```

By using the `--export-manifest` option of the `guix shell` command, I was able to generate a manifest in the form of a. This manifest is code - [Guile](https://www.gnu.org/software/guile/) code, which is an implementation of the [Scheme](http://schemers.org/Scheme) programming lanugage. Guix is written mostly in Guile, and uses it as a Domain-specific language (DSL) does it tho? https://guix.gnu.org/en/blog/2020/guile-3-and-guix/ for many things. todo
GUILE IS NOT A DOMAIN SPECIFIC LANUGAGE
https://youtu.be/eWXoKjWCh60?si=VvaLP9Abyzl5toM8&t=875

Let's try it! Per the [manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-shell.html#Invoking-guix-shell), `guix shell` will automatically look for a `manifest.scm` file in the working directory or any parents, which means the only thing I need to do to get started with development is this:

```bash
$ guix shell
...
$ src/inline-website.py --help
usage: inline-website.py [-h] [-v] [-o OUTPUT] [-w] ...

positional arguments:
  REMAINDER

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
  -w, --watch
```

Now that we have this fancy manifest, what can we do?

[The cookbook](https://guix.gnu.org/cookbook/en/html_node/The-benefits-of-manifests.html) has more information on the benefits of manifests - todo

Actually, what can't we do?
todo pyyaml

todo do this anywhere?
https://zero-to-nix.com/start/init-flake

### Creating a one-off developer environment
    I want to develop my `inline-website` project without installing all the dependencies to the rest of my system

### Creating a one-off software environment
### Installing packages in a one-off environment
    `guix shell`

The manual states `guix shell` will create an "*augmented* environment, where the new packages are added to search path environment variables such as `PATH`"

