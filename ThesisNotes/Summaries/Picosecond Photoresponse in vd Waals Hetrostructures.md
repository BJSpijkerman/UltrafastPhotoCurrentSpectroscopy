
Massicotte, M. _et al._ Picosecond photoresponse in van der Waals heterostructures. _Nature Nanotech_ **11**, 42–46 (2016).

The aim of this work is to investigate the out-of-plane extraction dynamics, loss mechanisms and photoresponse speed in vertival graphene/$WSe_2$/Graphene ($G/WSe_2/G$) vd Waals hetrostructures to achieve simultaneously  high quantum efficiency and picosecond photodetection speeds.

## Methodology
- <b>Approach</b>: Time-resolved photocurrent autocorrelation spectroscopy using two push-pulses of $\approx200\,\text{fs}$ centered around $1.55\,\text{ev}$ to probe carrier depletion and extraction dynamics.
- <b>Experimental setups</b>:
	- <b>Time-resolved Autocorreltaion</b>: Used to record the autocorrelation of the non-linear photocurrent response at high laser powers ($>10\,\text{kWcm}^-2$) to extract response time $\tau$ for the symetric photocurrent dip arround $\Delta t=0$.![[MassicotteResult.png]]
	- <b>Spectroscopic mapping and efficiency</b>: Scanning photocurrent microscopy and continuous-wave/quasi-CW power-dependent measurements across exciton absorption peaks (A, B, A').![[MassicotteAbs.png]]

## Key findings
- <b>Ultrafast response times</b>: Achieved intrinsic photoresponse times as short as $\tau = 5.5\,\text{ps}$ (corresponding to a bandwidth $f \approx 100\,\text{GHz}$) for monolayer and trilayer ($2.2\,\text{nm}$) devices, comparable to pure graphene photodetectors.
- <b>Drift diffusive Transport scaling</b>: For thicker channels ($L\leq7.4\,\text{nm}$) the extraction time scales quadratically with thickness ($\tau\propto L^2$) and inversely with bias voltage ($\tau\propto V_B^{-1}$) confirming out-of-plane drift-diffusive transport with carrier mobility $\mu\approx0.010\,\text{cm}^{2}\text{V}^{-1}\text{s}^{-1}$.
- <b>Intrinsic Speed bounds</b>: Carrier extraction speed saturates at $\tau_s\approx3-5\,\text{ps}$ for thin layers due to the bottleneck of interfacial charge transfer and hot exciton dissociation at the graphene$/WSe_2$ interface.
- <b>High efficiency optimization</b>: Internal quantum efficiency (IQE) is dictated by the competition between extraction rate ($1/\tau_d$) and recombination loss rate ($1/\tau_r$). Trilayer $\text{WSe}_2$ ($2.2\,\text{nm}$) was identified as the optimal design, yielding both ultrafast response ($5.5\text{ ps}$) and high $\text{IQE} > 70\%$.

## Limitations
- <b>Monolayer Efficiency collapse</b>: Monolayer $\text{WSe}_2$ devices exhibited a poor $\text{IQE}$ ($\sim 6\%$) despite short response times, because ultrafast recombination and energy transfer to graphene outcompete charge extraction.
- <b>Circuit-level RC bottlenecks</b>: While the _intrinsic_ material response rate reaches $100\text{ GHz}$ ($5.5\,\text{ps}$), actual _external circuit_ electronic bandwidths were RC-limited to $\sim 1.6\,\text{ns}$ in unoptimized contact geometries.
- <b>High power non-linearities</b>: Time-resolved extraction relies on sublinear photocurrent saturation at high optical fluences ($>10\,\text{kW cm}^{-2}$), where phase-space filling and carrier-carrier interactions alter carrier dynamics compared to low-power linear regimes.