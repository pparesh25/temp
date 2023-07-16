# -*- coding: utf-8 -*-
"""
Created on Mon May 15 02:30:04 2023

@author: ppare
"""

import urllib.request
import os
import socket
import zipfile
from datetime import datetime, timedelta

def download_file(url, output_folder):
    filename = os.path.basename(url)
    output_path = os.path.join(output_folder, filename)
    urllib.request.urlretrieve(url, output_path)
    print("Downloaded:", filename)
    return output_path

def extract_files(zip_file, output_folder):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    print("Extracted:", zip_file)

output_folder = "C:/data_fo"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

delta = end - start
date_range = []
for i in range(delta.days + 1):
    date = start + timedelta(days=i)
    if date.weekday() < 5:  # Skip Saturday (5) and Sunday (6)
        date_range.append(date)

socket.setdefaulttimeout(1)  # Set the timeout to 1 seconds

downloaded_files = []

for date in date_range:
    url = "https://archives.nseindia.com/content/historical/DERIVATIVES/{}/{}".format(
        date.strftime("%Y"), date.strftime("%b").upper())
    date_str = date.strftime("%d%b%Y").upper()
    filename = "fo{}bhav.csv.zip".format(date_str)
    url = "{}/{}".format(url, filename)
    #print("URL:", url)
    try:
        downloaded_file = download_file(url, output_folder)
        downloaded_files.append(downloaded_file)
    except Exception as e:
        print("Error downloading file:", url)
        print(e)

for file in downloaded_files:
    try:
        extract_files(file, output_folder)
    except Exception as e:
        print("Error extracting file:", file)
        print(e)

print("All downloads and extractions completed.")
