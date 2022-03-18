#!/bin/sh

# dependencies for build.py
# pandoc
apk add curl
curl -L https://github.com/jgm/pandoc/releases/download/2.17.1.1/pandoc-2.17.1.1-linux-amd64.tar.gz | tar --strip-components=1 -xzC /usr/local

pip install asyncinotify chevron pyyaml 

