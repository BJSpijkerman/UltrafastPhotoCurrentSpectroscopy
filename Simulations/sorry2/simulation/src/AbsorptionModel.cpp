#include "AbsorptionModel.hpp"
#include "Constants.hpp"
#include <cmath>


// Initialize the class with laser parameter struct
LaserSource::LaserSource(const LaserParameters& laser_params)
{
	wavelength = laser_params.wavelength;
	omega_0 = 2.0 * M_PI * Constants.c / wavelength;
	tau_pulse = laser_params.tau_pulse;
	T_sigma = tau_pulse / (4.0 * std::sqrt(std::log(2.0)));
	t_peak = 4.0 * T_sigma;
	laser_power = laser_params.laser_power;
	w0 = laser_params.w0;
}


// Calculate absorbed fluence according to Lambert Beer
void LaserSource::initLambertBeer(void)
{
	double E_pulse = laser_power / f_rep;
	fluence = (1.0 - R_opt) * 2.0 * E_pulse / (M_PI * w0 * w0)
	I_0 = fluence / (std::sqrt(M_PI) * T_sigma);
}


// Get the source term at some time t
double LaserSource::getSource(double t)
{
	double arg = (t - T_0) / T_sigma;
	return I_0 * std::exp(-arg * arg);
}
