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
