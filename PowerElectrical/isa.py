import sys

def IsaCalculator(altitude):
    """"Returns: density, temperature, pressure"""

    rho0 = 1.225
    T0 = 298.15
    p0 = 101325
    g0 = 9.80665
    M = 0.0289644
    R = 8.3144598
    if (altitude <= 11000):
        lapse = -0.0065
        rho = rho0 * (T0 / (T0 + lapse * altitude))**(1 + g0*M/(R*lapse))
        p = p0 * (T0 / (T0 + lapse * altitude))**(g0*M/(R*lapse))
        T = T0 + lapse*altitude
    else:
        sys.stderr.write("Only suitable for troposphere (altitudes up to 11000 m)")
        p = 22632.10
        T = 216.65
        rho = 0.36391
    return rho, T, p

