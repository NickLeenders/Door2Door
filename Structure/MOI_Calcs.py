import numpy as np
import sys
sys.path.insert(0, '../Airframe/')
from masses_cg_positions import x_positions, z_positions, w_components
from mass_calculation import mass_iteration
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import *
from aero import drag, Propellers
sys.path.insert(0, '../PowerElectrical/')
import power
import matplotlib.pyplot as plt


def moi_calc(n_stiff,h,w,t):
    top_stiff = n_stiff/2
    A_stiff = 0.00006
    t_skin = t
    y_dst = h/2
    moi_z = (A_stiff * h/2 * h/2 * n_stiff) + (h/2 * h/2 * t_skin * w) + (1/12 * t_skin * h*h*h)
    spacing = w / (top_stiff-1)
    x_dist = []
    i=0
    if top_stiff % 2 ==0:
        
        while i < top_stiff/2:
            if i == 0:
                xdst = spacing/2
                x_dist.append(xdst)
                i=i+1
            else:
                xdst = x_dist[i-1] + spacing
                x_dist.append(xdst)
                i=i+1
    else:
        while i < (top_stiff-1)/2:
            xdst = (i+1) * spacing
            x_dist.append(xdst)
            i = i+1
    moi_x = (w/2 * w/2 * t_skin * h*2) + (2/12 * t_skin * w * w * w)
    for k in range(len(x_dist)):
        moi_add = x_dist[k] * x_dist[k] * A_stiff * 4
        moi_x  = moi_x + moi_add
    return moi_z , moi_x
    


a = moi_calc(,0.15,0.8,0.008)