import sys
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals
sys.path.insert(0, '../Airframe/')
#from masses_cg_positions import x_positions, z_positions, w_components
sys.path.insert(0, '../PowerElectrical/')
from power import ThrustCalculator
from aero import Propellers

Masstotal= 1600 #w_components().MTOW
Ws_cr=Masstotal*9.80665 #N
We_cr= 0#N

rho0=1.225
h= aero_vals().h


#variables
sweepquart=0 #deg
taper=1 #-
dihedral=0 #deg
twist=0 #deg/m
vflow_takeoff=0  #m/s
vflow_cr= 0 #m/s
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
#q0=0.5*rho0*v_takeoff**2
#q_cr=0.5*rho_cr*v_cr**2
#####

# Sreq and design cl
#Sreq=Ws_cr/(q0*cl_max)
#cl_des=0.5*(Ws_cr+We_cr)/(q_cr*Sreq)
#####

# Mach and Reynolds
#Mach_takeoff=v_takeoff/((gamma*R*T0)**0.5)
#Re_takeoff=rho0*v_takeoff*c/mu

#Mach_cr=v_cr/((gamma*R*T_cr)**0.5)
#Re_cr=rho_cr*v_cr*c/mu
#####

#TO
takeOff_t = ThrustCalculator(28, 0.0, 1500 / 2.5, 0, 0.8, 1)
takeOff_l = Propellers(takeOff_t.thrust, takeOff_t.velocity,
                                takeOff_t.rho, takeOff_t.cl, 1)

#CRUISE
Cruise_t = ThrustCalculator(69.4, h, 1500, 0, 0.8, 0)
Cruise_l = Propellers(Cruise_t.thrust, Cruise_t.velocity,
                                Cruise_t.rho, Cruise_t.cl, 0)


print(takeoff_1.v_wakeHLP)
print(takeoff_1.v_wakeCP)
print('next')
print(Cruise_1.v_wakeHLP)
print(Cruise_1.v_wakeCP)

#cd_cr=0.05
#wingdrag= q_cr*Sreq*cd_cr
#print(wingdrag)