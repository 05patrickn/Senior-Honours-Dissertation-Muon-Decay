import numpy as np
import matplotlib.pyplot as plt

numbers = np.array([1.040e0, 1.870e0, 3.453e0, 6.827e0, 1.092e1, 3.180e1, 4.384e1, 6.951e1, 1.099e2, 1.787e2, 2.473e2])
energy = np.array([10, 14, 20, 30, 40, 80, 100, 140, 200, 300, 400, 800])
momentum = np.array([4.704e1, 5.616e1, 6.802e1, 8.509e1, 1.003e2, 1.527e2, 1.764e2, 2.218e2, 2.868e2, 3.917e2, 4.945e2])

# Divide each number by 7.874 using NumPy
result = numbers / 7.874

x = np.arange(1, 12, 1)
depths = [0.13208026, 0.23749047, 0.43853188, 0.86703073, 1.38684277, 4.03860808, 5.56769114, 8.82778766, 13.95732791, 22.69494539, 31.40716281]

counts_corr = np.array([89, 14, 33, 41, 47])


plt.plot(depths, momentum)
plt.xlabel('Depth [cm]')
plt.ylabel('Momentum [MeV/c]')
plt.title('Depth vs Momentum')
plt.grid(True)
plt.show()



# Calculate the error using the square root of counts
error = np.sqrt(counts_corr)

# Convert momentum_muon from MeV/c to GeV/c
momentum_muon = np.array([167.6, 236.6, 299.3, 359.4, 418.9]) / 1000

plt.figure(figsize=(8, 4))
# Create another plot for momentum_muon vs counts with error bars and logarithmic scale
plt.errorbar(momentum_muon, counts_corr, yerr=error, marker='o', linestyle='-', color='black', capsize=2, elinewidth=0.8, capthick=0.8)
plt.xscale('log')  # Set x-axis to logarithmic scale
plt.xlabel('Muon Momentum [GeV/c]')
plt.ylabel('Differential Counts')
plt.title('Muon Momentum vs Counts (Logarithmic Scale)')
plt.grid(True)
plt.show()

print(result)
