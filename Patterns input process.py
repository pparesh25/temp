# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 23:54:22 2023

@author: ppare
"""

#PPP
import pandas as pd

# Read the data from a CSV file
df = pd.read_csv('input_file.csv')

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
                   'Start': 'Start',
                   'End': 'End'}, inplace=True)

# Delete the original columns
df.drop(['Approx. Target', 
         'Volatility Stop', 
         'Trade Status', 
         'Ultimate High/Low',
         'Ultimate H/L Date',
         #'Breakout Price',
         'Fill Price',
         'Avg 3 Mo. Volume',
         'Height',
         'Stage',
         ], axis=1, inplace=True)

# Calculate the difference in days between 'Breakout Date' and 'Trade Date'
df['Breakout Day'] = (pd.to_datetime(df['Breakout Date'], format='%m/%d/%Y') - pd.to_datetime(df['End'], format='%m/%d/%Y')).dt.days

# Calculate the difference in days between 'Breakout Date' and 'Trade Date'
df['Holding Day'] = (pd.to_datetime(df['Trade Date'], format='%m/%d/%Y') - pd.to_datetime(df['Breakout Date'], format='%m/%d/%Y')).dt.days

# Calculate the difference in days between 'Breakout Date' and 'Trade Date'
df['Start to Trade Date Day'] = (pd.to_datetime(df['Trade Date'], format='%m/%d/%Y') - pd.to_datetime(df['Start'], format='%m/%d/%Y')).dt.days


# Convert 'Target %' and 'Stop %' columns to numeric data type
df['Target %'] = pd.to_numeric(df['Target %'].str.rstrip('%'))
df['Stop %'] = pd.to_numeric(df['Stop %'].str.rstrip('%'))

# Calculate the risk-reward ratio
df['Risk Reward'] = df['Target %'] / df['Stop %'] * -1

# Calculate daily return in %
df['Daily Return %'] = df.apply(lambda row: row['Target %'] / row['Holding Day']
                                if row['Breakout'] == 'Up' and row['Trade Action'] == 'Target' and row['Holding Day'] > 0 else None, axis=1)

# Convert 'Daily Return %' column to numeric data type
df['Daily Return %'] = pd.to_numeric(df['Daily Return %'], errors='coerce')

# Sort the data by 'Daily Return %' column in descending order
df_sorted = df.sort_values(by='Daily Return %', ascending=False)

# Reset the index after sorting
df_sorted = df_sorted.reset_index(drop=True)

# Save the sorted DataFrame to an Excel file
df_sorted.to_excel('output_file.xlsx', index=False)
