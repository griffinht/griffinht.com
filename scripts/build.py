#!/usr/bin/env python3

import sys
import os
import subprocess
import importlib
import argparse
import shutil
import chevron
import yaml

NAME="build"
VERSION="0.0.1"
AUTHOR="griffinht"
DEFAULT_INPUT=""
DEFAULT_OUTPUT=""

def build_directory(verbose, input_path, output_path):
  os.makedirs(output_path, exist_ok=True)

def build_template(verbose, input_path, template_path, output_path):
  print("template found" + input_path + " + "  + template_path + " -> " + output_path)
  with open(template_path, "r") as stream:
    try:
      template = yaml.safe_load(stream)
      if verbose:
        print("template .yml - parsing with mustache")
      with open(input_path, "r") as input:
        with open(output_path, "w") as output:
          output.write(chevron.render(input, template))
    except yaml.YAMLError as e:
      print(e)
      return

def build_file(verbose, copy, input_path, output_path):
  if copy:
    shutil.copyfile(input_path, output_path)
  else:
    try:
      os.readlink(output_path)
    except FileNotFoundError:
      os.symlink(os.getcwd() + os.path.sep + input_path, output_path)
    except Exception as e:
      raise e

def watch(verbose, copy, input, output):
  print("import pyinotify")
  pyinotify = importlib.import_module("pyinotify")

  def update(update):
    sys.stdout.flush()
    #buildDirectory(verbose, copy, update.path, update.name, output)

  wm = pyinotify.WatchManager()
  wm.add_watch(input, pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY, update, rec=True)
  print("looping")
  sys.stdout.flush()
  notifier = pyinotify.Notifier(wm)
  notifier.loop()

def buildDirectory(verbose, copy, input, output):
  length = len(input)
  for path, directories, files in os.walk(input):
    post_path  = path[length:]

    for directory in directories:
      input_path = path + os.path.sep + directory
      output_path = output + post_path + os.path.sep + directory

      build_directory(verbose, input_path, output_path)
    for file in files:
      input_path = path + os.path.sep + file
      output_path = output + post_path + os.path.sep + file

      extension = file.split(".")
      if extension[-1] == "yml":
        if verbose:
          print(input_path + "->" + output_path + ": ", end = "")
        for f in files:
          if f.split(".")[0] == extension[0]:
            build_template(verbose, path + os.path.sep + f, input_path, output + post_path + os.path.sep + f)
            break
      elif not extension[-1] == "mustache":
        build_file(verbose, copy, input_path, output_path)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--version", action="version", version=NAME + " v" + VERSION + " by " + AUTHOR)
  parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT)
  parser.add_argument("-w", "--watch", default=False, action='store_true')
  parser.add_argument("-q", "--quiet", default=False, action='store_true')
  parser.add_argument("-c", "--copy", default=False, action='store_true')#todo description
  parser.add_argument("REMAINDER", nargs=argparse.REMAINDER)
  parsed = parser.parse_args(sys.argv[1:])

  output = parsed.output
  isWatch = parsed.watch
  verbose = not parsed.quiet
  copy = parsed.copy
  length = len(parsed.REMAINDER)
  if length == 0:
    input = DEFAULT_INPUT
  else:
    input = parsed.REMAINDER[0]
    if length > 1:
      print("warning: ignoring extraneous arguments: " + str(parsed.REMAINDER[1:]))

  if isWatch:
    print("watching " + os.getcwd() + os.path.sep + input)
    watch(verbose, copy, input, output)
  else:
    print("building " + os.getcwd() + os.path.sep + input)
    buildDirectory(verbose, copy, input, output)

if __name__ == '__main__':
    main()