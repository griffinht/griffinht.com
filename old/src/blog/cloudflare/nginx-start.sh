#!/bin/sh

nginx -e /dev/stderr -p "$PWD" "$@"
