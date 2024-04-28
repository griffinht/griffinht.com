#!/bin/sh

find / -type f -name template.html | head -n 1
while [ "$PWD" != '/' ]; do
    file="$(find "$PWD" -maxdepth 1 -name template.html -print -quit)
    if [ -n 
pandoc asianeggandrice.md --standalone --template template.html -o asianeggandrice.html
