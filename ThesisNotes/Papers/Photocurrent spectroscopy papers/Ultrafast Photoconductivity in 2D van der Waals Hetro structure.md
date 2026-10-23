
Tao, Y., Hong, C. & Kim, J.-H. Ultrafast reversible photoconductivity in 2D MoTe2/Pt van der Waals heterostructure. _Science AdvAnceS_ (2025).

The aim of this work is to demonstrate a light-induced electric field reversal at a $MoTe_2/Pt$ Schottky junction, enabling ultrafast voltage-controlled photoconductivity polarity inversion from negative (NPC) to positive (PPC) photocurrent on a picosecond timescale without requiring additional gating components or structural modifications

## Methodology
- <b>Approach</b>: Ultrafast photocurrent pump-probe detection combined with lock-in amplifier phase tracking to resolve sub-nanosecond transient electric field dynamics at a vd Waals metal-semiconductor interface.![[YeTaovdWaalsSetup.png]]
	- <b>Experimental Setup</b>:
		- <b>Optical Pump-probe</b> $800\,\text{nm}$ pulses with a duration of $13\,\text{fs}$ and a repetition rate of $80\,\text{MHz}$ are split into two beams with perpendicular polarization (to prevent interface artifacts WHY) These beams are applied in the usual pump probe way.
		- <b>Phase-sensitive detection</b> The photocurrent is measured in $\left|I_{ph}\right|$ and $arg\left(I_{ph}\right)$ with a two-channel lock-in amplifier synced with a $100\,\text{Hz}$ optical chopper where $\theta\approx0^{\circ}$ corresponds to PPC and $\theta\approx180^{\circ}$ corresponds to NPC

## Key findings
- <b>Ultrafast polarity inversion</b>: This work observed a photoinduced transition from NPC to PPC within $100\,\text{ps}$ following excitation.
- <b>Mechanism</b>: This polarity inversion is driven by asymetric carrier dynamics at the $MoTe_2/Pt$ interface. Here ultrafast hole transfer to the $Pt$ electrode (sub-picosecond) leaves the excess electrons, inverting the local electric field in the vd Waals hetrostructure, subsequent carrier recombination then gradually restores the original field.![[YeTaovdWaalsResult.png]]
- <b>Presice Electrical Control</b>: Applied reverse bias voltage mdulates the inversion duration $T$ and transition speed $\tau$.
- <b>High-speed device capability</b>: as a programmable NPC/PPC photodetector opperating near its off-state, acheaving a response time of $3.8\,\text{ps}$ ($\approx250\,\text{GHz}$)with a $12.5\,\text{mV}$ step and theoretical linear sensitivity slope of $455\,\text{fs}/\text{mV}$.

## Limitations
- <b>Dependence on high pump fluence</b>: The transition field required high optical excitation densities ($\approx3.26\cdot10^{19}\,\text{cm}^-3$) to sufficiently screen and invert the intrinsic barrier.
- <b>Metal defect sensitivity</b>: Surface states, interface defects and contact quality variability can broaden the transition speed beyond its theoretical limit.