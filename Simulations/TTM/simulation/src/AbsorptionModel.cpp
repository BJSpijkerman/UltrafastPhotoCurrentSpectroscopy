#include "AbsorptionModel.hpp"

double getSource(double t, double Dt, const SourceParameters& params)
{
	double arg_1 = (t - params.T0) / params.SIGMA_t;
	double arg_2 = (t - params.T0 - Dt) / params.SIGMA_t;
	return params.S01 * std::exp(-0.5 * arg_1 * arg_1);// + params.S02 * std::exp(-0.5 * arg_2 * arg_2);
}
