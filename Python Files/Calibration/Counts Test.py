import matplotlib.pyplot as plt
from datetime import datetime, timezone

# Define the file paths and associated voltage values
file_paths = {
    "673.5V": "23-09-26-11-04-final.data"
}

# Choose a data file to plot
selected_file = "673.5V"  # Choose the desired data file

# Get the file path for the selected data file
selected_file_path = file_paths[selected_file]

# Initialize lists to store data points, counts, and times
data_points = []
counts = []
times = []

# Read the data and aggregate counts in 20000 data point intervals
interval = 10000
total_decays = 0
data_points_read = 0
current_time = 0  # Assuming time starts at 0 and increments with each data point
time_increment = 1  # Adjust this based on your actual time increments

with open(selected_file_path, 'r') as file:
    for line in file:
        # Check if we've reached the interval
        if data_points_read >= interval:
            data_points.append(data_points_read)  # Append the data points read so far
            counts.append(total_decays)
            
            # Convert Unix timestamp to UTC
            utc_time = datetime.utcfromtimestamp(current_time)
            times.append(utc_time)
            
            total_decays = 0
            data_points_read = 0

        count, _ = line.strip().split()
        if count.startswith("400"):
            last_two_digits = int(count[-2:])
            total_decays += last_two_digits

        data_points_read += 1
        current_time += time_increment

# Plot time versus counts
plt.figure(figsize=(10, 6))
plt.plot(times, counts, marker='o', linestyle='-')
plt.xlabel('Time [UTC]')
plt.ylabel('Number of Counts')
plt.title('Number of Decays over Time')
plt.grid(True)
plt.show()
