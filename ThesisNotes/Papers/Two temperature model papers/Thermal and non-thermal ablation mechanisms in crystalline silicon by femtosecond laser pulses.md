This paper investigates the spatial and temporal carrier-lattice dynamics during femtosecond laser ablation of silicone to determine ablation profiles and damage thresholds.

## Key Takaways
- <b>Research Objective</b>: To develop a 2D axisymmatric carrier density two-temperature model to simulate femtosecond laser-matter interactions in crystalline silicon and determine the optimal abaladion width and depth
- <b>Experimental Comparison</b>: The model's 2D thermal and non-thermal ablation predictions were compared with experimental results using single $180\,\text{fs}$ pulses ($\lambda=515\,\text{nm}$) across fluences ranging from $0.75$ to $9\,\text{J}/\text{cm}^2$.
- <b>Core Ablation Mechanism Insight</b>: Femtosecond laser ablation of silicon is <b>thermal in nature at low fluences</b> ($\leq 1\,\text{J}/\text{cm}^2$), but transitions to a <b>non-thermal mechanism at high fluences</b> ($>1\,\text{J}/\text{cm}^2$) due to rapid optical excitation occurring faster than carrier-lattice energy relaxation times

## Fundamental physical framework (n-TTM)
The interaction process is divided into five stages: absorption, heating, energy transfer, thermomechanical response, and ablation. The 2D axisymmetric system simultaniously solves:
- <b>Carrier density evolution equation</b>: Models electron-hole pair dynamics influenced by single-photon absorption, Auger recombination ($\gamma n^3$), impact ionization ($\eta n$), and ambipolar diffusion ($D_0$).
- <b>Carrier energy balance equation</b>: Tracks temperature ($T_{\text{e}}$) using thermal conductivity ($k_{\text{c}}$), heat capacity ($C_{\text{e}}$), carrier-lattice coupling ($K$), photon energy absorption, bandgap energy changes ($E_{\text{g}}$), and impact ionization energy losses.
- <b>Lattice energy balance equation</b>: Tracks lattice temperature ($T_{\text{l}}$) while incorporating latent heat of melting (H_{\text{m}}$) to handle phase transitions.

## Threshold fluence determination
By plotting the square of crater diameters ($D^2$) against the logarithmic laser fluence ($F_0$), damage thresholds were evaluated:
- <b>Experimental ablation threshold</b>: Determined to be $0.27\pm0.02\,\text{J}/\text{cm}^2$.
- <b>Simulation thresholds</b>:
	- <b>Critical carrier density criterion</b>: $0.22\,\text{J}/\text{cm}^2$ (reaches critical carrier density $N_{\text{cr}}=2.7\cdot10^{27}\,\text{m}^{-3}$).
	- <b>Melting temperature criterion</b>: $0.25\,\text{J}/\text{cm}^2$ (lattice reaches silicon melting point $T_{\text{m}}=1689\,\text{K}$).
- <b>Agreement</b>: The simulated threshold based on the melting criterion ($0.25\,\text{J}/\text{cm}^2$) matched closest with the experimental ablation threshold.

## Temporal distribution dynamics
- <b>Very low fluence</b>: ($0.015\,\text{J}/\text{cm}^2$) carrier temperature ($T_{\text{e}}$) peaks early at $0.4\,\text{ps}$ ($4500\,\text{K}$) because initial carrier heat capacity is low. Carrier number density (n) peacks much later at $1.2\,\text{ps}$, ($2.25\cdot10^{26}\,\text{m}^{-3}$) before decaying via Auger recombination. $T_{\text{e}}$ and T_{\text{l}}$ reach thermal equilibrium around $8\,\text{ps}$.
- <b>Higher fluence</b>: ($0.15\,\text{J}/\text{cm}^2$) carrier density peaks early at $0.61\,\text{ps}$, ($2.1\cdot10^{27}\,\text{m}^{-3}$), closely followed by carrier temperature peaking at $0.65\,\text{ps}$, ($9600\,\text{K}$). Impact ionization causes a minor temporary drop in carrier temperature as energetic carriers transfer energy to generate more free carriers.

## Ablation crater morphology and depth results
- <b>Heat-affected zone (HAZ)</b>: Because the $180\,\text{fs}$ pulse duration is shorter than the carrier-lattice relaxation time ($1-10\,\text{ps}$), energy deposition is rapid producing a minimal heat-affected zone ($<1\,\mu\text{m}$) and steep thermal gradients.
- <b>Profile comparison</b>:
	- Thermal simulations slightly over-predict both crater diameter and ablation depth compared to non-thermal simulations.
	- Simulation depth values generally overestimate experimental FIB cross-section depth measurements.
- <b>Mechanism transition</b>: At fluences $\leq1\,\text{J}/\text{cm}^2$, thermal and non-thermal simulated crater profiles are nearly identical. At higher fluences (>1\,\text{J}/\text{cm}^2), the non-thermal ablation model aligns much closer with experimental observations because non-equilibrium carrier excitation occurs faster than lattice energy transfer.