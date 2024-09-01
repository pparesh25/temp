# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 21:29:18 2024

@author: ppare
"""
from datetime import date
import pandas as pd

# Read the data from a CSV file
df = pd.read_csv('input_file.csv', skiprows=10)

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