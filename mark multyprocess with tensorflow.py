import os
import pandas as pd
import talib as ta
import time
from multiprocessing import Pool, freeze_support

# Path to the data directory
data_dir = 'C:/data1'

# List all the files in the data directory
files = os.listdir(data_dir)

# Create an empty DataFrame to store the results
results = pd.DataFrame(columns=['symbol', 'date', 'close', 'EMA_50', 'EMA_150', 'EMA_200', 'EMA_200_30', '52 week high', '52 week low', 'Mark','Down from 52w high'])

# Function to process each file
def process_file(file):
    # Check if the file is a text file
    if file.endswith('.txt'):
        # Read the file into a DataFrame, assuming no header row
        filepath = os.path.join(data_dir, file)
        df = pd.read_csv(filepath, header=None, names=['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'])

        # Calculate the moving averages
        df['EMA_50'] = ta.EMA(df['close'], timeperiod=50).round(2)
        df['EMA_150'] = ta.EMA(df['close'], timeperiod=150).round(2)
        df['EMA_200'] = ta.EMA(df['close'], timeperiod=200).round(2)

        # Obtain the 200-day EMA before 30 days
        df['EMA_200_30'] = df['EMA_200'].shift(30)

        # Calculate the 52-week high and low based on close values
        df['52 week high'] = ta.MAX(df['high'], timeperiod=252)
        df['52 week low'] = ta.MIN(df['low'], timeperiod=252)
        
        df['Down from 52w high'] = (((df['52 week high'] - df['close'])/df['52 week high'])*100).round(2)

        # Filter the DataFrame to get the last row
        last_row = df.iloc[[-1]]

        # Reverse the DataFrame to iterate from the last date
        reversed_df = df.iloc[::-1]

        # Find the date when the condition is first met starting from the last date and moving backwards
        first_match_date = ''
        for index, row in reversed_df.iterrows():
            if row['close'] > row['EMA_50'] > row['EMA_150'] > row['EMA_200']:
                first_match_date = row['date']
            else:
                break

        # Assign the first match date to the 'Mark' column
        last_row = df.iloc[[-1]].copy()
        last_row['Mark'] = first_match_date
        
        # Return the last row
        return last_row[['symbol', 'date', 'close', 'EMA_50', 'EMA_150', 'EMA_200', 'EMA_200_30', '52 week high', '52 week low', 'Mark','Down from 52w high']]

if __name__ == '__main__':
    # Start measuring execution time
    start_time = time.time()

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

    # Stop measuring execution time
    end_time = time.time()

    # Calculate and print the execution time
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    # Export the results to a CSV file
    results.to_csv('output.csv', index=False)
