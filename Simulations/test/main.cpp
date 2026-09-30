#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <iomanip>

// Physical Constants for Gold (SI units)
constexpr double GAMMA = 70.0;       // J / (m^3 * K^2)
constexpr double C_L   = 2.5e6;      // J / (m^3 * K)
constexpr double G0    = 2.6e16;     // W / (m^3 * K)

// Laser Source Parameters
constexpr double TAU   = 100e-15;    // Pulse FWHM (100 fs)
// Convert FWHM to Gaussian standard deviation: sigma = tau / sqrt(8 * ln(2))
const double SIGMA     = TAU / (2.0 * std::sqrt(2.0 * std::log(2.0)));
constexpr double T0    = 500e-15;    // Pulse peak time (500 fs)
constexpr double F     = 250.0;      // Absorbed fluence (J/m^2)
constexpr double D_P   = 15e-9;      // Optical penetration depth (15 nm)

// Calculated peak volumetric power density
const double S0 = F / (D_P * SIGMA * std::sqrt(2.0 * M_PI));

// High-Te electron heat capacity Ce(Te)
double get_Ce(double Te) {
    if (Te < 3000.0) {
        return GAMMA * Te;
    } else {
        // d-band contribution correction for Te >= 3000 K
        return GAMMA * Te + 1.2e-2 * std::pow(Te - 3000.0, 2.1);
    }
}

// High-Te electron-phonon coupling factor G(Te)
double get_G(double Te) {
    if (Te < 3000.0) {
        return G0;
    } else {
        // High-temperature correction
        return G0 + 1.8e10 * std::pow(Te - 3000.0, 1.8);
    }
}

// Gaussian laser pulse source term S(t)
double get_Source(double t) {
    double arg = (t - T0) / SIGMA;
    return S0 * std::exp(-0.5 * arg * arg);
}

// State vector holding [Te, Tl]
struct State {
    double Te;
    double Tl;

    State operator+(const State& other) const {
        return {Te + other.Te, Tl + other.Tl};
    }

    State operator*(double scalar) const {
        return {Te * scalar, Tl * scalar};
    }
};

// Evaluates system derivatives dY/dt = f(t, Y)
State system_derivatives(double t, const State& y) {
    double Ce = get_Ce(y.Te);
    double G  = get_G(y.Te);
    double S  = get_Source(t);

    double dTe_dt = (-G * (y.Te - y.Tl) + S) / Ce;
    double dTl_dt = ( G * (y.Te - y.Tl)) / C_L;

    return {dTe_dt, dTl_dt};
}

// Classical 4th-Order Runge-Kutta step
State rk4_step(double t, const State& y, double dt) {
    State k1 = system_derivatives(t, y);
    State k2 = system_derivatives(t + 0.5 * dt, y + k1 * (0.5 * dt));
    State k3 = system_derivatives(t + 0.5 * dt, y + k2 * (0.5 * dt));
    State k4 = system_derivatives(t + dt, y + k3 * dt);

    return y + (k1 + k2 * 2.0 + k3 * 2.0 + k4) * (dt / 6.0);
}

int main() {
    // Simulation parameters
    double t_start = 0.0;
    double t_end   = 10e-12; // 10 picoseconds
    int num_steps  = 20000;  // Fine resolution (~0.5 fs timesteps)
    double dt      = (t_end - t_start) / num_steps;

    // Initial state: room temperature (300 K)
    State state = {300.0, 300.0};
    double t = t_start;

    // Output file generation
    std::ofstream outFile("gold_ttm_results.csv");
    outFile << "Time_ps,Te_K,Tl_K\n";

    for (int step = 0; step <= num_steps; ++step) {
        // Output every 20 steps to keep CSV light
        if (step % 20 == 0) {
            outFile << std::fixed << std::setprecision(6) 
                    << (t * 1e12) << "," << state.Te << "," << state.Tl << "\n";
        }

        // Perform numerical integration step
        state = rk4_step(t, state, dt);
        t += dt;
    }

    outFile.close();
    std::cout << "Simulation finished successfully! Output written to gold_ttm_results.csv\n";

    return 0;
}
