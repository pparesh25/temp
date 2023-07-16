# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 03:34:12 2023

@author: ppare
"""
#PPP
import pandas as pd
import os
import matplotlib.pyplot as plt
import mplfinance as mpf

# Load the data from the Excel file
file_path = r"C:\Users\ppare\output_file.xlsx"
df = pd.read_excel(file_path)

# Filter the data based on the condition
filtered_df = df[df['Daily Return %'] > 0.25]

# Extract the stock symbol from the 'Stock' column
filtered_df['Stock'] = filtered_df['Stock'].str.split('.').str[0]

# Iterate over the filtered stocks and plot OHLC charts
for index, row in filtered_df.iterrows():
    pattern_name = row['Pattern Name']
    stock = row['Stock']
    pattern_width = str(int(row['Pattern Width']))
    breakout_day  = str(int(row['Breakout Day']))
    holding_day   = str(int(row['Holding Day']))
    daily_return = "{:.2f}".format(row['Daily Return %'])

    # Create the folder based on the pattern name if it doesn't exist
    folder_path = os.path.join(r"C:\Patterns images", pattern_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get the stock data file path
    stock_file = os.path.join(r"C:\Users\ppare\Documents\Patternz data", stock + ".txt")

    # Load the stock data from the text file
    stock_data = pd.read_csv(stock_file, header=None, names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data.set_index('Date', inplace=True)

    # Get the start and end dates from the filtered dataframe
    stock_start_date = row['Start']
    stock_end_date = row['Trade Date']

    # Filter the stock data based on the specified date range
    stock_data = stock_data.loc[stock_start_date:stock_end_date]

    # Plot the OHLC chart and get the axes object
    fig, axes = mpf.plot(stock_data, type='candle', style='yahoo', title=stock, ylabel='Price', returnfig=True)

    # Convert dates to corresponding index values
    end_index = stock_data.index.get_loc(row['End'])
    breakout_index = stock_data.index.get_loc(row['Breakout Date'])

    # Mark the "End" date with a red marker
    axes[0].axvline(x=end_index, color='red', linestyle='--')

    # Mark the "Breakout Date" with a green marker
    axes[0].axvline(x=breakout_index, color='green', linestyle='--')

    # Save the chart as an image in the corresponding folder
    image_name = pattern_name+' '+ stock +' '+ pattern_width +' '+ breakout_day +' '+ holding_day +' '+ str(daily_return) + '.png'
    image_path = os.path.join(folder_path, image_name)
    plt.savefig(image_path)

    plt.close()

print("Images exported successfully.")
