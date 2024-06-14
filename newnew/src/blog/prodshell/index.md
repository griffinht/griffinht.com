# Developer Shells

While writing this I decided to turn `shell.sh` in to a standalone project!

Here is a pattern I have begun to use for my Docker compose files. 

I end up having a pile of shell scripts littered across all my Docker compose.

# The shell pattern

I decided to create a `shell.sh` script, which takes one argument 

`shell.sh`
```sh
#!/bin/sh

set -e

export SHELL_ENV="$1"
echo "entering $SHELL_ENV"

. "./$SHELL_ENV"

"$SHELL"

echo "exited $SHELL_ENV"
```

`prod.env`
```sh
export DOCKER_HOST="ssh://root@hostname"
```

## Example usage

```
shell.sh
scripts
- whichenv.sh
project
- compose.yml
- prod.env
- local.env
```

From my project folder, I can enter the shell for production.

```sh
$ ../shell.sh prod.env
entered prod.env
$ docker ps
...
$ whichenv.sh
you are in the prod.env environment!
$ exit
exited prod.env
$ whichenv.sh
Unknown command: whichenv.sh
```

The `docker` CLI reads the `DOCKER_HOST` environment variable to determine which host to run Docker commands. Since we set `DOCKER_HOST` to our production machine, `docker ps` shows us the containers on that machine, instead of the local machine.

This also works flawlessly with tools such as [`lazydocker`](https://github.com/jesseduffield/lazydocker) - the `DOCKER_HOST` environment variable is all that is needed to configure most Docker related tools.

I also demonstrated the `whichenv.sh` script - here is how that worked:

`scripts/whichenv.sh`
```sh
#!/bin/sh

echo you are in the "$SHELL_ENV" environment!
```

Since we added `scripts` to our `$PATH` variable, we are able to run any executable program in that folder.


## Example script: `ssh`

`scripts/ssh`
```sh
#!/bin/sh

# allow the user to use ssh as usual if arguments are provided
# ssh to the remote machine if no arguments are provided
```

### Usage

```
$ # default arguments
$ ssh
root@prod ~# logout
Connection to prod closed.
$ # allow for regular ssh usage
$ ssh user@otherhost
user@otherhost ~#
```

### Usage

## Example script: `mount.sh`

Often I find myself wanting to browse the 

`scripts/mount.sh`
```sh
todo
```

### Usage

```sh
$ ../shell.sh prod.env
entered prod.env
$ docker ps
$ mount.sh
mounted root@hostname
$ ls mnt
volumea
volumeb
$ exit
unmounted root@hostname
$ exit
exited prod.env
$
```

# Local environments, improved

`local.env`
```sh
export todo
```





# Other ideas

## Shell customization

This is a great opportunity for customization.

```sh
$ ../shell.sh prod.env
[prod.env] $ exit
$
```

Other ideas include setting the title of the terminal, or maybe changing the color of the cursor?

## Login scripts

`scripts/login`
```sh
#!/bin/sh

set -xe

ssh "$SSH_HOST" uptime
echo there are "$(docker ps --quiet | wc -l)" containers running
```

`shell.sh`
```
...

if [ -f "$scripts_dir/login" ]; then
    "$scripts_dir/login"
fi
"$SHELL"
```

### Usage

```
$ ../shell.sh prod.env
entering prod.env
16:34:38  up 2 days 16:57,  0 users,  load average: 0.00, 0.00, 0.00
there are 3 containers running
$ 
```
