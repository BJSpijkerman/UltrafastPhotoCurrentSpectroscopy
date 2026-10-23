#include "Numerics.hpp"
#include "MaterialModels.hpp"

State systemDerivatives(double t,
		const State& y,
		const Spline& heat_cap_model,
		const Spline& ep_coupling_model,
		const SourceParameters& source_params)
{
	double Ce = getCe(y.Te, heat_cap_model);
	double Cl = getCl(y.Tl);
	double G  = getG(y.Te, ep_coupling_model);
	double S  = getSource(t, source_params);

	double dTe_dt = (-G * (y.Te - y.Tl) + S) / Ce;
	double dTl_dt = ( G * (y.Te - y.Tl)) / Cl;

	return {dTe_dt, dTl_dt};
}


State rk4Step(double t,
		const State& y,
		double dt,
		const Spline& heat_cap_model,
		const Spline& ep_coupling_model,
		const SourceParameters& source_params)
{
	State k1 = systemDerivatives(t, y, heat_cap_model, ep_coupling_model, source_params);
	State k2 = systemDerivatives(t + 0.5 * dt, y + (0.5 * dt) * k1, heat_cap_model, ep_coupling_model, source_params);
	State k3 = systemDerivatives(t + 0.5 * dt, y + (0.5 * dt) * k2, heat_cap_model, ep_coupling_model, source_params);
	State k4 = systemDerivatives(t + dt, y + dt * k3, heat_cap_model, ep_coupling_model, source_params);

	return y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4);
}
