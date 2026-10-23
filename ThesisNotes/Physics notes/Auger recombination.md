[wikipedia page](https://en.wikipedia.org/wiki/Carrier_generation_and_recombination#Auger_recombination) about charge generation and recombination processes.
__Auger recombination__ is a fundamental __non-radiative carrier recombination process__ in semiconductor physics where an electron and a hole recombine, but instead of emitting a photon, the released transition energy is transferred directly to a third charge carrier. See (b).
![[augerRecombination.jpg|700]]

## Core Mechanism
1. <b>Energy Transfer</b>: A conduction band electron recombines with a valance band hole, releasing energy equal to (or greater than) the bandgap.
2. <b>Excitation of a Third Carrier</b>: Rather than generating light (radiative emission) or lattice heat directly (phonons), this energy is absorbed radiationlessly by a nearby third carrier - either and electron in the conduction band or a hole in the valance band.
3. <b>Thermalization</b>: The excited third carrier is kicked to a higher energy level within its perspective band (hot carrier) and subsequently loses this extra energy as thermal heat through collisions with the crystal lattice.

## Key Properties & Mathematical Dependance
- <b>Three-Particle Interaction</b>: Because Auger recombination involves three interacting carriers, its rate depends heavily on high carrier concentrations:
	- in $n$-type materials or high electron concentrations, the rate scales proportionally to $n^2p$ (two electrons one hole).
	- in $p$-type materials or high hole concentrations, the rate scales proportionally to $np^2$ (one electron two holes).
- <b>Carrier Lifetime Impact</b>: Because the rate scales cubicly with total carrier concentration ($\propto\Delta n^3$ under high injection), Auger recombination becomes the dominant loss mechanism at high carrier densities and high operating temperatures.

## Practical Importance in Devices
- <b>LED Efficiency Droop</b>: In high-power light-emitting diodes (LEDs) and laser diodes, Auger recombination is a major cause of efficiency loss at high operating currents.
- <b>Solar Cells</b>: Highly doped regions or regions operating under concentrated sunlight experience significant efficiency limits due to Auger recombination reducing minority carrier lifetimes.
- <b>Reverse Process</b>: The inverse process of Auger recombination is [[Impact ionization]], where a single energetic carrier generates a new electron-hole pair upon impact.