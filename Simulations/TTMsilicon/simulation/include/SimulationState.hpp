#ifndef SIMULATION_STATE_HPP
#define SIMULATION_STATE_HPP

struct TemperatureState
{
	double Te{0.0};
	double Tl{0.0};

	State operator+(const State& other) const
	{
		return {Te + other.Te, Tl + other.Tl};
	}

	State operator*(double scalar) const
	{
		return {Te * scalar, Tl * scalar};
	}
};

inline TemperatureState operator*(double scalar, const State& state)
{
	return state * scalar;
}

struct DielectricState
{
	double real;
	double imag;
};

struct SimulationState
{
	TemperatureState Temp;
	DielectricState eps;
	double n;
};

#endif
