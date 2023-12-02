import math
# Define the data and uncertainties
carbon_muon_halflife = [2020, 2043, 2041, 2040, 2025, 2035, 2060, 2030, 2040, 2029, 2026.3, 2045, 2029]
carbon_muon_halflife_uncertainty = [20, 35, 30, 4, 8, 30, 1.6, 10, 3, 1.5, 2, 3]

# Calculate the inverse squares of the uncertainties
uncertainty_inverse_squares = [1 / (uncertainty ** 2) for uncertainty in carbon_muon_halflife_uncertainty]

# Calculate the weighted values for each data point
weighted_values = [value / (uncertainty ** 2) for value, uncertainty in zip(carbon_muon_halflife, carbon_muon_halflife_uncertainty)]

# Calculate the sum of the weighted values
sum_weighted_values = sum(weighted_values)

# Calculate the sum of the weights (inverse squares of uncertainties)
sum_weights = sum(uncertainty_inverse_squares)

# Calculate the weighted mean half-life
weighted_mean_half_life = sum_weighted_values / sum_weights

# Print the result
print("Weighted Mean Carbon Muon Half-life:", weighted_mean_half_life, "ns")

# Calculate the weighted uncertainty
weighted_uncertainty = 1 / math.sqrt(sum_weights)

# Print the result
print("Weighted Uncertainty for Mean Carbon Muon Half-life:", weighted_uncertainty, "ns")