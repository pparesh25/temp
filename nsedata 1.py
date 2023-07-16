# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 19:43:53 2023

@author: ppare
"""

import nsepy
import requests
import pandas as pd
import io
import datetime
import sys
import time

# Set the date for which you want the data
date = '2023-04-07'

# Check if the selected date is a weekend day
selected_date = datetime.datetime.strptime(date, '%Y-%m-%d')
if selected_date.weekday() >= 5:
    print('Warning: Selected date is a weekend day. Please select a weekday.')
    sys.exit()

# Get the list of Nifty indices
url = 'https://www1.nseindia1.com/content/indices/ind_nifty50list.csv'
response = requests.get(url)
nifty_list = pd.read_csv(io.StringIO(response.text))
nifty_indices = nifty_list['Symbol'].tolist()

# Download all index data for the given date
start_time = time.time()
nse_index_data = pd.DataFrame()
for index in nifty_indices:
    index_data = nsepy.get_history(symbol=index, start=date, end=date, index=True)
    nse_index_data = pd.concat([nse_index_data, index_data])

# Download all stock data for the given date
nse_stock_data = pd.DataFrame()
for stock in nsepy.stock_list():
    stock_data = nsepy.get_history(symbol=stock, start=date, end=date)
    nse_stock_data = pd.concat([nse_stock_data, stock_data])

# Save the data to a single CSV file
nse_data = pd.concat([nse_index_data, nse_stock_data])
nse_data.to_csv('nse_data_{}.csv'.format(date), index=False)
end_time = time.time()

# Print the execution time
print('Execution time: {} seconds'.format(end_time - start_time))
