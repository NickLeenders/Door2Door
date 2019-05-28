from math import *
import numpy as np
#Program for determinig the aileron size
import sys
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals

def aileron_sizing():
    Cr = (3*aero_vals().chord*(1+aero_vals().taper_ratio))/(2*(1 + aero_vals().taper_ratio + aero_vals().taper_ratio**2))

    clda1 = (2*aero_vals().cl_a*aero_vals().aileron_effectiveness*Cr)/(aero_vals().surface_area*aero_vals().wingspan)
    clda2 = (aero_vals().aileron_outer_pos**2/2 + (2*(aero_vals().taper_ratio - 1)*aero_vals().aileron_outer_pos**3)/(3*aero_vals().wingspan)) - \
            (aero_vals().aileron_inner_pos**2/2 + (2*(aero_vals().taper_ratio - 1)*aero_vals().aileron_inner_pos**3)/(3*aero_vals().wingspan))
    clda = clda1*clda2

    clp1 = (-4*(aero_vals().cl_a - aero_vals().cd_zero)*Cr)/(aero_vals().surface_area*aero_vals().wingspan**2)
    clp2 = ((aero_vals().wingspan*0.5)**3/3) + 0.5*((aero_vals().taper_ratio - 1)/aero_vals().wingspan)*(aero_vals().wingspan/2)**4
    clp = clp1*clp2

    P = -clda/clp*aero_vals().aileron_max_defl*(2*aero_vals().cruise_speed/aero_vals().wingspan)

    t = aero_vals().roll_rate/P

    return clda, clp, P, t
