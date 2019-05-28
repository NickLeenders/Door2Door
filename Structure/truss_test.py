import numpy as np
import sys
sys.path.insert(0, '../Airframe/')
from masses_cg_positions import x_positions, z_positions, w_components
#Info
L_sf = 4.9 
H_sf = 1.5
H_tail = 1
x_w = 2.8
x_ss_start = 0.5
H_nose = 0.7
##NODE LOCATIONS
n1 = [0,0]
n2 = [n1[0]+ x_w - x_ss_start , 0]
n3 = [(L_sf - n2[0])/2 + n2[0] , 0]
n4 = [L_sf , 0]
n5 = [n4[0] , H_tail]
n6 = [n3[0] , n5[1] + 0.1]
n7 = [n2[0] , H_sf]
n8 = [n1[0] , H_nose]

#FORCES

M_fuel = w_components().w_fuel
M_cell = 63
M_tank = 109
M_Frontpass = 90
M_Rearpass = 90*3
M_ElecM = 120
M_Emp = 21
M_Wing = 360

a = [[1 , 1],[0,n4[0]-n1[0]]]

b = [[(M_fuel+M_cell+M_tank+M_Frontpass+M_Rearpass+M_ElecM+M_Emp+M_Wing)*9.81],\
      [M_Wing*9.81*(n7[0]-n1[0])+M_Rearpass*9.81*(n2[0]-n1[0])+(M_Emp+M_ElecM)*(9.81*(n4[0]-n1[0]))]]

c = np.linalg.solve(a,b)

def truss_forces:
    t1 = M_fuel/2 + M_cell/2 + M_tank/2 + M_frontpass/2 - 
    
