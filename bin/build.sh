#!/bin/sh

set -e

build() {
    src="${1?error: please specify a source directory}"
    shift

    echo "building directory $src..."
    # find strip the $src from the output
    find "$src" -printf '%P\n' \
        | while read -r file; do
        build2.sh "$file" "$src" "$@";
    done
}

# entr outputs full path, we need to strip it to just get the file
watch_() {
    path="${1?}"
    shift
    src="${1?}"

    src_path="$(realpath "$src")"
    path="${path#"$src_path"}" 
    build2.sh "$path" "$@"
}

watch() {
    src="${1?error: please specify a source directory}"

    echo "watching directory $src..."
    find "$src" | WATCH=true VERBOSE=true entr "$0" watch_ /_ "$@"
}

action="$1"
shift

"$action" "$@"



#base_dir="$1"
#changed="$2"
#rm -r build
#mkdir -p build
#build "${changed#"$base_dir/"}"
