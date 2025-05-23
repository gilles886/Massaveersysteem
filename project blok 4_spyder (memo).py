# -*- coding: utf-8 -*-
"""
Created on Thu May 22 12:49:37 2025

@author: onnod
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Parameters van het systeem
m = 1       # massa, hoe kleiner des te lager de responstijd
k = 22.5       # veerconstante
c = 2*np.sqrt(m*k)     # kritische demping


# Inlezen van versnelling uit CSV
data = pd.read_csv('versnellingsprofiel_scherp.csv')  
tijd = data['# tijd (s)'].values
aandrijving = data[' versnelling (m/s^2)'].values
Nstap = len(tijd)
dt = tijd[1] - tijd[0]  # aangenomen dat tijdstappen gelijk zijn

# Voorgedefinieerde constanten
a = (k - 2 * m / dt**2) / (m / dt**2 + c / (2 * dt))
b = (m / dt**2 - c / (2 * dt)) / (m / dt**2 + c / (2 * dt))
F0e = m * aandrijving / (m / dt**2 + c / (2 * dt))  # omgerekende kracht

# Beginvoorwaarden
x0 = 0
v0 = 0

x = np.zeros(Nstap)
x[0] = x0
x[1] = x0 + dt * v0

# Numerieke oplossing met aangedreven kracht
for ti in range(1, Nstap - 1):
    x[ti + 1] = -a * x[ti] - b * x[ti - 1] + F0e[ti]

# Plot van positie in de tijd
plt.figure()
plt.plot(tijd, x)
plt.xlabel("Tijd (s)")
plt.ylabel("Positie (m)")
plt.title("Respons van de massa op versnellingsprofiel")
plt.grid()
plt.show()

#berekening van de versnelling uit de uitwijking van de veer
a_uit_veerpositie = (k * x) / m

#plot van de het versnellingsprofiel
plt.figure()
plt.plot(tijd, aandrijving, label="versnelling van versnellingsprofiel")
plt.plot(tijd, a_uit_veerpositie, label="Versnelling van massa uit veerpositie")
plt.title("versnellingsporfiel en berekende versnelling uit positie")
plt.ylabel("Versnelling m/s^2")
plt.xlabel("tijd (S)")
plt.grid()
plt.legend()
plt.show()

# Bepaal de responstijd als het tijdsverschil tussen de piek van de systeemrespons en de piek van de input (versnellingsprofiel)
responstijd = tijd[np.argmax(a_uit_veerpositie)] - tijd[np.argmax(aandrijving)]
print('Responstijd van het systeem:', responstijd, 's')

