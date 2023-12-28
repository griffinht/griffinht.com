https://www.futurile.net/
    so many cool guix tricks!
    the goat!
https://pages.stat.wisc.edu/~yandell/R_for_data_sciences/connect/docker.html
https://issues.guix.gnu.org/55680

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
$ guix shell python python-chevron python-markdown
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
$ guix shell python python-chevron python-markdown --export-manifest > manifest.scm
```

`manifest.scm`
```scheme
;; What follows is a "manifest" equivalent to the command line you gave.
;; You can store it in a file that you may then pass to any 'guix' command
;; that accepts a '--manifest' (or '-m') option.

(specifications->manifest
  (list "python"
        "python-chevron"
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

### Installing packages in a one-off environment
    `guix shell`

### Installing packages in a container
    `guix shell --container`
nsenter?
### Packaging packages
    `guix pack`

The [manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-pack.html) says how `guix pack` allows us to "pass software to people who are not (yet!) lucky enough to be using Guix".

> note that `guix pack` also supports taking a list of packages via the command line - `guix pack python python-chevron python-markdown` would produce the same result as `guix pack --manifest=manifest.scm`

#### as a tarball
#### as a docker image
#### as a DEB
#### as an RPM
#### more
### todo channels?

Let's try bundling up all the dependencies in to a tarball

> pro tip: for local development, consider disabling compression with the `--compression=none` flag - it's much faster (but a little larger)

```bash
$ tar -xz < "$(guix pack --manifest=manifest.scm)"
$ tree -L 3 gnu
gnu
└── store
    ├── 007vydgsvjpz061fxgs01nj1n65dxf6i-python-pyyaml-6.0
    │   ├── lib
    │   └── share
    ├── 0h9hwcbqwl6msl1v0vwhmcfjhga84hp9-python-wheel-0.40.0
    │   ├── bin
    │   ├── lib
    │   └── share
    ├── 0lm4jxcmzxfdn95y28d3y3axp85jnnn3-tcl-8.6.12
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 0yfa08vx7wmz4b2z8i6wn9myjfm0ay5a-python-packaging-bootstrap-21.3
    │   ├── lib
    │   └── share
    ├── 149q8hs1l9vblr5qwi6dry0i5jqmsc7y-python-3.10.7
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 1fjm5sqgiwl2rcy9fwn69abaahx6z3sq-ncurses-6.2.20210619
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 1i83gaifl3bmsx5j9k4h90ydwkfm18jf-libpng-1.6.37
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 1jxsnfvrawp8czn0ml8bp5df8n3ibqa4-python-six-bootstrap-1.16.0
    │   ├── lib
    │   └── share
    ├── 21g9zdpgvnfvf36z16k0badjv0mg1shh-libxft-2.3.4
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 31cgfs6dwhlv5hmcx6wgrqh2lkxnfpps-bzip2-1.0.8
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 4jp981ms6nwyv844r4xf1blfyakz96x8-python-markdown-3.3.4
    │   ├── bin
    │   ├── lib
    │   └── share
    ├── 5qr7rpyyb29w9inrslpc8n1c2a98ydcs-python-toolchain-3.10.7
    │   └── bin
    ├── 6ncav55lbk5kqvwwflrzcr41hp5jbq0c-gcc-11.3.0-lib
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 94rdaacvsqf05zhw88w92y8bkvgxdfpl-expat-2.5.0
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── 9fpds5slpkxm7j5arhcq8iys03lwwx2m-emacs-subdirs
    │   └── share
    ├── aslr8ym1df4j80ika5pfxy5kbfv4iz3w-bash-5.1.16
    │   ├── bin
    │   ├── etc
    │   ├── lib
    │   └── share
    ├── d6v343l5328yg64dmw7ww4sw4f2pr8va-libx11-1.8.7
    │   ├── include
    │   ├── lib
    │   └── share
    ├── fcfhlgn6rgbhgg17kwxdhp8l7b58xych-python-pip-23.1
    │   ├── bin
    │   ├── lib
    │   └── share
    ├── fgl39clk8v1h142vxkwiwkhqjp1svg3f-python-chevron-0.14.0
    │   ├── bin
    │   └── lib
    ├── h855kddqbay0pcbwr8a7i8m6ilz67cfn-python-3.10.7
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── hl6lb3irs8wrfv49fnirxshsq590pi9v-zlib-1.2.13
    │   ├── include
    │   ├── lib
    │   └── share
    ├── ivywpq9ff4kl8na87r6gig5z7i7vf9q8-python-pypa-build-0.7.0
    │   ├── bin
    │   ├── lib
    │   └── share
    ├── j2flhwg0sm59blypg3wdc6d4crdzj3rh-freetype-2.13.0
    │   ├── bin
    │   ├── include
    │   ├── lib
    │   └── share
    ├── ka0rng7n5bmxprppshpqhmkzf8hx8nq9-libxcb-1.15
    │   ├── include
    │   ├── lib
    │   └── share
    ├── kl7vp2gvcp2f2r2xrsiyzcvl794wz6sh-openssl-3.0.8
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── l0y8jkmip7qpa7x33972mn0dsfy8ac01-libffi-3.4.4
    │   ├── include
    │   ├── lib
    │   └── share
    ├── l71i95gr8rhh5jzjs1i4nh9g9nrir609-python-toml-0.10.2
    │   ├── lib
    │   └── share
    ├── ln6hxqjvz6m9gdd9s97pivlqck7hzs99-glibc-2.35
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   ├── libexec
    │   ├── sbin
    │   ├── share
    │   └── var
    ├── mcllmdn8li69sacc0cciqrb3lyz35haz-sqlite-3.39.3
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── nigj1sqxh39ghqpwx5chrkf14h8iwpnq-fontconfig-minimal-2.14.0
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── p425d7r839x9f3w0kl7rf4cd516a3ag4-libxau-1.0.10
    │   ├── include
    │   ├── lib
    │   └── share
    ├── q8p6b4yikc9g368qfja859f7531wnvwa-tk-8.6.12
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── rcq6448hglszg33iy2wi0hy6g6n0b6s2-python-3.10.7
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── rg3fzmw1l4ljqgjq4vq9j3a7v199mzwy-xz-5.2.8
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── rkqkby3dxsvdnijcbh7rlbz71p7hv3mq-libxrender-0.9.10
    │   ├── include
    │   ├── lib
    │   └── share
    ├── v0yfip4qfayzzn6a2q4crj8wpjvgf03p-python-wrapper-3.10.7
    │   └── bin
    ├── v9p25q9l5nnaixkhpap5rnymmwbhf9rp-bash-minimal-5.1.16
    │   ├── bin
    │   ├── etc
    │   └── share
    ├── vcsr8llvqi5rnxyb2vwclrnijzy7l7im-profile
    │   ├── bin
    │   ├── etc
    │   ├── include -> /gnu/store/h855kddqbay0pcbwr8a7i8m6ilz67cfn-python-3.10.7/include
    │   ├── lib
    │   ├── manifest
    │   └── share
    ├── vgjr502n1fs9w6k00m0qcy0lbq5by2is-libyaml-0.2.5
    │   ├── include
    │   ├── lib
    │   └── share
    ├── xkr1i02q2j0j0l8hksbnh9kcrdrizyk4-readline-8.1.2
    │   ├── bin
    │   ├── include
    │   ├── lib
    │   └── share
    ├── xswizvlbq908adhnsykybxnsblzx9xvn-python-setuptools-67.6.1
    │   ├── lib
    │   └── share
    ├── xwwisbnpbg73wzh9rfmghm51i1k32030-bzip2-1.0.8
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── y69k9rk030p8vad3d9mpm0xy7xaz6h1v-python-pyparsing-3.0.6
    │   ├── lib
    │   └── share
    ├── y9hn5c5dpvs5y1qdz39s3x4fps03l67s-info-dir
    │   └── share
    ├── yp3qv6rzszzjnh3b3hw9122wjcd6ls6h-python-nose-1.3.7
    │   ├── bin
    │   ├── lib
    │   └── share
    ├── z60r50m2crx3qlha1k4ciywidyl1x5r9-libxdmcp-1.1.3
    │   ├── include
    │   ├── lib
    │   └── share
    ├── z655ilai81pbzbm35zwfqc64ha7wl37k-gdbm-1.23
    │   ├── bin
    │   ├── etc
    │   ├── include
    │   ├── lib
    │   └── share
    ├── zan3d655r50cv5gxvj2l5yybwhy6x3n4-font-dejavu-2.37
    │   └── share
    ├── zq0ny4dv3mhswbci0mac7pxb7lbylf8r-python-pep517-bootstrap-0.9.1
    │   ├── lib
    │   └── share
    └── zzyywykw7kriln18rxqd82f0k5kidla7-bash-static-5.1.16
        ├── bin
        └── share

223 directories, 1 file
```

What is all this stuff? Why do we even need half of it?

Let's see why sqlite is in here:


Now why don't you try running it on your (linux) machine!


```bash
guix shell
```

https://news.ycombinator.com/item?id=36239195

https://guix.gnu.org/cookbook/en/guix-cookbook.html#Software-Development





https://guix.gnu.org/en/blog/2023/write-package-definitions-in-a-breeze/



# No parentheses? No problem!

Parenthenses can be scary. Let's define a package in JSON!




# Look mom, no guix? no package manager? uhhhh

# cloud buzzwords

Iaas
guix operating-system

Terraform???
guix image




## 
```bash
$ name="$(docker create nginx:alpine)" docker export "$name" | tar
```

```bash
$ guix build nginx | xargs tree
/gnu/store/pvqw03ax02qj46wnd6p8zpj7k35b230s-nginx-1.23.3
├── etc
│   └── ld.so.cache
├── sbin
│   └── nginx
└── share
    ├── doc
    │   └── nginx-1.23.3
    │       └── LICENSE
    ├── man
    │   └── man8
    │       └── nginx.8.gz
    └── nginx
        ├── conf
        │   ├── fastcgi.conf
        │   ├── fastcgi.conf.default
        │   ├── fastcgi_params
        │   ├── fastcgi_params.default
        │   ├── koi-utf
        │   ├── koi-win
        │   ├── mime.types
        │   ├── mime.types.default
        │   ├── nginx.conf
        │   ├── nginx.conf.default
        │   ├── scgi_params
        │   ├── scgi_params.default
        │   ├── uwsgi_params
        │   ├── uwsgi_params.default
        │   └── win-utf
        └── html
            ├── 50x.html
            └── index.html

11 directories, 21 files
```


https://www.youtube.com/watch?v=eWXoKjWCh60

run guix services in container
    make a whole os and cram it in a container
run just one guix service with a lightweight init???
    boom?
    

