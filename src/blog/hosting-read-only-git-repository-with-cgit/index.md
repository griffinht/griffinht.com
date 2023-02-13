---
file_content: {{> ../article}}
file_extension: .html
title: Hosting a read-only Git repository with cgit
root: ../../
source: blog/hosting-read-only-git-repository-with-cgit/index.md
datetime: 2022-04-24
---

`cgit` ([source](https://git.zx2c4.com/cgit/)) is a web interface ([CGI](https://en.wikipedia.org/wiki/Common_Gateway_Interface)) for [Git](https://git-scm.com/) written in C. `cgit` is seems to be the least complicated way to host Git repositories over the web. It is an example of software that does one thing and does it well. [Other web interfaces](https://git.wiki.kernel.org/index.php/Interfaces,_frontends,_and_tools#Web_Interfaces) are either unmaintained or more complex than `cgit` (see [GitLab](https://about.gitlab.com/) or [Gitea](https://gitea.com/)). 

cgit does not attempt to implement user identies, pull requests, issue trackers, or continuous integration. As a result, it is has a small footprint and is relatively easy to deploy.

#### Deployment

`cgit` can be deployed by creating a [Docker](https://docs.docker.com/get-started/overview/) image.

`cgit` requires an HTTP server which supports CGI scripts. [nginx](https://nginx.org/en/) is an HTTP server and reverse proxy which supports [FastCGI](https://en.wikipedia.org/wiki/FastCGI) via the [nginx FastCGI module](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html).

[Alpine Linux](https://www.alpinelinux.org/) is used as a base image because it is lightweight.

`Dockerfile`
```
FROM nginx:alpine

RUN apk --no-cache add spawn-fcgi fcgiwrap cgit py3-pip \
    && pip install pygments markdown

COPY fcgi.sh /docker-entrypoint.d/fcgi.sh
COPY nginx /etc/nginx/
COPY cgitrc /etc/cgitrc
COPY cgit/ /usr/share/webapps/cgit/
```

The [official nginx Docker image](https://hub.docker.com/_/nginx/) will run any scripts in the `/docker-entrypoint.d/` directory. This is where the script to create the `FastCGI` socket can be placed. 

`/docker-entrypoint.d/fcgi.sh`
```
#!/bin/sh
spawn-fcgi -M 666 -s /var/run/fcgiwrap.socket /usr/bin/fcgiwrap
```

This script uses `spawn-fcgi` ([source](https://redmine.lighttpd.net/projects/spawn-fcgi/wiki)) ([manpage](https://linux.die.net/man/1/spawn-fcgi)) to spawn a `FastCGI` server using the `/usr/bin/fcgiwrap` binary bound to the Unix socket `unix:/var/run/fcgiwrap.sock` with file mode `666`.

`nginx` can be configured to use this socket with by specifying some parameters ([docs](https://www.nginx.com/resources/wiki/start/topics/examples/fastcgiexample/)).

`/etc/nginx/nginx.conf`
```
events {}
http {
    server {
        listen 80 default_server;
        server_name _;
        include mime.types;

        # directory with cgit assets such as cgit.png or cgit.css
        root /usr/share/webapps/cgit;
        try_files $uri @cgit;

        location @cgit {
            include fastcgi_params;
            # Unix socket which was spawned with spawn-fcgi
            fastcgi_pass unix:/var/run/fcgiwrap.socket;
            # cgit.cgi is installed by the Alpine package
            fastcgi_param SCRIPT_FILENAME /usr/share/webapps/cgit/cgit.cgi;
            
            # https://example.com/$uri?$args
            fastcgi_param PATH_INFO $uri;
            fastcgi_param QUERY_STRING $args;
        }
    }
}
```

`cgit` can be configured with a single configuration file.

`/etc/cgitrc` ([manpage](https://linux.die.net/man/5/cgitrc)) ([source](https://git.zx2c4.com/cgit/tree/cgitrc.5.txt))
```
# optional, provides formatting for source code
# requires python3-pygments
source-filter=/usr/lib/cgit/filters/syntax-highlighting.py
# optional, provides formatting for the about page
# requires python-markdown
about-filter=/usr/lib/cgit/filters/about-formatting.sh
# note that if the python dependencies for the above scripts are not installed, then the about page and source code will render blank

# what file to look for to serve the readme, which is placed in the about page for each repository
readme=:README.md
readme=:readme.md
readme=:README.html
readme=:readme.html
readme=:README.htm
readme=:readme.htm
readme=:README.txt
readme=:readme.txt
readme=:README
readme=:readme

# setting a blank value will hide the cgit version at the bottom of the page
footer=
# link for clicking on the logo
logo-link=https://example.com
root-title=My cgit instance
root-desc=This is awesome cgit instance, which contains all my Git repositories
# used as the about page for the entire instance, viewed by clicking about in the top left corner
# /usr/share/webapps/cgit/README.md
root-readme=README.md

# /usr/share/webapps/cgit/
# needs to be prefixed with the virtual-root, see below
css=/git/cgit.css
logo=/git/cgit.png

# where cgit expects HTTP requests to come from
# https://example.com/git/
virtual-root=/git/

# where cgit will look for Git repositories in the filesystem
# make sure scan-path is at the bottom
# https://lists.zx2c4.com/pipermail/cgit/2017-February/003466.html
scan-path=/git/
```

Make sure to place all assets (such as a custom `cgit.png`) in the `/usr/share/webapps/cgit/`.

#### Create new repository
`git init --bare $NAME`

It is important to create a bare Git repository, or else it may not be possible to `git push` ([source](https://stackoverflow.com/questions/5540883/whats-the-practical-difference-between-a-bare-and-non-bare-repository)).

#### Import existing repositories from GitHub
To import existing repositories [GitHub](https://github.com/), use this shell command. It requires `curl jq git`. Replace `$USER` with your GitHub user.


`curl https://api.github.com/users/"$USER"/repos | jq -r '.[].html_url' | while read -r url; do git clone --bare "$url"; done`

#### Read More
[https://wiki.archlinux.org/title/cgit](https://wiki.archlinux.org/title/cgit)

#### Notable public cgit instances
[Kernel.org](https://git.kernel.org/pub/scm/)
[FreeBSD](https://cgit.freebsd.org/)
[Texas Instruments](https://git.ti.com/cgit)
[GNU Savannah](https://git.savannah.gnu.org/cgit/)

