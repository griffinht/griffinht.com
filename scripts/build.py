#!/usr/bin/env python3

import sys
import os
import subprocess
import importlib
import argparse
import shutil
import chevron
import yaml
import time

NAME="build"
VERSION="0.0.1"
AUTHOR="griffinht"
DEFAULT_INPUT=""
DEFAULT_OUTPUT=""

def build_template(input, file, template, output):
  print(input, file, template, output)
  with open(input + os.path.sep + template, "r") as template_stream:
    try:
      template_yaml = yaml.safe_load(template_stream)
      with open(input + os.path.sep + file, "r") as input_stream:
        with open(output + os.path.sep + file, "w") as output_stream:
          output_stream.write(chevron.render(input_stream, template_yaml, partials_path=input))
    except Exception as e:
      print(e)
      return

def build_file(copy, input_path, output_path):
  if copy:
    try:
      shutil.copyfile(input_path, output_path)
    except FileNotFoundError as e:
      print(e)
      return
    except Exception as e:
      raise e
  else:
    try:
      os.readlink(output_path)
    except FileNotFoundError:
      os.symlink(os.getcwd() + os.path.sep + input_path, output_path)
    except Exception as e:
      raise e

def build(copy, input, file, output, files=None):
  if os.path.isdir(input + os.path.sep + file):
    os.makedirs(output + os.path.sep + file, exist_ok=True)
  else:
    file_extension = file.split(".")
    if not file_extension[-1] == "mustache":
      if files == None:
        files = os.listdir(input)
      for f in files:
        f_extension = f.split(".")
        if f_extension[0] == file_extension[0]:
          if file_extension[-1] == "yml":
            _file = f
            _template = file
          elif f_extension[-1] == "yml":
            _file = file
            _template = f
          else:
            continue
          sys.stdout.flush()
          build_template(input, _file, _template, output)
          return
      build_file(copy, input + os.path.sep + file, output + os.path.sep + file)

def build_directory(copy, input, output):
  input_length = len(input)
  for path, directories, files in os.walk(input):
    _output = output + path[input_length:]

    for directory in directories:
      build(copy, path, directory, _output)
    for file in files:
      build(copy, path, file, _output, files=files)

def watch(copy, input, output):
  print("import asyncinotify")
  asyncinotify = importlib.import_module("asyncinotify")
  asyncio = importlib.import_module("asyncio")
  async def _loop():
    print("adding recursive watches...")
    with asyncinotify.Inotify() as inotify:
      mask = asyncinotify.Mask.CLOSE_WRITE | asyncinotify.Mask.CREATE | asyncinotify.Mask.DELETE | asyncinotify.Mask.MODIFY | asyncinotify.Mask.MOVE
      inotify.add_watch(input, mask)
      for path, directories, files in os.walk(input):
        for directory in directories:
          inotify.add_watch(path + os.path.sep + directory, mask)
      print("watches added")
      sys.stdout.flush()
      async for event in inotify:
        file = str(event.name)
        _input = str(event.path)[:-len(file) - 1]
        _output = output + _input[len(input):]
        print(event.mask, _input, file, _output, end=" ")
        sys.stdout.flush()

        if (event.mask & asyncinotify.Mask.CLOSE_WRITE) > 0:
          print("CLOSE_WRITE")
          build(copy, _input, file, _output)
        elif (event.mask & asyncinotify.Mask.CREATE) > 0:
          print("CREATE")
          build(copy, _input, file, _output)
        elif (event.mask & asyncinotify.Mask.DELETE) > 0:
          print("DELETE")
          try:
            os.remove(_output + os.path.sep + file)
          except FileNotFoundError as e:
            print(e)
            continue
          except IsADirectoryError as e:
            print(e)
            continue
        elif (event.mask & asyncinotify.Mask.MODIFY) > 0:
          print("MODIFY")
          build(copy, _input, file, _output)
        elif (event.mask & asyncinotify.Mask.MOVED_FROM) > 0:
          print("MOVED_FROM")
          try:
            os.remove(_output + os.path.sep + file)
          except FileNotFoundError as e:
            print(e)
            continue
          except IsADirectoryError as e:
            print(e)
            continue
        elif (event.mask & asyncinotify.Mask.MOVED_TO) > 0:
          print("MOVED_TO")
          build(copy, _input, file, _output)
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