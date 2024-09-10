# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 23:36:00 2024

@author: ppare
"""

import os
import sys
import time
import pandas as pd
import mplfinance as mpf
from datetime import date
import matplotlib.pyplot as plt
from multiprocessing import Pool


# Start measuring execution time
start_time = time.time()

# Read the data from a CSV file
df = pd.read_csv('input_file.csv', skiprows=10)

# Convert the 'Stock' column to string
df['Stock'] = df['Stock'].astype(str)

# Remove NSE SME Stocks
df = df[~df['Stock'].str.endswith('_SME.txt')]

# Extract the stock symbol from the 'Stock' column
df['Stock'] = df['Stock'].str.split('.').str[0]

# Split the "Approx. Target" column by 'or' and create new columns
df[['Approx. Target Value', 'Approx. Target Percentage']] = df['Approx. Target'].str.split(' or ', expand=True)

# Split the "Volatility Stop" column by 'or' and create new columns
df[['Volatility Stop Value', 'Volatility Stop Percentage']] = df['Volatility Stop'].str.split(' or ', expand=True)

# Extract the trade action and trade date from the "Trade Status" column
df['Trade Action'] = df['Trade Status'].str.extract(r'(Target|Stop|Open)')
df['Trade Date'] = df['Trade Status'].str.extract(r'(\d{2}/\d{2}/\d{4})')

df.rename(columns={'Pattern Description': 'Pattern Name',
                   'Approx. Breakout Price': 'Breakout Price',
                   'Pattern Width (days/price bars)': 'Pattern Width',
                   'Approx. Target Value': 'Target', 
                   'Approx. Target Percentage': 'Target %',
                   'Volatility Stop Value': 'Stop',
                   'Volatility Stop Percentage': 'Stop %',
                   #'Start': 'Start',
                   #'End': 'End'
                   }, inplace=True)

# Delete the original columns
df.drop(['Target %',
         'Stop %',
         'Approx. Target', 
         'Volatility Stop', 
         'Trade Status', 
         'Ultimate High/Low',
         'Ultimate H/L Date',
         'Breakout Price',
         'Fill Price',
         #'Avg 3 Mo. Volume',
         'Height',
         'Stage',
         ], axis=1, inplace=True)

# Calculate the difference in days between 'End' and 'Breakout Date'
df['Breakout Day'] = (pd.to_datetime(df['Breakout Date'], format='%m/%d/%Y') - pd.to_datetime(df['End'], format='%m/%d/%Y')).dt.days


# Convert 'Trade Date' column to datetime
df['Trade Date'] = pd.to_datetime(df['Trade Date'], format='%m/%d/%Y')


# 'Plot Start' = 'Start' - 300 days
df['Plot Start'] = pd.to_datetime(df['Start'], format='%m/%d/%Y') - pd.to_timedelta(300, unit='D')

# Convert 'Plot Start' column to datetime
df['Plot Start'] = pd.to_datetime(df['Plot Start'], format='%m/%d/%Y')

# 'Plot End' = date today 
df['Plot End'] = pd.to_datetime(date.today(), format='%m/%d/%Y')

# Convert 'Plot End' column to datetime
df['Plot End'] = pd.to_datetime(df['Plot End'], format='%m/%d/%Y')

# Sort the data by 'Daily Return %' column in descending order
df_sorted = df.sort_values(by='End', ascending=False)

# Reset the index after sorting
df_sorted = df_sorted.reset_index(drop=True)

# Save the sorted DataFrame to an Excel file
df_sorted.to_excel('output_file.xlsx', index=False)
print("Data has been written to 'output_file.xlsx'.")

# Step 1: Read the existing Excel file into a DataFrame
output_df = pd.read_excel('output_file.xlsx')

# Step 2: Read the CSV file into another DataFrame
query_df = pd.read_csv('query-results.csv')

# Step 3: Merge the two DataFrames based on the specified columns
# Assuming you want to match 'Stock' from output_df with 'NSE Code' from query_df
merged_df = pd.merge(output_df, query_df, left_on='Stock', right_on='NSE Code', how='left')

# Step 4: Drop rows where 'NSE Code' is NaN
merged_df = merged_df.dropna(subset=['NSE Code'])

# Step 5: Filter the DataFrame based on the specified conditions
filtered_df = merged_df[(merged_df['FII holding'] > 2)] #| (merged_df['Market Capitalization'] > 1000)]

filtered_df = filtered_df.loc[(merged_df['Market Capitalization'] > 1000)]

# Reset the index after sorting
filtered_df = filtered_df.reset_index(drop=True)

# Step 4: Write the updated DataFrame back to the Excel file

# You can overwrite the existing file or create a new one
with pd.ExcelWriter('output_file.xlsx', engine='openpyxl', mode='a') as writer:
    filtered_df.to_excel(writer, index=True, index_label='Index', sheet_name='Updated Data')
    # Notify the user
    print("Fundamental data has been merged to 'output_file.xlsx'.")

# Define the function to process each stock
def process_stock(row):
    pattern_name = row['Pattern Name']
    stock = row['Stock']
    Index = str(int(row['Index']))

    # Create the folder based on the pattern name if it doesn't exist
    folder_path = os.path.join(r"C:\Patterns images", pattern_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get the stock data file path
    stock_file = os.path.join(r"C:\Patternsdata", stock + ".txt")

    # Load the stock data from the text file
    stock_data = pd.read_csv(stock_file, header=None, names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data.set_index('Date', inplace=True)

    # Get the start and end dates from the filtered dataframe
    stock_start_date = row['Plot Start']
    stock_end_date = row['Plot End']

    # Filter the stock data based on the specified date range
    stock_data = stock_data.loc[stock_start_date:stock_end_date]

    # Plot the OHLC chart and get the axes object
    fig, axes = mpf.plot(stock_data, type='candle', volume=True, style='charles', figsize=(48, 22),
                         ylabel_lower='Volume', panel_ratios=(3, 1), title=stock, ylabel='Price', returnfig=True)

    # Customize the grid lines
    plt.grid(True, linestyle=':', linewidth=0.3, color='gray')

    # Convert dates to corresponding index values
    start_index = stock_data.index.get_loc(row['Start'])
    end_index = stock_data.index.get_loc(row['End'])

    # Mark the "Start" and "End" dates
    axes[0].axvline(x=start_index, color='blue', linestyle=':')
    axes[0].axvline(x=end_index, color='green', linestyle=':')

    # Overlay fundamental data on the chart
    stock_fundamentals = df[df['Stock'] == stock].iloc[0]
    text_str = f"""
    Compny Name: {stock_fundamentals['Name']}
    Industry: {stock_fundamentals['Industry']}
    Current Market Price: {stock_fundamentals['Current Price']}
    Intrinsic Value: {stock_fundamentals['Intrinsic Value']}
    Market Capitalization: {stock_fundamentals['Market Capitalization']}
    Operating margin: {stock_fundamentals['OPM']}
    FII Holding: {stock_fundamentals['FII holding']}
    DII Holding: {stock_fundamentals['DII holding']}
    Promoter Holding: {stock_fundamentals['Promoter holding']}
    Public holding: {stock_fundamentals['Public holding']}
    Price to Book Value: {stock_fundamentals['Price to book value']}
    Industry PBV: {stock_fundamentals['Industry PBV']}
    EPS: {stock_fundamentals['EPS']}
    P/E Ratio: {stock_fundamentals['Price to Earning']}
    Industry PE: {stock_fundamentals['Industry PE']}
    Debt to equity: {stock_fundamentals['Debt to equity']}
    Sales growth 5Years: {stock_fundamentals['Sales growth 5Years']}
    Profit growth 5Years: {stock_fundamentals['Profit growth 5Years']}
    Pledged percentage: {stock_fundamentals['Pledged percentage']}
    Dividend yield: {stock_fundamentals['Dividend yield']}
    Trading Volume Avg 3 Month: {stock_fundamentals['Avg 3 Mo. Volume']}
    DMA 50: {stock_fundamentals['DMA 50']}
    DMA 200: {stock_fundamentals['DMA 200']}
    """
    font_properties = {'family': 'monospace', 'weight': 'bold', 'size': 22}
    plt.figtext(0.22, 0.60, text_str, fontdict=font_properties, color='blue', ha='left', bbox=dict(facecolor='pink', alpha=0.2))

    # Save the chart as an image
    image_name = Index + ' ' + stock + ' ' + pattern_name + '.png'
    image_path = os.path.join(folder_path, image_name)
    plt.savefig(image_path)
    plt.close()



# Load the data from the Excel file
file_path = r"C:\Users\ppare\output_file.xlsx"
df = pd.read_excel(file_path, sheet_name='Updated Data')

# Create a multiprocessing pool and process the rows
if __name__ == '__main__':
    with Pool() as pool:
        pool.map(process_stock, [row for _, row in df.iterrows()])

        print("Images exported successfully.")

        # Stop measuring execution time
        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time:", execution_time, "seconds")

    sys.exit()