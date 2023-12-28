#!/usr/bin/env bash

NAME="$(docker create nginx:alpine)"
docker export "$NAME" | tar --list | grep etc/nginx
docker rm "$NAME"
