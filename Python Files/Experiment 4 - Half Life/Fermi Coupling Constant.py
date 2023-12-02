import numpy as np

# Given values
tau_plus = 2.174e-6  # in seconds
tau_plus_uncertainty = 0.005e-6
hbar = 6.582e-25  # GeV.s
m = 0.10566  # tau mass in GeV
c = 1  # speed of light

# Calculate Fermi coupling constant
GF = np.sqrt((192 * np.pi**3 * hbar) / (tau_plus * m**5 * c**4))

# Calculate uncertainty
delta_GF = GF * np.sqrt((tau_plus_uncertainty / tau_plus)**2)

print(f"Fermi coupling constant (GF): {GF} GeV^-5")
print(f"Uncertainty in GF: {delta_GF} GeV^-5")
