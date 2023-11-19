import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Load data from the file
file_path = "C:/Users/05pat/OneDrive/Escritorio/OneDrive - University of Edinburgh/Year 4/Senior Honours/Python Files/Solar Flair/Flair data/X2.07_17_52_03_03_2023.txt"

with open(file_path, 'r') as file:
    lines = file.readlines()

# Initialize empty lists for data extraction
Time = []
Counts = []
StdDev = []

# Extract data from the file with error handling
for line in lines:
    parts = line.split(': ')
    if len(parts) >= 2:
        time_part = parts[0]
        data_part = parts[1]
        if data_part.startswith('Sum=') and 'StdDev=' in data_part:
            Time.append(time_part.strip())
            count_part = data_part.split(', ')[0]
            stddev_part = data_part.split(', ')[1]
            Counts.append(int(count_part.split('=')[1]))
            StdDev.append(float(stddev_part.split('=')[1]))

# Convert Time to datetime objects
time_objects = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S") for t in Time]

# Convert the marker timestamps to datetime objects


# Calculate the rolling mean with a window size (e.g., 10 data points)
window_size = 5
rolling_mean = np.convolve(Counts, np.ones(window_size) / window_size, mode='valid')

# Adjust the time objects to match the rolling mean size
time_objects = time_objects[window_size - 1::3]  # Select every other time object

# Convert the marker timestamp to a datetime object
marker_time = datetime.strptime("2023-03-03 17:52:00", "%Y-%m-%d %H:%M:%S")

# Calculate rolling standard deviation for error bars
rolling_stddev = np.array([np.std(Counts[i:i+window_size]) / np.sqrt(window_size) for i in range(len(Counts) - window_size + 1)])
rolling_stddev = rolling_stddev[::3]  # Select every other standard deviation value

# Select every other rolling mean value
rolling_mean = rolling_mean[::3]

# Plot the rolling mean with error bars for every other point
plt.errorbar(time_objects, rolling_mean, yerr=rolling_stddev, marker='o', color='b', label=f'Rolling Mean (Window={window_size})')

plt.axvline(x=marker_time, color='r', linestyle='--', label='X2.07 flair at 03/03/2023, 17:52')

# Formatting the plot
plt.xlabel('Date and Hour')
plt.ylabel('Average Counts [Arb. Units]')
plt.title(f'Average Muon counts over time with Rolling Mean and Error Bars (Window={window_size})')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.subplots_adjust(bottom=0.25)  # Add spacing at the bottom

# Customize x-axis date formatting to display only the date and hour
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:00'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))  # Adjust the interval as needed

# Show the plot
plt.show()
