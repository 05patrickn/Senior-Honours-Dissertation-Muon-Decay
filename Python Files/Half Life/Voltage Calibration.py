import matplotlib.pyplot as plt

# Define the file paths and associated voltage values
file_paths = {
    "V600": "23-09-22-15-24.data",
    "V625": "23-09-22-15-18.data",
    "V650": "23-09-22-15-32.data",
    "V675": "23-09-22-15-38.data",
    "V700": "23-09-22-15-45.data",
    "V725": "23-09-22-15-50.data",
    "V750": "23-09-22-15-56.data",
    "V775": "23-09-22-16-02.data"
}

# Initialize lists to store voltage and counts
voltages = []
counts = []

# Set the maximum number of data points to read per file
max_data_points = 300

# Iterate through the file paths and read the first 300 data points
for key, file_path in file_paths.items():
    total_decays = 0
    data_points_read = 0
    
    with open(file_path, 'r') as file:
        for line in file:
            if data_points_read >= max_data_points:
                break
            
            count, _ = line.strip().split()
            if count.startswith("400"):
                last_two_digits = int(count[-2:])
                total_decays += last_two_digits
            
            data_points_read += 1

    # Extract voltage from the key (e.g., "V600" => voltage 600)
    voltage = int(key[1:])
    
    # Append the voltage and total decays to the lists
    voltages.append(voltage)
    counts.append(total_decays)

# Plot Voltage versus counts
plt.figure(figsize=(10, 6))
plt.plot(voltages, counts, marker='o')
plt.xlabel('Voltage [V]')
plt.ylabel('Moun Decay Counts')
plt.title('Detector Voltage Calibration: Voltage [V] vs Moun Decay Counts (300 timestamps = 5 minutes)')
plt.grid(True)
plt.show()
