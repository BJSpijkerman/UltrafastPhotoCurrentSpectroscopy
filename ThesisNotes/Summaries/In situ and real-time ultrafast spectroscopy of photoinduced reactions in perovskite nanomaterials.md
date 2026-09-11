
Han, G. R. _et al._ In situ and real-time ultrafast spectroscopy of photoinduced reactions in perovskite nanomaterials. (2024)

To develop and demonstrate asynchronous and interferometric transient absorption (AI-TA) spectroscopy for high-speed, broad dynamic range, real-time _in situ_ monitoring of photophysical carrier dynamics and photoinduced structural/chemical transformations in colloidal perovskite nanomaterials.

## Methodology
- <b>Approach</b>: Asynchronous optical sampling using two synchronized Ti:Saphire mode-locked lasers ($80\,\text{MHz}$ repetition rate, detuned by $\Delta f=51.2-460.8\,\text{Hz}$) paired with self-referenced  interferometric homodyne detection using a balanced photodetector.
- <b>Experimental capabilities</b>:
	- <b>No linear stage for pump-probe delay</b>: Eliminates mechanical delay stages to continuously acquire full $120\,\text{ps}$ to $1\,\text{ns}$ delay windows within fractions of a millisecond ($187.5\,\mu\text{s}$ per scan).
	- <b>Three fold Time-Division Multiplexing</b>: Simultaneously tracks pump-probe delay time ($t_{\text{pump-probe}}$, sub-picosecond to nanosecond), probe autocorrelation wavelength ($\lambda_{\text{probe}}$, $390-450\,\text{nm}$ via FFT), and reaction time ($t_{\text{react}}$, seconds to hours).
- <b>Target material systems</b>:
	- <b>Photo-substitution</b>: $\text{CsPb(Br/Cl)}_3$ perovskite nanocrystals (PeNCs, $\approx7.2\,\text{nm}$) dispersed in chloroform/toluene mixtures under continuous light exposure.
	- <b>Photon driven transformation</b>: 2-monolayer ($2\text{ML}$) $\text{CsPbBr}_3$ perovskite nanoplatelets (PeNPLs, $\approx20\,\text{nm}$ lateral size) in hexane undergoing light-induced aggregation/coalescence.

## Key findings
- <b>Real-Time photoinduced Halide Substitution</b>: AI-TA tracked the continuous _in situ_ anion exchange ($\text{Br}^- \rightarrow \text{Cl}^-$) of $\text{CsPb(Br/Cl)}_3$ PeNCs driven by photoinduced electron transfer to chloroform over a $\approx100\,\text{min}$ reaction timescale:
	- The bandgap photo-bleach (PB) peak continuously blue-shifted from $440\text{ nm}$ to $403\text{ nm}$ without changing particle size.
	- As Cl content increased, the sub-picosecond hot carrier thermalization/renormalization duration shortened due to decreased pump excess energy, while electron trapping into shallow defects accelerated from $20.2\text{ ps}$ down to shorter lifetimes.
- <b>Agglomeration-induced hot phonon bottleneck</b>: In $2\text{ML}$ $\text{CsPbBr}_3$ PeNPLs, real-time light-induced stacking into superlattices/agglomerates caused a progressive slowdown in hot carrier cooling from $0.08\,\text{ps}$ to $0.12\,\text{ps}$. The reduced out-of-plane carrier-phonon coupling in stacked structures suppressed thermal dissipation to the surroundings.
- <b>Higher order tensor analysis</b>: Demonstrates that a single AI-TA measurement can be structured as a rank-three tensor and analyzed via higher-order SVD (HOSVD) to uncouple carrier dynamics ($P_1$), spectral energy shifts ($P_2$), and reaction progress ($P_3$).

## Limitations
- <b>Focus Aggregation and Degradation Artifacts</b>: Extended light exposure over long reaction times ($>400\,\text{scans} / >40\,\text{min}$) eventually causes sample degradation, scattering artifacts, and local precipitation at the laser focal volume, necessitating discarded data segments.
- <b>Selective detection window</b>: In PeNPL coalescence, as nanoplatelets transform into higher ML counts ($3\text{ML}+$) or bulk phases, their bandgap shifts to longer wavelengths ($>500\,\text{nm}$), falling outside the NUV probe bandwidth ($390-450\,\text{nm}$) and leaving higher-order products undetected.
- <b>Photoreaction Coupling</b>: Because the laser pulses act as both the probing tool and the reaction stimulus, decoupling intrinsic probe-induced effects from deliberate photochemistry requires careful control of laser fluence and sample stirring.