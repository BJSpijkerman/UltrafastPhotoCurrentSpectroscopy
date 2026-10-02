import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("simulation/build/output.dat", sep=r"\s+", names=["t", "Te", "Tl"])

# Convert time to picoseconds upfront
df["t_ps"] = df["t"] * 1e12

c		= 299792458					# Speed of light [m/s]
LAMBDA	= 800 * 10**(-9)			# Wavelength of absorbed light 800 nm [m]
omega	= 2 * np.pi * c / LAMBDA	# Angular frequency of absorbed light [Rad/s]
e		= 1.60217663 * 10**(-19)	# Electron charge [C]
n_sp	= 5.9 * 10**(28)			# sp-electron number density [m^-3]
m_sp	= 9.1093837 * 10**(-31)		# Free electron mass taken as band mass due to sp-electrons being nearly free [kg]
nu_cold = 0.084 * 10**(+15)			# Electron-ion scattering rate at 300K [1/s]
A		= nu_cold / 300				# Electron-ion scattering coefficient [1/sK]
nu_T	= A * df["Tl"]				# Scattering rate dependent on lattice temperature [s^-1]
sigma = (e**2 * n_sp / m_sp) * nu_T / (nu_T**2)
sigma_0 = (e**2 * n_sp / m_sp) * nu_cold / nu_cold**2

rho = 1 / sigma
rho_0 = 1 / sigma_0


fig = plt.figure(figsize=(9, 5))
ax = fig.add_subplot()
ax.grid(True)

# Main plots
ax.plot(df["t_ps"], df["Te"], color="r", label="Te")
ax.plot(df["t_ps"], df["Tl"], color="b", label="Tl")
ax.set_xlabel("Time [ps]")
ax.set_ylabel("Temperature [K]")
ax.set_xlim([0, 50])
ax.legend(loc="upper left")

# 1. Create inset axes [x, y, width, height] in relative coordinates (0 to 1)
# Positioned at top-right (x=0.55, y=0.45) with 40% width and 45% height
ax_inset = ax.inset_axes([0.55, 0.45, 0.4, 0.45])
ax_inset.grid(True)

# 2. Plot the same data inside the inset
ax_inset.plot(df["t_ps"], df["Te"], color="r")
ax_inset.plot(df["t_ps"], df["Tl"], color="b")

# 3. Set limits for the zoomed region (adjust these to your region of interest)
ax_inset.set_xlim([1, 10])       # Example: zoom in on the first 5 ps
ax_inset.set_ylim([295, 310])   # Example: zoom in on the temperature peak/crossover

# 4. Optional: Add indicator lines pointing from the main axes to the inset box
ax.indicate_inset_zoom(ax_inset, edgecolor="gray")

fig.tight_layout()


fig_sigma = plt.figure(figsize=(9,5))
ax_s = fig_sigma.add_subplot()
ax_s.grid()
ax_s.plot(df["t_ps"], rho)
ax_s.set_xlabel("Time [ps]")
ax_s.set_ylabel("Resistivity [$\Omega$/m]")

fig_sigma.tight_layout()
plt.show()
