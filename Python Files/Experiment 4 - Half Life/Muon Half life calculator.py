def calculate_Tneg(Tobs, Tneg, p):
    Tpos=(Tneg*Tobs*p)/((Tneg*p)+Tneg-Tobs)
#    Tpos=-(Tneg*Tobs*p)/(Tobs-Tneg-(Tneg*p))
    return Tpos

# Given values
Tobs = 2.113
Tneg = 2.0398 #(https://en.wikipedia.org/wiki/Muon) https://122.physics.ucdavis.edu/course/cosmology/sites/default/files/files/Muon%20Lifetime/muon-nuc-capture.pdf
p = 1.2766 #https://www.sciencedirect.com/science/article/pii/S0370269310008725

# Calculate Tneg
Tpos = calculate_Tneg(Tobs, Tneg, p)

# Print the result
print(f"Tpos: {Tpos:.6f}")
