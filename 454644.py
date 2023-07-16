# -*- coding: utf-8 -*-
"""
Created on Sun May 21 11:04:03 2023

@author: ppare
"""

import os
import requests
from datetime import datetime, timedelta
import pandas as pd


# Specify the start and end dates for the date range
start_date_str = input('Enter the start date (YYYY-MM-DD): ')
end_date_str = input('Enter the end date (YYYY-MM-DD): ')

# Convert the date strings to datetime objects
start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

# Set the destination directory to save the files
destination_dir = 'C:/dataind'

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Specify the base URL
base_url = 'https://archives.nseindia.com/content/indices'

# Iterate over the date range
current_date = start_date
while current_date <= end_date:
    if current_date.weekday() < 5:
        # Format the date in the required format for the file name
        date_str = current_date.strftime('%d%m%Y')

        # Specify the file name
        file_name = f'ind_close_all_{date_str}.csv'

        # Construct the complete URL
        url = f'{base_url}/{file_name}'

        try:
            # Download the file with a timeout of 1 second
            response = requests.get(url, timeout=1)

            if response.status_code == 200:
                # Save the file to the destination directory
                file_path = os.path.join(destination_dir, file_name)
                with open(file_path, 'wb') as file:
                    file.write(response.content)

                # Check if the file was downloaded successfully
                if os.path.getsize(file_path) > 0:
                    print(f'Downloaded index file for {current_date.date()} successfully.')
                else:
                    print(f'Failed to download the index file for {current_date.date()}.')

            else:
                print(f'Failed to download the index file for {current_date.date()}. Error: {response.status_code}')

        except requests.exceptions.RequestException:
            print(f'Timeout occurred Probable holiday {current_date.date()}.')

    # Move to the next date
    current_date += timedelta(days=1)

# Rename the files
files_renamed = False
for filename in os.listdir(destination_dir):
    if filename.startswith("ind_close_all_") and filename.endswith(".csv"):
        date_str = filename.split("_")[-1].split(".")[0]
        date = datetime.strptime(date_str, "%d%m%Y").date()
        new_filename = date.strftime("%Y-%m-%d-NSE-IND.csv")
        file_path = os.path.join(destination_dir, filename)
        new_file_path = os.path.join(destination_dir, new_filename)
        
        if os.path.exists(file_path):
            os.rename(file_path, new_file_path)
            print(f"Renamed file: {filename} to {new_filename}")
            files_renamed = True
        else:
            print(f"File not found: {filename}")

if not files_renamed:
    print("No files matching the criteria were found.")

# Directory path
directory = 'C:/dataind'

# List of columns to be removed
columns_to_remove = ['Points Change', 'Change(%)', 'Turnover (Rs. Cr.)', 'P/E', 'P/B', 'Div Yield']

# List of valid index names
valid_index_names = [
    'Nifty 50', 'Nifty Next 50'
]

# Mapping of index name changes
index_name_mapping = {
    'Nifty 50': 'NSENIFTY',
    'Nifty Next 50': 'NIFTYJUNIOR',
}

# Read files and process them
for filename in os.listdir(directory):
    if filename.endswith('.csv') and '-NSE-IND' in filename:
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        
        # Remove unwanted columns
        df.drop(columns=columns_to_remove, inplace=True)
        
        # Change date format in Index Date column
        df['Index Date'] = pd.to_datetime(df['Index Date'], format='%d-%m-%Y').dt.strftime('%Y%m%d')
        
        # Remove rows with invalid index names
        df = df[df['Index Name'].isin(valid_index_names)]
        
        # Replace index names with the updated mapping
        df['Index Name'] = df['Index Name'].replace(index_name_mapping)
        
        # Save the updated dataframe
        df.to_csv(filepath, index=False)
