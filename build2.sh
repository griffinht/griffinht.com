#!/usr/bin/env bash

set -e

markdown_to_html() {
    pandoc -t html
}

markdown_to_page() {
    jq -n \
        --arg file "$(markdown_to_html)" \
    '{
        "file": $file
    }' | mustache "src/$templates_dir/template.html"
}

copy() {
    cp "$1" "$2"
}


static_dir=static
templates_dir=templates

build() {
    file="${1?error: please specify a relative file path to build}"
    shift
    input_dir="${1?error: please specify an input directory}"
    output_dir="${2?error: please specify an output directory}"

    if [[ "$file" == *"$static_dir" ]]; then
        echo "$file ($static_dir)"
        if [ ! -L "$output_dir/$file" ]; then
            ln -s "$(realpath "$input_dir/$file")" "$output_dir/$file"
        fi
        return 0
    fi
    if [[ "$file" == *"$static_dir"* ]]; then
        return 0
    fi

    echo "building file $file..."
    if [ -f "$input_dir/$file" ]; then
        if [ "$WATCH" == true ] && [[ "$file" == *$templates_dir/* ]]; then
            echo template change, rebuilding...
            # yes i hate this lol
            for subfile in "$input_dir/$(dirname "$file")/../"*.md; do
                build "$(dirname "$(dirname "$file")")/$(basename "$subfile")" "$@"
            done
            return 0
        fi
        if [[ "$file" == *.md ]]; then
            output_file="${file%.md}.html"
            echo "$file -> $output_file (template)"
            markdown_to_page < "$input_dir/$file" > "$output_dir/$output_file"
            return 0
        fi
    elif [ -d "$input_dir/$file" ]; then
        echo "$file (mkdir)"
        set -x
        mkdir -p "$output_dir/$file"
        set +x
        return 0
    else
        echo ERROR ERROR "$input_dir $file"
        return 1
    fi
}

build "$@"
