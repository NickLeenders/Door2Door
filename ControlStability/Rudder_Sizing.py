import numpy as np
import sys
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals

b_R_b_v = 0.7 #ratio between rudder span and vertical tail span (source)
d_R_left = 30 #[degrees]
d_R_right = -30 #[degrees]
V_min_contr = 0.8*aero_vals().vstall #[m/s] minimal controllable speed, 0.8 safety factor (source)


print (V_min_contr)

