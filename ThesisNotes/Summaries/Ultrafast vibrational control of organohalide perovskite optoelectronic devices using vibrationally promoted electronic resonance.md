
Gallop, Nathaniel. P. _et al._ Ultrafast vibrational control of organohalide perovskite optoelectronic devices using vibrationally promoted electronic resonance. _Nat. Mater._ **23**, 88–94 (2024).

The goal if this work is to demonstrate ultrafast vibrational control (VC) in arganohalide perovskite optoelectronic devices ($\text{FAPbBr}_3$) by selectively exciting intermolecular vibrations of the organic formamidinium ($FS^+$) cation, unraveling the mechanism and timescales of coupling between the organic cation and the inorganic lead-halide lattice.

## Methodology
- <b>Approach</b>: Implemented vibrationally promoted electronic resonance (VIPER) spectroscopy paired with electrical photocurrent detection (PC_VIPER) and photoluminescence readout (PL-VIPER).
- <b>Experimental setups</b>:
	- <b>PC-VIPER</b>: Interferometrically seperated mid-IR pre-excitation pulses ($\approx1720\,\text{cm}^{-1}$, $\approx100\,\text{fs}$) populate excited vibrational states of the $FA^+$ cation, followed by an off-resonant visible pulse ($\approx580\,\text{nm}$) that promotes the sub-ensemble to the electronic excited state, driving measurable photocurrent.
	- <b>PL-VIPER</b>: Identical optical pump sequence applied to $FAPbBr_3$ nanocrystalline films, monitoring emitted photoluminescence action spectra.
- <b>Samples studied</b>: Bulk $\text{FAPbBr}_3$ solar cells, control all-inorganic $\text{CsPbBr}_3$ solar cells, and colloidal $\text{FAPbBr}_3$ nanocrystals.
- <b>Theoretical modeling</b>: Ab initio molecular dynamics (AIMD) simulations (using Quantum ESPRESSO) on a $2\times 2\times 2$ $\text{FAPbBr}_3$ supercell, including normal-mode perturbations to simulate non-equilibrium vibrational excitation.

## Key findings
- <b>Vibrationally assisted photocurrent</b>: Selective IR excitation of the $\nu(\text{N-C=N})$ stretching mode of $\text{FA}^+$ at $1,720\text{ cm}^{-1}$ promotes sub-bandgap electronic absorption, generating a distinct photocurrent signal in $\text{FAPbBr}_3$ that is absent in $\text{CsPbBr}_3$.
- <b>Ultrafast coupling window</b>: VIPER signal exhibits very short lifetime ($\approx280\,\text{fs}$ for PC-VIPER and $\approx240\,\text{fs}$ for PL-VIPER), significantly faster than the vibrational population relaxation time ($\approx2.8\,\text{ps}$) or free induced decay ($\approx850\,\text{fs}$)
- <b>Hydrogen-bond mediated mechanism</b>: AIMD simulations reveal that the $\approx300\,\text{fs}$ signal decay corresponds to the "wobbling" rotational motion and stochastic breaking/re-formation of cation-halide ($\text{N-H}\cdots\text{Br}$) hydrogen bonds.
- <b>Inorganic lattice distortion</b>: Hydrogen-bonding dynamics dynamically distort the $\text{PbBr}_3$ octahedra, directly modulating the perovskite bandgap and demonstrating that cation mobility controls intrinsic non-radiative recombination channels.

## Limitations
- <b>Short operational window</b>: Vibrational control is limited to a transient sub-picosecond window ($\approx300\,\text{fs}$) due to rapid rotational dephasing and hydrogen-bond fluctuations of the cation.
- <b>Off-resonant optical fluence needs</b>: Requires intense mid-IR pulse trains to populate excited vibrational manifolds sufficiently before off-resonant electronic probing.
- <b>Mode selectivity constraints</b>: Only the $\nu(\text{N-C=N})$ mode at $1720\,\text{cm}^{-1}$ showed strong vibronic coupling, whereas adjacent modes like $\delta_1(\text{NH}_2)$ ($1620\,\text{cm}^{-1}$) failed to yield a measurable VIPER signal.