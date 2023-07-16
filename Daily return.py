# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 21:56:42 2023

@author: ppare
"""

import pandas as pd

# Read the Excel file
df = pd.read_excel('output_file.xlsx')

# Calculate daily return in %
df['Daily Return %'] = df.apply(lambda row: float(row['Target %'].strip('%')) / ( row['Pattern Width'])
                                if row['Breakout'] == 'Up' and row['Trade Action'] == 'Target' else None, axis=1)


# Save the modified DataFrame to Excel
df.to_excel('output_file.xlsx', index=False)
