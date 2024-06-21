All of the

I wanted to run some monitoring jobs which weren't managed by prometheus.

# Thin vs Heavy CI

## Thin

the ci server is a job dispatcher which contains only the tools needed to dispatch and monitor the jobs

## Heavy

the ci server is a special pet which gets loaded up with various packages and files over time which have everything I need to run all of my jobs

# asd

It's okay to have pets, even very heavy pets like a long running toy VM.
However, the CI server and the pets can be separated

## what is ci?

merely a way to publicly expose build logs?

### docker

```

```

- security! why not just use a remote docker - no need for the ability to compromise the entire ci server with one bad job

### ssh

```
ssh
```

- requires ci server have ssh keys
- could lead to a more heavy ci server
    - i have ssh, so i could write all my ci jobs on the ci server instead of other places and having the ci server only dispatch jobs

### webhook

```
curl
```

- super lightweight, basically the same as ssh idk
- enforces a lightweight ci

### guix

give each job access to guix
but still why not just ssh to a guix machine and give them that?




# features

## define jobs in vcs

running a job should give a link to where the job is defined

## run on commit/git hook

## run on timer/cron

we need a scheduler

### a scheduler

- view all jobs
- view job runs
- job definitions
    - can be live reloaded
- monitoring
    - alert when job fails
- no database
    - only state would maybe be time since last run which will be scraped by prom!
- not distributed
https://www.reddit.com/r/linuxadmin/comments/gh591f/comment/fq7rz44/?context=3

https://github.com/healthchecks/healthchecks
todo monitor cron and make sure the jobs don't fail! but oh thats the job of the ci but oh what if the ci is down idk!

## build info

### result

exit code

### logs

https://laminar.ohwg.net/docs.html#Colours-in-log-output
streaming

### info

i should be able to point to a url or write information to the web ui about the job - not just by echoing the output, but say adding a link or a picture

laminar doesn't support this womp womp

laminar uses ansi_up, which supports printing colors and OSC urls to the terminal. This means 

```bash
echo -e "Click here for more information: \e]8;;https://www.example.com\ahttps://www.example.com\e]8;;\a"
```

to make a clickable link

https://github.com/drudru/ansi_up

### stats

cpu usage and other metrics?
https://github.com/jhuckaby/Cronicle

## alert on failure

`laminar/cfg/after`

```sh
#!/bin/sh

# public url to ci, so we can click links
url=http://localhost:8080
# alertmanager url for submitting alerts
alertmanager_url=alertmanager:9093

if [ "$RESULT" != success ]; then
    # todo add labels and stuff
    echo "$JOB failed, see $url/jobs/$JOB/$RUN" | curl \
        -X POST \
        -d @- \
        "${alertmanager_url}/post"
fi
```

## build artifacts

laminar has built in support for this, but i think i'd rather use an s3 bucket
then i can just link to the location in the bucket in laminar  



## badges

https://laminar.ohwg.net/docs.html#Badges

i can add my own badges with archives todo!
