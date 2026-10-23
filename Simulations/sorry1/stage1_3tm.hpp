#ifndef STAGE1_3TM_ODE_HPP
#define STAGE1_3TM_ODE_HPP

#include <vector>
#include <cmath>

// Physical constants
constexpr double e = 1.602176634e-19;
constexpr double hbar = 1.054571817e-34;
constexpr double kB = 1.380649e-23;
constexpr double c = 2.99792458e8;

// Laser parameters
constexpr double wavelength = 775e-9;
constexpr double omega_0 = 2.0 * M_PI * c / wavelength;
constexpr double tp = 350e-15;
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

// State vector [n_e, n_h, T_e, T_h, T_l]
using StateVector = std::vector<double>;

// Operator overload
StateVector operator+(const StateVector& a, const StateVector& b);
StateVector operator*(double scalar, const StateVector& vec);

// Helper functions
double get_tau(double n_e);
double get_C_carrier(double n_carrier);
double laser_intensity(double t);

// 3TM differential equations
StateVector system_ode(double t, const StateVector& U);

#endif
