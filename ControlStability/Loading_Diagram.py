from math import *
from OEW_CG import *

x_fuel = 0.5
x_payload = [2.51, 2.71]

w_fuel = 90
w_payload = [80, 270]

seat_pitch = 0.2

mass = []
CG_range_fb = []
CG_range_bf = []

for i in range(len(x_payload)):
    CG_new = 0

    CG_new = (function_OEW_CG()*function_total_EOW_mass() + CG_new + x_payload[i]*w_payload[i])/(function_total_EOW_mass() + CG_new + w_payload[i])
    CG_range_fb.append(CG_new)

print CG_range_bf







