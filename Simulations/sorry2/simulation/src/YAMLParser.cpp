#include "YAMLParser.hpp"
#include <yaml-cpp/yaml.h>

void loadConfig(const std::string* cfg_name);
{
	SimulationSettings settings;
	YAML::Node cfg = YAML::LoadFile(cfg_name)

	settings.laser_params.wavelength = cfg["Laser_Parameters"]["wavelength"].as<double>() * 1e-9;
	settings.laser_params.tau_pulse = cfg["Laser_Parameters"]["tau_pulse"].as<double>() * 1e-15;
	settings.laser_params.laser_power = cfg["Laser_Parameters"]["laser_power"].as<double>();
	settings.laser_params.f_rep = cfg["Laser_Parameters"]["f_rep"].as<double>();
	settings.laser_params.T_0 = cfg["Laser_Parameters"]["T_0"].as<double>() * 1e-12;
	settings.laser_params.w0 = cfg["Laser_Parameters"]["T_0"].as<double>() * 1e-3;

	settings.material_params.m_e_coeff = cfg["Material_Parameters"]["m_e_coeff"].as<double>();
	settings.material_params.m_h_coeff = cfg["Material_Parameters"]["m_h_coeff"].as<double>();
	settings.material_params.alpha_0 = cfg["Material_Parameters"]["alpha_0"].as<double>();
	settings.material_params.beta_0 = cfg["Material_Parameters"]["beta_0"].as<double>();
	settings.material_params.gamma_e = cfg["Material_Parameters"]["gamma_e"].as<double>();
	settings.material_params.gamma_h = cfg["Material_Parameters"]["gamma_h"].as<double>();
	settings.material_params.theta_e = cfg["Material_Parameters"]["theta_e"].as<double>();
	settings.material_params.theta_h = cfg["Material_Parameters"]["theta_h"].as<double>();

	return settings;
}
