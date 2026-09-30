#include "SimulationState.hpp"
#include "SplineHelpers.hpp"
#include "AbsorptionModel.hpp"

#ifndef NUMERICS_HPP
#define NUMERICS_HPP

State systemDerivatives(double t,
		double Dt,
		const State& y,
		const Spline& heat_cap_model,
		const Spline& ep_coupling_model,
		const SourceParameters& source_params);

State rk4Step(double t,
		double Dt,
		const State& y,
		double dt,
		const Spline& heat_cap_model,
		const Spline& ep_coupling,
		const SourceParameters& source_parameters);

#endif
