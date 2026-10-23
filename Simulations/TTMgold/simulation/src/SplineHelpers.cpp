#include "SplineHelpers.hpp"
#include <algorithm>
#include <stdexcept>

Spline::Spline(const FileData& data)
{
	build(data);
}

void Spline::build(const FileData& data)
{
	size_t n = data.x.size();
	if (n < 2 || data.x.size() != data.y.size())
	{
		throw std::invalid_argument("Insuffucient or mismathced data size for cubic spline construction.");
	}

	x_arr_ = data.x;
	size_t num_intervals = n - 1;
	coeffs_.resize(num_intervals);

	std::vector<double> h(num_intervals);
	for (size_t i = 0; i < num_intervals; ++i)
	{
		h[i] = data.x[i + 1] - data.x[i];
	}

	std::vector<double> alpha(n, 0.0);
	for (size_t i = 1; i < num_intervals; ++i)
	{
		alpha[i] = (3.0 / h[i]) * (data.y[i + 1] - data.y[i]) - (3.0 / h[i -1]) * (data.y[i] - data.y[i - 1]);
	}

	std::vector<double> l(n, 0.0), mu(n, 0.0), z(n, 0.0), c(n, 0.0);
	l[0] = 1.0;

	for (size_t i = 1; i < num_intervals; ++i)
	{
		l[i] = 2.0 * (data.x[i + 1] - data.x[i - 1]) - h[i - 1] * mu[i - 1];
		mu[i] = h[i] / l[i];
		z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i];
	}

	l[num_intervals] = 1.0;

	for (int j = static_cast<int>(num_intervals) - 1; j >= 0; --j)
	{
		c[j] = z[j] - mu[j] * c[j + 1];
	}

	for (size_t i = 0; i < num_intervals; ++i)
	{
		coeffs_[i].x = data.x[i];
		coeffs_[i].a = data.y[i];
		coeffs_[i].b = (data.y[i + 1] - data.y[i]) / h[i] - h[i] * (c[i + 1] + 2.0 * c[i]) / 3.0;
		coeffs_[i].c = c[i];
		coeffs_[i].d = (c[i + 1] - c[i]) / (3.0 * h[i]);
	}
}


double Spline::sample(double target_x) const
{
	// Ensure spline is initialized
	if (coeffs_.empty() || x_arr_.empty()) return 0.0;

	size_t num_intervals = coeffs_.size() - 1;

	// Clamp lower bound
	if (target_x <= x_arr_.front())
	{
//		double dx = target_x - coeffs_[0].x;
		return coeffs_[0].a;
	}

	// Clamp Upper bound
	if (target_x >= x_arr_.back())
	{
		size_t last = num_intervals - 1;
//		double dx = target_x - coeffs_[last].x;
		return coeffs_[last].a;
	}

	// Binary search for interior parts
	auto it = std::lower_bound(x_arr_.begin(), x_arr_.end(), target_x);
	size_t idx = std::distance(x_arr_.begin(), it);

	if (idx > 0)
	{
		idx -= 1;	// Step back to get left side of interval
	}

	double dx = target_x - coeffs_[idx].x;
	return coeffs_[idx].a + coeffs_[idx].b * dx + coeffs_[idx].c * dx * dx + coeffs_[idx].d * dx * dx * dx;
}
