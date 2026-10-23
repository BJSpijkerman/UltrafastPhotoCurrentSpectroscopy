#include <string>
#include "AbsorptionModel.hpp"

#ifndef YAML_PARSER_HPP
#define YAML_PARSER_HPP

struct SimulationSettings
{
	LaserParameters laser_params;
	MaterialParameters material_params;

	InitialConditions initial_cond;
};


SimulationSettings loadConfig(const std::string& cfg_name);

#endif
