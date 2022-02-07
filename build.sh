#!/bin/sh

SOURCE=src
BUILD=build

build() {
    file="$1"
    short=$(echo "$file" | cut -c $((${#SOURCE}+1))-);
    if [ -d "$file" ]; then
        mkdir -p "$BUILD""$short"
    else
        if [ "${file: -9}" == ".mustache" ]; then
            echo mustache: "$file"
        elif [ "${file: -5}" == ".html" ]; then
            echo template: "$file"
            echo | mustache - "$file" > "$BUILD""$short"
        else
            echo file: "$file"
            cp "$file" "$BUILD""$short"
        fi
    fi
}

if [ "$1" == "--watch" ]; then
    inotifywait -r -m -e close_write --format %f "$SOURCE" | 
        while read -r file; 
            do ./build.sh "$file"; 
        done
elif [ -n "$1" ]; then
    build "$1"
else
    mkdir -p "$BUILD"
    rm -r "$BUILD"/*
    for file in $(find "$SOURCE"/*); do
        build "$file"
    done
fi
