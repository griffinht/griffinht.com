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
import markdown

NAME="build"
VERSION="0.0.1"
AUTHOR="griffinht"
DEFAULT_INPUT=""
DEFAULT_OUTPUT=""

def strip_extension(file):
    index = file.rfind(".")
    if (index == -1):
        # file -> file
        return file
    else:
        # file.extension -> file
        # file.file.extension -> file.file
        return file[0:index]
    

def build(input_dir, name, output_dir, files=None):
    # can be cached by previous function caller
    if files == None:
        files = os.listdir(input_dir)

    file = None
    template_file = None
    content_file = None
    mustache_file = False
    
    for f in files:
        if not f.startswith(name):
            continue

        extension = f.split(".")[-1]
        if extension == "yml" or extension == "yaml":
            template_file = f
        elif extension == "md":
            content_file = f
        elif extension == "mustache":
            mustache_file = True
        elif file == None:
            file = f

    # file either has no extension or is a mustache file
    # file or file.mustache
    if file == None:
        if mustache_file:
            # file.mustache
            # mustache files are ignored
            print(input_dir + os.path.sep + name + ".mustache (ignored)")
            return
        else:
            # file
            # files with no extension should be treated normally
            file = name
    
    # no yaml or content
    if template_file == None:
        #print(input_dir + os.path.sep + file + " (file)")
        shutil.copyfile(input_dir + os.path.sep + file, output_dir + os.path.sep + file)
        return

    # yaml but no content
    if content_file == None:
        print(input_dir + os.path.sep + file + " (template)")
        with open(input_dir + os.path.sep + template_file, "r") as template_stream:
            try:
                template = yaml.safe_load(template_stream)
            except Exception as e:
                print(e)
                return
            with open(input_dir + os.path.sep + file, "r") as input_stream:
                    with open(output_dir + os.path.sep + file, "w") as output_stream:
                        output_stream.write(chevron.render(input_stream, template, partials_path=input_dir))
    else:
        # yaml with content
        print(input_dir + ": " + file + " (template + content)")
        with open(input_dir + os.path.sep + template_file, "r") as template_stream:
            try:
                template = yaml.safe_load(template_stream)
            except Exception as e:
                print(e)
                return

            with open(input_dir + os.path.sep + content_file, "r") as content_stream:
                content = content_stream.read()
            template["content"] = markdown.markdown(content, extensions=['extra'])

            with open(input_dir + os.path.sep + file, "r") as input_stream:
                    with open(output_dir + os.path.sep + file, "w") as output_stream:
                        output_stream.write(chevron.render(input_stream, template, partials_path=input_dir))

def build_directory(input_dir, output_dir):
    input_dir_length = len(input_dir)
    for input_path, directories, files in os.walk(input_dir):
        output_path = output_dir + input_path[input_dir_length:]

        for directory in directories:
            os.makedirs(output_path + os.path.sep + directory, exist_ok=True)
#            build(input_path, directory, output_path)
        
        files_set = set()

        for file in files:
            files_set.add(strip_extension(file))

        for file in files_set:
            build(input_path, file, output_path, files=files)

def watch(input, output):
    print("import asyncinotify")
    asyncinotify = importlib.import_module("asyncinotify")
    asyncio = importlib.import_module("asyncio")
    async def _loop():
        print("adding watches recursively...")
        with asyncinotify.Inotify() as inotify:
            mask = asyncinotify.Mask.CLOSE_WRITE | asyncinotify.Mask.CREATE | asyncinotify.Mask.DELETE | asyncinotify.Mask.MODIFY | asyncinotify.Mask.MOVE
            inotify.add_watch(input, mask)
            # what is this loop here for???
            for path, directories, files in os.walk(input):
                for directory in directories:
                    inotify.add_watch(path + os.path.sep + directory, mask)
                print("watches added")
                sys.stdout.flush()

                async for event in inotify:
                    file = str(event.name)
                    _input = str(event.path)[:-len(file) - 1]
                    output_dir = output + _input[len(input):]
                    print(event.mask, _input, file, output_dir, end=" ")
                    sys.stdout.flush()

                    if (event.mask & asyncinotify.Mask.CLOSE_WRITE) > 0:
                        print("CLOSE_WRITE")
                        build(_input, file, output_dir)
                    elif (event.mask & asyncinotify.Mask.CREATE) > 0:
                        print("CREATE")
                        build(_input, file, output_dir)
                    elif (event.mask & asyncinotify.Mask.DELETE) > 0:
                        print("DELETE")
                        try:
                            os.remove(output_dir + os.path.sep + file)
                        except FileNotFoundError as e:
                            print(e)
                            continue
                        except IsADirectoryError as e:
                            print(e)
                            continue
                    elif (event.mask & asyncinotify.Mask.MODIFY) > 0:
                        print("MODIFY")
                        build(_input, file, output_dir)
                    elif (event.mask & asyncinotify.Mask.MOVED_FROM) > 0:
                        print("MOVED_FROM")
                        try:
                            os.remove(output_dir + os.path.sep + file)
                        except FileNotFoundError as e:
                            print(e)
                            continue
                        except IsADirectoryError as e:
                            print(e)
                            continue
                    elif (event.mask & asyncinotify.Mask.MOVED_TO) > 0:
                        print("MOVED_TO")
                        build(_input, file, output_dir)
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
    parser.add_argument("REMAINDER", nargs=argparse.REMAINDER)
    parsed = parser.parse_args(sys.argv[1:])

    output = parsed.output
    isWatch = parsed.watch
    length = len(parsed.REMAINDER)
    if length == 0:
        input = DEFAULT_INPUT
    else:
        input = parsed.REMAINDER[0]
    if length > 1:
        print("warning: ignoring extraneous arguments: " + str(parsed.REMAINDER[1:]))

    if isWatch:
        print("watching " + os.getcwd() + os.path.sep + input)
        watch(input, output)
    else:
        print("building " + os.getcwd() + os.path.sep + input)
        build_directory(input, output)

if __name__ == '__main__':
    main()
