#ifndef ABSORPTION_MODEL_HPP
#define ABSORPTION_MODEL_HPP

struct LaserParameters
{
	double wavelength;
	double tau_pulse;
	double laser_power;
	double f_rep;
	double T_0;
	double w0;
}:


class LaserSource
{
public:

	LaserSource(const LaserParameters& laser_params);
	~LaserSource() = default;

	void initLambertBeer(void);
	double getSource(double t);

private:
	double wavelength;
	double omega_0;
	double tau_pulse;
	double T_sigma;
	double t_peak;
	double fluence;
	double I_0;
	double T_0;
	double laser_power;
	double w0;
};

#endif
