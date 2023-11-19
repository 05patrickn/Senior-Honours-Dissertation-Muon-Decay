import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Load data from the file
file_path = "C:/Users/05pat/OneDrive/Escritorio/OneDrive - University of Edinburgh/Year 4/Senior Honours/Python Files/Solar Flair/Flair data/NOFLAIR_02_03_22_09_2023.txt"

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

"""
# Convert the marker timestamps to datetime objects
marker_time_1 = datetime(2013, 10, 28, 2, 12)
marker_time_2 = datetime(2013, 11, 5, 22, 12)
marker_time_3 = datetime(2013, 10, 25, 15, 12)
marker_time_4 = datetime(2013, 10, 25, 8, 1)
marker_time_5 = datetime(2013, 11, 8, 4, 26)
marker_time_6 = datetime(2013, 10, 28, 2, 12)
marker_time_7 = datetime(2013, 11, 1, 19, 53)
marker_time_8 = datetime(2013, 10, 29, 21, 54)
"""
# Calculate the rolling mean with a window size (e.g., 10 data points)
window_size = 5
rolling_mean = np.convolve(Counts, np.ones(window_size) / window_size, mode='valid')

# Adjust the time objects to match the rolling mean size
time_objects = time_objects[window_size - 1::6]  # Select every other time object

# Calculate rolling standard deviation for error bars
rolling_stddev = np.array([np.std(Counts[i:i+window_size]) / np.sqrt(window_size) for i in range(len(Counts) - window_size + 1)])
rolling_stddev = rolling_stddev[::6]  # Select every other standard deviation value

# Select every other rolling mean value
rolling_mean = rolling_mean[::6]

# Plot the rolling mean with error bars for every other point
plt.errorbar(time_objects, rolling_mean, yerr=rolling_stddev, marker='.',capsize=2, elinewidth=0.8, capthick=0.8, color='black', label=f'Rolling Mean (Window={window_size})')

# Add vertical lines at the marker timestamps
#plt.axvline(x=marker_time_1, color='r', linestyle='--', label='X1 flare at 28/10/2013 02:12')
#plt.axvline(x=marker_time_2, color='orange', linestyle='--', label='X3.3 flare at 05/11/2013 22:12')
#plt.axvline(x=marker_time_3, color='y', linestyle='--', label='X2.1 flare at 25/10/2013 15:12')
#plt.axvline(x=marker_time_4, color='g', linestyle='--', label='X1.7 flare at 25/10/2013 08:01')
#plt.axvline(x=marker_time_5, color='green', linestyle='--', label='X1.1 flare at 08/11/2013 04:26')
#plt.axvline(x=marker_time_6, color='purple', linestyle='--', label='X1 flare at 28/10/2013 02:12')
#plt.axvline(x=marker_time_7, color='red', linestyle='--', label='M6.3 flare at 01/11/2013 19:53')
#plt.axvline(x=marker_time_8, color='red', linestyle='--', label='X2.3 flare at 29/10/2013 21:54')


# Formatting the plot
plt.xlabel('Date and Hour')
plt.ylabel('Mean Counts')
plt.title(f'Rolling Mean Muon counts (Window={window_size}) during no solar flares')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.subplots_adjust(bottom=0.25)  # Add spacing at the bottom

# Customize x-axis date formatting to display only the date and hour
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=24))  # Adjust the interval as needed

# Show the plot
plt.show()
