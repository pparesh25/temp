# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 22:56:33 2023

@author: ppare
"""

import os

directory = 'C:\\data1'

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)
        
        # Read the content of the file
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        # Remove the header line
        lines = lines[1:]
        
        # Write the modified content back to the file
        with open(filepath, 'w') as file:
            file.writelines(lines)

        print(f"Header removed from {filename}")
