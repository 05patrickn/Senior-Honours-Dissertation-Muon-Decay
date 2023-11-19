import matplotlib.pyplot as plt

# Define the file paths and associated voltage values
file_paths = {
    "673.5V-Mat": "23-08-28-13-23-Mat Raw Data.data"
}

# Choose a data file to plot
selected_file = "673.5V-Mat"  # Choose the desired data file

# Get the file path for the selected data file
selected_file_path = file_paths[selected_file]

# Initialize lists to store data points and counts
data_points = []
counts = []

# Read the data and aggregate counts in 20000 data point intervals
interval = 1000
total_decays = 0
data_points_read = 0
with open(selected_file_path, 'r') as file:
    for line in file:
        # Check if we've reached the interval
        if data_points_read >= interval:
            data_points.append(data_points_read)  # Append the data points read so far
            counts.append(total_decays)
            total_decays = 0
            data_points_read = 0
        
        count, _ = line.strip().split()
        if count.startswith("400"):
            last_two_digits = int(count[-2:])
            total_decays += last_two_digits
        
        data_points_read += 1

# Plot the number of decays in 20000 data point intervals
plt.figure(figsize=(10, 6))
plt.bar(data_points, counts, width=10, align='edge')  # Adjusted width and alignment
plt.xlabel('Data Point Interval')
plt.ylabel('Number of Decays')
plt.title('Number of Decays in 20000 Data Point Intervals')
plt.grid(axis='y')
plt.show()
