# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 01:49:40 2023

@author: ppare
"""

# Remove raw based on column date 
import os

# Specify the input directory containing the input files
input_directory = 'C:/data/'

# Specify the output directory to save the filtered files
output_directory = 'C:/data1/'

# Get a list of all files in the input directory
files = os.listdir(input_directory)

# Process each file
for file_name in files:
    # Check if the file is a .txt file
    if file_name.endswith('.txt'):
        # Construct the full file paths
        input_file_path = os.path.join(input_directory, file_name)
        output_file_path = os.path.join(output_directory, file_name)
        
        # Open the input and output files
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
            # Read the input file line by line
            for line in input_file:
                # Split the line into fields
                fields = line.strip().split(',')
                # Extract the date from the fields
                date = fields[1]
                # Check if the date is before or on December 30, 2022
                if date <= '20221230':
                    # Write the line to the output file
                    output_file.write(line)
