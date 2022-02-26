#!/usr/bin/env python3

import sys
import os
import subprocess
import importlib
import argparse

NAME="build"
VERSION="0.0.1"
AUTHOR="griffinht"
DEFAULT_INPUT=""
DEFAULT_OUTPUT="build"

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


def build(input, file, output):
  print(file + ": ", end = "")
  if (os.path.isdir(input + os.path.sep + file)):
    print("making directories")
    os.makedirs(input + os.path.sep + file, exist_ok=True)
  else:
    print("building file")

def watch(directory):
  print("import pyinotify")
  pyinotify = importlib.import_module("pyinotify")

  def update(update):
    sys.stdout.flush()
    build(update.path + update.name)

  wm = pyinotify.WatchManager()
  wm.add_watch(directory, pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY, update, rec=True)
  print("looping")
  sys.stdout.flush()
  notifier = pyinotify.Notifier(wm)
  notifier.loop()

def buildDirectory(input, output):
  for path, directories, files in os.walk(input):
    for directory in directories:
      build(path, directory, output)
    for file in files:
      build(input, file, output)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--version", action="version", version=NAME + " v" + VERSION + " by " + AUTHOR)
  parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT)
  parser.add_argument("-w", "--watch", default=False)
  parser.add_argument("REMAINDER", nargs=argparse.REMAINDER)
  parsed = parser.parse_args(sys.argv[1:])

  print(str(parsed))
  #if parsed.version
  output = parsed.output
  watch = parsed.watch
  length = len(parsed.REMAINDER)
  if length == 0:
    input = DEFAULT_INPUT
  else:
    input = parsed.REMAINDER[0]
    if length > 1:
      print("warning: ignoring extraneous arguments: " + str(parsed.REMAINDER[1:]))
  sys.exit(0)

  print(input + ", " + output + ", " + str(watch))

  if (len(sys.argv) > 1):
    if (sys.argv[1] == "--watch"):
      directory = ""
      if (len(sys.argv) > 2):
        directory = sys.argv[2]
      print("watching " + os.getcwd() + os.path.sep + directory)
      watch(directory)
    else:
      print("building " + sys.argv[1])
      #buildDirectory(sys.argv[1])
  else:
    print("building " + os.getcwd())
    #buildDirectory("")

if __name__ == '__main__':
    main()