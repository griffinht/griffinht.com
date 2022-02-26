#!/usr/bin/env python

import sys
import os
import subprocess
import importlib

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


def build(file):
  print("build: " + file)
  if (file.endswith(os.path.sep)):
    os.makedirs(file, exist_ok=True)
  else:
    print(file)

def watch(directory):
  print("import pyinotify")
  pyinotify = importlib.import_module("pyinotify")

  def update(update):
    print("update")
    print(update.mask)
    sys.stdout.flush()
    build(update.path + update.name)

  wm = pyinotify.WatchManager()
  wm.add_watch(directory, pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY, update)
  print("looping")
  sys.stdout.flush()
  notifier = pyinotify.Notifier(wm)
  notifier.loop()

def buildDirectory(directory):
  for path, directories, files in os.walk(directory):
    for directory in directories:
      build(path + os.path.sep + directory)
    for file in files:
      build(path + os.path.sep + file)

def init():
  if (len(sys.argv) > 1):
    if (sys.argv[1] == "--watch"):
      directory = ""
      if (len(sys.argv) > 2):
        directory = sys.argv[2]
      print("watching " + os.getcwd() + os.path.sep + directory)
      watch(directory)
    else:
      print("building " + sys.argv[1])
      buildDirectory(sys.argv[1])
  else:
    print("building " + os.getcwd())
    buildDirectory("")

init()