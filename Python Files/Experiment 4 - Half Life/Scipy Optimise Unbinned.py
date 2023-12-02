import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import math

# Define the file paths and associated voltage values
file_paths = {
    "Final": "C:/Users/05pat/OneDrive/Escritorio/OneDrive - University of Edinburgh/Year 4/Senior Honours/Senior-Honours-Muon-Decay-GitHub/Raw Data/year.data"
    # You can add more file paths here if needed
}

# Initialize a list to store data points with values within the specified decay time range
data_points = []

min_decay_time_ns = 1400
max_decay_time_ns = 20000

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

# Sort the data points
sorted_data_points = np.sort(data_points_microseconds)

def exponential_decay(x, A, tau,a, m, C):
    return A * np.exp(-x / tau)+m*x+ C

initial_params = [21206, 2.12,2, 0.01, 1000]

# Data
sorted_data_points = np.sort(data_points_microseconds)[::-1]

unique_elements, counts = np.unique(data_points, return_counts=True)

y_data = counts
x_data = np.unique(sorted_data_points)



# Use curve_fit to find the best-fit parameters
params, params_covariance = curve_fit(exponential_decay, x_data, y_data, p0=initial_params)

# Extract the fitted parameters
A_fit, tau_fit,a_fit, m_fit, C_fit = params


print("Fitted Parameters:")
print(f"A = {A_fit:.3f}")
print(f"τ = {tau_fit:.5f}")
print(f"m = {m_fit:.3f}")
print(f"C = {C_fit:.3f}")

# Generate the fitted curve
fitted_curve = exponential_decay(x_data, A_fit, tau_fit,a_fit, m_fit, C_fit)

# Calculate the chi-squared value
chi_squared = np.sum(((y_data - fitted_curve) ** 2) / fitted_curve)

print(f"Chi-Squared: {chi_squared:.3f}")



################### Residuals ###################################
residuals = y_data - fitted_curve


bins = 30

# Calculate residuals
residuals = y_data - fitted_curve

# Reshape the array to have 'bins' columns
binned_data_y = residuals.reshape(-1, bins)

# Calculate the mean and standard deviation along axis 1 (rows)
binned_means_y = np.mean(binned_data_y, axis=1)
binned_stdev_y = np.std(binned_data_y, axis=1, ddof=1)  # ddof=1 for sample standard deviation

# Reshape the array to have 'bins' columns
binned_data_x = x_data.reshape(-1, bins)

# Calculate the mean along axis 1 (rows)
binned_means_x = np.mean(binned_data_x, axis=1)


# Plot the original data and the fitted curve
plt.figure(figsize=(12, 4))  # Increase the figure width to accommodate both plots side by side

# Subplot for the original data and fitted curve
plt.subplot(1, 2, 1)
plt.scatter(x_data, y_data, label='Data', color='black', marker='.')
plt.plot(x_data, fitted_curve, label=f'Scipy_Optimise Half-life = {tau_fit:.3f} μs', color='r')
plt.legend()
plt.xlabel('Decay Time (μs)')
plt.ylabel('Counts [Arb. Units]')
plt.title('Muon Half Life decay curve for year-long measurement')

# Subplot for the residuals
plt.subplot(1, 2, 2)
plt.errorbar(binned_means_x, binned_means_y, yerr=binned_stdev_y, fmt='.', label='Residuals', color='black', capsize=2, elinewidth=0.8, capthick=0.8)
plt.axhline(y=0, color='r', linestyle='--', label='Zero Residuals')
plt.legend()
plt.xlabel('Decay Time (μs)')
plt.ylabel('Counts Residuals [Arb. Units]')
plt.title('Residuals of Muon Half Life Decay Fit (bin_size=30)')


plt.tight_layout()  # Adjust layout for better spacing
plt.show()

