from math import *
import matplotlib.pyplot as plt

m = 1558.              # Take-off mass in kg
Sto = 500.0            # Take-off length in M set by requirement
t = 30.                # Take-off time
Vstall = 30.
Vto = 1.2 * Vstall     #
g = 9.81
rho_s = 1.225          # air density in kg/m^3 at sealevel
m = 1558               # takeoff weight in kg
u = 0.025              # rolling resitance
b = 8.8                # span in m
c = 1.2                # chord in m
e = 0.85
S = b * c              # wing area # in m^2
A = b ** 2 / S
a = 2.0 * Sto / (t ** 2) # acceleration in m/s^2
K = 1 / (pi * A * e)
Cd = 0.027

CLg = u / (2 * K)
Cdg = Cd +K*CLg**2

T = m * a + (0.027 + K * CLg ** 2) * 0.5 * rho_s * Vto ** 2 * S + 0.025 * (CLg * 0.5 * rho_s * Vto * S - m*g) #in N


A1 = g * (T0 / m * g - u)
B1 = g / (m * g) * (0.5 * rho_s * S * (CDg - u * CLg))
S1 = 1 / (2 * B) * log(A / (A - B * Vto ** 2))



