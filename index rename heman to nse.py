# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 22:32:14 2023

@author: ppare
"""

import os

# Define the mapping for symbol replacements

symbol_mapping = {
    
    'NSENIFTY': 'Nifty 50',
    'NIFTYJUNIOR': 'Nifty Next 50',
    'NIFTYMIDCAPLIQ15': 'Nifty Midcap Liquid 15',
    'NSE100': 'Nifty 100',
    'NIFTY200': 'Nifty 200',
    'NSE500': 'Nifty 500',
    'NSEMIDCAP150': 'Nifty Midcap 150',
    'MIDCAP50': 'Nifty Midcap 50',
    'NSEMIDCAP': 'NIFTY Midcap 100',
    'NSESMLCAP100': 'NIFTY Smallcap 100',
    'NIFTYLARGEMIDCAP250': 'NIFTY LargeMidcap 250',
    'NIFTYAUTO': 'Nifty Auto',
    'BANKNIFTY': 'Nifty Bank',
    'NIFTYFINSERVICE': 'Nifty Financial Services',
    'NIFTYFMGC': 'Nifty FMCG',
    'NSEIT': 'Nifty IT',
    'NIFTYMEDIA': 'Nifty Media',
    'NIFTYMETAL': 'Nifty Metal',
    'NIFTYPHARMA': 'Nifty Pharma',
    'NIFTYPVTBANK': 'Nifty Private Bank',
    'NIFTYPSUBANK': 'Nifty PSU Bank',
    'NIFTYREALTY': 'Nifty Realty',
    'NIFTYCOMMODITIES': 'Nifty Commodities',
    'NIFTYCONSUMPTION': 'Nifty India Consumption',
    'NIFTYCPSE': 'Nifty CPSE',
    'NIFTYENERGY': 'Nifty Energy',
    'NIFTY100ESG': 'NIFTY100 ESG',
    'NIFTY100ENHESG': 'NIFTY100 Enhanced ESG',
    'NIFTYINFRA': 'Nifty Infrastructure',
    'NIFTYMNC': 'Nifty MNC',
    'NIFTYPSE': 'Nifty PSE',
    'NIFTYSMEEMERGE': 'NIFTY SME EMERGE',
    'NIFTYSERVSECTOR': 'Nifty Services Sector',
    'NIFTYSHARIAH25': 'Nifty Shariah 25',
    'NIFTY50SHARIAH': 'Nifty50 Shariah',
    'NIFTY500SHARIAH': 'Nifty500 Shariah',
    'NIFTYABGROUP': 'Nifty Aditya Birla Group',
    'NIFTYMAHINDRA': 'Nifty Mahindra Group',
    'NIFTYTATA': 'Nifty Tata Group',
    'NIFTYTATA25CAP': 'Nifty Tata Group 25% Cap',
    'NIFTYLIQ15': 'Nifty100 Liquid 15',
    'NIFTY500VALUE50': 'NIFTY500 Value 50',
    'NIFTYQUALLOWVOL30': 'NIFTY Quality Low-Volatility 30',
    'NIFTYALPHAQUALLOWVOL30': 'NIFTY Alpha Quality Low-Volatility 30',
    'NIFTYALPHAQUALVALLOWVOL30': 'NIFTY Alpha Quality Value Low-Volatility 30',
    'NIFTY50EQUALWEIGHT': 'NIFTY50 Equal Weight',
    'NIFTY100EQUALWEIGHT': 'Nifty100 Equal Weight',
    'NIFTY100LOWVOL30': 'Nifty100 Low Volatility 30',
    'NSEDEFTY': 'Nifty50 USD',
    'NIFTY50DIVPOINT': 'Nifty50 Dividend Points',
    'NIFTYDIVOPPS50': 'Nifty Dividend Opportunities 50',
    'NIFTYALPHA50': 'Nifty Alpha 50',
    'NIFTY50ARBITRAGE': 'Nifty 50 Arbitrage',
    'NIFTY50FUTINDEX': 'Nifty 50 Futures Index',
    'NIFTY50FUTTRINDEX': 'Nifty 50 Futures TR Index',
    'NIFTYHIGHBETA50': 'Nifty High Beta 50',
    'NIFTYLOWVOL50': 'Nifty Low Volatility 50',
    'NIFTY50VALUE20': 'Nifty50 Value 20',
    'NIFTYGROWSECT15': 'Nifty Growth Sectors 15',
    'NIFTY50TR2XLEV': 'Nifty50 TR 2x Leverage',
    'NIFTY50PR2XLEV': 'Nifty50 PR 2x Leverage',
    'NIFTY50TR1XINV': 'Nifty50 TR 1x Inverse',
    'NIFTY50PR1XINV': 'Nifty50 PR 1x Inverse',
    'NIFTY-GS-COMPSITE': 'Nifty Composite G-sec Index',
    'NIFTY-GS-4-8YR': 'Nifty 4-8 yr G-Sec Index',
    'NIFTY-GS-8-13YR': 'Nifty 8-13 yr G-Sec',
    'NIFTY-GS-10YR': 'Nifty 10 yr Benchmark G-Sec',
    'NIFTY-GS-10YR-CLN': 'Nifty 10 yr Benchmark G-Sec (Clean Price)',
    'NIFTY-GS-11-15YR': 'Nifty 11-15 yr G-Sec Index',
    'NIFTY-GS-15YRPLUS': 'Nifty 15 yr and above G-Sec Index',
    'VIX': 'India VIX'
    
}

# Define the cutoff date
cutoff_date = '20221230'

# Input and output directory paths
input_directory = 'C:/data'
output_directory = 'C:/data1'

# Get a list of all .txt files in the input directory
input_files = [f for f in os.listdir(input_directory) if f.endswith('.txt')]

# Process each input file
for input_file in input_files:
    input_file_path = os.path.join(input_directory, input_file)

    # Read the input file
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Filter and modify the lines
    filtered_lines = []
    for line in lines:
        symbol, date, *values = line.split(',')
        if date <= cutoff_date:
            if symbol in symbol_mapping:
                 symbol = symbol_mapping[symbol]
            filtered_lines.append(','.join([symbol, date] + values))

    # Generate the new file name based on symbol mapping
    symbol_name = symbol_mapping.get(input_file.split('.')[0], input_file.split('.')[0])
    output_file = f'{symbol_name}.txt'
    output_file_path = os.path.join(output_directory, output_file)

    # Save the filtered lines to the output file
    with open(output_file_path, 'w') as file:
        file.writelines(filtered_lines)

    # Print a success message for each file
    print(f'{input_file} renamed, modified, and saved as {output_file}.')

# Print a final success message
print('All files processed successfully.')