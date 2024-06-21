#!/bin/sh

file_path=asianeggandrice.html

while inotifywait -r -e modify '.'; do
    ./build.sh
done
