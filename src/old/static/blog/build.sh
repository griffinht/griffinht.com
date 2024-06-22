#!/bin/sh

input=web.md
output=file.html

echo hi
pandoc "$input" -o "$output" \
    --standalone \
    --template template.html \
    --lua-filter=tools/anchor-links.lua
