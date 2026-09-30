#include "YAMLParser.hpp"
#include <yaml-cpp/yaml.h>

void loadConfig(const std::string& cfg_name,
		FileSettings& f_settings,
		SourceParameters& source_config,
		SimulationSettings& simulation_settings)
{
	YAML::Node cfg = YAML::LoadFile(cfg_name);

	f_settings.heat_cap_file = cfg["MaterialFiles"]["heat_capacity_file"].as<std::string>();
	f_settings.ep_coupling_file = cfg["MaterialFiles"]["ep_coupling_file"].as<std::string>();

	source_config.tau = cfg["SourceSettings"]["tau"].as<double>() * 1e-15;
	source_config.Power = cfg["SourceSettings"]["Power"].as<double>();
	source_config.f_rep = cfg["SourceSettings"]["f_rep"].as<double>();
	source_config.thickness = cfg["SourceSettings"]["thickness"].as<double>() * 1e-9;
	source_config.T0 = cfg["SourceSettings"]["t_0"].as<double>() * 1e-12;
	source_config.w01 = cfg["SourceSettings"]["w01"].as<double>() * 1e-3;
	source_config.w02 = cfg["SourceSettings"]["w02"].as<double>() * 1e-3;
	source_config.Dp = cfg["SourceSettings"]["penetration_depth"].as<double>() * 1e-9;

	simulation_settings.t_start = cfg["SimulationSettings"]["t_start"].as<double>() * 1e-12;
	simulation_settings.t_end = cfg["SimulationSettings"]["t_end"].as<double>() * 1e-12;
	simulation_settings.dt = cfg["SimulationSettings"]["dt"].as<double>() * 1e-15;
	simulation_settings.Dt_start = cfg["SimulationSettings"]["Dt_start"].as<double>() * 1e-12;
	simulation_settings.Dt_end = cfg["SimulationSettings"]["Dt_end"].as<double>() * 1e-12;
	simulation_settings.dDt = cfg["SimulationSettings"]["dDt"].as<double>() * 1e-15;
}
