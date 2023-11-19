import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Load data from the new file
file_path = "C:/Users/05pat/OneDrive/Escritorio/OneDrive - University of Edinburgh/Year 4/Senior Honours/Python Files/Solar Flair/Flair data/X1.1_15_48_11_02_2023.txt"

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

# Convert the marker timestamp to a datetime object
marker_time = datetime.strptime("2023-02-11 15:48:00", "%Y-%m-%d %H:%M:%S")

# Plot the counts over time in bins of 100
bin_size = 10
num_bins = len(time_objects) // bin_size

binned_time = [time_objects[i * bin_size:(i + 1) * bin_size] for i in range(num_bins)]
binned_counts = [sum(Counts[i * bin_size:(i + 1) * bin_size]) / bin_size for i in range(num_bins)]
binned_stddev = [np.std(Counts[i * bin_size:(i + 1) * bin_size]) / np.sqrt(bin_size) for i in range(num_bins)]

# Plot the binned counts over time with error bars
plt.errorbar([bin[-1] for bin in binned_time], binned_counts, yerr=binned_stddev, marker='o', color='b', label='Counts with Error Bars')

# Add a vertical line at the marker timestamp
plt.axvline(x=marker_time, color='r', linestyle='--', label='X1.1 flair at 11/02/2023, 15:48')

# Formatting the plot
plt.xlabel('Date')
plt.ylabel('Average Counts [Arb. Units]')
plt.title('Average Muon counts over time during X1.1 flair event on 11/02/2023, 15:48')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.subplots_adjust(bottom=0.25)  # Add spacing at the bottom

# Customize x-axis date formatting to display only the date and hour
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:00'))
# Set the minimum x-axis interval to 6 hours
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))

# Show the plot
plt.show()
