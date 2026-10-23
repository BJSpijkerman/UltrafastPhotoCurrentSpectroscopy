#include "Silicon.hpp"
#include "Constants.hpp"


// Constructor
Silicon::Silicon(const MaterialParameters& material_params)
{
	m_e_eff = material_params.m_e_coeff * Constants.m_e;
	m_h_eff = material_params.m_h_coeff * Constants.m_e;
	alpha_0 = material_params.alpha_0;
	beta_0 = material_params.beta_0;
	gamma_e = material_params.gamma_e;
	gamma_h = material_params.gamma_h;
	theta_e = material_params.theta_e;
	theta_h = material_params.theta_h;
}


// get lifetime of (WTF WAS THIS AGAIN?)
double Silicon::getTau(double n_e)
{
	double ratio = n_e / 8.0e26;
	return tau_0 * (1.0 + ratio * ratio);
}


// Get carrier heat capacity
double getCCarrier(double n_carrier)
{
	return 1.5 * n_carrier * Constants.kB;
}
