import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("simulation/build/output.dat", sep=r"\s+", names=["t", "Te", "Tl"])

# Convert time to picoseconds upfront
df["t_ps"] = df["t"] * 1e12

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
plt.show()
