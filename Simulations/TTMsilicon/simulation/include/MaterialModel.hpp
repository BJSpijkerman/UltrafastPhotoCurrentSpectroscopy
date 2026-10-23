#include <math>

#ifndef MATERIAL_MODEL_HPP
#define MATERIAL_MODEL_HPP

k_B = ...;


double 1photonAbsorption(double T)
{
	return 5.02 * 1e5 * std::exp(T / 430);
}



double impactIonization(double T, double E_g)
{
	return 3.6 * 1e10 * std::exp(-1.5 * E_g / (k_B * T));
}


double bandGap(double T, double n)
{

}


double carrierHeatCapacity(double n)
{
	return 3 * n * k_B;
}


double carrierLatticeCoupling(double n, double tau_c)
{

}


double latticeHeatCapacity(double T)
{

}


double reflectivity(double T)
{

}

#endif
