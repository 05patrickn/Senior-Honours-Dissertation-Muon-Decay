import datetime
import time
import os
import numpy as np 

def process_file_paths(file_paths):
    # Initialize lists to store values and formatted UTC times
    values_list = []
    formatted_utc_times_list = []

    # Read the lines and extract timestamps
    for key, path in file_paths.items():
        with open(path, 'r') as file:
            lines = file.readlines()

            # Extract timestamps and find the closest mark to start from
            timestamps = [datetime.datetime.utcfromtimestamp(int(timestamp)) for value, timestamp in (entry.strip().split() for entry in lines) if value.startswith("400")]
            closest_mark = None
            for timestamp in timestamps:
                minute = timestamp.minute
                if minute in {10, 25, 40, 55}:
                    closest_mark = timestamp
                    break
            
            if closest_mark is not None:
                start_time = closest_mark
                break

    # Process the lines based on the start time
    for key, path in file_paths.items():
        with open(path, 'r') as file:
            lines = file.readlines()
            for entry in lines:
                value, timestamp = entry.strip().split()
                if value.startswith("400"):
                    timestamp = int(timestamp)
                    utc_time = datetime.datetime.utcfromtimestamp(timestamp)

                    # Check if the entry is after the start time
                    if utc_time >= start_time:
                        formatted_utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
                        formatted_utc_times_list.append(formatted_utc_time)
                        values_list.append(value[-2:])

    return values_list, formatted_utc_times_list

data_files = [
    ("13-10-11-12-38.data", "25/10/2013, 15:03, X2.1"),
    ("13-10-25-17-00.data", "28/10/2013, 02:03, X1"),
    ("21-06-28-15-49.data", "03/07/2021, 14:29, X1.59"),
    ("21-10-20-16-09(Week3).data", "28/10/2021, 15:35, X1"),
    ("22-03-23-13-06.data", "30/03/2022, 17:37, X1.3"),
    ("23-01-09-10-46.data", "10/01/2023, 22:47, X1"),
    ("23-02-06-12-57.data", "11/02/2023, 15:48, X1.1"),
    ("23-02-15-12-28.data", "17/02/2023, 20:16, X2.2"),
    ("23-02-28-13-15.data", "03/03/2023, 17:52, X2.07"),
    ("findtheflare.data", "03/07/2021, 14:29, X1.59"),
]


# Define the output directory
output_directory = r'C:/Users/05pat/OneDrive/Escritorio/OneDrive - University of Edinburgh/Year 4/Senior Honours/Senior-Honours-Muon-Decay-GitHub/Python Files/Solar Flare Experiment/Processed Data (5min chunk)'

for data_file, info in data_files:
    file_paths = {"1": data_file}
    decays, time_decay = process_file_paths(file_paths)

    # Convert decay values to integers
    decays = [int(x) for x in decays]

    # Chunk size
    chunk_size = 600  # 900 seconds in 15 min

    # Calculate the sum of decays in groups of 900
    sums_in_groups = [sum(decays[i:i + chunk_size]) for i in range(0, len(decays), chunk_size)]

    # Remove the last element from the list
    sums_in_groups = sums_in_groups[:-1]

    # Calculate the standard deviation in groups of 900
    std_in_groups = [np.std(decays[i:i + chunk_size]) for i in range(0, len(decays), chunk_size)]

    # Remove the last element from the list
    std_in_groups = std_in_groups[:-1]

    def generate_time_intervals(start_time_str, num_intervals, interval_minutes):
        # Convert start_time_str to a time object
        start_time = time.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')

        # Convert interval_minutes to seconds
        interval_seconds = interval_minutes * 60

        # Generate time intervals
        time_intervals = []
        current_time = start_time
        for i in range(num_intervals):
            # Convert current_time back to a formatted string
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
            time_intervals.append(formatted_time)

            # Increment current_time by the interval
            current_time = time.localtime(time.mktime(current_time) + interval_seconds)

        return time_intervals

    time_decay_start = time_decay[0]
    interval_minutes = chunk_size/60

    num_intervals = len(sums_in_groups)
    time_intervals = generate_time_intervals(time_decay_start, num_intervals, interval_minutes)
    
    # Replace slashes and colons with underscores in the output file name
    date_time = info.split(', ')[1].replace('/', '_').replace(':', '_')
    output_file_name = f"{info.split(', ')[2]}_{date_time}_{info.split(', ')[0].replace('/', '_').replace(':', '_')}.txt"  

    # Create the full path to the output file
    output_file_path = os.path.join(output_directory, output_file_name)

    # Combine time_intervals, sums_in_groups, and std_in_groups data
    output_data = [f"{time_interval}: Sum={sum_value}, StdDev={std_value}" for time_interval, sum_value, std_value in
                   zip(time_intervals, sums_in_groups, std_in_groups)]

    # Open the output file for writing
    with open(output_file_path, 'w') as output_file:
        # Write the data to the file
        output_file.write('\n'.join(output_data))

    # Confirm that the data has been written to the file
    print(f"Data has been saved to {output_file_path}")

