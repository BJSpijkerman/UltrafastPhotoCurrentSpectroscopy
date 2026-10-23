We are going to find the boundary conditions of the Maxwell's equations for the $\vec{E}$ and $\vec{B}$ fields across an interface, therefore lets start by stating the Maxwell equations:
$$
\nabla\cdot\vec{D}=\rho
$$
$$
\nabla\times\vec{E}=-\frac{\partial\vec{B}}{\partial t}
$$
$$
\nabla\cdot\vec{B}=0
$$
$$
\nabla\times\vec{H}=\frac{1}{\mu_0}\vec{J}+\frac{1}{c^2}\frac{\partial\vec{D}}{\partial t}
$$
![[BCimage.png|700]]
When integrating the second and fourth Maxwell equations over this surface and using some vector calculus theorem we get:
$$
\int\int_Sd\vec{A}\cdot(\nabla\times\vec{E})=\oint_{\partial S}d\vec{l}\cdot\vec{E}=-\frac{\partial}{\partial t}\int\int_Sd\vec{A}\cdot\vec{B}
$$
$$
\int\int_Sd\vec{A}\cdot(\nabla\times\vec{E})=\oint_{\partial S}d\vec{l}\cdot\vec{H}=\int\int_Sd\vec{A}\cdot\left(\frac{1}{\mu_0}\vec{J}+\frac{1}{c^2}\frac{\partial\vec{D}}{\partial t}\right)
$$
which we can solve (assuming no surface charge),
$$
\left(E_{//1}-E_{//2}\right)=\frac{\partial}{\partial t}Bh
$$
$$
H_{//2}-H_{//1}=0
$$
Introducing $H=nE$ for non-magnetic materials these can be combined into:
$$
E_i+E_r=E_t
$$
$$
n_1\left(E_i-E_r\right)=n_2E_t
$$
Now we realize that: $E_i=E,\;E_r=rE\;E_t=tE$, which leads to the simplification,
$$
1+r=t
$$
$$
1-t = \frac{n_2}{n_1}t
$$
solving for $r$ and $t$ then gives
$$
r = \frac{n_1-n_2}{n_1+n_2}\quad\frac{2n_2}{n_1+n_2}
$$