#!/bin/sh

build() {
    file="$1"
    short=$(echo "$file" | cut -c 4-);
    if [ -d "$file" ]; then
        mkdir -p build"$short"
    else
        if [ "${file: -9}" == ".mustache" ]; then
            echo mustache: "$file"
        elif [ "${file: -5}" == ".html" ]; then
            echo template: "$file"
            echo | mustache - "$file" > build"$short"
        else
            echo file: "$file"
            cp "$file" build"$short"
        fi
    fi
}

if [ "$1" == "--watch" ]; then
    inotifywait -r -m -e close_write --format %f src | 
        while read -r file; 
            do ./build.sh "$file"; 
        done
elif [ -n "$1" ]; then
    build "$1"
else
    mkdir -p build
    rm -r build/*
    for file in $(find src/*); do
        build "$file"
    done
fi
