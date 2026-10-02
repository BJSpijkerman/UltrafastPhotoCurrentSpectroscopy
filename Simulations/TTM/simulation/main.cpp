#include <iostream>
#include <fstream>

#include "YAMLParser.hpp"
#include "FileReader.hpp"
#include "SplineHelpers.hpp"
#include "Numerics.hpp"
#include "progressbar/progress_bar.hpp"

int main(int argc, char** argv)
{
	std::string config_path = "../../settings.yaml";
	if (argc > 1)
	{
		config_path = argv[1];
	}

	try
	{
		FileSettings file_settings;
		SourceParameters source_params;
		SimulationSettings sim_settings;

		loadConfig(config_path, file_settings, source_params, sim_settings);
		source_params.initLambertBeer();

		FileData heat_cap_data = readFile(file_settings.heat_cap_file);
		FileData ep_coupling_data = readFile(file_settings.ep_coupling_file);

		Spline heat_cap_spline(heat_cap_data);
		Spline ep_coupling_spline(ep_coupling_data);

		std::cout << "Fluence " << source_params.F_1 << " J/m^2" << std::endl;
		std::ofstream out(sim_settings.out_file);

		ProgressBar bar;
		bar.set_status_text("Running simulation.");
		bar.set_fill_bar_remainder_with("-");


		int i = 0;
		int i_max = (sim_settings.t_end - sim_settings.t_start) / sim_settings.dt;
		State state{300.0, 300.0}; // Initial Te and Tl at 300K
		for (double t = sim_settings.t_start; t <= sim_settings.t_end; t += sim_settings.dt)
		{
			if (i % 20 == 0)
			{
				out << t << " " << state.Te << " " << state.Tl << "\n";
				float progress = static_cast<float>(i) / static_cast<float>(i_max) * 100.0f;
				bar.set_progress(progress);
				bar.write_progress(std::cout);
			}
			state = rk4Step(t, state, sim_settings.dt, heat_cap_spline, ep_coupling_spline, source_params);
			i++;
		}

		std::cout << std::endl << "Simulation completed successfully. Output saved to: " << sim_settings.out_file << std::endl;
	}
	catch (const std::exception& e)
	{
		std::cerr << "Simulation Error: " << e.what() << std::endl;
		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}
