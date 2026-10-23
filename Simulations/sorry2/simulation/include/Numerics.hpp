#include <algorithm>
#include "StateVector.hpp"

#ifndef NUMERICS_HPP
#define NUMERICS_HPP

StateVector system_ode(double t, const StateVector& U, const Silicon& Si);

StateVector rk4Step(double& t, const double dt, const StateVector& U, const Silicon& Si);

#endif
