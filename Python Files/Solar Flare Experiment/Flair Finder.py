import os
import pandas as pd
from datetime import datetime

# File path for the CSV containing dates and sizes
csv_file_path = r'C:\Users\05pat\OneDrive\Escritorio\OneDrive - University of Edinburgh\Year 4\Senior Honours\Important data\Solar Flair data.csv'

# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)

# Extract the dates and sizes from the DataFrame
dates = df['Date'].tolist()
sizes = df['Size'].tolist()
times = df['Time'].tolist()
unix_timestamps = []

for date_str in dates:
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    unix_timestamps.append(int(date_obj.timestamp()))

# Directory path for the ".data" files
directory = r'C:\Users\05pat\OneDrive\Escritorio\OneDrive - University of Edinburgh\Year 4\Senior Honours\extra muon data'

# List all files in the directory
file_list = os.listdir(directory)

# Iterate through each file in the directory
for filename in file_list:
    # Check if the file has the ".data" extension
    if filename.endswith('.data'):
        with open(os.path.join(directory, filename), 'r') as file:
            # Read and process the content of the data file line by line
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    timestamp = int(parts[1])
                    # Check if the timestamp matches any desired timestamp
                    if timestamp in unix_timestamps:
                        index = unix_timestamps.index(timestamp)
                        date_from_unix_timestamp = dates[index]
                        size_from_unix_timestamp = sizes[index]
                        time_from_unix_timestamp = times[index]
                        print(f'{filename}, {date_from_unix_timestamp}, {time_from_unix_timestamp}, {size_from_unix_timestamp}')
                        break  # Exit the loop when the timestamp is found

    # You can add more conditions for other file types as necessary

# Optionally, you can combine and analyze the data from the files as needed.
