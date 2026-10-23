#include "SimulationState.hpp"


#ifndef NUMERICS_HPP
#define NUMERICS_HPP

TemperatureState temperatureDerivatives(double t,
		const TemperatureState& y,
		double n,
		const SourceModel& source_model);

TemperatureState TemperatureRK4Step(double t,
		const TemperatureState& y,
		double dt,
		const SourceModel& source_model);

double carrierKR4Step(double t,
		double n,
		double dt,
		const SourceModel& source_model);

double dielectricRK4Step(double t
		const Dielectric& eps,
		const TemperatureState& T,
		double n,
		double dt);

#endif
