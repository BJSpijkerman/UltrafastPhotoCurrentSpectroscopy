

#ifndef SILICON_HPP
#define SILICON_HPP

struct MaterialParameters
{
	double m_e_coeff;
	double m_h_coeff;
	double alpha_0;
	double beta_0;
	double gamma_e;
	double gamma_h;
	double theta_e;
	double theta_h;
};


class Silicon
{
public:

	Silicon(const MaterialParameters& material_params);
	~Silicon() = default;

	double getTau(double n_e);
	double getCCarrier(double n_carrier);
	
	double m_e_eff;
	double m_h_eff;
	double alpha_0;
	double beta_0;
	double gamma_e;
	double gamma_h;
	double theta_e;
	double theta_h;
	double C_l = 1.63e6;
	double tau_0 = 240e-15;
};
