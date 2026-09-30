#include <cmath>
#include <iostream>
#ifndef ABSORPTION_MODEL_HPP
#define ABSORPTION_MODEL_HPP

struct SourceParameters
{
	double tau{100e-15};		// Pulse duration (s)
	double SIGMA_t{100e-15};	// Calculated temporal width
	double Power{1.0};		// Laser power (W)
	double f_rep{1e3};		// Repitition rate (Hz)
	double thickness{100e-9};	// Film thickness (m)
	double R_opt{0.93};		// Optical reflectivity;
	double Dp{15e-9};		// Oprical penetration depth

	double T0{0.0};			// First pulse delay (s)
	double w01{1.0};
	double A_1{1.0};
	double F_1{0.0};
	double S01{0.0};

	double w02{1.0};
	double A_2{1.0};
	double F_2{0.0};
	double S02{0.0};

	void initThinFilm()
	{
		SIGMA_t = tau / (2.0 * std::sqrt(2.0 * std::log(2.0)));
		double E_pulse = Power / f_rep;
		F_1 = (1.0 - R_opt) * 2.0 * E_pulse / (M_PI * w01 * w01);
		S01 = F_1 / (thickness * SIGMA_t * std::sqrt(2.0 * M_PI));
		F_2 = (1.0 - R_opt) * 2.0 * E_pulse / (M_PI * w02 * w02);
		S02 = F_2 / (thickness * SIGMA_t * std::sqrt(2.0 * M_PI));
	}

	void initLambertBeer()
	{
		// ADD THIS PRINT:
		std::cout << "EXACT Dp USED: " << Dp << " m" << std::endl;
		std::cout << "tau " << tau << std::endl;
		std::cout << "R_opt " << R_opt << std::endl;
		std::cout << "Power " << Power << std::endl;
		std::cout << "f_rep " << f_rep << std::endl;
		std::cout << "w0 " << w01 << std::endl;
		std::cout << "Dp " << Dp << std::endl;
		SIGMA_t = tau / (2.0 * std::sqrt(2.0 * std::log(2.0)));
		F_1 = (1.0 - R_opt) * 2.0 * Power / (M_PI * f_rep * w01 * w01);
		S01 = F_1 / (Dp * SIGMA_t * std::sqrt(2.0 * M_PI));
		std::cout << S01 << std::endl;
//		F_2 = (1.0 - R_opt) * 2.0 * Power / (M_PI * f_rep * w02 * w02);
//		S02 = F_2 / (Dp * SIGMA_t * std::sqrt(2.0 * M_PI));
	}
};

double getSource(double t, double Dt, const SourceParameters& params);

#endif
