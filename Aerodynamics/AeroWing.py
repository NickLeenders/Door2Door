import sys
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals
sys.path.insert(0, '../Airframe/')
from masses_cg_positions import x_positions, z_positions, w_components

Masstotal= w_components().MTOW
Ws_cr=Masstotal*9.80665 #N
We_cr= #N

h= aero_vals().h

#variables
sweepquart=0 #deg
taper=1 #-
dihedral=0 #deg
twist=0 #deg/m
vflow_takeoff=  #m/s
vflow_cr=  #m/s
clmax=1.5

b= 4.4 #m
c= 1.2 #m
######

# ISA
def ISA(h, R, lapse, g, T0, rho0):
    T_cr=T0-lapse*h
    rho_cr=rho0*(T_cr/T0)**(g/(lapse*R)-1)
    return(T_cr, rho_cr)
######

# Extra velocities and q's
v_takeoff=vflow+vinf_takeoff
v_cr=vflow+vinf_cr
q0=0.5*rho0*v_takeoff**2
q_cr=0.5*rho_cr*v_cr**2
#####

# Sreq and design cl
Sreq=Ws_cr/(q0*cl_max)
cl_des=0.5*(Ws_cr+We_cr)/(q_cr*Sreq)
#####

# Mach and Reynolds
Mach_takeoff=v_takeoff/((gamma*R*T0)**0.5)
Re_takeoff=rho0*v_takeoff*c/mu

Mach_cr=v_cr/((gamma*R*T_cr)**0.5)
Re_cr=rho_cr*v_cr*c/mu
#####

cd_cr=0.05

wingdrag= q_cr*Sreq*cd_cr
print(wingdrag)