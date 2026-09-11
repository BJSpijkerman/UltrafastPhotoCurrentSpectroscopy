
Zheng, W. _et al._ Photothermal effects control ultrafast charge transport in titanium carbide MXenes. _Nat Commun_ **17**, 1201 (2026).

To elucidate the physical mechanism driving long-lived negative photoconductivity (NPC) in two-dimensional titanium carbide MXene ($\text{Ti}_3\text{C}_2\text{T}_x$) and determine whether the phenomenon stems from persistent non-equilibrium hot carriers or a slow photothermal energy dissipation bottleneck.

## Methodology
- <b>Approach</b>: Complementary combination of temperature-dependent THz time-domain spectroscopy (THz-TDS), optical pump-THz probe (OPTP) spectroscopy, and variable repetition-rate transient reflectivity measurements (TRM).
	- <b>Static THz-TDS</b>: Tracks non-equilibrium conductivity $\sigma(\omega)$ and Drude scattering parameters across temperatures ($97-286\,\text{K}$) op spray coated $\text{Ti}_3\text{C}_2\text{T}_x$ thin films ($\approx25\,\text{nm}$ thick).
	- <b>OPTP Spectroscopy</b>: Tracks non-equilibrium photoconductivity dynamics ($\Delta\sigma$) while systematically tuning pump photon energy ($h\nu=0.71-3.88\,\text{eV}$) and sample temperatures ($78-287\,\text{K}$)
	- <b>Variable Repetition-Rate TRM</b>: Probes transient reflectivity changes ($\Delta R/R$) at the pump $600\,\text{nm}$ and probe $790\,\text{nm}$ across various pulse repetition rates (13-256\,\text{ns}$ effective pulse delays).
- <b>Theoretical modeling</b>: Developed a parameter-free photothermal-electronic model combining Drude mobility parameters ($\mu\propto\tau$) with the known temperature-dependent heat capacity of $\text{Ti}_3\text{C}_2\text{T}_x$.

## Key findings
- <b>Thermal origin of NPC</b>: Optical absorption induces ultrafast carrier-phonon thermalization ($<1\,\text{ps}$), depositing energy directly into the phonon bath. The resulting lattice temperature rise ($\Delta T$) enhances carrier-phonon momentum scattering ($\tau$ drops), suppressing carrier mobility ($\mu$) and inducing negative photoconductivity.
- <b>Photon temperature and energy scaling</b>: Long-lived photoconductivity ($\Delta\sigma$) scales strictly linearly with absorbed photon energy density ($N_{\text{abs}} \times h\nu$). Equivalent conductivity states are produced at different pump wavelengths if total absorbed power is matched. Furthermore, lower baseline temperatures yield larger NPC amplitudes due to reduced lattice heat capacity.
- <b>Anomalously slow heat dissipation</b>: Transient reflectivity reveals that residual lattice heat persists over $100\,\text{ns}$, featuring an exponential thermal decay time constant of $40 \pm 1\,\text{ns}$.
- <b>Phonon Heat Reservoir Model</b>: $\text{Ti}_3\text{C}_2\text{T}_x$ acts as a highly efficient phonon heat reservoir where absorbed optical energy remains trapped due to a severe out-of-plane thermal bottleneck (low interfacial Kapitza conductance or low interlayer thermal conductivity).

## Limitations
- <b>Interfacial vs. cross-plane ambiguity</b>: The measurements establish an overall out-of-plane thermal transport bottleneck but cannot quantitatively decouple interfacial Kapitza thermal resistance from intrinsic interlayer flaking thermal conductivity.
- <b>Surface termination broadening</b>: Calculations rely on DFT effective mass parameters ($m^* = 0.28\ m_0$) for hydroxyl terminations, whereas experimental samples contain mixed surface groups ($-\text{O}$, $-\text{OH}$, $-\text{F}$, $-\text{Cl}$) that slightly modulate local band dispersions.