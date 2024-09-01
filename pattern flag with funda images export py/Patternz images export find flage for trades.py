# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 22:24:53 2024

@author: ppare
"""
###
import pandas as pd
import os
import matplotlib.pyplot as plt
import mplfinance as mpf

# Load the data from the Excel file
file_path = r"C:\Users\ppare\output_file.xlsx"
df = pd.read_excel(file_path,sheet_name='Updated Data')

# Iterate over the filtered stocks and plot OHLC charts
for index, row in df.iterrows():
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
    fig, axes = mpf.plot(stock_data, type='candle', volume=True, style='charles',figsize=(48, 22),
                         ylabel_lower='Volume', panel_ratios=(3, 1),title=stock, ylabel='Price', returnfig=True)
    
    # Customize the grid lines
    plt.grid(True, linestyle=':', linewidth=0.3, color='gray')
    
    # Example modification: Change the background color of the chart
    #axes[0].set_facecolor('black')
    
    
    
    # Convert dates to corresponding index values
    start_index = stock_data.index.get_loc(row['Start'])
    end_index = stock_data.index.get_loc(row['End'])
    
    # Mark the "Start" date with a blue marker
    axes[0].axvline(x=start_index, color='blue', linestyle=':')

    # Mark the "End" date with a green marker
    axes[0].axvline(x=end_index, color='green', linestyle=':')
    
    '''
    breakout_index = stock_data.index.get_loc(row['Breakout Date'])
    target_index = stock_data.index.get_loc(row['Trade Date'])
    
    # Mark the "Breakout Date" with a brown marker
    axes[0].axvline(x=breakout_index, color='brown', linestyle=':')
    
    # Mark the "Trade Date" with a red marker
    axes[0].axvline(x=target_index, color='red', linestyle=':')
    '''
    
    # Overlay fundamental data on the chart
    # Extract relevant fundamental data for the current stock
    stock_fundamentals = df[df['Stock'] == stock].iloc[0]

    # Prepare the text to display
    text_str = f"""
    Compny Name: {stock_fundamentals['Name']}
    Industry: {stock_fundamentals['Industry']}
    Current Market Price: {stock_fundamentals['Current Price']}
    Intrinsic Value: {stock_fundamentals['Intrinsic Value']}
    Market Capitalization: {stock_fundamentals['Market Capitalization']}
    FII Holding: {stock_fundamentals['FII holding']}
    DII Holding: {stock_fundamentals['DII holding']}
    Promoter Holding: {stock_fundamentals['Promoter holding']}
    Price to Book Value: {stock_fundamentals['Price to book value']}
    EPS: {stock_fundamentals['EPS']}
    P/E Ratio: {stock_fundamentals['Price to Earning']}
    Debt to equity: {stock_fundamentals['Debt to equity']}
    Sales growth 5Years: {stock_fundamentals['Sales growth 5Years']}
    Profit growth 5Years: {stock_fundamentals['Profit growth 5Years']}
    Pledged percentage: {stock_fundamentals['Pledged percentage']}
    Dividend yield: {stock_fundamentals['Dividend yield']}
    Trading Volume Avg 3 Month: {stock_fundamentals['Avg 3 Mo. Volume']} 
    """
    # Define font properties
    font_properties = {
        'family': 'monospace',  # Change to 'sans-serif', 'monospace', etc. as needed
        'weight': 'bold',    # Options: 'normal', 'bold', 'light', etc.
        'size': 22           # Font size
    }
    
    # Add the text to the chart
    plt.figtext(0.22, 0.68, text_str, fontdict=font_properties, color='blue', ha='left', bbox=dict(facecolor='pink', alpha=0.2))
   

    # Save the chart as an image in the corresponding folder
    image_name = Index +' '+ stock +' ' + pattern_name + '.png'
    image_path = os.path.join(folder_path, image_name)
    plt.savefig(image_path)

    plt.close()

print("Images exported successfully.")