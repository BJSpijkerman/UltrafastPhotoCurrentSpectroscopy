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

		std::cout << "sigma_t " << source_params.SIGMA_t << std::endl;
		std::cout << "Fluence " << source_params.F_1 << std::endl;
		std::cout << "Power density / V " << source_params.S01 << std::endl;
		std::ofstream out(sim_settings.out_file);

		ProgressBar bar;
		bar.set_status_text("Running simulation.");
		bar.set_fill_bar_remainder_with("-");

		int k = 0;
//		int total_steps = static_cast<int>(std::abs(sim_settings.Dt_end - sim_settings.Dt_start) / sim_settings.dDt);

//		for (double Dt = sim_settings.Dt_start; Dt <= sim_settings.Dt_end; Dt += sim_settings.dDt)
//		{
			int i = 0;
			State state{300.0, 300.0}; // Initial Te and Tl at 300K
			for (double t = sim_settings.t_start; t <= sim_settings.t_end; t += sim_settings.dt)
			{
				if (i % 20 == 0)
				{
					out << t << " " << state.Te << " " << state.Tl << "\n";
				}
				state = rk4Step(t, 0.0, state, sim_settings.dt, heat_cap_spline, ep_coupling_spline, source_params);
				i++;
			}
//			if (k % 20 == 0)
//			{
//				float progress = (static_cast<float>(k) / (total_steps - 1)) * 100.0f;
//				bar.set_progress(progress);
//				bar.write_progress(std::cout);
//			}
//			k++;
//		}
		std::cout << std::endl << "Simulation completed successfully. Output saved to: " << sim_settings.out_file << std::endl;
	}
	catch (const std::exception& e)
	{
		std::cerr << "Simulation Error: " << e.what() << std::endl;
		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}
