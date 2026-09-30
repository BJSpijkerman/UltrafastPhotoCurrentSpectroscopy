To describe the out of equilibrium behavior of the gold film samples I have constructed a two temperature model according to: _Caruso and Novko - 2022_. this paper can be found in the papers folder. This model treats the electrons and lattice as two heat baths which are within equilibrium with itself, but out of equilibrium with each-other.
![[TTM_schematic.png|700]]

The governing equations of this system are:
$$
C_{\text{e}}(T_{\text{e}})\frac{\partial T_{\text{e}}}{\partial t} = g(T_{\text{e}})\left(T_{\text{ph}}- T_{\text{e}}\right) + S(t),
$$
$$
C_{\text{ph}}(T_{\text{ph}})\frac{\partial T_{\text{ph}}}{\partial t}=g(T_{\text{e}})\left(T_{\text{e}}-T_{\text{ph}}\right),
$$
where $C_i(T_i)$ are the heat capacities of the electrons and phonons respectively, $T_i$ their effective temperature, $g(T_{\text{e}})$ the electron-phonon coupling and $S(t)$ a source term.  For the electronic heat capacity and electron-phonon coupling I have taken the tabulated values from https://compmat.org/electron-phonon-coupling/ 
<iframe src="https://compmat.org/electron-phonon-coupling/"></iframe>
This website collects data from Density Functional calculatons from several sources from about $300\,\text{K}$ to $50000\,\text{K}$. The data for gold is obtained from the work of Zhibin [Lin and Leonid V. Zhigilei]  which is then interpolated by cubic splines.

The lattice heat capacity is taken to be the volumetric heat capacity of gold: $C_{\text{l}}=\rho c_{\text{p}}=\left(19283\,\text{kg}/\text{cm}^3 \right)\times\left(129.045\,\text{J}/\text{kg}\cdot\text{cm}^3\right)=2.5\cdot10^6$. Values for the density of gold and its specific heat are taken from wikipedia (# sue me).

The source term is assumed to be a temporally distributed Gaussian,
$$
S(t) = S_0e^{-\left(t-T_0\right)/2\sigma_{\text{t}}^2},
$$
where $S_0$ is the peak volumetric power density, $T_0$ is the arrival time of the pulse and $\sigma_{\text{t}}$ is the temporal width of the pulse which is calculated from the Full Width Half Max $\tau$ using the standard formula for a Gaussian $\sigma_{\text{t}}=\tau/\left(2\sqrt{2\log(2)}\right)$, for a pulse with $\tau=100\,\text{fs}$ the Gaussian width is: $\sigma_{\text{t}}\approx42.47\,\text{fs}$. The peak volumetric power density is calculated from the absorbed fluence with the formula,
$$
S_0=\frac{F_{\text{abs}}}{\sigma_{\text{t}}\sqrt{2\pi}},
$$
where $F_{\text{abs}}$ is the absorbed fluence,
$$
F_{\text{abs}}= \left(1-R_{\text{opt}}\right)\frac{2E_{\text{pulse}}}{\pi w_0},
$$
where $R_{\text{opt}}$ is the optical reflectivity of gold at $800\,\text{nm}$, $\approx0.93$, $E_{\text{pulse}}$ is the energy in a single pulse. This is calculated from the average power diverted to the sample and the repitition rate of the pulses: $E_{\text{pulse}}=P_{\text{avg}}/f_{\text{rep}}$. $w_0$ is the Gaussian beam width.

For the model we take the following parameters for the laser:
- $P_{\text{avg}}=100\,\text{mW}$;
- $f_{\text{rep}}=1\,\text{kHz}$;
- $w_0=5\,\text{mm}$;
- $\sigma_{\text{t}}=42.47\,\text{fs}$.
- 
This leads to the energy per pulse: $E_{\text{pulse}}=(100\,\text{mW})/(1\,\text{kHz})=100\,\mu\text{W}$. The absorbed fluence is then,
$$
F_{\text{abs}}=\left(1-0.93\right)\frac{2\times(100\,\mu\text{W})}{\pi\times(1\,\text{mm})^2}=0.178254\,\text{J}/\text{m}^2=1782.54\,\text{J}/\text{cm}^2
$$
This makes the total volumetric power density,
$$
S_0=\frac{(1782.54\,\text{J}/\text{cm})}{(43.47\,\text{fs})\times\sqrt{2\pi}}=1.116\cdot10^{20}\,\text{W}/{m}^3
$$
As a check we can derrive the equilibrium temperature of the lattice when a certain amount of energy has been dumped into the system.
This leads to the results shown below
![[TTMresult.png]]

#### Check against the Sommerfeld expansion for an ideal gass of free electrons
Since the Fermi level of gold is located withing the conduction band it is sufficient to consider the outer electrons of gold as a nearly free electron gass at temperatures lower than $3000\,\text{K}$, when the thermal energy becomes large enough to sufficiently excite electrons from the highly localized atomic d-shell into the conduction band leaving holes in the lower energy levels. By this we can check the Density Functional Theory calculation by  [Lin and Leonid V. Zhigilei] in the range from $300\,\text{K}$ to $3000\,\text{K}$ which is most of our range. The internal energy of the electrons $U_{\text{e}}(T)$ can be calculated using,
$$
U_{\text{e}}(T) = \int_0^{\infty}d\varepsilon\,\varepsilon g(\varepsilon)f(\varepsilon,T),
$$
where $g(\varepsilon)$ is the density of states for a free elctron-gass and $f(\varepsilon,T)$ is the Fermi-Dirac distribution. For low thermal energies compared to the Fermi-energy, $k_{\text{B}}T << E_{\text{F}}$ this integral can be evaluated using the Sommerfeld expansion.
$$
U_{\text{e}}(T)\approx U_0+\frac{\pi^2}{6}\left(k_{\text{B}}T\right)^2g(E_{\text{F}}).
$$
The heat capacity is defines as the change in energy with temperature giving,
$$
C_{\text{e}}(T)=\frac{dU_{\text{e}}}{dT}=\left(\frac{\pi^2k_{\text{B}}^2g(E_{\text{F}})}{3}\right)T = \gamma T.
$$
The density of states for a free electron-gass at the Fermi-energy is known to be,
$$
g(E_{F})=\frac{m^*}{\pi^2\hbar^2}\left(3\pi^2n_{\text{e}}\right)^{1/3}\approx 1.81\cdot10^47\,\text{states}/\text{J}\cdot\text{m}^3,
$$
where $m^*$ is the effective band mass of the electrons and $n_{\text{e}}$ is the particle density of the electrons. The coefficient $\gamma$ evaluates to $\gamma\approx70\,\text{J}{m}^3\text{K}^2$. Comparing the two leads to the figure shown below.
![[SommerfeldDFTcomparison.png]]
In the figure one can see reasonable agreement with the calculated values. The DFT calculations start however to diverge from the Sommerfeld solution after $2500\,\text{K}$.

#### Estimation of equilibrium lattice temperature
The change in energy of the electronic heat bath is,
$$
\Delta U_{\text{e}}=\int_{T_0}^{T_{\text{eq}}}dT_{\text{e}}\,C_{\text{e}}=\int_{T_0}^{T_{\text{eq}}}\,\gamma T_{\text{e}}=\frac{\gamma}{2}\left(T_{\text{eq}}^2-T_0^2\right),
$$
where $\Delta U_{\text{e}}$ is the change in energy from before excitation to after full equilibration, $T_0$ the initial temperature of the system, $T_{\text{eq}}$ the effective electron temperature after full equilibration, $T_{\text{e}}$ the effective electron temperature, $C_{\text{e}}$ the electronic heat capacity and $\gamma$ the Sommerfeld coefficient $\gamma = 70\,\text{J}/\text{m}^3\text{K}$. Taking the lattice heat capacity to be a constant the change in internal energy of the lattice heat bath becomes,
$$
\Delta U_{\text{ph}}=C_{\text{ph}}\left(T_{\text{eq}}-T_0\right),
$$
where $\Delta U_{\text{ph}}$ is the internal energy change of the lattice and $C_{\text{ph}}$ is the heat capacity of the lattice. Now combining these to obey energy conservation,
$$
\Delta U_{\text{ph}} + \Delta U_{\text{e}} = E_{\text{vol}},
$$
where $E_{\text{vol}}$ is the absorbed volumetric energy calculated by $E_{\text{vol}}=F_{\text{abs}}/d_{\text{p}}$, where $d_{\text{p}}$ is the skin-depth for gold $d_{\text{p}}\approx15\,\text{nm}$, thus $E_{\text{vol}}=\left(0.178254\,\text{J}/\text{m}^2\right)/\left(15\,\text{nm}\right)=1.188\cdot10^7\text{J}$. The above formula for energy conservation can be rearranged into the quadratic equation,
$$
\frac{\gamma}{2}T_{\text{eq}}^2+C_{\text{l}}T_{\text{eq}}-\left[E_{\text{vol}}+\left(\frac{\gamma}{2}+C_{\text{l}}\right)T_0\right]=0.
$$
This system than has the solutions:
$$
T_{\text{eq},1}=\frac{-C_{\text{l}}+\sqrt{C_{\text{l}}^2+2\gamma\left(E_{\text{vol}}+\gamma T_0/2+C_{\text{l}}T_0\right)}}{\gamma}=303.47\,\text{K},
$$
$$
T_{\text{eq},2}=\frac{-C_{\text{l}}-\sqrt{C_{\text{l}}^2+2\gamma\left(E_{\text{vol}}+\gamma T_0/2+C_{\text{l}}T_0\right)}}{\gamma}=-71.73\,\text{K},
$$
where T_{\text{eq},2} is the negative value and rejected and $T_{\text{eq}, 1}$ is the accepted positive value. The lattice temperature should thus rise by about $3-4\,\text{K}$, which is does as shown in the figure.