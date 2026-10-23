#include "FileReader.hpp"
#include <vector>

#ifndef SPLINE_HELPERS_HPP
#define SPLINE_HELPERS_HPP

struct SplineCoefficients
{
	double a{0.0};
	double b{0.0};
	double c{0.0};
	double d{0.0};
	double x{0.0};	// Left endpoint of interval
};

class Spline
{
public:
	//Spline() = default;
	Spline(const FileData& data);

	void build(const FileData& data);
	double sample(double target_x) const;

private:
	std::vector<SplineCoefficients> coeffs_;
	std::vector<double> x_arr_;
};

#endif
