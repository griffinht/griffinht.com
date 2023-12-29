https://www.futurile.net/
    so many cool guix tricks!
    the goat!
https://pages.stat.wisc.edu/~yandell/R_for_data_sciences/connect/docker.html
https://issues.guix.gnu.org/55680
https://guix.gnu.org/blog/2019/gnu-guix-1.0.0-released/

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



























# THIS IS THE REAL START

Guix is hard and scary. I wanted use it to install my packages, manage my system, manage my other systems, and package my software, to but the [scary parentheses](link to guile) and other Guixyness kept getting in the way. This is my attempt at learning the foundations of Guix, step by step from package manager to the future of software development.

Our story begins with `inline-website`, a tiny and semi broken Python script I wrote to create this website, mostly because I didn't want to learn how to use one of the many existing static site generators. Unfortunately, `inline-website` has *dependencies*. Thanks to the advent of package managers, blah blah bnlah quit yappin

blah blah blah quit yappin

```bash
todo pick a specific commit so the reader can follow along?
$ git clone todo.griffinht.com/todo
$ python3 src/inline-website.py
Traceback (most recent call last):
  File "/home/griffin/git/inline-website/src/inline-website.py", line 11, in <module>
    import chevron
ModuleNotFoundError: No module named 'chevron'
```

That's because `inline-website.py` tried to `import chevron`, which is a Python module I don't have installed.

`src/inline-website.py`
```python
#!/usr/bin/env python3

import chevron
import pyyaml
import markdddadf

...
```

> the `#!/shebang` [Wikipedia](https://en.wikipedia.org/wiki/Shebang_%28Unix%29) allows me to make my python script executable - instead of `python src/inline-website.py` I may simply `chmod +x src/inline-website.py && ./src/inline-website.py`

Let's fix this:

```bash
$ pip install chevron pyyaml markdown
```

But you are a seasoned software developer. You are sick of all these random language specific package managers. What you need is the one true package manager. Docker to the rescue!
todo read a blog post about why docker is so great

`pip` `npm` `cargo` `whatever go uses`
Let's not even get started with Java's package managers.

watch the sarcasm
There is only one small issue with this genius plan. Docker is not a package manager. see why todo

`Dockerfile`
```Dockerfile

COPY src .

RUN pip install chevron pyyaml markdown


ENTRYPOINT "inline-website.py"
```

Docker is the last package manager you will ever need! Just `git clone && docker build . --tag inline-website && docker run --rm up`?
This isn't the most ergonomic approach, but you know what comes next.

`docker-compose.yml`
```yaml
inline-website:
    image:
        build: .
    volumes: src./sadf
```

`git clone && docker compose up`. Done.

Problem solved! kKind of. This is akward and many things don't work - how can you
Check out all these workarounds 
java maven
sockets?
host communication?
gui applications?

But it is nice to run untrusted code in a compact little contained container.


Sure it tends to be more of a pain to instal but it can be installed eveywher link to install
Sure it requires root but actually it doesn't require root but it kind of does
But podman doesnn't so that's cool but podman has its own issues
And why am I worrying about volumes and networking and user land proxies and namespaces oh my! I just wanted `import chevron`

Anyways, let's ignore this for now. Docker also allows us to use our software elsewhere. I'm going to work on this website, `griffinht.com`, which is generated from `inline-website`.

```bash
$ git clone asdftodo
$ docker run --rm --volume ./src:asd inline-website
```

We already know the first issue - ergonomics

`docker-compose.yml`
```yaml
build:
    image: inline-website
```

```bash
$ docker compose run build
```

I can also build and package ("Dockerize") as a Docker image:

`Dockerfile`
```Dockerfile
FROM inline-website as build

COPY src .

RUN inline-website bruh bruh todo
```

Now from my 
`Dockerfile`
```Dockerfile
FROM nginx

COPY --from=inline-website /buildtodo .
```


why?
Docker is not a package manager. It may look and feel like a package manager at times, but Docker is not a package manager.


Let's start from the beginning and see how this entire process looks with Guix.



todo compare blogs which go through the above process?

Enough of Dockerize - let's Guixify all the things!

# Guix time

## Introduction to Guix as a package manager

Rewinding to our original problem, we want a way to install the Python modules `chevron`, `markdown`, and `yaml`, but we don't want to use `pip`.

Starting with `chevron`, I wonder who packages this already? [Repology](https://repology.org/project/python:chevron/versions) shows there are a variety of non PyPI repositories with the Python module `chevron`. Guix is on that list! We also could have queried Guix's official library of packages (channel todo) directly with `guix search`.

```bash
$ guix search python markdown
name: python-markdown
version: 3.3.4
outputs:
+ out: everything
systems: x86_64-linux i686-linux
dependencies: python-nose@1.3.7 python-pyyaml@6.0
location: gnu/packages/python-xyz.scm:13176:2
homepage: https://python-markdown.github.io/
license: Modified BSD
synopsis: Python implementation of Markdown  
description: This package provides a Python implementation of John Gruber's Markdown.  The library features international input, various Markdown extensions, and several HTML output formats.  A command line wrapper markdown_py is also provided to convert Markdown files to HTML.
relevance: 35

...
```

> there is also a web search at https://packages.guix.gnu.org/

## Building packages
    `guix build` ([manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-build.html))

Guix can build `python-chevron` for us. `guix build` will build a package and output the location of the resulting files.

```bash
$ tree -L 5 -I 'chevron-*' $(guix build python-chevron)
/gnu/store/fgl39clk8v1h142vxkwiwkhqjp1svg3f-python-chevron-0.14.0
├── bin
│   └── chevron
└── lib
    └── python3.10
        └── site-packages
            └── chevron
                ├── __init__.py
                ├── main.py
                ├── metadata.py
                ├── __pycache__
                ├── renderer.py
                └── tokenizer.py

7 directories, 6 files
```

> `guix build` is a very powerful tool - let's check out `tar -xf $(guix build python-chevron --source) && tree -L bruh todo`

The `guix build` output contains the Python files we need for `import chevron` to work. But how do we tell Python where to find them? Let's see how `pip` does it:

```bash
$ pip install chevron
$ tree -L 1 ~/.local/share/pip/chevron
/home/griffin/.local/share/pip/chevron
├── __init__.py
├── main.py
├── metadata.py
├── __pycache__
├── renderer.py
└── tokenizer.py

2 directories, 5 files
$ env | grep PYTHON
PYTHONPATH=:/home/griffin/.local/share/pip:/home/griffin/.local/share/pip:/home/griffin/.local/share/pip:/home/griffin/.local/share/pip
$ pip uninstall chevron
```

Looks like `pip` sets the `PYTHONPATH` environment variable to the place where `pip` installs Python modules.

Let's append the path from `guix build python-chevron` to `PYTHONPATH`:

```bash
$ PYTHONPATH="$(guix build python-chevron)/lib/python3.10/site-packages:$PYTHONPATH" ./src/inline-website.py
Traceback (most recent call last):
  File "/home/griffin/git/inline-website/./src/inline-website.py", line 12, in <module>
    import yaml
ModuleNotFoundError: No module named 'yaml'
```

It worked! Python was able to find import the `chevron` module from the output of `guix build python-chevron`. Now Python is complaining about missing the other two modules we need, `yaml` and `mustache`. However, this manual `guix build` approach is rather awkward.

What if there was a way to build and install several packages to a certain place? This kind of be similar to how `pip` installs everything to `~/.local/share/pip`.

## Installing packages to a profile
    `guix package` ([manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-package.html))

Let's try installing these packages to our *user* profile. Compare this to package managers like Debian's `apt` or Arch's `pacman` - they install packages to the system profile, available to any user tod oreference,. This is why they require root privileges (`sudo`) todo ehhh?. Many language specific package managers like `pip` or `npm` often instead install packages to places like the user profile (`~/.local/share/pip` from `pip`) or the project directory (`node_modules` from `npm`). Guix can install packages to anywhere - the system, the user, or the project directory (todo link to guix pack? uhhh idk) idksystem wide packages and user packages, but here we want to install as us, the user confuding todo! todo remove This is like how `pip` would install packages to a user specific `site-packages`, without requiring root. todo guix differs in the store!

```bash
$ guix package --install python-chevron python-pyyaml python-markdown
The following packages will be installed:
...
hint: Consider setting the necessary environment variables by running:

     GUIX_PROFILE="/home/griffin/.guix-profile"
     . "$GUIX_PROFILE/etc/profile"

Alternately, see `guix package --search-paths -p "/home/griffin/.guix-profile"'.
$ ./src/inline-website.py
Traceback (most recent call last):
  File "/home/griffin/git/inline-website/./src/inline-website.py", line 11, in <module>
    import chevron
ModuleNotFoundError: No module named 'chevron'
```

> pro tip: try some aliases instead, like `guix install` or `guix remove` todo link

It didn't work. After all, why would it? In order for `python` to import an external module, it needs to be available in the `PYTHONPATH` environment variable. Where should we point our `PYTHONPATH` to find the Python modules Guix just installed for us? You can probably guess the answer based on the hint that `guix package` gave us, but we will get there.

It works, but where does `guix package` install packages?

`~/.guix-profile`? Kind of! todo Learn more about [the Store](https://guix.gnu.org/manual/en/html_node/The-Store.html)



Debian users may be familiar with this problem - removing a package will not remove its dependencies until `sudo apt autoremove` is ran. This can be helpful with brittle system which may have incidentally been relying on idk todo. This can be annoying when todo debian find which packages have been installed by the user. This mixes declarative and imperative i think
I'm not sure if `pip` handles this at all - we `pip uninstall chevron` but all the other things are still there?





We have actually been relying on the system installed version of `python3` - in my case, the Debian todo link to deb repo?




Where did we just install these packages to?
If this were Debian
`/usr/bin`
`/etc/bin`
whatever

We can even describe this profile with . This would kind of be like `pip list` or `apt list --installed`. Guix also provides many other goodies, like `guix gc --refe` or `guix graph` to generate a graph. Let's check it out!

todo insert guix graph here

There are some really cool concepts that I didn't cover here. The [manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-package.html) is a great reference if you'd like to learn more about upgrades, rollbacks, transactions, generations, reproducibility, uhhh and more. https://guix.gnu.org/manual/en/html_node/Features.html

One of the killer features of Guix is `guix shell`. Let's go back to the original scenario: we just `git clone`'d a repository and want to install some Python modules so we can do some developing. I don't actually want to gunk up my system or user profile with these project specific dependencies. What if there was a way to create an ephemeral developer environment with exactly what I needed for `inline-website`? `apt` installs everything systemwide, `pip` installs everything to my user profile, `npm` installs everything to the `node_modules` in the project workspace, and Docker just puts everything in a magical container. Guix has `guix shell`.

> yes, `pip --target` can install to the current directory and `npm --global` installs to the user profile (or systemwide??), and `apt` might be able to install to the user profile without root access using [some trickery](https://askubuntu.com/questions/339/how-can-i-install-a-package-without-root-access) (and Docker can use all of these tools :))

## Installing packages in an ephemeral environment
## Installing packages in a one-off environment
    `guix shell`


```bash
$ guix shell --manifest=manifest.scm -- ./src/inline-website.py --help
usage: inline-website.py [-h] [-v] [-o OUTPUT] [-w] ...

positional arguments:
  REMAINDER

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
  -w, --watch
```

It worked! But how did it work? How was my Python script able to `import chevron`?

```bash
$ guix shell python python-chevron python-pyyaml python-markdown --pure --search-paths
export PATH="/gnu/store/vcsr8llvqi5rnxyb2vwclrnijzy7l7im-profile/bin"
export GUIX_PYTHONPATH="/gnu/store/vcsr8llvqi5rnxyb2vwclrnijzy7l7im-profile/lib/python3.10/site-packages"
$ GUIX_PYTHONPATH="/gnu/store/vcsr8llvqi5rnxyb2vwclrnijzy7l7im-profile/lib/python3.10/site-packages" ./src/inline-website --help
usage: inline-website.py [-h] [-v] [-o OUTPUT] [-w] ...

positional arguments:
  REMAINDER

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
  -w, --watch
```

```bash
$ guix shell python python-chevron python-pyyaml python-markdown --pure -- env
guix shell: error: env: command not found
$ guix shell python python-chevron python-pyyaml python-markdown --pure -- env
guix shell: error: env: command not found
```

Woops. Looks like our `guix shell` was a little *too* pure - we lost the `env` command!


Remeber when I said how Docker has containers but we have `guix shell`? `guix shell` is great, but it is not a container. And contaniers are great - (see why containers are great). Oftentimes I want to develop in a container - but how can I do that with Guix? Good thing there is `guix shell --container`.

### Creating a container
### Installing packages in a container
    `guix shell --container`
    `guix container`
nsenter?
https://guix.gnu.org/manual/en/html_node/Invoking-guix-container.html

Let's take `guix shell` one step further by creating an *isolated* environment containing nothing but the packages we asked for. 

```bash
$ guix shell --container --manifest=manifest.scm -- ./src/inline-website.py --help
guix shell: error: ./src/inline-website.py: command not found
```

This is a real container and it really does contain nothing but the packages we asked for (and the files from the current working directory).

If you thought `guix shell --pure` was bleak, prepare yourself for the barren world of `guix shell --container`

```bash
$ which env
/usr/bin/env
$ guix shell --pure -- $(which env)
$ guix shell --container -- $(which env)

### Packaging packages
    `guix pack`

The [manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-pack.html) says how `guix pack` allows us to "pass software to people who are not (yet!) lucky enough to be using Guix". "creates a shrink-wrapped *pack* or *software bundle* ... containing the binaries of the software you're intereste in, and all its dependnecies"

> The guix pack command creates a shrink-wrapped pack or software bundle: it creates a tarball or some other archive containing the binaries of the software you’re interested in, and all its dependencies. The resulting archive can be used on any machine that does not have Guix, and people can run the exact same binaries as those you have with Guix. 

> note that `guix pack` also supports taking a list of packages via the command line - `guix pack python python-chevron python-markdown` would produce the same result as `guix pack --manifest=manifest.scm`

#### as a tarball

```
$ guix pack --format=tarball --manifest=manifest.scm
```

### Vendoring packages

https://news.ycombinator.com/item?id=38793206
package vendoring has been heralded as

who else supports vendoring?
    cargo
        https://news.ycombinator.com/item?id=26724833
    npm
    go
    not debian!
        https://news.ycombinator.com/item?id=38160382
        link that guix hpc ludovid article?

guix makes this trivial, if desired
Let's dockerize this!

```Dockerfile
FROM scratch

COPY pack .
```

Just kidding, this approach is silly when `guix pack` can make a Docker image for us - see the next section!

### Packaging/shrink wrapping software environments/manifests
#### as a docker image
#### as a DEB
#### as an RPM
#### more
### todo channels?

### Packaging

Guix empowers us to create our own packages. Kind of like how `npm` and `pip` allow us to package JavaScript and Python applications, and Docker has 

> Where is the user package repository for Guix? It doesn't really exist (yet!?) - see the nix equivalent or guix channels. Right now, Guix is to Arch and Debian as <doesn't exist> is to docker hub/aur/not debian lol 

Going back to the original scenario, I am looking to package `inline-website` then use it in my `griffinht.com` project so I can generate my static site! Then I want to use `griffinht.com` in my home lab so I can deploy with nginx!

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

link to Decoding guix packages


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
    

But I don't want all this blot!

What bloat?

glibc!

We need glibc

I have glibc!

What glibc?

ldd glibc

Where did you get this?

It's on every system!

What systems?

Debian, Ubuntu, Arch, - everything!

How? find differences?

# On cheating when packaging

Docker is always cheating
    nooo you can't just ship the whole machine
    `FROM debian` docker go brrr
    noo you can't just switch to a different distro when the one you were using doesn't have the package you need
    `FROM arch` go brrr

Debian makes it hard to cheat - how can I even define my own package? Often this results in akwardly building from source when I want my software to just work
I think this is why many people dislike Debian - they have their favorite software that can't be packaged on Debian and they read https://news.ycombinator.com/item?id=38160382 and it just seems silly, so they
Compare this to Arch where vendoring is allowed - is it??? todo

Guix allows us to cheat however much we want - you won't find much cheating in the official guix channel (link) but here is an example of doing it yourself
Guix empowers everyone to become a full fledged hacker of their environment - try that in debian (lol) or swap gcc to clang or build from source (aur) or add a dep or change a build flag (gentoo) https://guix.gnu.org/en/blog/2023/parameterized-packages-for-gnu-guix/ https://blog.lispy.tech/
But parentehsees are indeed scary - and as (link cool blog post guix for non guix) puts it, guix often throws no bones in helping you. Error messages are completely opaque or hidden. If you can find the backtrace, you probably have no idea what wrong type to apply means - you just wanted to make a little software package!

# If Guix is so great why aren't we using it?

Use nix if you want transactional functional magic but way more people and packages
    nix cheats more - vendoring dependencies
    non free software

Guix is a gnu project
    see non guix

https://www.youtube.com/watch?v=LnU8SYakZQQ

# Guixify my software
# Guixify my $HOME
# Guixify my neovim
# Guixify my home lab
    # Guixify my docker
    # Guixify my vm
    # Guixify my vps
    # Guixify my desktop
show how guix runs circles around other package managers
continously give other package manager examples
    then should how guix does it better
    guix graph
    guix build --source
    guix gc
