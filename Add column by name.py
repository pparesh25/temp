# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 20:46:47 2023

@author: ppare
"""

import os
import pandas as pd

data_folder = "C:\\data"

# Iterate over the files in the data_folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    
    # Read the file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Remove the file extension from the filename
    filename_without_extension = os.path.splitext(filename)[0]
    
    # Add a new column with the modified file name as the first column
    df.insert(0, 'Symbol', filename_without_extension.upper())
    
    # Write the updated DataFrame back to the file
    df.to_csv(file_path, index=False)

print("Adding uppercase file names as the first column is complete.")

