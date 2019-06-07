import numpy as np
import sys
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals
sys.path.insert(0, '../Aerodynamics/')
from aero import Propellers
sys.path.insert(0, '../PowerElectrical/')
from power import ThrustCalculator
sys.path.insert(0, '../Airframe/')
from masses_cg_positions import y_positions

b_R_b_v = 0.7 #ratio between rudder span and vertical tail span (source)
d_R_left = 30 #[degrees]
d_R_right = -30 #[degrees]
V_min_contr = 0.8*aero_vals().vstall #[m/s] minimal controllable speed, 0.8 safety factor (source)
Cruise_t = ThrustCalculator(1928.0, aero_vals().vinfcr, aero_vals().h, 400000.0/aero_vals().vinfcr)
Cruise_l = Propellers(Cruise_t.thrust, Cruise_t.velocity,
                                Cruise_t.rho, Cruise_t.aero_vals.cl_cr, 0)

T_per_CP = Cruise_l.thrustCP/Cruise_l.numberCP #Thrust per cruise propeller
T_per_HLP = Cruise_l.thrustHLP/Cruise_l.numberHLP #Thrust per HLP

T_CP_one = T_per_CP * 0.5* Cruise_l.numberCP
T_HLP_one = T_per_HLP * 0.5 * Cruise_l.numberHLP

N_A = T_per_HLP *y_positions().y_prop_position[0] +  T_per_HLP *y_positions().y_prop_position[1] + T_per_HLP *y_positions().y_prop_position[2] + T_per_HLP *y_positions().y_prop_position[3]+  T_per_CP*y_positions().y_prop_position[-1]


print (T_per_CP)
print(T_per_HLP)
print (N_A)
#N_A = #Na= -TLyt

