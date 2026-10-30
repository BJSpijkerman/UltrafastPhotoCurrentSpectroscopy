For the fundamentals of the two temperature model see [[Two-Temperature and non-thermal lattice models]]  

To compare with the [[Two temperature model for gold]] we have to note that in silicon not only does the temperature of the electronic heat bath change so does the carrier density, due to the absorbed light pulse exciting electrons over the bandgap.
![[excitationImg.pdf]]
This means that where as in the two temperature model for gold $\Delta N=0$ was implicitly enforced we now need to also model the change in population of the conduction band, going from $\Delta\sigma=\Delta\mu N$ to $\Delta\sigma=\Delta\mu\Delta N$. To this end we add carrier generation and relaxation dynamics through several processes. Such as [[Auger recombination]] and [[Impact ionization]]. The carrier number evolution is then,
$$
\frac{\partial n}{\partial t}=-\gamma n^3 + \eta n + \frac{\alpha}{\hbar\omega}I+\frac{\beta}{\hbar\omega}I^2,
$$
where $n$ is the number of carriers, $\gamma$ is the Auger recombination coefficient, $\eta$ is the impact ionization coefficient, $\alpha$ is the $1$ photon absorption rate, $\beta$ is the $2$ photon absorption rate, $I$ is the incident intensity, $\hbar$ is the reduced Plank constant and $\omega$ the angular frequency of the incident light. The model equations for the subsystem heat baths then are,
$$
C_{\text{c}}\frac{\partial T_{\text{c}}}{\partial t}=-K\left(T_{\text{c}}-T_{\text{l}}\right) + \left(\alpha+\beta I+\Theta n\right)I-\frac{\partial n}{\partial t}\left(E_{\text{g}}+3k_{\text{B}}T_{\text{c}}\right)-n\left(\frac{\partial E_{\text{g}}}{\partial n}\frac{\partial n}{\partial t}+\frac{\partial E_{\text{g}}}{\partial T_{\text{c}}}\frac{\partial T_{\text{c}}}{\partial t}\right),
$$
where $C_{\text{c}}$ is the carrier heat capacity, $K$ is the carrier lattice coupling constant, $\Theta$ is the carrier absorption rate, $E_{\text{g}}$ is the band gap, and $T_{\text{c}}$ is the carrier temperature.
- The term:$-K\left(T_{\text{c}}-T_{\text{l}}\right)$ incorporates the energy exchange between the carrier and lattice heatbaths	
$$
C_{\text{l}}\frac{\partial T_{\text{l}}}{\partial t}=K\left(T_{\text{c}}-T_{\text{l}}\right),
$$
where $C_{\text{l}}$ is the lattice heat capacity, and $T_{\text{l}}$ is the lattice temperature. These equations where adapted from [[Thermal and non-thermal ablation mechanisms in crystalline silicon by femtosecond laser pulses]], this paper also gives parameterizations of the coefficients.

The __Linear absorption coefficient__,
$$
\alpha(T_i) = 5.02\cdot10^5e^{T_i/430}\quad\left[1\,\text{m}^{-1}\right].
$$
The __Auger recombination coefficient__,
$$
\gamma = 3.8\cdot10^{-43}\quad\left[\text{m}^6\text{s}^{-1}\right].
$$
The __Impact ionization coefficient__,
$$
\eta(T_i,E_{\text{g}}) = 3.6\cdot10^{10}e^{-1.5E_{\text{g}}/k_{\text{B}}T_i}.
$$
The __Band gap__,
$$
E_{\text{g}}(T_i, n)=1.16 - 7.2\cdot10^{-4}\left(\frac{T_i^2}{T_i+\left(1080\,\text{K}\right)}\right) - 1.5\cdot10^8n^{1/3}\quad\left[\text{eV}\right].
$$
The __Carrier heat capacity__,
$$
C_{\text{c}}(n)=3nk_{\text{B}}\quad\left[\text{Jm}^{-3}\text{K}^{-1}\right].
$$
The __Carrier-Lattice coupling__,
$$
K(n,\tau_{\text{c-l}})=3nk_{\text{B}}/\tau_{\text{c-l}}\quad\left[\text{Wm}^{-3}\text{K}^{-1}\right].
$$
The __Carrier-Lattice relaxation time__,
$$
\tau_{\text{c-l}}(n)=240\left[1+\left(n/6\cdot10^26\right)^2\right]\quad\left[\text{fs}\right].
$$
The __Lattice heat capacity__,
$$
C_{\text{l}}(T_i)=1.987\cdot10^6+354T_i-3.68\cdot10^6T_i^{-2}\quad\left[\text{Jm}^{-3}\text{K}^{-1}\right].
$$
The __Reflectivity__,
$$
R(T_i)=0.37+10^{-5}\left(T_i-T_{\text{room}}\right).
$$
