[[Three-Temperature modeling of laser-induced damage process in Silicon]] describes a carrier three temperature simulation coupled to Maxwell's equations to capture the carrier evolutions of hole and electron populations, along with their mutual equilibration. The paper also gives an expression of the dielectric function. It is an expansion of the [[Carrier Two temperature model]], where the electrons and holes are considered seperately. In this model the population of electrons and holes are:
$$
\frac{\partial n_{\text{e(h)}}}{\partial t}=\frac{\alpha}{\hbar\omega_0}I+\frac{\beta}{2\hbar\omega_0}I^2 - \gamma_{\text{e}}n_{\text{e}}^2n_{\text{h}}-\gamma_{\text{h}}n_{\text{e}}n_{\text{h}}^2 + \frac{1}{2}\left(\theta_{\text{e}}n_{\text{e}}+\theta_{\text{h}}n_{\text{h}}\right),
$$
where The first two terms of the right hand side are carrier generation terms are one and two photon absorption, the third and fourth terms are Auger recombination and the last two terms are impact ionization. __Note that this equation will give the same number of electrons and holes when the initial carrier and hole populations are set to zero $0$__. The carrier temperature equations are:
$$
C_{\text{e(h)}}\frac{\partial T_{\text{e(h)}}}{\partial t}=m_{\text{r,e(h)}}\left(\alpha_{\text{f}}I+\beta I^2\right)+E_{\text{g}}\gamma_{\text{e(h)}}n_{\text{e(h)}}^2n_{\text{h(e)}}-\frac{C_{\text{e(h)}}}{\tau}\left(T_{\text{e(h)}}-T_{\text{l}}\right)\\--\frac{\partial n_{\text{e(h)}}}{\partial t}\left(m_{\text{r,e(h)}}E_{\text{g}}+\frac{3}{2}k_{\text{B}}T_{\text{e(h)}}H^{1/2}_{-1/2}\left(\eta_{\text{e(h)}}\right)\right)\\-m_{\text{r,e(h)}}n_{\text{e(h)}}\left(\frac{\partial E_{\text{g}}}{\partial T_{\text{l}}}\frac{\partial T_{\text{l}}}{\partial t}+\frac{\partial E_{\text{g}}}{\partial n_{\text{e(h)}}}\frac{\partial n_{\text{e(h)}}}{\partial t}\right).
$$...
The evolution of the lattice temperature is:
$$
C_{\text{l}}\frac{\partial T_{\text{l}}}{\partial t}=\frac{C_{\text{e}}}{\tau}\left(T_{\text{e}}-T_{\text{l}}\right)+\frac{C_{\text{h}}}{\tau}\left(T_{\text{h}}-T_{\text{l}}\right).
$$
...