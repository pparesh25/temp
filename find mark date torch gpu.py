# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 01:25:38 2023

@author: ppare
"""

import os
import pandas as pd
import torch
import talib as ta
import numpy as np
import time

# Set device to GPU if available, otherwise use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Print device information
print("Device:", device)

# Path to the data directory
data_dir = 'C:/data1'

# List all the files in the data directory
files = os.listdir(data_dir)

# Create an empty DataFrame to store the results
results = pd.DataFrame(columns=['symbol', 'date', 'close', 'EMA_50', 'EMA_150', 'EMA_200', 'EMA_200_30', '52 week high', '52 week low', 'Mark','Down from 52w high'])

# Start measuring execution time
start_time = time.time()

# Iterate over each file
for file in files:
    # Check if the file is a text file
    if file.endswith('.txt'):
        # Read the file into a DataFrame, assuming no header row
        filepath = os.path.join(data_dir, file)
        df = pd.read_csv(filepath, header=None, names=['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'])

        # Convert the DataFrame to a PyTorch Tensor
        close_tensor = torch.tensor(df['close'].values, dtype=torch.float32).to(device)

        # Convert PyTorch Tensor to NumPy array
        close_array = close_tensor.cpu().numpy()

        # Convert the NumPy array to double
        close_double = close_array.astype(np.double)

        # Calculate the moving averages using talib on the double array
        ema_50 = ta.EMA(close_double, timeperiod=50).round(2)
        ema_150 = ta.EMA(close_double, timeperiod=150).round(2)
        ema_200 = ta.EMA(close_double, timeperiod=200).round(2)

        # Convert the calculated moving averages back to a DataFrame
        df['EMA_50'] = pd.Series(ema_50)
        df['EMA_150'] = pd.Series(ema_150)
        df['EMA_200'] = pd.Series(ema_200)

        # Obtain the 200-day EMA before 30 days
        df['EMA_200_30'] = df['EMA_200'].shift(30)

        # Calculate the 52-week high and low based on close values
        df['52 week high'] = ta.MAX(df['high'], timeperiod=252)
        df['52 week low'] = ta.MIN(df['low'], timeperiod=252)
        
        df['Down from 52w high'] = (((df['52 week high'] - df['close'])/df['52 week high'])*100).round(2)

        # Filter the DataFrame to get the last row
        last_row = df.iloc[[-1]]

        # Reverse the DataFrame to iterate from the last date
        reversed_df = df.iloc[::-1]

        # Find the date when the condition is first met starting from the last date and moving backwards
        first_match_date = ''
        for index, row in reversed_df.iterrows():
            if row['close'] > row['EMA_50'] > row['EMA_150'] > row['EMA_200'] :
                first_match_date = row['date']
                
            else:
                break

        # Assign the first match date to the 'Mark' column
        last_row = df.iloc[[-1]].copy()
        last_row['Mark'] = first_match_date

        # Append the last row to the results DataFrame
        results = pd.concat([results, last_row[['symbol', 'date', 'close', 'EMA_50', 'EMA_150', 'EMA_200', 'EMA_200_30', '52 week high', '52 week low', 'Mark','Down from 52w high']]], ignore_index=True)

# Stop measuring execution time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")

# Export the results to a CSV file
results.to_csv('output.csv', index=False)
