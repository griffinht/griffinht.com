#!/usr/bin/env bash

set -e
set -o pipefail

static_dir=static
templates_dir=templates

markdown_to_html() {
    pandoc -t html
}

html_to_page() {
    if [ "$#" -gt 0 ]; then
        data_file="${1?}"
        data="$(yq -o json "$data_file")"
    else
        data='{}'
    fi
    jq --raw-input -n \
        --argjson data "$data" \
    '{
        "file": input,
        "data": $data
    }' | mustache "src/$templates_dir/template.html"
}
#cat src/index.md | html_to_page src/data.yml

copy() {
    cp "$1" "$2"
}


build() {
    data_file="${1?error: please specify the file build, relative to the input directory (like index.md from ./src/index.md)}"
    shift
    input_dir="${1?error: please specify an input directory (like ./src)}"
    output_dir="${2?error: please specify an output directory (like ./build)}"
    special_file="data.yml"

    if [[ "$data_file" == *"$static_dir" ]]; then
        echo "$data_file ($static_dir)"
        if [ ! -L "$output_dir/$data_file" ]; then
            ln -s "$(realpath "$input_dir/$data_file")" "$output_dir/$data_file"
        fi
        return 0
    fi
    if [[ "$data_file" == *"$static_dir"* ]]; then
        return 0
    fi

    if [ "$VERBOSE" == true ]; then
        echo
        echo "building file $data_file..."
    fi

    if [ -f "$input_dir/$data_file" ]; then
        if [ "$WATCH" == true ] && [[ "$data_file" == *$templates_dir/* ]]; then
            echo template change, rebuilding...
            # yes i hate this lol
            for subfile in "$input_dir/$(dirname "$data_file")/../"*.md; do
                build "$(dirname "$(dirname "$data_file")")/$(basename "$subfile")" "$@"
            done
            return 0
        fi
        if [[ "$data_file" == *.md ]]; then
            output_file="${data_file%.md}.html"
            echo "$data_file -> $output_file (template)"
            output="$output_dir/$output_file"
            if [ "$output_dir" == /dev/stdout ] || [ "$output_dir" == - ]; then output=/dev/stdout; fi
            markdown_to_html < "$input_dir/$data_file" | html_to_page "$special_file" > "$output"
            return "$?"
        fi
    elif [ -d "$input_dir/$data_file" ]; then
        echo "$data_file (mkdir)"
        mkdir -p "$output_dir/$data_file"
        return 0
    else
        echo ERROR ERROR "$input_dir $data_file"
        return 1
    fi
}

build "$@"
