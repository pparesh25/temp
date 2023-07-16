# -*- coding: utf-8 -*-
"""
Created on Sun May 14 21:35:56 2023

@author: ppare
"""

import urllib.request
import os
from datetime import datetime, timedelta

def download_file(url, filename):
    urllib.request.urlretrieve(url, filename)

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

base_url = "https://archives.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}bhav.csv.zip"
output_folder = r"C:\data"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for date in date_range:
    date_str = date.strftime("%Y/%b").upper()
    filename = "cm{}bhav.csv.zip".format(date.strftime("%d%b%Y").upper())
    url = base_url.format(date.year, date_str, filename)
    output_path = os.path.join(output_folder, filename)

    try:
        print("Downloading:", filename)
        download_file(url, output_path)
        print("Download complete:", filename)
    except Exception as e:
        print("Error downloading:", filename)
        print(e)

print("All downloads completed.")
