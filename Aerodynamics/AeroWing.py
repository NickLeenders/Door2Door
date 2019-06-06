import sys
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals, wing_vals
sys.path.insert(0, '../Airframe/')
#from masses_cg_positions import x_positions, z_positions, w_components
sys.path.insert(0, '../PowerElectrical/')
from power import ThrustCalculator
from aero import Propellers, drag

Masstotal= 1928.0 #w_components().MTOW
Ws_cr=Masstotal*9.80665 #N
We_cr=(Masstotal-90)*9.80665 #N


h= aero_vals().h



#variables
sweepquart=0 #deg
taper=1 #-
dihedral=0 #deg
twist=0 #deg/m
cl_max=1.5 #1.5 #1.85
cd=0.018 #0.018 #0.032

b= 8.8 #m
c= 1.083#m
######

# ISA
#def ISA(h, R, lapse, g, T0, rho0):
#    T_cr=T0-lapse*h
#    rho_cr=rho0*(T_cr/T0)**(g/(lapse*R)-1)
#    return(T_cr, rho_cr)
######

rho_cr=aero_vals().rho_cr
T_cr=aero_vals().T_cr


vtakeoff=39 #
vcruise=69.4 #
vstall=vtakeoff/1.2

#TO
takeOff_t = ThrustCalculator(1928.0, vstall, 0.0, 0.5, 0, 1.1, 1)
takeOff_l = Propellers(takeOff_t.thrust, takeOff_t.velocity,
                                takeOff_t.rho, takeOff_t.aero_vals.cl_takeoff, 1)

#CRUISE
Cruise_t = ThrustCalculator(1928.0, vcruise, h, 400000.0/69.4)
Cruise_l = Propellers(Cruise_t.thrust, Cruise_t.velocity,
                                Cruise_t.rho, Cruise_t.aero_vals.cl_cr, 0)


v_takeoff= 0.173*takeOff_l.v_wakeCP+0.524*takeOff_l.v_wakeHLP+0.313*vtakeoff
v_cr= 0.173*Cruise_l.v_wakeCP+0.524*Cruise_l.v_wakeHLP+0.313*vcruise

#print(takeOff_l.v_wakeHLP)
#print(takeOff_l.v_wakeCP)
#print(v_takeoff)

#print('next')
#print(Cruise_l.v_wakeHLP)
#print(Cruise_l.v_wakeCP)
#print(v_cr)





#Mach and Reynolds
Mach_takeoff=v_takeoff/((aero_vals().gamma*aero_vals().R*aero_vals().T0)**0.5)
Re_takeoff=aero_vals().rho0*v_takeoff*c/aero_vals().mu

Mach_cr=v_cr/((aero_vals().gamma*aero_vals().R*T_cr)**0.5)
Re_cr=rho_cr*v_cr*c/aero_vals().mu
#####



# Extra velocities and q's
q0=0.5*aero_vals().rho0*v_takeoff**2
q_cr=0.5*rho_cr*v_cr**2
#####

# Sreq and design cl
Sreq=Ws_cr/(q0*cl_max)
cl_des=0.5*(Ws_cr+We_cr)/(q_cr*Sreq)
#####

#print(v_takeoff)
print('########## Sreq and cl_des')
print(Sreq)
print(cl_des)

#print(Re_cr/(10**6), 'Million')
#print(Mach_cr)

#print(rho_cr)
#print(aero_vals().mu/rho_cr)
#cd_cr=0.05
#wingdrag= q_cr*Sreq*cd_cr
#print(wingdrag)




#drag=0.5*1.09*v_cr**2*Sreq*cd
drag=drag(0,0,0,0,0,0,0)
print(drag)
print(wing_vals().taper_ratio, wing_vals().MAC)