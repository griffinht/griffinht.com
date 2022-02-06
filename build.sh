#!/bin/sh

rm -r build/*
for file in $(find src/*); do
    short=$(echo "$file" | cut -c 4-);
    if [ -d "$file" ]; then
        mkdir -p build"$short"
    else
        if [ "${file: -9}" == ".mustache" ]; then
            echo template: "$file"
            echo | mustache - "$file" > build/"$(echo $short | head -c -10)"
        else
            echo file: "$file"
            cp "$file" build"$short"
        fi
    fi
done
