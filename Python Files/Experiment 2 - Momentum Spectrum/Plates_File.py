import matplotlib.pyplot as plt
import numpy as np

# Define the file paths and associated voltage values
file_paths = [
    "23-10-31-12-37.data",
    "23-10-31-12-49.data",
    "23-10-31-13-03.data",
    "23-10-31-13-17.data",
    "23-10-31-13-29.data",
    "23-10-31-13-41.data"
]

# Initialize lists to store total counts and errors
total_counts = []
errors = []
number_plates = np.arange(0, 60, 10)

# Define the number of data points to read
num_data_points_to_read = 600

# Loop through the file paths and calculate the total counts in each file
for selected_file in file_paths:
    # Get the file path for the selected data file
    selected_file_path = selected_file

    # Initialize variables to store the total count and squared sum of counts for the current file
    total_count = 0
    squared_sum_counts = 0

    # Read the data and calculate the total count for the first 600 data points
    data_points_read = 0
    good_data_points_read = 0
    with open(selected_file_path, 'r') as file:
        for line in file:
            if good_data_points_read >= num_data_points_to_read:
                break  # Stop reading after 600 data points

            count, _ = line.strip().split()
            if count.startswith("400"):
                last_two_digits = int(count[-2:])
                total_count += last_two_digits
                
                good_data_points_read += 1
            data_points_read += 1



    # Append the total count
    total_counts.append(total_count)
    error=np.sqrt(total_counts)
# Plot the total number of counts in each file for the first 600 data points with error bars
print (error)
bar_width = 5  # Adjust the width of the bars
plt.figure(figsize=(10, 6))
plt.bar(number_plates, total_counts, width=bar_width,yerr=error, color='black', capsize=5)
plt.xlabel('Number of Steel Plates')
plt.ylabel('Total Number of Counts')
plt.title('Total Counts Vs Number of plates with Error Bars')
plt.grid(axis='y')
plt.show()
