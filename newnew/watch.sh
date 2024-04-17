#!/bin/sh

watch_directory=src
build=build

inotifywait -m -r -e modify,create,delete $watch_directory |
while read path action file; do
    path_ = "${file#$watch_directory
    if "$action" == DELETE; then
        rm "build/$path"
    fi
    echo "$file" $action $path
done
