import csv
from datetime import datetime

# Initialize lists to store data
formatted_utc_times_list = []
pressure_list = []

# Read the data from the CSV file
file_path = "preassure data.csv"

with open(file_path, 'r') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)

    # Skip the header if any
    next(csv_reader)

    # Iterate through the rows and extract data
    for row in csv_reader:
        # Parse the date/time and pressure from the row
        utc_datetime = datetime.strptime(row[0], '%d/%m/%Y %H:%M')
        formatted_utc_time = utc_datetime.strftime('%Y-%m-%d %H:%M:%S')
        pressure = float(row[1])

        # Append to the respective lists
        formatted_utc_times_list.append(formatted_utc_time)
        pressure_list.append(pressure)


# Define the start and end datetime for the range
start_datetime = datetime.strptime('2023-08-28 12:25:00', '%Y-%m-%d %H:%M:%S')
end_datetime = datetime.strptime('2023-09-22 13:10:00', '%Y-%m-%d %H:%M:%S')

# Filter the pressure values within the specified range
filtered_pressure_list = []
for i in range(len(formatted_utc_times_list)):
    utc_datetime = datetime.strptime(formatted_utc_times_list[i], '%Y-%m-%d %H:%M:%S')
    if start_datetime <= utc_datetime <= end_datetime:
        filtered_pressure_list.append(pressure_list[i])

# Print the filtered pressure values
print(filtered_pressure_list)
