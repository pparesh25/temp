''' if code not work Replace "latin-1" in 
line 14 with the appropriate encoding like

"latin-1" , "utf-16" , "cp1252" , "iso-8859-1"

 '''

import csv
import os

txt_folder = "C:/BSE"
csv_file = "C:/CSV/name.csv"

encoding = "latin-1"

# Read the CSV file into a dictionary
name_dict = {}
with open(csv_file, 'r', encoding=encoding) as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        name_dict[row[0]] = row[1]

# Iterate over the text files in the folder
for file_name in os.listdir(txt_folder):
    if file_name.endswith(".txt"):
        file_path = os.path.join(txt_folder, file_name)
        
        # Read the contents of the text file
        lines = []
        with open(file_path, 'r', encoding=encoding) as txt_file:
            lines = txt_file.readlines()
        
        # Replace the numbers with names
        modified_lines = []
        for line in lines:
            columns = line.strip().split(',')
            if columns[0] in name_dict:
                columns[0] = name_dict[columns[0]]
            modified_lines.append(','.join(columns))
        
        # Write the modified contents back to the text file
        with open(file_path, 'w', encoding=encoding) as txt_file:
            txt_file.write('\n'.join(modified_lines))