#include <string>

#ifndef SETTINGS_HPP
#define SETTINGS_HPP

struct FileSettings
{
	std::string heat_cap_file;
	std::string ep_coupling_file;
};

struct SimulationSettings
{
	double t_start{0.0};
	double t_end{10e-12};
	double dt{1e-15};

	double Dt_start{0.0};
	double Dt_end{1e-12};
	double dDt{1e-13};

	std::string out_file{"output.dat"};
};

#endif
