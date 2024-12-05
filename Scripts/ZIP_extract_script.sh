#!/bin/bash

# Input and output folder names
input_folder="Phoenix_sample"
output_folder="Phoenix_sample_output"

# Create the output folder if it doesn't already exist
mkdir -p "$output_folder"

# Check if the input folder exists, exit with an error if it doesn't
if [ ! -d "$input_folder" ]; then
    echo "Input folder '$input_folder' does not exist!"
    exit 1
fi

# Iterate over all files in the input folder
for file in "$input_folder"/*; do

    # Check if the file is a ZIP archive by inspecting its file type
    if file "$file" | grep -q "Zip archive data"; then
        # If it is a ZIP file, extract it using 7z with a password 'infected'
        echo "Extracting ZIP file: $file"
        7z x -p'infected' "$file" -o"$output_folder" 
    else
        # If it's not a ZIP file, skip and notify
        echo "Skipping non-ZIP file: $file"
    fi
done


