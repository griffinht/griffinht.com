#!/bin/bash
set -e

# remove when script terminates via ctrl+c
# shellcheck disable=SC2064
trap "docker rm --force '$(docker run --rm -v "$(pwd)"/build:/usr/share/nginx/html:ro --publish 8080:80 --detach nginx)'" INT

# install inotify-tools
if ! command -v inotifywait > /dev/null; then
  if [[ $(id -u) -ne 0 ]]; then
    sudo apt install inotify-tools;
  else
    apt install inotify-tools;
  fi
fi

# build when changes are detected in src dir
while inotifywait -e close_write ./src; sleep 0.1; do make build; done
