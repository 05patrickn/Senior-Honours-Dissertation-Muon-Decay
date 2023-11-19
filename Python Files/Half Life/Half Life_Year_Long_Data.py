import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Define the file paths and associated voltage values
file_paths = {
    "Final": "C:/Users/05pat/OneDrive/Escritorio/OneDrive - University of Edinburgh/Year 4/Senior Honours/Raw Data/year.data"
    # You can add more file paths here if needed
}

# Initialize a list to store data points with values within the specified decay time range
data_points = []

min_decay_time_ns = 800
max_decay_time_ns = 20000
bins = 160  # FIXME 500 bins?

# Iterate through the file paths and read the data
for key, file_path in file_paths.items():
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into decay time and other information
            decay_time_ns, _ = line.strip().split()
            # Convert decay time to integer
            decay_time_ns = int(decay_time_ns)

            # Check if the decay time is within the specified range
            if min_decay_time_ns <= decay_time_ns <= max_decay_time_ns:
                data_points.append(decay_time_ns)

# Convert data points from nanoseconds to microseconds
data_points_microseconds = np.array(data_points) / 1000.0

# Assume sorted_data_points is the sorted array of data points in microseconds
sorted_data_points = np.sort(data_points_microseconds)

# Compute the histogram with specified number of bins
hist, bin_edges = np.histogram(sorted_data_points, bins)

# Define the exponential decay model function
def exponential_decay(t, N0, tau, background):
    return N0 * np.exp(-t / tau) + background

# Fit the decay constant (tau) using curve_fit
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Set the bounds for the parameters (tau between 1.5 and 2.5)
bounds = ([0, 2.0, 0], [100000, 2.15, 200])

params, covariance = curve_fit(exponential_decay, bin_centers, hist, bounds=bounds)

# Extract the decay constant (tau) from the fit parameters
tau = params[1]
N0 = params[0]
background = params[2]

print(f"Half Life: {tau:.7f} microseconds")
print(f"Background: {background:.2f} counts")
print(f"N0: {N0:.2f} counts")

# Plot the scatter graph with bins
#plt.scatter(bin_centers, hist, marker='.', color='blue', label=f'Data with {bins} bins')

# Calculate expected values from the exponential decay model
expected_values = exponential_decay(bin_centers, *params)

# Calculate chi-squared
chi_squared = np.sum((hist - expected_values) ** 2 / expected_values)

# Calculate uncertainties
uncertainties = np.sqrt(np.diag(covariance))

print(f"Chi-squared: {chi_squared:.2f}")
print(f"Uncertainties (N0, tau, background): {uncertainties}")

# Add error bars to the scatter plot
plt.errorbar(bin_centers, hist, yerr=np.sqrt(hist), fmt='none', ecolor='black', capsize=2, elinewidth=0.8, capthick=0.8, label=f'{bins} bins with uncertainties')

# Plot the fitted curve with uncertainties
plt.fill_between(bin_centers, exponential_decay(bin_centers, *(params - uncertainties)), exponential_decay(bin_centers, *(params + uncertainties)), color='black', alpha=0.3)
plt.plot(bin_centers, exponential_decay(bin_centers, *params), color='black', label=f'Exponential Fit (τ ≈ {tau:.3f} ± {uncertainties[1]:.3f} microseconds)')

plt.xlabel('Time [microseconds]')
plt.ylabel('Counts')
plt.title('Observed decay times for Muons: 30,000 decay events.')
plt.grid(True)
plt.legend()

plt.show()

