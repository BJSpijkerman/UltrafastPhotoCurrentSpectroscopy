#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <algorithm>
#include <iomanip>

/*	Physical constants & Laser parameters	*/
constexpr double e = 1.602176634e-19;
constexpr double hbar = 1.054571817e-34;
constexpr double kB = 1.380649e-23;
constexpr double c = 2.99792458e8;

// Laser parameters
constexpr double wavelength = 775e-9;
constexpr double omega_0 = 2.0 * M_PI * c / wavelength;
constexpr double tp = 100e-15;
const double T_sigma = tp / (4.0 * std::sqrt(std::log(2.0)));
const double t_peak = 4.0 * T_sigma;
constexpr double fluence = 0.18 * 1e4;
const double I_0 = fluence / (std::sqrt(M_PI) * T_sigma);

// Material parameters (silicon)
constexpr double Eg = 1.12 * e;
constexpr double m_e_eff = 0.26 * 9.109383e-31;
constexpr double m_h_eff = 0.38 * 9.109383e-31;
constexpr double m_r_e = m_e_eff / (m_e_eff + m_h_eff);
constexpr double m_r_h = m_h_eff / (m_e_eff + m_h_eff);

constexpr double alpha_0 = 1.0e5;
constexpr double beta_0 = 2.0e-11;
constexpr double gamma_e = 1.0e-43;
constexpr double gamma_h = 1.0e-43;
constexpr double theta_e = 1.0e10;
constexpr double theta_h = 1.0e10;

// Heat capacity & coupling
constexpr double C_l = 1.63e6;
constexpr double tau_0 = 240e-15;

// State vector representation: [n_e, n_h, T_e, T_h, T_l]
using StateVector = std::vector<double>;

// Operator overload for StateVector arithmetic
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


// Helper functions for physics
inline double get_tau(double n_e)
{
	// Density dependent relaxation time
	double ratio = n_e / 8.0e26;
	return tau_0 * (1.0 + ratio * ratio);
}

inline double get_C_carrier(double n_carrier)
{
	// Approximate carrier heat capacity
	return 1.5 * n_carrier * kB;
}

inline double laser_intensity(double t)
{
	// Laser pulse profile
	double term = (t - t_peak) / T_sigma;
	return I_0 * std::exp(-term * term);
}

/*	3TTM equations	*/
StateVector system_ode(double t, const StateVector& U)
{
	// Safeguard floor limits to avoid non-physical numbers
	double n_e = std::max(U[0], 1.0e20);
	double n_h = std::max(U[1], 1.0e20);
	double T_e = std::max(U[2], 300.0);
	double T_h = std::max(U[3], 300.0);
	double T_l = std::max(U[4], 300.0);

	double I = laser_intensity(t);
	double tau = get_tau(n_e);

	// Carrier generation / Recombination rates
	double dn_dt = (alpha_0 * I) / (hbar * omega_0) +
		(beta_0 * I * I) / (2.0 * hbar * omega_0) -
		gamma_e * n_e * n_h -
		gamma_h * n_h * n_h * n_e + 
		0.5 * (theta_e * n_e + theta_h * n_h);

	// Heat capacities
	double C_e = std::max(get_C_carrier(n_e), 1.0e-5);
	double C_h = std::max(get_C_carrier(n_h), 1.0e-5);

	// Electron temperature rate
	double dT_e_dt = (1.0 / C_e) * (
			m_r_e * (alpha_0 * I + beta_0 * I * I) +
			Eg * gamma_e * n_e * n_e * n_h -
			(C_e / tau) * (T_e - T_l) -
			dn_dt * (m_r_e * Eg + 1.5 * kB * T_e)
			);

	// Hole temperature rate
	double dT_h_dt = (1.0 / C_h) * (
			m_r_h * (alpha_0 * I + beta_0 * I * I) +
			Eg * gamma_h * n_h * n_h * n_e -
			(C_h / tau) * (T_h - T_l) -
			dn_dt * (m_r_h * Eg + 1.5 * kB * T_h)
			);

	// Lattice temperature rate
	double dT_l_dt = (1.0 / C_l) * (
			(C_e / tau) * (T_e - T_l) +
			(C_h / tau) * (T_h - T_l)
			);

	return {dn_dt, dn_dt, dT_e_dt, dT_h_dt, dT_l_dt};
}


/*	Main integration loop (RK4)	*/
int main()
{
	double t_max = 10.0e-12;
	double dt = 0.1e-15;
	size_t time_steps = static_cast<size_t>(t_max / dt);

	// Initial state vector U [n_e0, n_h0, T_e0, T_h0, T_l]
	double n_intrinsic = 1.5e6;
	StateVector U = {n_intrinsic, n_intrinsic, 300.0, 300.0, 300.0};

	// Open file to stream results
	std::ofstream outFile("3tm_stage1_output.csv");
	outFile << "time_ps,n_e_cm3,T_e_K,T_h_K,T_l_K\n";

	std::cout << "Starting Stage 1 Simulation (" << time_steps << " steps)...\n";

	for (size_t step = 0; step < time_steps; ++step)
	{
		double t = step * dt;

		// Log output every 100 steps (~10 fs resolution)
		if (step % 100 == 0)
		{
			double time_ps = t * 1.0e12;
			double n_e_cm3 = U[0] * 1.0e-6;
			outFile << std::scientific << std::setprecision(6)
				<< time_ps << "," << n_e_cm3 << ","
				<< U[2] << "," << U[3] << "," << U[4] << "\n";
		}

		// Classical 4-th order Runge-Kutta step
		StateVector k1 = system_ode(t, U);
		StateVector k2 = system_ode(t + 0.5 * dt, U + (0.5 * dt) * k1);
		StateVector k3 = system_ode(t + 0.5 * dt, U + (0.5 * dt) * k2);
		StateVector k4 = system_ode(t + dt, U + dt * k3);

		U = U + (dt / 6.0) * (k1 + (2.0 * k2) + (2.0 * k3) + k4);

		// Enforce physical lower bounds
		U[0] = std::max(U[0], n_intrinsic);
		U[1] = std::max(U[1], n_intrinsic);
		U[2] = std::max(U[2], 300.0);
		U[3] = std::max(U[3], 300.0);
		U[4] = std::max(U[4], 300.0);
	}

	outFile.close();
	std::cout << "Simulation complete. Data saved to 3tm_stage1_output.csv\n";

	return 0;
}
