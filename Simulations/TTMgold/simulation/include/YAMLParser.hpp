#include <string>
#include "Settings.hpp"
#include "AbsorptionModel.hpp"

#ifndef YAML_PARSER_HPP
#define YAML_PARSER_HPP

void loadConfig(const std::string& cfg_name,
		FileSettings& f_settings,
		SourceParameters& source_params,
		SimulationSettings& simulation_settings);

#endif
