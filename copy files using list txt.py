# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 20:29:45 2023

@author: ppare
"""

import os
import shutil

symbol_list_file = "symbol_name_list.txt"
eod_data_folder = "C:\\data"
destination_folder = "C:\\data1"

# Read the symbol names from symbol_name_list.txt and convert them to lowercase
with open(symbol_list_file, 'r') as file:
    symbol_names = [symbol.lower() for symbol in file.read().splitlines()]

# Iterate over the files in the eod_data_folder
for filename in os.listdir(eod_data_folder):
    # Convert the filename to lowercase for comparison
    lowercase_filename = filename.lower()
    
    # Check if the lowercase filename is in the symbol_names list
    if lowercase_filename[:-4] in symbol_names:  # Assuming the file extensions are .csv
        # Create the source and destination file paths
        source_path = os.path.join(eod_data_folder, filename)
        destination_path = os.path.join(destination_folder, filename)
        
        # Copy the file to the destination folder
        shutil.copy2(source_path, destination_path)
        print(f"File {filename} copied successfully.")

print("Copying files based on symbol names is complete.")


