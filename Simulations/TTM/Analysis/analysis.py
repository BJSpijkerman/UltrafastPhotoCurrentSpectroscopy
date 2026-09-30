import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

# 1. Load data and group into a list of 2D arrays
df = pd.read_csv("simulation/build/output.dat", sep=r"\s+", names=["t", "Dt", "Te", "Tl"])
dt_groups = [group.to_numpy() for _, group in df.groupby("Dt")]

# Unit Conversion Factor (e.g., seconds to picoseconds)
# Change to 1e3 if original 't' is in nanoseconds, or 1e-3 if in femtoseconds
TIME_FACTOR = 1e12

# 2. Set up figure and plot lines
fig, ax = plt.subplots(figsize=(8, 5))
(line_te,) = ax.plot([], [], label=r"$T_e$", color="crimson", lw=2)
(line_tl,) = ax.plot([], [], label=r"$T_l$", color="dodgerblue", lw=2)

# Update axis label to reflect picoseconds
ax.set_xlabel("Time (ps)")
ax.set_ylabel("Temperature")
ax.legend(loc="upper right")
ax.grid(True, linestyle="--", alpha=0.6)

# Convert global x-axis limits to ps
ax.set_xlim(df["t"].min() * TIME_FACTOR, df["t"].max() * TIME_FACTOR)
ax.set_ylim(
    min(df["Te"].min(), df["Tl"].min()),
    max(df["Te"].max(), df["Tl"].max()) * 1.05,
)

title_text = ax.text(
    0.5,
    1.02,
    "",
    transform=ax.transAxes,
    ha="center",
    fontsize=12,
    fontweight="bold",
)


# 3. Update function
def update(frame_idx):
    current_data = dt_groups[frame_idx]

    # Convert t column to ps on the fly
    t_ps = current_data[:, 0] * TIME_FACTOR
    dt_val = current_data[0, 1]
    te = current_data[:, 2]
    tl = current_data[:, 3]

    # Update line data with converted time
    line_te.set_data(t_ps, te)
    line_tl.set_data(t_ps, tl)

    title_text.set_text(f"Temperature Evolution | $D_t$ = {dt_val:.2e}")

    return line_te, line_tl, title_text


# 4. Run animation
anim = FuncAnimation(
    fig, update, frames=len(dt_groups), interval=100, blit=False
)

plt.show()
