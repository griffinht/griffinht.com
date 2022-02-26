#!/usr/bin/env python

import sys
import os
import subprocess

SOURCE="src"
BUILD="build"

"""
def build():
    file="$1"
    short=$(echo "$file" | cut -c $((${#SOURCE}+1))-);
    if [ -d "$file" ]; then
        mkdir -p "$BUILD""$short"
    else
        if [ "${file: -9}" = ".mustache" ]; then
            echo mustache: "$file"
        elif [ "${file: -4}" = ".yml" ]; then
            echo yml: "$file"
        elif [ "${file: -5}" = ".html" ]; then
            echo template: "$file"
            yml="$(echo $file | rev | cut -c 6- | rev)".yml
            if [ ! -f "$yml" ]; then
                yml='/dev/null'
            else
                echo '^ using yml ^'
            fi
            cat "$yml" | mustache - "$file" > "$BUILD""$short"
        else
            echo file: "$file"
            cp "$file" "$BUILD""$short"
        fi
    fi
"""
"""
if (sys.argv[1] == "--watch" ):
    inotifywait -r -m -e close_write --format %w%f "$SOURCE" | 
        while read -r file; 
            do ./build.sh "$file"; 
        done
elif [ -n "$1" ]; then
    build "$1"
else
    mkdir -p "$BUILD"
    rm -r ."$BUILD"/*
    for file in $(find "$SOURCE"/*); do
        build "$file"
    done
fi
"""
def build(directory):
  print(directory)

def setup():
  print(setup)
  print("installing pyinotify with pip...")
  completedProcess = subprocess.run(["dpip", "install", "pyinotify"])
  if (completedProcess.returncode != 0):
    print("error installing pyinotify" + completedProcess.returncode)

setup()

if (len(sys.argv) > 1):
  if (sys.argv[1] == "--watch"):
    directory = ""
    if (len(sys.argv) > 2):
      directory = sys.argv[2]
    print("watching " + os.getcwd() + "/" + directory)
  else:
    print("building " + sys.argv[1])