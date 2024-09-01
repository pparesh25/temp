# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 23:28:45 2024

@author: ppare
"""

import pandas as pd

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
print("Data has been merged and written to 'output_file.xlsx'.")
