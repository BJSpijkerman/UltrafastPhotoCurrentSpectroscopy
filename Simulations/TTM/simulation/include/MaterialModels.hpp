#include "SplineHelpers.hpp"

#ifndef MATERIAL_MODELS_HPP
#define MATERIAL_MODELS_HPP

inline double getCe(double Te, const Spline& heat_cap_spline)
{
	double T = Te * 1e-4;
	return heat_cap_spline.sample(T) * 1e5;
}

inline double getCl(double Tl)
{
	return 2.5e6;
}

inline double getG(double Te, const Spline& ep_coupling_spline)
{
	double T = Te * 1e-4;
	return ep_coupling_spline.sample(T) * 1e17;
}

#endif
