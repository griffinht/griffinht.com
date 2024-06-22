#!/bin/sh

set -xe

testt() {
    temp="$(mktemp -d)"
    echo "$temp"
    build.sh build test/input "$temp" > /dev/stderr
    diff test/output "$temp" > /dev/stderr
    rm -rf "$temp"
}

testt
