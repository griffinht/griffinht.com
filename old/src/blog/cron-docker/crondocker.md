https://github.com/jhuckaby/Cronicle
https://healthchecks.io/
https://github.com/search?q=cron&type=repositories
https://crontab.guru/

# Getting started with `mcron` and Docker
# Using `mcron` and DOcker to run my containerized jobs

Docker is not an appropriate tool for task scheduling. For example, a Letsencrypt renewal job or a backup is something that needs to run regularly but not 

It would be incorrect to try to daemonize these tasks, and I have tried

My restic backup script looked something like this:

```sh
#!/bin/sh
set -e

time() {
  date +%Y-%m-%dT%T
}
echo SCRIPT STARTED
time

backup() {
  echo BACKUP
  time
  restic \
    --cleanup-cache \
    --verbose \
    backup "$BACKUP"
  time
  restic forget --prune --keep-daily 3 --keep-weekly 1 --keep-monthly 1
  time
}

echo START BACKUP LOOP
while true; do
  echo BACKUP LOOP
  time
  backup
  echo SLEEP
  time
  sleep 1d
  echo DONE SLEEPING
  time
done
```

The script boils down to running in an 
What if something goes wrong? The script is set to simply exit. How am I to be notified when something breaks? Additionally, this can be prone to resource leakage and wasteful resources. Compare that to `cron`, a purpose built daemon to run for a long time and report failures and job output and stuff. `cron` is significantly better than `while true; do script; sleep 1d; done`. `cron` gives monitoring and stuff.

Without `cron`, each job needs to be daemonized individually, often by writing a bug prone shell script. Look at the error handling I `set -e` - the script just exits on job failure, telling nobody.

# Surveying the existing cron options

I am going to need to add my 

## Why not just bind mount your scripts to an existing image?

This breaks Docker contexts, which is how I currently deploy my images. For example:
```bash
$ docker context use remote-server
$ docker compose up --build --detach
(won't work with bind mounts since the host is now remote)
```

## Why not just `rsync scripts remote`

I'd rather let Docker do the work

## Why not use a Dockerfile?
guix :)

## Guix

```sh
$ guix search cron
...
```

[https://packages.guix.gnu.org/search/?query=cron](https://packages.guix.gnu.org/search/?query=cron)

If something as simple as a job runner isn't packaged by Guix (todo doesn't hav ea guix package), then I figure it probably isn't worth using. That's why I'm going to use GNU [`mcron`](https://www.gnu.org/software/mcron/).

```sh
$ guix shell mcron
```

The whitepage documents some brief, such as being able to write jobs down the the second, and supporting rootless operation by default without a rootful daemon

Some brief documentation is available as a manpage, and the full documentation is available as an `info` manual, as many GNU projects are. I have always struggled to navigate through `info` manuals in my terminal. This isn't a problem as the online formats are nice and readable ([link](https://www.gnu.org/software/mcron/manual/)).

I'm going to test things out with a simple job which runs every minute. Note that `mcron` is written in [Guile](https://www.gnu.org/software/guile/) and also supports writing jobs in Scheme, a Lisp dialect. Neat!

`cron/mycrontab.vixie`
```cron
* * * * * echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false
```

```sh
$ mcron
mcron: There was an error reading files in your ~/.config/cron (or ~/.cron)
directory. Double-check the folder and file permissions and syntax.
$ XDG_CONFIG_HOME=$PWD mcron
```

By default, `mcron` will look for scripts in the `~/.config/cron` directory. This location can be changed by setting the standard `XDG_CONFIG_HOME` environment variable, as documented in the "Invoking mcron" ([ref](https://www.gnu.org/software/mcron/manual/mcron.html#Invoking-mcron)) section of the manual.

Per the "Invoking mcron" section of the manual, the behavior of `mcron` is to look for Vixie-style crontabs with the `.vixie` or `.vix` extension (Scheme files should end in `.guile` or `.gle`).

If `mcron` isn't finding the jobs you are looking for, considering adding the `--schedule[=N]` flag to print the next N running jobs and exit (omit N is to print the next 8 jobs).

```sh
$ XDG_CONFIG_HOME=$PWD mcron --schedule

Tue 02 Jan 2024 08:24:00 AM EST -0500
echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false

Tue 02 Jan 2024 08:25:00 AM EST -0500
echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false

Tue 02 Jan 2024 08:26:00 AM EST -0500
echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false

Tue 02 Jan 2024 08:27:00 AM EST -0500
echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false

Tue 02 Jan 2024 08:28:00 AM EST -0500
echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false

Tue 02 Jan 2024 08:29:00 AM EST -0500
echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false

Tue 02 Jan 2024 08:30:00 AM EST -0500
echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false

Tue 02 Jan 2024 08:31:00 AM EST -0500
echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false

```

There are my jobs! I'm going to try running them with the `--log` argument for debugging, which writes information to the standard output. Note that errors are always printed to standard output. See the "Invoking mcron" section of the manual for examples of how to use `--log-format` to customize the log output.



```sh
$ XDG_CONFIG_HOME=$PWD mcron --log
2024-01-02T08:25:00 echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false: running...
2024-01-02T08:25:00 echo "hello to output file" > output; echo "hi to stdout"; echo "hi to stderr" > /dev/stderr; false: /gnu/store/v9p25q9l5nnaixkhpap5rnymmwbhf9rp-bash-minimal-5.1.16/bin/bash: line 1: sendmail: command not found
```
Please excuse the `/gnu/store/v9p...9rp-bash-minimal-5.1.16/bin/bash` - this is thanks to my Guix setup (link). Pretend this says `/bin/bash`.

Anyways, `mcron`, tried to use the `sendmail` program to inform me of the status of my job. 

> e-mail? is this the 90s? where is my modern alerting? - relax, you don't have to have any kind of e-mail infrastructure in order to get notifications from `mcron`. read on!

Note that `mcron` only tries to use `sendmail` when job output is generated. `mcron` will send an e-mail when a job exits with a non zero exit code. See the [Sending output as e-mail](https://www.gnu.org/software/mcron/manual/mcron.html#Sending-output-as-e_002dmail) section of the manual for more information.

This means that a program that fails with a non zero exit code but does not generate any output will not notify the user of the job failure.

`cron/mycrontab.vixie`
```cron
* * * * * false
```

```sh
$ XDG_CONFIG_HOME=$PWD mcron --log
2024-01-02T08:35:00 false: running...
2024-01-02T08:35:00 false: completed in 0.007s
```

Let's install and configure sendmail:

```sh
$ exit
$ guix search sendmail
...
```
https://packages.guix.gnu.org/search/?query=sendmail

There are several options

```sh
$ guix shell sendmail mcron
```

How is this better than a shell script? :)










Starting with the [`package` reference](https://guix.gnu.org/manual/en/html_node/package-Reference.html), I will be defining a Guix package for my crontab.

# Docker healthcheck

# Monitoring/Observability

## Metrics

## Alerting
