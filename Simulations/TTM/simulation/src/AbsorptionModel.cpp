#include "AbsorptionModel.hpp"

double getSource(double t, const SourceParameters& params)
{
	double arg_1 = (t - params.T0) / params.SIGMA_t;

	return params.S01 * std::exp(-0.5 * arg_1 * arg_1);
}
