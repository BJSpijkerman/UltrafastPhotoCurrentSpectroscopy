The stage mounting plate is constructed to circumvent the issue that the stage in its current way of being mounted on the table is allowed to tilt by about $300\,\mu\text{m}$ over its $200\,\text{mm}$ length. this produces a shift in the laser spot of about $2.5\,\text{mm}$. 
![[stageTilt.png]]

To estimate the size of $b$ one can simply realize the shift in angles for both the laser beam and stage must be equation if the stage is rigid giving:
$$
\frac{b}{20\,\text{cm}}=\frac{c}{160\,\text{cm}},
$$
where $c=2.5\,\text{mm}$. thus the deflection of the stage is 
$$
b=\frac{\left(0.25\,\text{cm}\right)\cdot\left(20\,\text{cm}\right)}{\left(160\,\text{cm}\right)} \approx313\,\mu\text{m}
$$
To stop this tilting we have designed a new mounting plate based on the mechanical drawings of the stage
![[stageMechanicalDrawing.png]]

To ensure fitting to the optical table we have measured the holes in the optical table to be of size __M6__ and spaced by $25\,\text{mm}$. Based on this the following CAD model was made.
![[Screenshot_20261110_085749.png]]
For a load of $2.2$ metric tonnes we get the following results using a FEM model
![[simulation.png]]

With this it is decided that making the mounting plate out of steel is good enough for our purposes in any configuration of the feet, as the current configuration would definitely be most susceptible to bending.