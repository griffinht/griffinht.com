terminology: build server vs ci server

# secrets
# remote triggering
# the ability to build our software!
# saving it somewhere

What to use as a build server?

# Systems

Whether the system is a container or a VM or a physical machine, we run in to the following issues

Debian, Ubuntu, etc

packages would be installed system wide

```bash
sudo apt install nmap
```

Now we have an extra package laying around the system!

And its not repeatable at all!

# Containers

```Dockerfile
FROM debian

RUN apt update && apt install nmap
```

Problem solved! Except of course we need our source code!

```Dockerfile
FROM debian

RUN apt update && apt install nmap git && git clone $URL
```

```Dockerfile
FROM debian

RUN apt update && apt install nmap git

CMD git clone $URL
```

```Dockerfile
...
```

`docker run --rm debian sh -c 'apt update && apt install nmap git && git clone $URL'`

Build output? multi docker image?

We basically have Github Actions/Woodpecker CI at this point
https://woodpecker-ci.org/docs/usage/plugins/overview

# Guix




# building stuff

```sh
#!/bin/sh
repository="$1"

dir="$(mktemp -d)"
git clone "$repository" "$dir"

cleanup() {
    rm -rf "$dir"
}
trap cleanup EXIT

(
cd "$dir"

./ci/run
)
```

What is `./ci/run`? It's a script which my build server expects everything it builds to have!

```
ci
    run
src
    index.html
README
```

`ci/run`
```sh
#!/bin/sh

make build
```

Let's run it!
make: command not found

Let's install make!
# the host

sudo apt install make

# docker

docker run --rm --volume ./ci:/stuff debian sh -c 'apt update && apt install make'

see above for Dockerfile vs docker command comparison
generally considered acceptable to add build deps to dockerfile and then the dockerfile has to be rebuilt if the build deps change but that is usually rare enough
problem solved!

here is where things really start to fall apart
all we wanted was to install some build dependencies! why do we now have to worry about volumes and persistence!

# guix

guix shell make

well that was easy!

if we want we can containerize it of course
guix shell --container

or we can really containerize it

guix shell docker -- DOCKER_HOST=bruh docker run --rm bruh

or we can virtualize it

guix system vm wouldn't that be cool!
actually we could have done this all along if qemu was installed
... neat!
