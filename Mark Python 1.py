import os
import pandas as pd
import numpy as np
import time

#PPP
# Set the directory where the data files are located
data_dir = "C:\\ExportedData"

# Set the output file path
output_file = "C:\\Program Files (x86)\\AmiBroker\\Data\\WatchLists\\Mark Python.tls"

# Start timer
start_time = time.time()

# Loop over all files in the directory
with open(output_file, "w") as f:
    for filename in os.listdir(data_dir):
        
        # Check that the file is a text file
        if filename.endswith(".txt"):
            
            # Get the symbol name from the file name
            symbol = filename.split(".")[0]
            
            # Load the data from the file into a DataFrame
            filepath = os.path.join(data_dir, filename)
            df = pd.read_csv(filepath, header=None, names=["Date", "Close"])
            df.set_index("Date", inplace=True)
            df.index = pd.to_datetime(df.index)
            
            # Calculate the EMA's
            ema_50 = df["Close"].ewm(span=50, adjust=False).mean()
            ema_150 = df["Close"].ewm(span=150, adjust=False).mean()
            ema_200 = df["Close"].ewm(span=200, adjust=False).mean()
            
            # Calculate the 52 week high and low
            high_52_week = df["Close"].rolling(window=252).max()
            low_52_week = df["Close"].rolling(window=252).min()
            
            # Calculate the 200 EMA change from 30 days ago
            if len(ema_200) >= 31:
                ema_200_last = ema_200.iloc[-1]
                ema_200_30_days_ago_last = ema_200.iloc[-31]
                ema_200_change = ema_200_last / ema_200_30_days_ago_last
            else:
                ema_200_last = np.nan
                ema_200_30_days_ago_last = np.nan
                ema_200_change = np.nan
            
            # Check if the conditions are met at the last date
            last_date = df.index[-1]
            close_last = df["Close"].iloc[-1]
            ema_50_last = ema_50.iloc[-1]
            ema_150_last = ema_150.iloc[-1]
            ema_200_last = ema_200.iloc[-1]
            high_52_week_last = high_52_week.iloc[-1]
            low_52_week_last = low_52_week.iloc[-1]
            if close_last > ema_50_last and close_last > ema_150_last and close_last > ema_200_last and \
               close_last >= 0.8 * high_52_week_last and close_last >= 0.5 * low_52_week_last and \
               ema_200_last > 1.05 * ema_200_30_days_ago_last:
                f.write(symbol + "\n")
    
# End timer
end_time = time.time()

# Calculate execution time
execution_time = end_time - start_time
print("Execution time: {} seconds".format(execution_time))

