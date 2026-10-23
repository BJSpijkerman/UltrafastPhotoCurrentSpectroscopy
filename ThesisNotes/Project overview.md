
<span style='color:red'>Note this note was made in preparation of the catch up with Ioannis and should be incorporated elsewhere according to the guidelines set out in:</span> [[15-10-2026]]
### Introduction
In this work we attempt to the non-linear effects created by repeated hot carrier generation in gold. The energy deposited generates hot electrons which have a different scattering rate than the "cold" electrons this creates a change in the conductivity of the sample. When the gold is illuminated by two successive light pulses with a separation time shorter than the thermal relaxation time there will be a correlation between the effect of the two pulses due to the temperature dependence of the electronic heat capacity $C_{\text{e}}(T_{\text{e}})$.  In the figure below the temperature changes driven by two successive pulses is show, note that the second pulse has a non-linear effect if it arrives to close to the first one.
![[TempResponseTielrooij.png|677]]
[[Generation of photovoltage in graphene on a femtosecond timescale through efficient carrier heating]]

### Optical setup
The experimental technique for such conductivity measurements is called photocurrent correlation spectroscopy. Such experiments consist of two interferometrically seperated pulses hitting the sample a short time $\Delta t$ apart. The resulting change in conductivity of the sample can then be read out electronically (choosing the DC conductivity as the observable) to isolate those processes that contribute to charge generation and transport ($\Delta\sigma=\Delta\mu\Delta N$)
[[Ultrafast Spectroscopy with Photocurrent detection]].
A schematic of image of the proposed setup is shown below. This setup consists of $800\,\text{nm}$ light pulses with $100\,\text{fs}$ duration entering a Mach-Zehnder intererometer at a rate of $1\,\text{kHz}$. Fluence is carefully controlled to not cause any interband excitations, allowing for the assumption that all modification to the conductivity are due to changes to electron mobility i.e. $\Delta\sigma=\Delta\mu N$.
![[setup.pdf]]

### Two temperature model
To estimate the signal strength we have constructed a two-temperature model, where the electrons and lattices are described by two coupled heat baths. The incoming laser is absorbed by a model based on Lambert-Beer absorption.

The results using a fluence of $178.254\,\mu\text{J}/\text{cm}^2$ is shown below, where we can see that the equilibrium temperature is approximately $T_{\text{eq}}\approx347.123\,\text{K}$, inducing a change in resistance on the order on tens of nano Ohms.
![[TTMresult_adjusted.png]]
![[TTMresultResistivity_adjusted.png]]

### Electronic readout
For the electronic readout of the measurement signal there are two main connections we can make.
- __4-point measurement__:
  __+__ Isolates from contact resistance.
  __+__ Measured voltage scales linearly with the bias current $I_{\text{bias}}$.
  __-__ Measured voltage scales with $1/d$, where $d$ is the probe separation.
- __Direct current measurement__:
  __+__ Measured voltage scales with linearly with probe separation.
  __-__ Includes contact measurement in noise.