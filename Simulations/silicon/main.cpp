#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iomanip>
#include <fstream> // Required for file stream output

struct SiliconParams {
    const double k_B = 1.380649e-23;
    const double hbar = 1.0545718e-34;
    const double m_e = 9.109383e-31;
    const double m_eff = 0.32 * m_e;

    const double hnu = 2.48e-19;
    const double E_g = 1.79e-19;

    double n_0 = 1.0e22;
    double gamma = 3.8e-43;
    double theta = 0.0;

    double C_l = 1.6e6;
    double k_l = 148.0;
    double k_c = 10.0;
    double G = 1.0e17;

    double R = 0.32;
    double alpha = 1000.0;
};

double computeCc(double Tc, double n, const SiliconParams& mat) {
    double Fermi_energy = (std::pow(mat.hbar, 2.0) / (2.0 * mat.m_eff)) 
                        * std::pow(3.0 * M_PI * M_PI * n, 2.0 / 3.0);
    double C_classical = 1.5 * n * mat.k_B;
    double ratio = (M_PI * M_PI * mat.k_B * Tc) / (3.0 * Fermi_energy);
    return C_classical * std::sqrt(1.0 + ratio * ratio);
}

struct LaserParams {
    double fluence = 50.0;
    double t_p = 100.0e-15;
    double t_0 = 300.0e-15;
};

double laserSource(double x, double t, const SiliconParams& mat, const LaserParams& laser) {
    if (t < 0) return 0.0;
    double temporal = std::exp(-4.0 * std::log(2.0) * std::pow((t - laser.t_0) / laser.t_p, 2.0));
    double spatial = (1.0 - mat.R) * mat.alpha * std::exp(-mat.alpha * x);
    double I_0 = laser.fluence / (laser.t_p * std::sqrt(M_PI / (4.0 * std::log(2.0))));
    return I_0 * spatial * temporal;
}

int main() {
    SiliconParams Si;
    LaserParams Laser;

    const double L = 5.0e-6;
    const int Nx = 200;
    const double dx = L / (Nx - 1);
    const double t_final = 5.0e-12;

    std::vector<double> n(Nx, Si.n_0);
    std::vector<double> Tc(Nx, 300.0);
    std::vector<double> Tl(Nx, 300.0);

    std::vector<double> n_new(Nx, Si.n_0);
    std::vector<double> Tc_new(Nx, 300.0);
    std::vector<double> Tl_new(Nx, 300.0);

    double Cc_initial = computeCc(300.0, Si.n_0, Si);
    double dt = 0.2 * (dx * dx * Cc_initial) / (2.0 * std::max(Si.k_c, Si.k_l));
    const int Nt = static_cast<int>(t_final / dt);

    // 1. Open CSV Stream for Surface Temporal Dynamics (x = 0 over time)
    std::ofstream time_file("surface_vs_time.csv");
    time_file << "time_ps,n_surface_m3,Tc_surface_K,Tl_surface_K,Cc_surface\n";

    // Frequency of output stream writes (saving every 10 steps to reduce file size)
    const int write_stride = 10;

    for (int step = 0; step < Nt; ++step) {
        double current_time = step * dt;

        // Stream surface state (x = 0) at regular step intervals
        if (step % write_stride == 0) {
            double Cc_surface = computeCc(Tc[0], n[0], Si);
            time_file << (current_time * 1e12) << ","
                      << n[0] << ","
                      << Tc[0] << ","
                      << Tl[0] << ","
                      << Cc_surface << "\n";
        }

        for (int i = 0; i < Nx; ++i) {
            double x = i * dx;

            double d2Tc_dx2 = 0.0;
            double d2Tl_dx2 = 0.0;
            if (i > 0 && i < Nx - 1) {
                d2Tc_dx2 = (Tc[i + 1] - 2.0 * Tc[i] + Tc[i - 1]) / (dx * dx);
                d2Tl_dx2 = (Tl[i + 1] - 2.0 * Tl[i] + Tl[i - 1]) / (dx * dx);
            } else if (i == 0) {
                d2Tc_dx2 = 2.0 * (Tc[1] - Tc[0]) / (dx * dx);
                d2Tl_dx2 = 2.0 * (Tl[1] - Tl[0]) / (dx * dx);
            } else if (i == Nx - 1) {
                d2Tc_dx2 = 2.0 * (Tc[Nx - 2] - Tc[Nx - 1]) / (dx * dx);
                d2Tl_dx2 = 2.0 * (Tl[Nx - 2] - Tl[Nx - 1]) / (dx * dx);
            }

            double S_laser = laserSource(x, current_time, Si, Laser);
            double G_gen = S_laser / Si.hnu;
            double R_auger = Si.gamma * std::pow(n[i], 3.0);

            double dn_dt = G_gen + (Si.theta * n[i]) - R_auger;
            n_new[i] = n[i] + dt * dn_dt;

            double Cc_current = computeCc(Tc[i], n[i], Si);
            double coupling = Si.G * (Tc[i] - Tl[i]);
            double S_auger_reheat = R_auger * Si.E_g;
            double S_photo_thermal = G_gen * (Si.hnu - Si.E_g);
            double S_carrier_total = S_photo_thermal + S_auger_reheat;

            Tc_new[i] = Tc[i] + dt * ((Si.k_c / Cc_current) * d2Tc_dx2 
                                      - (coupling / Cc_current) 
                                      + (S_carrier_total / Cc_current));

            Tl_new[i] = Tl[i] + dt * ((Si.k_l / Si.C_l) * d2Tl_dx2 
                                      + (coupling / Si.C_l));
        }

        n = n_new;
        Tc = Tc_new;
        Tl = Tl_new;
    }
    time_file.close();

    // 2. Open CSV Stream for Final Spatial Profile (all x at t = t_final)
    std::ofstream space_file("spatial_profile_final.csv");
    space_file << "x_depth_nm,n_m3,Tc_K,Tl_K\n";

    for (int i = 0; i < Nx; ++i) {
        space_file << (i * dx * 1e9) << ","
                   << n[i] << ","
                   << Tc[i] << ","
                   << Tl[i] << "\n";
    }
    space_file.close();

    std::cout << "Simulation completed successfully.\n";
    std::cout << "Results saved to 'surface_vs_time.csv' and 'spatial_profile_final.csv'.\n";

    return 0;
}
