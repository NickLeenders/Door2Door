import numpy as np
import sys
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals, emp_vals, wing_vals
from aero import Propellers
sys.path.insert(0, '../PowerElectrical/')
from power import ThrustCalculator
from isa import IsaCalculator
sys.path.insert(0, '../Airframe/')
from masses_cg_positions import y_positions

def rudder_sizing():

    S_v_effective = 0.92*emp_vals().S_v
    b_R_b_v = 0.54 #ratio between rudder span and vertical tail span (source)
    b_R = b_R_b_v*emp_vals().b_v #[m] rudder span
    d_R_left = 30 #[degrees]
    d_R_right = -30 #[degrees]
    l_v_cgaft = 2.18
    l_v_cgfwd = 2.29


    V_min_contr = 0.8*aero_vals().vstall #[m/s] minimal controllable speed, 0.8 safety factor (source)
    [rho,T,p] =IsaCalculator(aero_vals().h) #isa conditions during cruise
    q = 0.5*aero_vals().vinfcr**2*rho #dynamic pressure
    q_v = 0.5*aero_vals().vinfcr**2*rho*0.8 #TODO find out what this is
    eta_v = q_v/q #ratio between the dynamic pressures
    V_v = S_v_effective*l_v_cgaft/(wing_vals().b*wing_vals().S) #vertical tail volume
    C_L_a_v = 4.5 #1/rad #TODO find this value


    Cruise_t = ThrustCalculator(1930, aero_vals().vinfcr, aero_vals().vinfcr, aero_vals().vinfcr, aero_vals().h, 400000.0/aero_vals().vinfcr)
    Cruise_l = Propellers(Cruise_t.thrust, Cruise_t.velocity,
                                    Cruise_t.rho, Cruise_t.aero_vals.cl_cr, 0)#update weight value

    T_per_CP = Cruise_l.thrustCP/Cruise_l.numberCP #Thrust per cruise propeller
    T_per_HLP = Cruise_l.thrustHLP/Cruise_l.numberHLP #Thrust per HLP

    N_A =-1* (T_per_HLP *y_positions().y_prop_position[0] +  T_per_HLP *y_positions().y_prop_position[1] + T_per_HLP *y_positions().y_prop_position[2] + T_per_HLP *y_positions().y_prop_position[3]+  T_per_CP*y_positions().y_prop_position[-1])
    C_n_dr= N_A/(q*wing_vals().S*wing_vals().b*np.radians(d_R_left))
    tau_R = C_n_dr/(-C_L_a_v*V_v*eta_v*b_R_b_v) #angle of attack effectiveness of the rudder, if this is larger than 1, return to step 1
    C_R_C_v = (tau_R*np.sqrt(0.7)/0.8)**2 #if this is larger than 0.5, use fully movable tail C_R/C_v=1 #TODO this is an assumed value, should follow from tau_R and figure 12.12
    C_R = C_R_C_v*emp_vals().c_v #[m], rudder chord
    A_R = C_R*b_R #[m^2], rudder area

    print ('NA',N_A)
    print ('Cndr',C_n_dr)
    print ('cr/cv',C_R_C_v)
    print ('tau_r',tau_R)
    print ("The chord of the rudder is: ", C_R, "[m]")
    print ("The span of the rudder is: ", b_R, "[m]")
    print ("The area of the rudder is: ", A_R, "[m^2]")

    return C_R, b_R, A_R

print (rudder_sizing())