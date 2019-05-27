#Python to output the scissor plot

import sys
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals

def control_curve():
    sh_over_s = 1/((aero_vals().cl_h/aero_vals().cl_a_minus_h)*(aero_vals().l_h/aero_vals().chord)*aero_vals().vh_over_v) - ()/()

def create_plot():
    pass
