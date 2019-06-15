from math import *
import numpy as np


import sys
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals, wing_vals

def aileron_sizing():
    Cr = (3*wing_vals().MAC*(1+wing_vals().taper_ratio))/(2*(1 + wing_vals().taper_ratio + wing_vals().taper_ratio**2))

    clda1 = (2*aero_vals().cl_alpha_a_minus_h*wing_vals().aileron_effectiveness*Cr)/(wing_vals().S*wing_vals().b)
    clda2 = (wing_vals().aileron_outer_pos**2/2 + (2*(wing_vals().taper_ratio - 1)*wing_vals().aileron_outer_pos**3)/(3*wing_vals().b)) - \
            (wing_vals().aileron_inner_pos**2/2 + (2*(wing_vals().taper_ratio - 1)*wing_vals().aileron_inner_pos**3)/(3*wing_vals().b))
    clda = clda1*clda2

    clp1 = (-4*(aero_vals().cl_alpha_a_minus_h - aero_vals().cd0)*Cr)/(wing_vals().S*wing_vals().b**2)
    clp2 = ((wing_vals().b*0.5)**3/3) + 0.5*((wing_vals().taper_ratio - 1)/wing_vals().b)*(wing_vals().b/2)**4
    clp = clp1*clp2

    P = -clda/clp*wing_vals().aileron_max_defl*(2*aero_vals().vinfcr/wing_vals().b)

    t = aero_vals().roll_rate/P

    print ('Cr:',Cr)
    print ('clda:',clda)
    print ('clp:', clp)
    print ('P:',P)
    print ('t:', t)

    return clda, clp, P, t

print (aileron_sizing())
