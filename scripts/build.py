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
DEFAULT_OUTPUT=""
DEFAULT_TEMPLATE_EXTENSION="template"

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


def build(verbose, copy, template_extension, input, file, output):
  def vprint(*string, **a):
    if verbose:
      print(*string, **a)
  vprint(input + os.path.sep + file + ": ", end = "")

  input_path = input + os.path.sep + file
  output_path = output + os.path.sep + file
  if os.path.isdir(input_path):
    vprint("directory - making directories")
    os.makedirs(output_path, exist_ok=True)
  else:
    extension = file.split(".")
    if extension[-1] in ["yml", "yaml", "json"]:
      vprint("template data - ignoring")
    elif template_extension in extension:
      print("template - parsing with mustache")
    else:
      vprint("file - ", end = "")
      if copy:
        vprint("copying")
      else:
        vprint("linking")


def watch(verbose, copy, template_extension, input, output):
  print("import pyinotify")
  pyinotify = importlib.import_module("pyinotify")

  def update(update):
    sys.stdout.flush()
    build(verbose, copy, template_extension, update.path, update.name, output)

  wm = pyinotify.WatchManager()
  wm.add_watch(input, pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY, update, rec=True)
  print("looping")
  sys.stdout.flush()
  notifier = pyinotify.Notifier(wm)
  notifier.loop()

def buildDirectory(verbose, copy, template_extension, input, output):
  for path, directories, files in os.walk(input):
    for directory in directories:
      build(verbose, copy, template_extension, path, directory, output)
    for file in files:
      build(verbose, copy, template_extension, input, file, output)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--version", action="version", version=NAME + " v" + VERSION + " by " + AUTHOR)
  parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT)
  parser.add_argument("-w", "--watch", default=False, action='store_true')
  parser.add_argument("-q", "--quiet", default=False, action='store_true')
  parser.add_argument("-c", "--copy", default=False, action='store_true')#todo description
  parser.add_argument("-t", "--template_extension", default=DEFAULT_TEMPLATE_EXTENSION)
  parser.add_argument("REMAINDER", nargs=argparse.REMAINDER)
  parsed = parser.parse_args(sys.argv[1:])

  output = parsed.output
  isWatch = parsed.watch
  verbose = not parsed.quiet
  copy = parsed.copy
  template_extension = parsed.template_extension
  length = len(parsed.REMAINDER)
  if length == 0:
    input = DEFAULT_INPUT
  else:
    input = parsed.REMAINDER[0]
    if length > 1:
      print("warning: ignoring extraneous arguments: " + str(parsed.REMAINDER[1:]))

  if isWatch:
    print("watching " + os.getcwd() + os.path.sep + input)
    watch(verbose, copy, template_extension, input, output)
  else:
    print("building " + os.getcwd() + os.path.sep + input)
    buildDirectory(verbose, copy, template_extension, input, output)

if __name__ == '__main__':
    main()