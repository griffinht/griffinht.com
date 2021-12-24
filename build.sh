#!/bin/bash
set -e

# install html-minifier
if ! command -v html-minifier > /dev/null; then
  if [[ $(id -u) -ne 0 ]]; then
      sudo npm install html-minifier -g;
    else
      npm install html-minifier -g;
    fi;
fi;

# build
rm -rf build/*
mkdir -p build
for file in ./src/*.html; do
    html-minifier \
        --collapse-whitespace \
        --remove-comments \
        --remove-optional-tags \
        --remove-redundant-attributes \
        --remove-script-type-attributes \
        --remove-tag-whitespace \
        --use-short-doctype \
        --minify-css true \
        --minify-js true \
        < "$file" > build/"$(basename $file)"
done
