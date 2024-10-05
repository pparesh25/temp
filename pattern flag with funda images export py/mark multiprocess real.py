import os
import pandas as pd
import talib as ta
import time
from multiprocess import Pool, freeze_support, cpu_count
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import date

# Start measuring execution time
start_time = time.time()

# Path to the data directory
data_dir = 'C:/data'

# List all the files in the data directory
files = os.listdir(data_dir)

# Create an empty DataFrame to store the results
results = pd.DataFrame(columns=['symbol', 'date', 'close', 'EMA_50', 'EMA_150', 'EMA_200', 'EMA_200_30', '52 week high', '52 week low', 'Mark', 'Down from 52w high'])

# Function to process each file
def process_file(file):
    # Check if the file is a text file
    if file.endswith('.txt'):
        # Read the file into a DataFrame, assuming no header row
        filepath = os.path.join(data_dir, file)
        df = pd.read_csv(filepath, header=None, names=['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'])
        
        # Convert 'date' column to datetime but do not set as index yet
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

        # Calculate the moving averages
        df['EMA_50'] = ta.EMA(df['close'], timeperiod=50).round(2)
        df['EMA_150'] = ta.EMA(df['close'], timeperiod=150).round(2)
        df['EMA_200'] = ta.EMA(df['close'], timeperiod=200).round(2)

        # Obtain the 200-day EMA before 30 days
        df['EMA_200_30'] = df['EMA_200'].shift(30)

        # Calculate the 52-week high and low based on close values
        df['52 week high'] = ta.MAX(df['high'], timeperiod=252)
        df['52 week low'] = ta.MIN(df['low'], timeperiod=252)

        df['Down from 52w high'] = (((df['52 week high'] - df['close']) / df['52 week high']) * 100).round(2)

        # Filter the DataFrame to get the last row
        last_row = df.iloc[[-1]]

        # Reverse the DataFrame to iterate from the last date
        reversed_df = df.iloc[::-1]

        # Find the date when the condition is first met starting from the last date and moving backwards
        first_match_date = ''
        for index, row in reversed_df.iterrows():
            if row['close'] > row['EMA_50'] > row['EMA_150'] > row['EMA_200'] > row['EMA_200_30'] :
                first_match_date = row['date']
            else:
                break

        # Assign the first match date to the 'Mark' column
        last_row = df.iloc[[-1]].copy()
        last_row['Mark'] = first_match_date

        # Return the last row
        return last_row[['symbol', 'date', 'close', 'EMA_50', 'EMA_150', 'EMA_200', 'EMA_200_30', '52 week high', '52 week low', 'Mark', 'Down from 52w high']]

if __name__ == '__main__':
    

    # Add the freeze_support() call
    freeze_support()

    # Create a pool of worker processes
    pool = Pool()

    # Process each file using parallel execution
    results = pool.map(process_file, files)

    # Close the pool to indicate that no more tasks will be submitted
    pool.close()

    # Wait for all processes to complete
    pool.join()

    # Concatenate the results
    results = pd.concat(results, ignore_index=True)

    # Export the results to a CSV file
    #results.to_csv('output.csv', index=False)
    with pd.ExcelWriter('output_file_mark.xlsx', engine='openpyxl', mode='a') as writer:
        results.to_excel(writer, index=False, sheet_name='Mark_Data' )
    
    # Step 1: Read the existing Excel file into a DataFrame
    output_df = pd.read_excel('output_file_mark.xlsx', sheet_name='Mark_Data')

    # Step 2: Read the CSV file into another DataFrame
    query_df = pd.read_csv('query-results.csv')

    # Step 3: Merge the two DataFrames based on the specified columns
    # Assuming you want to match 'symbol' from output_df with 'NSE Code' from query_df
    merged_df = pd.merge(output_df, query_df, left_on='symbol', right_on='NSE Code', how='left')

    # Step 4: Drop rows where 'NSE Code' is NaN
    merged_df = merged_df.dropna(subset=['NSE Code'])
    

    # Step 5: Filter the DataFrame based on the specified conditions
    filtered_df = merged_df[(merged_df['FII holding'] > 5)] #| (merged_df['Market Capitalization'] > 1000)]

    filtered_df = filtered_df.loc[(merged_df['Market Capitalization'] > 2000)]
    
    # Filter for rows where 'Mark' is NaN
    filtered_df = filtered_df[~filtered_df['Mark'].isna()]
    
    # Sort the data by 'Daily Return %' column in descending order
    df_sorted = filtered_df.sort_values(by='Mark', ascending=False)
    
    # 'Plot Start' = 'Start' - 300 days
    df_sorted['Plot Start'] = pd.to_datetime(df_sorted['Mark'], format='%m/%d/%Y') - pd.to_timedelta(500, unit='D')

    # Convert 'Plot Start' column to datetime
    df_sorted['Plot Start'] = pd.to_datetime(df_sorted['Plot Start'], format='%m/%d/%Y')

    # 'Plot End' = date today 
    df_sorted['Plot End'] = pd.to_datetime(date.today(), format='%m/%d/%Y')

    # Convert 'Plot End' column to datetime
    df_sorted['Plot End'] = pd.to_datetime(df_sorted['Plot End'], format='%m/%d/%Y')

    # Reset the index after sorting
    df_sorted = df_sorted.reset_index(drop=True)

    # Reset the index after sorting
    #filtered_df = filtered_df.reset_index(drop=True)

    # Step 4: Write the updated DataFrame back to the Excel file

    # You can overwrite the existing file or create a new one
    with pd.ExcelWriter('output_file_mark.xlsx', engine='openpyxl', mode='a') as writer:
        df_sorted.to_excel(writer, index=True, index_label='Index', sheet_name='Mark_Updated Data')

    # Notify the user
    print("Data has been merged and written to 'output_file.xlsx'.")
    


# Function to plot and save a single stock chart
def plot_save_chart(row):
    stock = row['symbol']
    Index = str(int(row['Index']))

    # Create the folder based on the pattern name if it doesn't exist
    folder_path = os.path.join(r"C:\Mark")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get the stock data file path
    stock_file = os.path.join(r"C:\data", stock + ".txt")

    # Load the stock data from the text file
    stock_data = pd.read_csv(stock_file, header=None, names=['symbol','Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    stock_data['Date'] = pd.to_datetime(stock_data['Date'], format='%Y%m%d')
    stock_data.set_index('Date', inplace=True)

    # Calculate EMAs
    stock_data['EMA_50'] = ta.EMA(stock_data['Close'], timeperiod=50)
    stock_data['EMA_150'] = ta.EMA(stock_data['Close'], timeperiod=150)
    stock_data['EMA_200'] = ta.EMA(stock_data['Close'], timeperiod=200)

    # Get the start and end dates from the filtered dataframe
    stock_start_date = row['Plot Start']
    stock_end_date = row['Plot End']

    # Filter the stock data based on the specified date range
    stock_data = stock_data.loc[stock_start_date:stock_end_date]

    # Create the plots
    ema_50 = mpf.make_addplot(stock_data['EMA_50'], color='blue')
    ema_150 = mpf.make_addplot(stock_data['EMA_150'], color='orange')
    ema_200 = mpf.make_addplot(stock_data['EMA_200'], color='red')

    # Plot the OHLC chart and get the axes object
    fig, axes = mpf.plot(stock_data, type='candle', volume=True, style='charles', figsize=(48, 22),
                         ylabel_lower='Volume', panel_ratios=(3, 1), title=stock, ylabel='Price',
                         addplot=[ema_50, ema_150, ema_200], returnfig=True)

    plt.grid(True, linestyle=':', linewidth=0.3, color='gray')

    # Convert dates to corresponding index values
    start_index = stock_data.index.get_loc(row['Mark'])

    # Mark the "Start" date with a blue marker
    axes[0].axvline(x=start_index, color='blue', linestyle=':')

    # Overlay fundamental data on the chart
    stock_fundamentals = row

    # Prepare the text to display
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
    DMA 50: {stock_fundamentals['DMA 50']}
    DMA 200: {stock_fundamentals['DMA 200']}
    """
    # Define font properties
    font_properties = {
        'family': 'monospace',
        'weight': 'bold',
        'size': 22
    }

    # Add the text to the chart
    plt.figtext(0.22, 0.60, text_str, fontdict=font_properties, color='blue', ha='left', bbox=dict(facecolor='pink', alpha=0.2))

    # Save the chart as an image in the corresponding folder
    image_name = Index + ' ' + stock + ' ' + '.png'
    image_path = os.path.join(folder_path, image_name)
    plt.savefig(image_path)

    plt.close()

# Main function to use multiprocessing
if __name__ == "__main__":
    # Load the data from the Excel file
    df = pd.read_excel("output_file_mark.xlsx", sheet_name='Mark_Updated Data')

    # Use multiprocessing pool to process in parallel
    with Pool(cpu_count()) as pool:
        pool.map(plot_save_chart, [row for _, row in df.iterrows()])

    print("Images exported successfully.")

    
    # Stop measuring execution time
    end_time = time.time()

    # Calculate and print the execution time
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

