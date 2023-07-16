# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 20:11:18 2023

@author: ppare
"""

import nsepy
import requests
import pandas as pd
import zipfile
import io
import datetime
import sys
import time

def download_bhavcopy(date):
    """
    Downloads the NSE Equity Bhavcopy zip file for the given date and extracts it.
    Returns a Pandas DataFrame with the data.
    """
    print('Downloading NSE Equity Bhavcopy')
    year = datetime.datetime.strptime(date, '%Y-%m-%d').year
    month = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%b').upper()
    url = 'https://www1.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}{}{}bhav.csv.zip'.format(year, month, datetime.datetime.strptime(date, '%Y-%m-%d').day, month, year)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Extract the zip file and read the CSV data into a Pandas DataFrame
        try:
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                filename = z.namelist()[0]
                with z.open(filename) as f:
                    df = pd.read_csv(f)
            return df
        except Exception as e:
            print('Could not extract NSE zip file.')
            print(e)
            return None
    else:
        print('Could not download NSE Bhavcopy file.')
        return None

# Set the date for which you want the data
date = '2023-04-07'

# Check if the selected date is a weekend day
selected_date = datetime.datetime.strptime(date, '%Y-%m-%d')
if selected_date.weekday() >= 5:
    print('Warning: Selected date is a weekend day. Please select a weekday.')
    sys.exit()

# Download the NSE Equity Bhavcopy for the given date
bhavcopy_data = download_bhavcopy(date)
while bhavcopy_data is None:
    # If there was an error downloading or extracting the Bhavcopy, try again
    print('Retrying download...')
    bhavcopy_data = download_bhavcopy(date)

# Get the list of Nifty indices
print('Downloading index data for NSENIFTY')
nifty_indices = ['NIFTY 50', 'NIFTY BANK', 'NIFTY IT', 'NIFTY PHARMA', 'NIFTY FMCG', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY ENERGY', 'NIFTY INFRA', 'NIFTY REALTY']
nse_index_data = pd.DataFrame()
for index in nifty_indices:
    index_data = nsepy.get_history(symbol=index, start=date, end=date, index=True)
    nse_index_data = pd.concat([nse_index_data, index_data])

# Combine the Bhavcopy and index data
nse_data = pd.concat([bhavcopy_data, nse_index_data])

# Save the data to a CSV file
nse_data.to_csv('nse_data_{}.csv'.format(date), index=False)

# Print the execution time
print('Data saved successfully.')
