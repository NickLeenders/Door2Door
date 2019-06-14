# -*- coding: utf-8 -*-



#taking loading due to braking as 0.75=0/75g



import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.insert(0, '../Airframe/')
from masses_cg_positions import *
from total_masses import total_mass

sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import wing_vals, emp_vals, aero_vals

sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import wing_vals, emp_vals, aero_vals

sys.path.insert(0, '../Structure/')
from mass_calculation import *

sys.path.insert(0, '../ControlStability/')
from OEW_CG import *


x_cg = function_XCG()
z_cg = function_ZCG()

g = 9.80665
acc = 0.25 * g #acc take-off 2.16 m/s^2
decc = 0.3 * g #aircraft brake at 0.2 

a = x_cg - x_positions().x_wheel_fr
b = x_positions().x_wheel_bk - x_cg 
c = z_cg
mass = mass_iteration(1600)

#a=dist to front wheels from cg
#b=""   to back wheel ""
#c=vertical distance to cg
#x= force on front wheel

def wheel_loading(a,b,c,mass,brake_g,acc_g):
    w = 3*mass[-1] * g
    #moments = weight * c + y * b - x * a
    x_load_decc = ((c*decc*mass[-1])+w*b)/(a+b)
    y_load_decc = w - x_load_decc
    x_load_acc = ((-c*acc*mass[-1])+w*b)/(a+b)
    y_load_acc = w - x_load_acc
    loads_front = [x_load_acc, x_load_decc]
    loads_back = [y_load_acc, y_load_decc]
    #acceleration g
    return(loads_front, loads_back)
   

frontloads = wheel_loading(a,b,c,mass,brake_g,acc_g)[0] 

backloads =  wheel_loading(a,b,c,mass,brake_g,acc_g)[1]

allowable_displacement = 0.075    

def spring_constant(frontloads,backloads,displacement):
    maxfront = max(frontloads)
    maxback = max(backloads)
    
    return(((maxfront/2)/displacement), (maxback/displacement))

print(spring_constant(frontloads,backloads,allowable_displacement))
   
