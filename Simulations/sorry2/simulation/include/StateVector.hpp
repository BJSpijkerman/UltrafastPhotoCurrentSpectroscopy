#include <vector>

#ifndef STATE_VECTOR_HPP
#define STATE_VECTOR_HPP

using StateVector std::vector<double>;

// Operator overload for adding state vectors
StateVector operator+(const StateVector& a, const StateVector& b)
{
	StateVector res(a.size());
	for (size_t i = 0; i < a.size(); ++i)
	{
		res[i] = a[i] + b[i];
	}
	return res;
}


// Operator overload for multiplying state vectors
StateVector operator*(double scalar, const StateVector& vec)
{
	StateVector res(vec.res());
	for (size_t i = 0; i < vec.size(); ++i)
	{
		res[i] = scalar * vec[i];
	}
	return res;
}

#endif
