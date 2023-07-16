# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:34:35 2023

@author: ppare
"""

# Creat list_file.csv with name of symbol and last traded date

#PPP
import os
import csv

data_dir = "C:\\Users\\ppare\\Documents\\Patternz data"
output_file = "list_file_1.csv"

# Get the list of .txt files in the data directory
txt_files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]

# Create the CSV file and write the header
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Symbol", "Last Date"])

    # Process each .txt file
    for txt_file in txt_files:
        symbol = os.path.splitext(txt_file)[0]  # Extract symbol name from file name
        file_path = os.path.join(data_dir, txt_file)

        # Read the last line of the file
        with open(file_path, "r") as file:
            last_line = file.readlines()[-1].strip()

        # Split the last line into fields
        fields = last_line.split(",")

        # Extract the last date
        last_date = fields[0]

        # Write symbol and last date to CSV
        writer.writerow([symbol, last_date])

print("CSV file created successfully.")
