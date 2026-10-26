import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('3tm_stage1_output.csv')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

# Carrier Density
ax1.plot(df['time_ps'], df['n_e_cm3'] / 1e21, 'r--', label=r'$n_e$')
ax1.set_ylabel(r'$n_e$ [$10^{21}$cm$^{-3}$]')
ax1.set_title('C++ 3TM Stage 1 Verification')
ax1.grid(True)
ax1.legend()

# Temperatures
ax2.plot(df['time_ps'], df['T_e_K'] , 'r--', label=r'$T_e$')
ax2.plot(df['time_ps'], df['T_h_K'] , 'g-', label=r'$T_h$')
ax2.plot(df['time_ps'], df['T_l_K'] , 'b-.', label=r'$T_l$')
ax2.set_xlabel('Time [ps]')
ax2.set_ylabel('Temperature [K]')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()

DICT = {
        "time_ps": df["time_ps"],
        "n_e": df["n_e_cm3"] / 1e21,
        "T_e": df["T_e_K"],
        "T_h": df["T_h_K"],
        "T_l": df["T_l_K"]
}

df = pd.DataFrame(DICT)
df.to_csv("data.csv")
