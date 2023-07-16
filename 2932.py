# -*- coding: utf-8 -*-
"""
Created on Sun May 21 15:19:38 2023

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
    print(f'Eq-bhavcopy {filename} downloaded.')
    return output_path

def extract_files(zip_file, output_folder):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    print("Zip file extracted:", zip_file)

def rename_files(directory):
    files = os.listdir(directory)
    renamed_files = []

    for file in files:
        if file.endswith("bhav.csv"):
            date = file[2:11]
            new_name = date + ".csv"
            new_name = new_name.replace("cm", "").replace("bhav", "")
            date_obj = datetime.strptime(date, "%d%b%Y")
            new_name = date_obj.strftime("%Y-%m-%d") + "-NSE-EQ.csv"
            old_path = os.path.join(directory, file)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            renamed_files.append((file, new_name))
        else:
            print(f"File '{file}' does not end with 'bhav.csv' and was not renamed.")

    if renamed_files:
        for old_name, new_name in renamed_files:
            print(f"File '{old_name}' renamed to: '{new_name}'")
    else:
        print("No files found or no files meet the desired condition.")

output_folder = "C:/data"

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
    if date.weekday() < 5: 
        date_range.append(date)

socket.setdefaulttimeout(1) 

downloaded_files = []

for date in date_range:
    url = "https://archives.nseindia.com/content/historical/EQUITIES/{}/{}".format(
        date.strftime("%Y"), date.strftime("%b").upper())
    date_str = date.strftime("%d%b%Y").upper()
    filename = "cm{}bhav.csv.zip".format(date_str)
    url = "{}/{}".format(url, filename)

    try:
        downloaded_file = download_file(url, output_folder)
        downloaded_files.append(downloaded_file)
    except Exception as e:
        print(f'Eq-bhavcopy {filename} not available probable holiday.')
        print(e)

for file in downloaded_files:
    try:
        extract_files(file, output_folder)
    except Exception as e:
        print("Error extracting file:", file)
        print(e)

for file in downloaded_files:
    os.remove(file)
    print("Zip file removed:", file)

rename_files(output_folder)


