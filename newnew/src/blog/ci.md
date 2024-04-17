# terminaly
server vs system

# what i learned after building my own ci pipeline from scratch

make a chart
github, gitea, all map to where?

# why does ci suck?

because pipelines aren't real and you don't need them!

# what did i build?

i created a general purpose job scheduler

## git server
- git push (only for me!)
    - can trigger jobs on push
    - todo git push deploy directly! why not!!!
        - just skip the job scheduler and go directly to the build server! duh!
        - but also it would be nice to log the deploy attempts with job scheduler somehow idk...
- git clone
- can be inspected
    - git.griffinht.com
- stats/metrics?

## job scheduler
- can be triggered
    - manually
    - on a git push
    - on a schedule
    - automatically, by other jobs as part of a pipeline
- can be monitored
    - if a job fails, i will eventually know about it!
    - if a critical job fails (db backup), i will know about it!
- can be inspected
    - check out all my jobs i have running!
    - look at the pretty colored output!
- use cases
    - schedule a 

## build server
- can be triggered
    - manually
    - by the job system
- secrets
    - can store secrets and provide them to running builds
    - probably secure?
- can save output to the artifact system
    - or any system of course! a docker registry, package publish, etc!
- monitoring/metrics? whats the right word here
    - just for metrics! no

notice how the build server does not alert me when builds fail!

## artifact system
- can be created by jobs
- can be uhhhh pruned?
- use cases
    - publish software that I build
    - automatically publish software by combining with the job system

don't write anything! instead create a graph of all this!


# why?

It's hard for me to use something without understanding it. I came in to this project thinking I knew what CI/CD was. If you asked me to set up CI for a project then I could easily have configured GitHub Actions to build and test the project, and even pushed say a Docker image to the Docker hub if I wanted to. But if you asked me which parts of Github were the job scheduler/git server/build server/artifact system then I would have a more fuzzy idea. Now I understand all the actual pieces idk

"laminar ci? but IAAC has been the de facto standard for the past 10 years! why jump back?"
"because laminar ci is not where you define your build pipelines"

# notes

look at the chart again
remember that I could of course swap each component out
consider the laminar ci author - they don't use github actions, but they do use github for source code hosting
here is an example job

i could swap my artifact system for any public s3 bucket
or use jenkins but only for artifacts i guess!

# magic tricks

this setup has enabled me to become heroku

git oush deploy here we come!
