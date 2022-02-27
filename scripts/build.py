#!/usr/bin/env python3

import sys
import os
import subprocess
import importlib
import argparse
import shutil

NAME="build"
VERSION="0.0.1"
AUTHOR="griffinht"
DEFAULT_INPUT=""
DEFAULT_OUTPUT=""
DEFAULT_TEMPLATE_EXTENSION="mustache"

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

def build_directory(verbose, input_path, output_path):
  if verbose:
    print("directory - making directories")
  os.makedirs(output_path, exist_ok=True)

def build_template(verbose, template_extension, input_path, output_path):
  if verbose:
    print("template - parsing with mustache")

def build_file(verbose, copy, input_path, output_path):
  if verbose:
    print("file - ", end = "")
  if copy:
    if verbose:
      print("copying")
    shutil.copyfile(input_path, output_path)
  else:
    if verbose:
      print("linking")
    try:
      os.readlink(output_path)
    except FileNotFoundError:
      os.symlink(os.getcwd() + os.path.sep + input_path, output_path)
    except Exception as e:
      raise e

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
  length = len(input)
  for path, directories, files in os.walk(input):
    post_path  = path[length:]



    for directory in directories:
      input_path = path + os.path.sep + directory
      output_path = output + post_path + os.path.sep + directory

      if verbose:
        print(input_path + "->" + output_path + ": ", end = "")

      build_directory(verbose, input_path, output_path)
    for file in files:
      input_path = path + os.path.sep + file
      output_path = output + post_path + os.path.sep + file

      if verbose:
        print(input_path + "->" + output_path + ": ", end = "")

      extension = file.split(".")
      if extension[-1] in ["yml", "yaml", "json"]:
        if verbose:
          print("template data - ignoring")
      elif template_extension in extension:
        if verbose:
          print("template - parsing with mustache")
      else:
        build_file(verbose, copy, input_path, output_path)

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