#!/bin/bash
set -e

# install html-minifier
if ! command -v html-minifier; then
  if [[ $(id -u) -ne 0 ]]; then
      sudo npm install html-minifier -g;
    else
      npm install html-minifier -g;
    fi;
fi;