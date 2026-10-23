#include "stage1_3tm.hpp"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <algorithm>


int main()
{
	double t_max = 10.0e-12;
	double dt = 0.1e-15;
	size_t time_steps = static_cast<size_t>(t_max / dt);

	// Initial conditions
	double n_intrinsic = 1.5e16;
	StateVector U = {n_intrinsic, n_intrinsic, 300.0, 300.0, 300.0};

	std::ofstream outFile("3tm_stage1_output.csv");
	outFile << "time_ps,n_e_cm3,T_e_K,T_h_K,T_l_K\n";

	std::cout << "Start Fase 1 Simulation (" << time_steps << " steps)...\n";

	for (size_t step = 0; step < time_steps; ++step)
	{
		double t = step * dt;

		if (step % 100 == 0)
		{
			double time_ps = t * 10e12;
			double n_e_cm3 = U[0] * 1.0e-6;
			outFile << std::scientific << std::setprecision(6)
				<< time_ps << "," << n_e_cm3 << ","
				<< U[2] << "," << U[3] << "," << U[4] << "\n";
		}

		// 4-th order Runge-Kutta step
		StateVector k1 = system_ode(t, U);
		StateVector k2 = system_ode(t + 0.5 * dt, U + (0.5 * dt) * k1);
		StateVector k3 = system_ode(t + 0.5 * dt, U + (0.5 * dt) * k2);
		StateVector k4 = system_ode(t + dt, U +  dt * k3);

		U = U + (dt / 6.0) * (k1 + (2.0 * k2) + (2.0 * k3) + k4);

		// Physical lower bounds
		U[0] = std::max(U[0], n_intrinsic);
		U[1] = std::max(U[1], n_intrinsic);
		U[2] = std::max(U[2], 300.0);
		U[3] = std::max(U[3], 300.0);
		U[4] = std::max(U[4], 300.0);
	}

	outFile.close();
	std::cout << "Simulation completed. Data save in 3tm_stage1_output.csv\n";

	return 0;
}
