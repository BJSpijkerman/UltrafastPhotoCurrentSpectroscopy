
Bakulin, A. A. _et al._ Mode-selective vibrational control of charge transport in $π$-conjugated molecular materials. _Nat Commun_ **6**, 7880 (2015).

The aim of this work is to show the possibility of charge transport modulation by means of exciting selective molecular vibration modes in a pentacene$/C60$ photoresistor. To demonstrate a new pathway to modulate photoconductivity and study electron-phonon coupling in (bio)molecular meterials.
> Specific molecular vibrations slectively accelerate carrier detrapping and increase photocurrent.

## Methodology
- <b>Approach</b>: Ultrafast photocurrent pump-probe-probe where the probe beam is send through an interferometer to probe the sample after excitation.![[BakulinSetup.png]]
- <b>Experimental Setup</b>:
	- <b>Optical excitation</b>: A vissible pump pulse ($665\,\text{nm}/1.9\,\text{eV}$) is used to generate carriers, followed by a Mach-Zehnder interferometric pair of mid-IR push pulses ($1150-1700\,\text{cm}^{-1}$) to create a coherent superposition of vibrational modes with high frequency resolution ($\approx10\,\text{cm}^{-1}$) and ultrafast time resolution.
	> The $1.9\,\text{eV}$ excitation is approximately resonant with the measured bandgap in room temperature pentacene crystals.
	 ![[pentaceneBG.png|236]]

	- <b>Electrical detection</b>: Lock-in current measurement across a comb-like electrode architecture under a continuous $5\,\text{V}$ bias to detect variationsin output photocurrent ($\delta J/J$).
- <b>Device architecture</b>: Pentacene ($70\,\text{nm}$)/ Fullerene $C_{60}$ ($15\,\text{nm}$) bi-layer photoresistors fabricated on $3-10\,\mu\text{m}$ interdigitated gold electrodes.
- <b>Theoretical moddeling</b>: (DFT) calculation evaluating non-local (peierls-type) electron-phonon couplings ($\nu_i=dt_i/dQ_i$) to model intermolecular transfer integral variations under mode-specific diisplacements.

## Key findings
- <b>Vibrational Enhancement of Photocurrent</b>: Coherently exciting specific IR-active molecular modes in pentacene and $C_{60}$ enhances photocurrent bu accelerating the de-trapping of long-lived carriers.
- <b>Mode-Selective Anisotropy</b>: Normalized photocurrent response does not scale simply with IR optical absorption, demonstrating true mode selectivity.
	- <b>Long axis modes</b>: ($1500-1700\,\text{cm}^{-1}$) vibrations allong the long axis of pentacene (e.g. $1540\;\text{and}\;1630\,\text{cm}^{-1}$) induce a $5-8$ times stronger photocurrent per absorbed photon compared to short axis modes.
	- <b>Short axis modes</b>: ($1300-1345\,\text{cm}^{-1}$) in-plane ring stretching along the short axis exhibits weak coupling to charge detrapping.
- <b>Validation of Peierls coupling</b>: Quantum mechanical calculations confirm that long-axis molecular deformations modulate the primary intermolecular transfer integrals ($t_1=75\,\text{meV},t_2=32\,\text{meV}$) along the herringbone crystal directions much more strongly than sort-axis motions.

## Limitations
- <b>Targeted bound state</b>: Vibrational excitation predominantly affects trapped, long-lived photocarriers rather than prompt geminate charge-transfer state dissociation at the hetrojunction interface.
- <b>Low Operating temperature/Fluence efficiency</b>: Requires intense ultrafast mid-IR pulse sequences to achieve non-equilibrium vibrational pipulations under ambient CW conditions, thermal equilibration quickly dissipates mode-specific energy.
- <b>Device Geometry requirement</b>: Requires interdigitated lateral electrode achitectures to ensure sufficient optical access of the mid-IR push pulses into the active organic layer without metalization shielding.