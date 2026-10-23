#ifndef SIMULATION_STATE_HPP
#define SIMULATION_STATE_HPP

struct State
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

inline State operator*(double scalar, const State& state)
{
	return state * scalar;
}

#endif
