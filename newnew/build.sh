#!/bin/sh

# chatgpt bs i wish i could find a build tool that does this
# todo build a tool which does this

source_dir="src/"
build_dir="build/"

# Define your build tool command (replace this with your actual command)
# Assume it takes an input file and an output directory as arguments
run_build_tool() {
    local input_file="$1"
    local output_dir="$2"
    local base_name=$(basename -- "$input_file")

    # Run your build tool here
    cp "$input_file" "$output_dir/$base_name"
    
    echo "Processed $input_file and placed the result in $output_dir/$base_name"
}

# Create the build directory if it doesn't exist
mkdir -p "$build_dir"

# Find all files in the source directory
find "$source_dir" -type f | while IFS= read -r file; do
    # Calculate the relative path from file to build_dir
    relative_path="${file#$source_dir}"
    
    # Calculate the destination directory path
    destination_dir="$build_dir$(dirname "$relative_path")"
    
    # Ensure the destination directory exists
    mkdir -p "$destination_dir"
    
    # Call your build tool for each file
    run_build_tool "$file" "$destination_dir"
done







# Define your command to generate 'index.html' for directories
generate_index_html() {
    local target_dir="$1"
    
    # Put your logic to generate an index.html here
    echo "Directory index for $(basename "$target_dir")" > "$target_dir/index.html"

    echo "Generated index.html in $target_dir"
}

# Generate an 'index.html' in every directory in the build output
# Including the top-level directory
generate_index_html "$build_dir"

find "$source_dir" -mindepth 1 -type d | while IFS= read -r dir; do
    # Calculate the relative directory path from the source
    relative_dir="${dir#$source_dir}"
    
    # Calculate the destination directory path
    destination_dir="$build_dir$relative_dir"
    
    # Ensure the destination directory exists
    mkdir -p "$destination_dir"
    
    # Generate an index.html file in the directory
    generate_index_html "$destination_dir"
done
