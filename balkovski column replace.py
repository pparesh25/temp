# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 19:32:17 2023

@author: ppare
"""

import pandas as pd

# Read the data from a CSV file
df = pd.read_csv('input_file.csv')

# Split the "Approx. Target" column by 'or' and create new columns
df[['Approx. Target Value', 'Approx. Target Percentage']] = df['Approx. Target'].str.split(' or ', expand=True)

# Split the "Volatility Stop" column by 'or' and create new columns
df[['Volatility Stop Value', 'Volatility Stop Percentage']] = df['Volatility Stop'].str.split(' or ', expand=True)

# Extract the trade action and trade date from the "Trade Status" column
df['Trade Action'] = df['Trade Status'].str.extract(r'(Target|Stop|Open)')
df['Trade Date'] = df['Trade Status'].str.extract(r'(\d{4}-\d{2}-\d{2})')

# Delete the original columns
df.drop(['Approx. Target', 'Volatility Stop', 'Trade Status', 'Ultimate High/Low','Ultimate H/L Date','Last Close'], axis=1, inplace=True)

df.rename(columns={'Pattern Description': 'Pattern Name',
                   'Approx. Breakout Price': 'Breakout Price',
                   'Pattern Width (days/price bars)': 'Pattern Width',
                   'Approx. Target Value': 'Target', 
                   'Approx. Target Percentage': 'Target %',
                   'Volatility Stop Value': 'Stop',
                   'Volatility Stop Percentage': 'Stop %',
                   }, inplace=True)

# Convert 'Breakout Date' column from DD-MM-YYYY to YYYY-MM-DD format
df['Breakout Date'] = pd.to_datetime(df['Breakout Date'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')

# Calculate the difference in days between 'Breakout Date' and 'Trade Date'
df['Holding Day'] = (pd.to_datetime(df['Trade Date']) - pd.to_datetime(df['Breakout Date'])).dt.days

# Convert 'Target %' and 'Stop %' columns to numeric data type
df['Target %'] = pd.to_numeric(df['Target %'].str.rstrip('%'))
df['Stop %'] = pd.to_numeric(df['Stop %'].str.rstrip('%'))

# Calculate the risk-reward ratio
df['Risk Reward'] = df['Target %'] / df['Stop %']*-1



# Save the modified DataFrame to an Excel file
df.to_excel('output_file.xlsx', index=False)








