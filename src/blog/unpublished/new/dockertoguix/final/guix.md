REF
https://github.com/pjotrp/guix-notes/blob/master/HACKING.org
https://guix.gnu.org/en/blog/2023/from-development-environments-to-continuous-integrationthe-ultimate-guide-to-software-development-with-guix/
https://guix.gnu.org/en/blog/2018/a-packaging-tutorial-for-guix/


TODO
todo which binary check why a binary is installed
https://www.futurile.net/
    so many cool guix tricks!
    the goat!
https://pages.stat.wisc.edu/~yandell/R_for_data_sciences/connect/docker.html
https://issues.guix.gnu.org/55680
https://guix.gnu.org/blog/2019/gnu-guix-1.0.0-released/



























# THIS IS THE REAL START

# Foreward uhhhhh
Guix is hard and scary. I wanted use it to install my packages, manage my system, manage my other systems, and package my software, to but the [scary parentheses](link to guile) and other Guixyness kept getting in the way. This is my attempt at learning the foundations of Guix, step by step from package manager to the future of software development.

I had been using Guix for about a year until I wrote this series. I started by installing `guix` to my existing Debian ([binary installation](https://guix.gnu.org/manual/en/html_node/Binary-Installation.html)) system because I wanted to manage my dotfiles and switch from the Gnome desktop environment to the Sway window manager. I had seen snippets of what Guix and Nix can do from occasional postings on Hacker News. I wanted to 

Now a year later I still find myself barely able to write a package myself and barely able to uhhh. I knew I could Guixify my home lab, which comprised of. I was kind of sick of Docker at this point, after having configured `nginx` and, then attempting to switch to Podman, then still wanting to use Docker Compose, but kubernetes idk
I was using Docker like it was a package manager, and Docker is not a package manager todo see thing.

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

Looks like we are missing some dependencies.

`src/inline-website.py`
```python
#!/usr/bin/env python3

import chevron
import pyyaml
import markdddadf

...
```

`inline-website.py` tried to `import chevron`, which is a Python module I don't have installed.

> the `#!/shebang` [Wikipedia](https://en.wikipedia.org/wiki/Shebang_%28Unix%29) allows me to make my python script executable - instead of `python3 src/inline-website.py` I may simply `chmod +x src/inline-website.py && ./src/inline-website.py`

Let's fix this:

```bash
$ pip install chevron pyyaml markdown
```

you me us we who?

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

cnfusing language kind of
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

aside: guix build in deptch with source and grafts? what is that
and changing compile flags and clang-toolchain and stuff

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

What if there was a way to build and install several packages to a certain place? Kind of like how ... todo This would be kind of similar to how `pip` installs everything to `~/.local/share/pip`.

## Installing packages to a profile
    `guix package` ([manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-package.html))

todo Let's try installing these packages with `guix package`. todo move the rest down Let's try installing these packages to our *user* profile. Compare this to package managers like Debian's `apt` or Arch's `pacman` - they install packages to the system profile, available to any user tod oreference,. This is why they require root privileges (`sudo`) todo ehhh?. Many language specific package managers like `pip` or `npm` often instead install packages to places like the user profile (`~/.local/share/pip` from `pip`) or the project directory (`node_modules` from `npm`). Guix can install packages to anywhere - the system, the user, or the project directory (todo link to guix pack? uhhh idk) idksystem wide packages and user packages, but here we want to install as us, the user confuding todo! todo remove This is like how `pip` would install packages to a user specific `site-packages`, without requiring root. todo guix differs in the store!

```bash
$ guix package --install python-chevron python-pyyaml python-markdown
The following packages will be installed:
todo fill this in
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

> pro tip: try some aliases instead, like `guix install <packages>` or `guix remove <packages>` todo link

It didn't work. After all, why would it? As we saw above, todo In order for `python` to import an external module, it needs to be available in the `PYTHONPATH` environment variable. Where should we point our `PYTHONPATH` to find the Python modules Guix just installed for us? Guix provides a hint for us in the output of `guix package`.

todo?

It works, but where does `guix package` install packages?

`~/.guix-profile`? Kind of! todo Learn more about [the Store](https://guix.gnu.org/manual/en/html_node/The-Store.html)

Instead of installing to the entire user profile, I only really want to install to this project.

todo rewrite
Every `guix package` operation is a transaction, allowing us to switch to previous generations with ease. Let's roll back to the previous generation (where nothing was installed) and then install everything to a special new *profile* `inline-website`. Remeber, a profile is merely a directory of installed packages. Remember our `guix build python-chevron` example from before? That was a single package. `guix package` allows us to install multiple packages to a directory, which is called a *profile*. If you wanted to compare Guix profiles to `pip`, then `pip`'s default profile (or directory of installed python modules) would be `~/.local/share/pip`. Debian's `apt` default "profile" (or directory of installed packages) would technically located at the system root `/`, which is where we find `/bin`, `/etc/`, `/lib`, and more.

```bash
$ guix package --roll-back
$ guix package --list-installed # will output nothing because nothing is installed
$ pwd
/home/griffin/git/inline-website
$ guix package --profile=my-profile --install python-chevron python-pyyaml python-markdown
The following packages will be installed:
   python-chevron  0.14.0
   python-markdown 3.3.4
   python-pyyaml   6.0

hint: Consider setting the necessary environment variables by running:

     GUIX_PROFILE="/home/griffin/git/inline-website/my-profile"
     . "$GUIX_PROFILE/etc/profile"

Alternately, see `guix package --search-paths -p "/home/griffin/git/inline-website/my-profile"'.
```

Let's explore what a Guix profile looks like:
Let's see how Guix represents these mysterious profiles:

```bash
$ ls -lh
total 20K
-rw-r--r-- 1 griffin griffin  121 Dec 29 08:09 Dockerfile
-rw-r--r-- 1 griffin griffin  366 Sep 19 21:33 Makefile
lrwxrwxrwx 1 griffin griffin   17 Dec 29 13:12 my-profile -> my-profile-1-link
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:12 my-profile-1-link -> /gnu/store/8l01qmyd7f8ac4nanbn8sqj7jrkq0hpn-profile
-rw-r--r-- 1 griffin griffin 1.2K Sep 19 21:33 README
drwxr-xr-x 2 griffin griffin 4.0K Dec 29 08:20 src
drwxr-xr-x 3 griffin griffin 4.0K Sep 19 21:33 test
```

We can see there are two new interesting symlinks. It also appears none of the actual contents of the packages have been installed in the directory. Instead, it looks like they might be at `/gnu/store/8l01qmyd7f8ac4nanbn8sqj7jrkq0hpn-profile`.

What if I removed a package?

```bash
$ guix package --profile=my-profile --remove python-chevron
The following package will be removed:
   python-chevron 0.14.0

The following derivation will be built:
  /gnu/store/kq6ffx5lfp3g2xqkivk3a6zp40ldqw9g-profile.drv

building CA certificate bundle...
listing Emacs sub-directories...
building fonts directory...
building directory of Info manuals...
building profile with 2 packages...
hint: Consider setting the necessary environment variables by running:

     GUIX_PROFILE="/home/griffin/git/inline-website/my-profile"
     . "$GUIX_PROFILE/etc/profile"

Alternately, see `guix package --search-paths -p "/home/griffin/git/inline-website/my-profile"'.
```

todo what is a derivation - `guix` has never seen a profile where `python-chevron` and `python-` - think of all the mixed libraryes whatever
if we do this again we can see no new derivatino is built - guix knows what happens when `python-chevron` and `python` are combined, and caches it for us - not actually tho idk
man idk maybe remove this blurb

```bash
$ ls -lh
total 20K
-rw-r--r-- 1 griffin griffin  121 Dec 29 08:09 Dockerfile
-rw-r--r-- 1 griffin griffin  366 Sep 19 21:33 Makefile
lrwxrwxrwx 1 griffin griffin   17 Dec 29 13:55 my-profile -> my-profile-2-link
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:12 my-profile-1-link -> /gnu/store/8l01qmyd7f8ac4nanbn8sqj7jrkq0hpn-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:55 my-profile-2-link -> /gnu/store/8pj526phyk0kw5yi8kizlp5nlkw1q8wz-profile
-rw-r--r-- 1 griffin griffin 1.2K Sep 19 21:33 README
drwxr-xr-x 2 griffin griffin 4.0K Dec 29 08:20 src
drwxr-xr-x 3 griffin griffin 4.0K Sep 19 21:33 test
```

Let's re-install `python-chevron`:

```bash
$ guix package --profile=my-profile --install python-chevron
The following package will be installed:
   python-chevron 0.14.0

The following derivation will be built:
  /gnu/store/dmmqwf8wbmzh9prdnkvb3b4c30mg6adv-profile.drv

building CA certificate bundle...
listing Emacs sub-directories...
building fonts directory...
building directory of Info manuals...
building profile with 3 packages...
hint: Consider setting the necessary environment variables by running:

     GUIX_PROFILE="/home/griffin/git/inline-website/my-profile"
     . "$GUIX_PROFILE/etc/profile"

Alternately, see `guix package --search-paths -p "/home/griffin/git/inline-website/my-profile"'.
$ ls -lh
total 20K
-rw-r--r-- 1 griffin griffin  121 Dec 29 08:09 Dockerfile
-rw-r--r-- 1 griffin griffin  366 Sep 19 21:33 Makefile
lrwxrwxrwx 1 griffin griffin   17 Dec 29 14:01 my-profile -> my-profile-3-link
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:12 my-profile-1-link -> /gnu/store/8l01qmyd7f8ac4nanbn8sqj7jrkq0hpn-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:55 my-profile-2-link -> /gnu/store/8pj526phyk0kw5yi8kizlp5nlkw1q8wz-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 14:01 my-profile-3-link -> /gnu/store/viznir6599bmw7zz8b1966gf71v2ymsn-profile
-rw-r--r-- 1 griffin griffin 1.2K Sep 19 21:33 README
drwxr-xr-x 2 griffin griffin 4.0K Dec 29 08:20 src
drwxr-xr-x 3 griffin griffin 4.0K Sep 19 21:33 test
```

Inspecting the results, we see `my-profile` now points to `my-profile-3-link`. Each of these three links are a *generation*. A profile is actually just a generation point in time and space uhhhhhhhh

```bash
$ guix package --profile=my-profile --list-generations
Generation 1	Dec 29 2023 13:11:02
  python-markdown	3.3.4 	out	/gnu/store/4jp981ms6nwyv844r4xf1blfyakz96x8-python-markdown-3.3.4
  python-pyyaml  	6.0   	out	/gnu/store/007vydgsvjpz061fxgs01nj1n65dxf6i-python-pyyaml-6.0
  python-chevron 	0.14.0	out	/gnu/store/fgl39clk8v1h142vxkwiwkhqjp1svg3f-python-chevron-0.14.0

Generation 2	Dec 29 2023 13:55:15
 - python-chevron	0.14.0	out	/gnu/store/fgl39clk8v1h142vxkwiwkhqjp1svg3f-python-chevron-0.14.0

Generation 3	Dec 29 2023 14:01:40	(current)
 + python-chevron	0.14.0	out	/gnu/store/fgl39clk8v1h142vxkwiwkhqjp1svg3f-python-chevron-0.14.0
```

We are free to switch between generations with ease using `--switch-generation` ([manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-package.html#index-generations).

Let's switch to the second generation of our profile, when we removed `python-chevron`, leaving us with `python-pyyaml` and `python-markdown`:

```bash
$  guix package --profile=my-profile --switch-generation=2
switched from generation 3 to 2
 ls -lh
total 20K
-rw-r--r-- 1 griffin griffin  121 Dec 29 08:09 Dockerfile
-rw-r--r-- 1 griffin griffin  366 Sep 19 21:33 Makefile
lrwxrwxrwx 1 griffin griffin   17 Dec 29 14:19 my-profile -> my-profile-2-link
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:12 my-profile-1-link -> /gnu/store/8l01qmyd7f8ac4nanbn8sqj7jrkq0hpn-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:55 my-profile-2-link -> /gnu/store/8pj526phyk0kw5yi8kizlp5nlkw1q8wz-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 14:01 my-profile-3-link -> /gnu/store/viznir6599bmw7zz8b1966gf71v2ymsn-profile
-rw-r--r-- 1 griffin griffin 1.2K Sep 19 21:33 README
drwxr-xr-x 2 griffin griffin 4.0K Dec 29 08:20 src
drwxr-xr-x 3 griffin griffin 4.0K Sep 19 21:33 test
$ guix package --profile=my-profile --list-installed
python-markdown	3.3.4	out	/gnu/store/4jp981ms6nwyv844r4xf1blfyakz96x8-python-markdown-3.3.4
python-pyyaml  	6.0  	out	/gnu/store/007vydgsvjpz061fxgs01nj1n65dxf6i-python-pyyaml-6.0
```

No files have been moved or copies or deleted - the only thing that changed was the `my-profile` symlink now points to `my-profile-2-link`

We can also roll back https://guix.gnu.org/manual/en/html_node/Invoking-guix-package.html#index-rolling-back

```
$ guix package --profile=my-profile --roll-back
switched from generation 2 to 1
$ guix package --profile=my-profile --roll-back
The following derivation will be built:
  /gnu/store/s418j4p738i062m49nl0jafl1j52k2g4-profile.drv

building profile with 0 packages...
switched from generation 1 to 0
$ guix package --profile=my-profile --roll-back
switched from generation 0 to 0
```

Rolling back from generation 1 to generation 0 actually created a special new generation: the 0th generation. The manual states how this generation "contains no files apart from its own metadata".

As shown again, rolling back from generation 0 effectively does nothing, as we are already at the 0th generation.

Let's inspect what the zeroth generation looks like

```bash
$ ls -lh
total 20K
-rw-r--r-- 1 griffin griffin  121 Dec 29 08:09 Dockerfile
-rw-r--r-- 1 griffin griffin  366 Sep 19 21:33 Makefile
lrwxrwxrwx 1 griffin griffin   17 Dec 29 14:21 my-profile -> my-profile-0-link
lrwxrwxrwx 1 griffin griffin   51 Dec 29 14:21 my-profile-0-link -> /gnu/store/yx25cxlsy5klj05fazxy18jjh2z5qi2f-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:12 my-profile-1-link -> /gnu/store/8l01qmyd7f8ac4nanbn8sqj7jrkq0hpn-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:55 my-profile-2-link -> /gnu/store/8pj526phyk0kw5yi8kizlp5nlkw1q8wz-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 14:01 my-profile-3-link -> /gnu/store/viznir6599bmw7zz8b1966gf71v2ymsn-profile
-rw-r--r-- 1 griffin griffin 1.2K Sep 19 21:33 README
drwxr-xr-x 2 griffin griffin 4.0K Dec 29 08:20 src
drwxr-xr-x 3 griffin griffin 4.0K Sep 19 21:33 test
```

What if we delete a generation?

```bash
$ guix package --profile=my-profile --delete-generations=1
deleting my-profile-1-link
$ ls -lh
total 20K
-rw-r--r-- 1 griffin griffin  121 Dec 29 08:09 Dockerfile
-rw-r--r-- 1 griffin griffin  366 Sep 19 21:33 Makefile
lrwxrwxrwx 1 griffin griffin   17 Dec 29 14:24 my-profile -> my-profile-2-link
lrwxrwxrwx 1 griffin griffin   51 Dec 29 14:21 my-profile-0-link -> /gnu/store/yx25cxlsy5klj05fazxy18jjh2z5qi2f-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 13:55 my-profile-2-link -> /gnu/store/8pj526phyk0kw5yi8kizlp5nlkw1q8wz-profile
lrwxrwxrwx 1 griffin griffin   51 Dec 29 14:01 my-profile-3-link -> /gnu/store/viznir6599bmw7zz8b1966gf71v2ymsn-profile
-rw-r--r-- 1 griffin griffin 1.2K Sep 19 21:33 README
drwxr-xr-x 2 griffin griffin 4.0K Dec 29 08:20 src
drwxr-xr-x 3 griffin griffin 4.0K Sep 19 21:33 test
```

> note: profiles are *just files*. `guix package --profile=my-profile` is the same as `guix package --profile=my-profile-2-link`. If we wanted to see what packages were installed in the third generation, then just `guix package --profile=my-profile-3-link --list-installed`.

What if we navigated to the `/gnu/store/8l01qmyd7f8ac4nanbn8sqj7jrkq0hpn-profile`
It's still there! How can we get rid of it? meet `guix gc`

It's gone!



# TODO todo
`guix gc`
this is def a separate article!
https://dthompson.us/posts/guix-for-development.html
https://news.ycombinator.com/item?id=34490376
https://en.wikipedia.org/wiki/GNU_Guix




We know how to install and remove packages from profiles, and how to switch between profiles. This still begs the question: What is a profile?

should this be introduced earlier??

Remember, a Guix profile is a directory of packages. What dose this look like?

Whenever we make a new profile with `guix package --install`, we see this:

```
The following derivation will be built:
  /gnu/store/dmmqwf8wbmzh9prdnkvb3b4c30mg6adv-profile.drv

building CA certificate bundle...
listing Emacs sub-directories...
building fonts directory...
building directory of Info manuals...
building profile with 3 packages...
```

What is Guix doing?

### Inspecting profile contents




In fact, remember when we `guix build chevron`? The `chevron` here is the same `chevron` from there! Let's see what `guix gc` has to say about this


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

# TODO
how to make the shebang work - see chevron bin/guix-bash magic

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
what user am i? --user=root
what login shell? why no /usr/bin/env? cat /etc/passwd
where is the shell if no args are given
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
```

/etc/passwd
/sys
compare system isolation

COMPARE systme shells, envirronments, etc
guix shell --pure
guix shell --container
guix pack --format=docker
FROM debian
FROM alpine
FROM scratch

is guix pack --format=docker the same as guix pack --format=tar FROM scratch COPY gnu /
guix pack allows specifying a label! neat!

its cheating when these arent all exaclty the same: guix shell and guix shell --pure and guix shell --container and guix pack 

/bin/sh always exists - is this what guix shell no args does?

### gnu-build-system and copy-build-system

### Advanced manifest trickery?
todo manfiest.md

### Packaging packages
    `guix pack`

The [manual](https://guix.gnu.org/manual/en/html_node/Invoking-guix-pack.html) says how `guix pack` allows us to "pass software to people who are not (yet!) lucky enough to be using Guix". "creates a shrink-wrapped *pack* or *software bundle* ... containing the binaries of the software you're intereste in, and all its dependnecies"

> The guix pack command creates a shrink-wrapped pack or software bundle: it creates a tarball or some other archive containing the binaries of the software you’re interested in, and all its dependencies. The resulting archive can be used on any machine that does not have Guix, and people can run the exact same binaries as those you have with Guix. 

> note that `guix pack` also supports taking a list of packages via the command line - `guix pack python python-chevron python-markdown` would produce the same result as `guix pack --manifest=manifest.scm`

#### as a tarball

```
$ guix pack --format=tarball --manifest=manifest.scm
```

### todo talk about networking
docker is great because with `docker compose up -d` you can have all the databases and other services your app needs instantly. but what if you wanted to communicate from the host to docker? or docker to the host?

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
    # Guixify ncspot
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
    wow these tools are really cool what if we could use them with other package managers?????? unguix them per say

# derivations what thel hell is this
https://guix.gnu.org/en/blog/2023/dissecting-guix-part-1-derivations/
