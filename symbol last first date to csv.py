# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 00:37:42 2023

@author: ppare
"""

import os
import csv

data_dir = "C:\\Users\\ppare\\Documents\\Patternz data"
output_file = "list_file_2.csv"

# Get the list of .txt files in the data directory
txt_files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]

# Create the CSV file and write the header
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Symbol", "First Date", "Last Date"])

    # Process each .txt file
    for txt_file in txt_files:
        symbol = os.path.splitext(txt_file)[0]  # Extract symbol name from file name
        file_path = os.path.join(data_dir, txt_file)

        # Read the first and last lines of the file
        with open(file_path, "r") as file:
            lines = file.readlines()

            if lines:  # Check if the file is not empty
                first_line = lines[0].strip()
                last_line = lines[-1].strip()

                # Split the lines into fields
                first_fields = first_line.split(",")
                last_fields = last_line.split(",")

                # Extract the first and last dates
                first_date = first_fields[0]
                last_date = last_fields[0]

                # Write symbol, first date, and last date to CSV
                writer.writerow([symbol, first_date, last_date])

print("CSV file created successfully.")
