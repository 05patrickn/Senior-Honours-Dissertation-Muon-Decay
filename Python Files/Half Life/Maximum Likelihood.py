import matplotlib.pyplot as plt
import numpy as np
from iminuit import Minuit
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore")

from scipy.integrate import quad

# Define the exponential decay function
def exponential_decay(x, A, tau, m, C):
    return A * np.exp(-x / tau) + m * x + C

# Define the negative log-likelihood function for Minuit
def neg_log_likelihood(x, A, tau, m, C):
    # Define the integrand
    integrand = lambda x: exponential_decay(x, A, tau, m, C)

    # Integrate the original function over the entire range
    integral, _ = quad(integrand, min_decay_time_ns, max_decay_time_ns)

    # Normalize the function
    pdf = lambda x: exponential_decay(x, A, tau, m, C) / integral

    return pdf(x)

# Define the file paths and associated voltage values
file_paths = {
    "Final": "C:/Users/05pat/OneDrive/Escritorio/OneDrive - University of Edinburgh/Year 4/Senior Honours/Raw Data/year.data"
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

# Data
sorted_data_points = np.sort(data_points_microseconds)[::-1]
y_data = np.arange(len(sorted_data_points))
x_data = np.array(sorted_data_points)

# Initial parameter values
initial_params =  [0,366479, 2.11255,-273.210, 5401.699]

# Use Minuit to find the best-fit parameters
minuit = Minuit(neg_log_likelihood, x=initial_params[0], A=initial_params[1], tau=initial_params[2], m=initial_params[3], C=initial_params[4])

minuit.migrad()

# Extract the fitted parameters
A_fit, tau_fit, m_fit, C_fit = minuit.values['A'], minuit.values['tau'], minuit.values['m'], minuit.values['C']

print("Fitted Parameters:")
print(f"A = {A_fit:.3f}")
print(f"τ = {tau_fit:.5f}")
print(f"m = {m_fit:.3f}")
print(f"C = {C_fit:.3f}")

# Generate the fitted curve
fitted_curve = exponential_decay(x_data, A_fit, tau_fit, m_fit, C_fit)



# Plot the original data and the fitted curve
plt.figure(figsize=(8, 6))
plt.scatter(x_data, y_data, label='Data', color='black', marker='.')
plt.plot(x_data, fitted_curve, label=f'Minuit Maximum Likelihood Half-life = {tau_fit:.3f} μs', color='r')
plt.legend()
plt.xlabel('Decay Time (μs)')
plt.ylabel('Counts [Arb. Units]')
plt.title('Muon Half Life decay curve for year-long measurement')
plt.show()

# Calculate and plot the residuals
residuals = y_data - fitted_curve
plt.figure(figsize=(8, 6))
plt.scatter(x_data, residuals, label='Residuals', color='black', marker='.')
plt.axhline(y=0, color='r', linestyle='--', label='Zero Residuals')
plt.legend()
plt.xlabel('Decay Time (μs)')
plt.ylabel('Residuals')
plt.title('Residuals of Muon Half Life Decay Fit')
plt.show()
