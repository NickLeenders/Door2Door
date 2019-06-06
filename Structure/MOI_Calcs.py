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


def moi_calc(n_stiff,h,w):
    top_stiff = n_stiff/2
    A_stiff = 0.00006
    t_skin = 0.008
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
        for k in range (len (x_dist)):
            
    else:
        while i < (top_stiff-1)/2:
            xdst = (i+1) * spacing
            x_dist.append(xdst)
            i = i+1
    moi_z = 0
    


a = moi_calc(22,3,15)