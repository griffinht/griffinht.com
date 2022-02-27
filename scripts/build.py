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

def build_template(input_path, template_path, output_path):
  print(input_path + " + "  + template_path + " -> " + output_path)
  with open(template_path, "r") as stream:
    try:
      template = yaml.safe_load(stream)
      with open(input_path, "r") as input:
        with open(output_path, "w") as output:
          output.write(chevron.render(input, template))
    except yaml.YAMLError as e:
      print(e)
      return

def build_file(copy, input_path, output_path):
  if copy:
    shutil.copyfile(input_path, output_path)
  else:
    try:
      os.readlink(output_path)
    except FileNotFoundError:
      os.symlink(os.getcwd() + os.path.sep + input_path, output_path)
    except Exception as e:
      raise e

def watch(copy, input, output):
  print("import asyncinotify")
  asyncinotify = importlib.import_module("asyncinotify")
  asyncio = importlib.import_module("asyncio")
  async def _loop():

    with asyncinotify.Inotify() as inotify:
      inotify.add_watch(input, asyncinotify.Mask.CLOSE_WRITE | asyncinotify.Mask.CREATE | asyncinotify.Mask.DELETE | asyncinotify.Mask.MODIFY | asyncinotify.Mask.MOVE)

      async for events in inotify:
        print(events)
        if (events.mask & asyncinotify.Mask.CLOSE_WRITE) > 0:
          print("CLOSE_WRITE")
        elif (events.mask & asyncinotify.Mask.CREATE) > 0:
          print("CREATE")
        elif (events.mask & asyncinotify.Mask.DELETE) > 0:
          print("DELETE")
        elif (events.mask & asyncinotify.Mask.MODIFY) > 0:
          print("MODIFY")
        elif (events.mask & asyncinotify.Mask.MOVE) > 0:
          print("MOVE")

        sys.stdout.flush()

  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  try:
      loop.run_until_complete(_loop())
  except KeyboardInterrupt:
      print('shutting down')
  finally:
      loop.run_until_complete(loop.shutdown_asyncgens())
      loop.close()

def build():

def build_directory(copy, input, output):
  length = len(input)
  for path, directories, files in os.walk(input):
    post_path  = path[length:]

    for directory in directories:
      output_path = output + post_path + os.path.sep + directory

      os.makedirs(output_path, exist_ok=True)
    for file in files:
      input_path = path + os.path.sep + file
      output_path = output + post_path + os.path.sep + file

      extension = file.split(".")
      if extension[-1] == "yml":
        for f in files:
          if f.split(".")[0] == extension[0]:
            build_template(path + os.path.sep + f, input_path, output + post_path + os.path.sep + f)
            break
      elif not extension[-1] == "mustache":
        build_file(copy, input_path, output_path)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--version", action="version", version=NAME + " v" + VERSION + " by " + AUTHOR)
  parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT)
  parser.add_argument("-w", "--watch", default=False, action='store_true')
  parser.add_argument("-c", "--copy", default=False, action='store_true')#todo description
  parser.add_argument("REMAINDER", nargs=argparse.REMAINDER)
  parsed = parser.parse_args(sys.argv[1:])

  output = parsed.output
  isWatch = parsed.watch
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
    watch(copy, input, output)
  else:
    print("building " + os.getcwd() + os.path.sep + input)
    build_directory(copy, input, output)

if __name__ == '__main__':
    main()