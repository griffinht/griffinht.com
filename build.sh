#!/bin/sh

set -e

build() {
    src="${1?error: please specify a source directory}"
    shift

    echo "building directory $src..."
    # find strip the $src from the output
    find "$src" -printf '%P\n' \
        | while read -r file; do
        ./build2.sh "$file" "$src" "$@";
    done
}

watch() {
    src="${1?error: please specify a source directory}"
    shift

    echo "watching directory $src..."
    find "$src" | WATCH=true entr ./build2.sh /_ "$src" "$@"
}

action="$1"
shift

"$action" "$@"



#base_dir="$1"
#changed="$2"
#rm -r build
#mkdir -p build
#build "${changed#"$base_dir/"}"
