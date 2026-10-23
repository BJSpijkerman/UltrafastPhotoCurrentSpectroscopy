This paper provides a review of theoretical and ab initio frameworks used to describe the coupled out-of-equilibrium dynamics of electrons and lattice vibrations in solid-state systems following ultrafast photo-excitation.

## Key Takeaways
- <b>Core Scope</b>: The review traces the theoretical evolution from phenomenological models the __Two-Temperature Model (TTM)__ and __Non-Thermal Lattice Model (NLM)__ to the parameter free, momentum-resolved __Time-Dependent Boltzmann Equation (TDBE)__.
- <b>TTM Limitations</b>: While computationally lightweight, the classical TTM assumed instantaneous local thermalization for both electrons (Fermi-Dirac) and phonons (Bose-Einstent), making it incapable of capturing non-thermal carrier distributions, non-thermal lattice states ("hot phonons"), or momentum-space anisotropies.
- <b>NLM / Multi-Temperature Models</b>: By partitioning phonons into $N$ distinct groups based on electron-phonon coupling strengths, the NLM accounts for anisotropic energy flow into strongly-coupled phonon modes.
- <b>TDBE Framework</b>: Solving the coupled TDBE using first-principles matrix elements (DFPT) provides a full momentum- and time-resolved picture of non-equilibrium populations ($f_{n,\vec{k}}$ and $n_{\vec{q}\nu}$) without relying on free parameters.
- <b>Application Focus</b>: The authors highlight graphene as a benchmark material to illustrate hot-carrier dynamics, tr-ARPES signatures, and momentum-selective phonon emission ("hot spots").

## The Two-Temperature Model (TTM) & Non-Thermal Lattice Model (NLM)
- <b>Classical TTM</b>: Couples an electronic thermal bath ($T_{\text{el}}$) and lattice bath ($T_{\text{ph}}$) via differential equations governed by electronic/phonon heat capacities ($C_{\text{el}}$, $C_{\text{ph}}$) and an electron-phonon coupling parameter $g$.
$$
\frac{\partial T_{\text{ph}}}{\partial t}=\frac{g}{C_{\text{ph}}}\left(T_{\text{el}}-T_{\text{ph}}\right),\;\; \frac{\partial T_{\text{el}}}{\partial t}=\frac{g}{C_{\text{el}}}\left(T_{\text{ph}}-T_{\text{el}}\right)+S(t).
$$
- <b>Microscopic TTM</b>: $g$ can be derived directly from first principles calculations using the Eliashberg function $\alpha^2F(\Omega)$.
- <b>NLM Extension</b>: To address the establishment of "hot phonons" (where strongly-coupled modes receive energy faster than weak modes), the lattice is split into $N_g$ phonon subgroups:
$$
\frac{\partial T^{\mu}_{\text{ph}}}{\partial t}=\frac{g_{\mu}}{C^{\mu}_{\text{ph}}}\left(T^{\mu}_{\text{el}}-T^{\mu}_{\text{ph}}\right)+\sum_{\mu'}\frac{T^{\mu'}_{\text{ph}}-T^{\mu}_{\text{ph}}}{\tau_{\mu\mu'}}
$$
This incorporated inter-branch phonon-phonon relaxation times ($\tau_{\mu\mu'}$).

## The Time-Dependent Boltzmann Equation (TDBE)
- <b>Formulation</b>: Tracks the time evolution of electronic occupations $f_{n\vec{k}}(t)$ and phonon occupations $n_{\vec{q}\nu}(t)$ through collision integrals:
$$
\partial_tf_{n\vec{k}}(t)=\Gamma_{n\vec{k}}(t),\;\;\partial_tn_{\vec{q}\nu}(t)=\Gamma_{\vec{q}\nu}(t)
$$
- <b>Collision Integrals from First Principles</b>: Derived via Fermi's golden Rule using ab initio density-functional perturbation theory (DFPT) matrix elements:
	- $\Gamma^{\text{ep}}_{n\vec{k}}$ & $\Gamma^{\text{pe}}_{\vec{q}\nu}$: Account for all phonon emission/absorption processes, enforcing energy ($\delta$-functions) and crystal momentum conservation.
	- $\Gamma^{\text{pp}}_{\vec{q}\nu}$: Accounts for three-phonon scattering processes arising from lattice anharmonicity.
- <b>Rigorous Link to TTM</b>: The TTM equations can be formally derived as a limiting case of the TDBE by assuming $f_{n\vec{k}}$ and $n_{\vec{q}\nu}$ maintain quasi-equilibrium thermal distributions at every instant.

## Case Study: Ultrafast Carrier & Lattice Dynamics in Graphene
- <b>Four-Step Thermalization</b>: (i) Photo-excitation $\rightarrow$ (ii) Carrier-carrier scattering & [[Auger-effect]] processes (~ $10\,\text{fs}$) $\rightarrow$ (iii) Optical phonon emission establishing a hot Fermi-Dirac distribution (~ $100\,\text{fs}$) $\rightarrow$ (iv) Energy dissipation to acoustic phonons (~ $1-10\,\text{ps}$).
- <b>Spectroscopic Signatures</b>: The paper demonstrated how tr-ARPES spectral functions and transient optical loss functions can be simulated using TTM/NLM temperatures of full TDBE distribution dynamics.
- <b>Reciprocal-Space Hot Spots</b>: TDBE simulations reveal that momentum and energy conservation constrain phonon emission to narrow regions of the Brillouin zone ($\Gamma$ and $K$ points for graphene: $\Gamma$, $K$, and $Q$ points for monolayer $\text{MoS}_2$), creating directional "hot spots" with elevated mode-resolved effective temperatures.

## Beyond the Boltzmann Formalism
The review concludes by highlighting physical phenomena that fall outside the TDBE domain and require specialized approaches:

- <b>Coherent Electron Dynamics</b>: Rapid phase-coherent polarization ($t<100\,\text{fs}$) requiring Density Matrix or Kadanoff-Baym / Non-Equilibrium Green's Functions (NEGF).
- <b>Coherent Lattice Dynamics</b>: Impulsive coherent phonon oscillations best modeled via classical/ab initio molecular dynamics (rt-TDDFT-MD) or quantum harmonic oscillator models.
- <b>Structural Phase Transitions</b>: Driven, highly non-linear, and non-perturbative lattice distortions requiring Ehrenfest dynamics or non-perturbative potential energy surface mapping.