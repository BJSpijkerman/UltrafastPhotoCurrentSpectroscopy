import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("gold_ttm_results.csv")
print(df.columns)

fig = plt.figure(figsize=(9, 5))
ax = fig.add_subplot()
ax.plot(df["Time_ps"], df["Te_K"])
ax.plot(df["Time_ps"], df["Tl_K"])
fig.tight_layout()
plt.show()
