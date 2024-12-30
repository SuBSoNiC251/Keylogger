#!/bin/bash

#THIS SCRIPT FILE IS FOR THE USER TO OBTAIN THE CODE FOR THE ENTIRE PROJECT AT ONCE

# Define the directory to start
start_directory="PUT YOUR DIRECTORY PATH OR ROOT OF THE PROJECT HERE IN WSL"

# Define the output file
output_file="PUT YOUR DIRECTORY PATH OR ROOT OF THE PROJECT HERE IN WSL/full_code.txt"

# Clear the output file if it exists
if [ -f "$output_file" ]; then
    rm "$output_file"
fi

# Function to process files in a directory
process_directory() {
    local directory=$1
    # Iterate over each item in the directory
    for item in "$directory"/*; do
        # Check if it's a directory
        if [ -d "$item" ]; then
            # Skip the "logs", "__pycache__", and "uploads" directories
            if [[ "$item" == *logs* ]] || [[ "$item" == *__pycache__* ]] || [[ "$item" == *uploads* ]] || [[ "$item" == RAG ]] || [[ "$item" == *.vscode* ]] || [[ "$item" == *build* ]] || [[ "$item" == *external* ]]; then
                continue
            else
                # If it's another directory, recursively process it
                process_directory "$item"
            fi
        elif [ -f "$item" ]; then
            # Skip files with ".log" extension
            if [[ "$item" == *.log ]] || [[ "$item" == *.txt ]]; then
                continue
            else
                # Write the file path to the output file
                echo "File: $item , the code for this file is : " >> "$output_file"
                
                # Write the content of the file to the output file
                cat "$item" >> "$output_file"
                echo -e "\n" >> "$output_file"  # Add a newline for better readability
            fi
        fi
    done
}

# Start processing from the start directory
process_directory "$start_directory"
