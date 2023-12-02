import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Load data from the file
file_path = "X1.3_17_37_30_03_2022.txt"

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

marker_time_1 = datetime(2022, 3, 30, 17, 37)


# Calculate the rolling mean with a window size (e.g., 10 data points)
window_size = 20
rolling_mean = np.convolve(Counts, np.ones(window_size) / window_size, mode='valid')

# Adjust the time objects to match the rolling mean size
time_objects = time_objects[window_size - 1::5]  # Select every other time object

# Calculate rolling standard deviation for error bars
rolling_stddev = np.array([np.std(Counts[i:i+window_size]) / np.sqrt(window_size) for i in range(len(Counts) - window_size + 1)])
rolling_stddev = rolling_stddev[::5]  # Select every other standard deviation value

# Select every other rolling mean value
rolling_mean = rolling_mean[::5]

# Plot the rolling mean with error bars for every other point
plt.errorbar(time_objects, rolling_mean, yerr=rolling_stddev, marker='.',capsize=2, elinewidth=0.8, capthick=0.8, color='black', label=f'Rolling Mean (Window={window_size})')

plt.axvline(x=marker_time_1, color='r', linestyle='--', label='X1.3 flare at 30/03/2022 17:37')

# Formatting the plot
plt.xlabel('Date and Hour')
plt.ylabel('Mean Counts')
plt.title(f'Rolling mean Muon counts (Window={window_size}) during solar flares')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.subplots_adjust(bottom=0.25)  # Add spacing at the bottom

# Customize x-axis date formatting to display only the date and hour
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %Hh'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=24))  # Adjust the interval as needed

# Show the plot
plt.show()
