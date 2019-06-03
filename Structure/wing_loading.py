import numpy as np
import sys
sys.path.insert(0, '../Airframe/')
from masses_cg_positions import x_positions, z_positions, w_components
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import *
import aero
from masses_cg_positions import x_positions, z_positions, w_components
sys.path.insert(0, '../PowerElectrical/')
import power

#DEFINE PARAMETERS
cruiseT = power.ThrustCalculator(69.4, 1500, 4000)
cruiseL = aero.Propellers(cruiseT.thrust, cruiseT.velocity, cruiseT.rho, cruiseT.cl)
L =(w_components().MTOW * 9.81)/(wing_vals().b - 2.4) ####LINK TO VALUE WHEN INPUT
W_w = (w_components().w_wing*9.81)/(wing_vals().b - 2.4)
T_cp = cruiseL.thrustCP / cruiseL.numberCP
T_hlp = cruiseL.thrustHLP / cruiseL.numberHLP
W_hlp = 52 #LINK THESE LATER
W_cp = 74  #LINK THESE LATER
D = ((drag(cruiseT.cd0,cruiseT.cl,wing_vals().b,wing_vals().MAC,cruiseT.e,cruiseT.velocity,cruiseT.rho))/2)/(wing_vals().b/2)


