import datetime
from collections import defaultdict
import time

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

# Example usage
file_paths = {
    "Pat": "23-02-28-13-15.data"
}

decays, time_decay = process_file_paths(file_paths)

# Print the lists
#print("decays:", decays)
#print("time_decay:",time_decay[0])


# Convert decay values to integers
decays = [int(x) for x in decays]

# Chunk size
chunk_size = 900 #900 seconds in 15 min interval

# Calculate the sum of decays in groups of 900
sums_in_groups = [sum(decays[i:i+chunk_size]) for i in range(0, len(decays), chunk_size)]

# Remove the last element from the list
sums_in_groups = sums_in_groups[:-1]





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

# Example usage
time_decay_start = time_decay[0]
interval_minutes = 15

# Assuming num_intervals is already defined
num_intervals = len(sums_in_groups)
# Generate 15-minute time intervals
time_intervals = generate_time_intervals(time_decay_start, num_intervals, interval_minutes)




print(time_intervals)
print(sums_in_groups)



