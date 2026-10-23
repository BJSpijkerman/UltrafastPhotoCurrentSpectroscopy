### Two-Temperature mode
In [[Ultrafast dynamics of electrons and phonons from the two temperature model to the time dependent Boltzmann equation]] the authors describe a first principles derivation of the two-temperature model. Consider two heat baths $S_1$ and $S_2$ in equilibrium with themselves but out-of-equilibrium with each other, their equiblibration (given that the temperature difference between the baths is small enough) can then be assumed linear,
$$
\frac{\Delta E_1}{\Delta t} = g_1\left(T_2-T_1\right),
$$
$$
\frac{\Delta E_2}{\Delta t} = g_2\left(T_1-T_2\right),
$$
where $E_1$ and $E_2$ / $T_1$ and $T_2$ are the energies and temperatures of heat baths $1$ and $2$, and $g_1$ and $g_2$ their coupling. Energy conservation dictates that $\Delta E_1 = -\Delta E_2$, giving rise to the condition $g_1=g_2=g$ (e.g. their coupling is symmetric). In the limit of infinitesimal time this becomes,
$$
\frac{\partial E_1}{\partial t}=g\left(T_2-T_1\right),
$$
$$
\frac{\partial E_2}{\partial t}=g\left(T_1-T_2\right).
$$
Now we introduce the heat capacity of the bath, this is done by the canonical definition: $C=\frac{\partial E}{\partial T}$. This lets us use the chain rule to write the change in energy of $S_1$ and $S_2$ as:
$$
\frac{\partial E}{\partial t}=\frac{\partial E}{\partial T}\frac{\partial T}{\partial t}=C\frac{\partial T}{\partial t}.
$$
Using the above formula we can write the most basic governing equations of the two temperature model,
$$
\frac{\partial T_1}{\partial t}=\frac{g}{c_1}\left(T_2-T_1\right),
$$
$$
\frac{\partial T_2}{\partial t}=\frac{g}{c_2}\left(T_1-T_2\right)
$$

The two-temperature model can be modified using several techniques to apply to a wide variety of different systems. The most common extension is to add a source term $S(t)$ to one of the heat baths. Three different situations are shown below, being the uncoupled, coupled and coupled+source.
![[TTMschematic.png]]
The heat baths $S_1$ and $S_2$ should be interpreted as the electronic and phononic subsystems. With this knowledge it is possible to derrive expressions for the heat capacities and coupling of the baths. The heat capacities can be derived using statistical mechanics,
$$
C_{\text{el}}=\int_{0}^{\infty}d\varepsilon\,D_{\text{el}}(\varepsilon)\frac{\partial f(\mu,\varepsilon,T_{\text{el}})}{\partial T_{\text{el}}},
$$
$$
C_{\text{ph}}=\int_{0}^{\infty}d(\hbar\omega)\,D_{\text{el}}(\omega)\hbar\omega\frac{\partial f(\omega,T_{\text{ph}})}{\partial T_{\text{ph}}},
$$
and the coupling constant $g$ can be expressed as,
$$
g=\frac{\pi k_{\text{B}}}{\hbar D_{\text{el}}(\varepsilon_{\text{F}})}\lambda\left<\omega^2\right>\int_{-\infty}^{\infty}d\varepsilon\,D_{\text{el}}^2\left(\varepsilon\right)\left(-\frac{\partial f(\mu,\varepsilon,T_{\text{el}})}{\partial\varepsilon}\right).
$$


### Non-Thermal Lattice model
In situations of hot phonons the lattice reaches a non-thermal state. This means that the lattice is not in equilibrium with itself, and 