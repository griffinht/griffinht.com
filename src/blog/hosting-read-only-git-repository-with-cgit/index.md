cgit ([source](https://git.zx2c4.com/cgit/)) is a web interface for Git written in C using the [CGI](https://en.wikipedia.org/wiki/Common_Gateway_Interface) written in C. cgit is seems to be the least complicated way to host Git repositories over the web. It fulfills the philosophy that software should do one thing and do it well. [Other web interfaces](https://git.wiki.kernel.org/index.php/Interfaces,_frontends,_and_tools#Web_Interfaces) are either unmaintained or more complex than cgit (see [GitLab](https://about.gitlab.com/) or [Gitea](https://gitea.com/)). 

cgit does not attempt to implement user identies, pull requests, issue trackers, or continous integration. As a result, it is has a small footprint and is relatively easy to deploy.

#### Dockerfile

Because cgit is a , it needs to have an HTTP server which supports CGI scripts. [nginx](https://nginx.org/en/) is an HTTP server and reverse proxy which can use FastCGI todo to server CGI scripts.

This `Dockerfile` uses [Alpine Linux](https://www.alpinelinux.org/) as a base image.

```
FROM nginx:alpine

RUN apk --no-cache add spawn-fcgi fcgiwrap cgit py3-pip \
    && pip install pygments markdown

COPY fcgi.sh /docker-entrypoint.d/fcgi.sh
COPY nginx /etc/nginx/
COPY cgitrc /etc/cgitrc
COPY cgit/ /usr/share/webapps/cgit/
```

#### Read More
[https://wiki.archlinux.org/title/cgit](https://wiki.archlinux.org/title/cgit)

#### Notable public cgit instances
[Kernel.org](https://git.kernel.org/pub/scm/)
[FreeBSD](https://cgit.freebsd.org/)
[Texas Instruments](https://git.ti.com/cgit)
[GNU Savannah](https://git.savannah.gnu.org/cgit/)





read only access via my website and `git clone`
read+write via private file server

clone all of your github directories to working directory

replace $USER with your github user
requires `curl jq git`
`curl https://api.github.com/users/"$USER"/repos | jq -r '.[].html_url' | while read -r url; do git clone --bare "$url"; done`

create new repository
`git init --bare $NAME`
