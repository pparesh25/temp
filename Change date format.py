# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 20:56:20 2023

@author: ppare
"""

import os
import pandas as pd

data_folder = "C:\\data1"

# Iterate over the files in the data_folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    
    # Read the file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Convert the date column format from MM/DD/YYYY to YYYYMMDD
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y%m%d')
    
    # Write the updated DataFrame back to the file
    df.to_csv(file_path, index=False)

print("Date format conversion is complete.")
