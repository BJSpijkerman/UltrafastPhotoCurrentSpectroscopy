
Tielrooij, K. J. _et al._ Generation of photovoltage in graphene on a femtosecond timescale through efficient carrier heating. _Nature Nanotech_ **10**, 437–443 (2015).

The aim of this work by Tielrooij <i>et all</i> is to determine the time scale of photovoltage generation in graphene driven by the photothermoelectric effect (PTE). The study assesses the energy transfer from photon --> electron --> heat and its efficiency across a broad optical spectrum and demonstrate its utillity as an ultrafast photodetector through not the photocurrent but the generated photovoltage.
>Photocurrent generation is associated with carrier cooling time  (now limiting factor)
>Photovoltage generation is associated with carrier heating time ($<50\,\text{fs}$)

## Methodology
- <b>Aproach</b>: Ultrafast time-resolved photovoltage measurements combined with spectral responsivity measurements.
- <b>Experimental setup</b>:
	- <b>Time-resolved photovoltage measurement</b>: Two-pulse photo excitation resulting in a temporal resolution of $\approx30\,\text{fs}$. ![[SetupTielrooij.png]]
	> Note that here the two beams are both sub $20\,\text{fs}$ pulses with center frequency $800\,\text{nm}$ and a $100\,\text{nm}$ band with. This is an interferometric kind of photovoltage measurement and no initial excitation pulse is needed due to graphene having a gapless spectrum. 
	
	- <b>Spectral responsivity</b>: These measurements are done to evaluate the internal quantum efficiency of the graphene and are done to characterize the photodetecting capabilities of the device and are of no relevance to my work.
- <b>Devices tested</b>:
	- Dual-gated graphene p-n junction on a $SiO_2/Si$ substrate.
	- Single-layer/bilayer graphene interfaceon a transparent 1-mm-thick quartz substrate (to prevent substrate-induced interference)

## Key findings
- <b>Ultrafast photovoltage generation</b>: The photovoltage generation occurs on a sub $50\,\text{fs}$ timescale. This is significantly faster than the picoseconds electron-cooling time. 
  >$\tau_{heat} \leq 50\,\text{fs}$,
  > 	$\tau_{cool}\approx1.3-1.5\,\text{ps}$.

- <b>Direct pulse duration measurement</b>: The study demonstrates direct electrical measurement of the autocorrellation of a sub $50\,\text{fs}$ laser pulse without relying on non-linear optical crystals. Instead the study utilizes the intrinsic non-linearity of the electronic heat capacity where,
  $$
	\Delta T=\int_{Q_0}^{Q_0+\Delta Q}\frac{dQ}{C_{el}\left(T_{el}\right)}.
  $$
  creating a response like in the image below.![[TempResponseTielrooij.png]]
  
  - <b>Flat Spectral Responsivity</b>: Related to the characterization as a photodiode
  - <b>Efficient carrier heating</b>: Related to IDK YET

