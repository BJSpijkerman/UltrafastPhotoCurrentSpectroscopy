import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("../MaterialData/heat_cap.dat", sep=r"\s+", names=["Te", "Ce"])

Te = df["Te"].to_numpy() * 1e4
Ce = df["Ce"].to_numpy() * 1e5

#Sommerfeld expansion approximation
gamma = 70
T = np.linspace(300, 3000, 10*4)
C = gamma * T

fig = plt.figure(figsize=(9, 5))
ax = fig.add_subplot()
ax.grid()
ax.plot(Te, Ce, label="DFT data")
ax.plot(T, C, label="Sommerfeld expansion")
ax.set_xlabel("Temperature [K]")
ax.set_ylabel("Heatcapacity $C_e$ [J/m$^3$K]")
ax.set_xlim([300, 3000])
ax.set_ylim([0, 2.5*10**5])
ax.legend()

fig.tight_layout()
plt.show()
