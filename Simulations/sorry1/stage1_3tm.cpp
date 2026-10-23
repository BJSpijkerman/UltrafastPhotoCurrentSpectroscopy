#include "stage1_3tm.hpp"
#include <algorithm>

StateVector operator+(const StateVector& a, const StateVector& b)
{
	StateVector res(a.size());
	for (size_t i = 0; i < a.size(); ++i)
	{
		res[i] = a[i] + b[i];
	}
	return res;
}

StateVector operator*(double scalar, const StateVector& vec)
{
	StateVector res(vec.size());
	for (size_t i = 0; i < vec.size(); ++i)
	{
		res[i] = scalar * vec[i];
	}
	return res;
}

double get_tau(double n_e)
{
	double ratio = n_e / 8.0e26;
	return tau_0 * (1.0 * ratio * ratio);
}

double get_C_carrier(double n_carrier)
{
	return 1.5 * n_carrier * kB;
}

double laser_intensity(double t)
{
	double term = (t - t_peak) / T_sigma;
	return I_0 * std::exp(-term * term);
}

StateVector system_ode(double t, const StateVector& U)
{
	double n_e = std::max(U[0], 1.0e20);
	double n_h = std::max(U[1], 1.0e20);
	double T_e = std::max(U[2], 300.0);
	double T_h = std::max(U[3], 300.0);
	double T_l = std::max(U[4], 300.0);

	double I = laser_intensity(t);
	double tau = get_tau(n_e);

	// Carrier generation / recombination
	double dn_dt = (alpha_0 * I) / (hbar * omega_0) + 
		(beta_0 * I * I) / (2.0 * hbar * omega_0) -
		gamma_e * n_e * n_e * n_h - gamma_h * n_h * n_h * n_e +
		0.5 * (theta_e * n_e + theta_h * n_h);

	// Heat capacity
	double C_e = std::max(get_C_carrier(n_e), 1.0e-5);
	double C_h = std::max(get_C_carrier(n_h), 1.0e-5);

	// Electron temerature change
	double dT_e_dt = (1.0 / C_e) * (
			m_r_e * (alpha_0 * I + beta_0 * I * I) +
			Eg * gamma_e * n_e * n_e * n_h -
			(C_e / tau) * (T_e - T_l) -
			dn_dt * (m_r_e * Eg + 1.5 * kB * T_l)
			);

	// Hole temperature change
	double dT_h_dt = (1.0 / C_h) * (
			m_r_h * (alpha_0 * I + beta_0 * I * I) +
			Eg * gamma_h * n_h * n_h * n_e -
			(C_h / tau) * (T_h - T_l) -
			dn_dt * (m_r_h * Eg + 1.5 * kB * T_h)
			);

	// Lattice temperature change
	double dT_l_dt = (1.0 / C_l) * (
			(C_e / tau) * (T_e - T_l) +
			(C_h / tau) * (T_h - T_l)
			);

	return {dn_dt, dn_dt, dT_e_dt, dT_h_dt, dT_l_dt};
}
