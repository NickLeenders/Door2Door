from math import *
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../Airframe/')
sys.path.insert(0, '../Aerodynamics/')
sys.path.insert(0, '../PowerElectrical/')
from aerodynamic_parameters import aero_vals, wing_vals, emp_vals
from masses_cg_positions import x_positions, z_positions
from OEW_CG import function_XCG, function_ZCG
from aero import Propellers
from power import ThrustCalculator


#Parameters Required For Calculation


g = 9.80665
Iyy = 10750
theta_dot_dot = 12/57.3
mu = 0.04

m = 1668

dCLflap = 0.5
CL0 = 0.24
CD0to = 0.038

Cm0 = 0.05
aw = 2
ih = -1
nh = 0.96
be_bh = 1.0


Cruise_t = ThrustCalculator(1930, 34.1, 36.10, 58.27,  0.0, 1.0, 0, 1.1, 1)
Cruise_l = Propellers(Cruise_t.thrust, Cruise_t.velocity,
                                Cruise_t.rho, Cruise_t.aero_vals.cl_cr, 0)#update weight value
T = Cruise_l.thrustCP + Cruise_l.thrustHLP

xmg = x_positions().x_wheel_bk
xcg = function_XCG()
xach = x_positions().x_tail - (0.7456*aero_vals().x_ac)
xacwf = aero_vals().mac_position+(wing_vals().MAC*aero_vals().x_ac)
zd = function_ZCG()
zmg = z_positions().z_drivetrain
zt = z_positions().z_propeller
zcg = function_ZCG()
h = zt
h0 = zcg

print ('xmg', xmg)
print ('xcg', xcg)
print ('xach', xach)
print ('xacwf', xacwf)
print ('zd', zd)
print ('zmg', zmg)
print ('zt', zt)
print ('zcg', zcg)

def elevator_sizing():
    # Calculation

    k = 1/(pi*wing_vals().e*wing_vals().A)
    CLc = 2*m*g/(aero_vals().rho_cr*aero_vals().vinfcr**2*wing_vals().S)
    CLto = CLc + dCLflap
    CDto = CD0to + k*CLto**2

    Dto = 0.5*aero_vals().rho0*aero_vals().vstall**2*wing_vals().S*CDto
    Lto = 1.1*m*g

    Macwf = 0.5*aero_vals().rho0*aero_vals().vstall**2*aero_vals().cm_ac*wing_vals().S*wing_vals().MAC

    Ff = mu*(m*g - Lto)
    a = (T-Dto-Ff)/m

    #Calculation pitching moments in the take-off rotation

    Mw = -m*g*(xmg-xcg)
    Md = Dto*(zd-zmg)
    Mt = -T*(zt-zmg)
    Mlwf = Lto*(xmg-xacwf)
    Ma = m*a*(zcg-zmg)

    print ('Mw', Mw)
    print ('macw', Macwf)
    print('Md', Md)
    print('Mt', Mt)
    print('Mlwf', Mlwf)
    print('Ma', Ma)

    Lh = (Mlwf + Macwf + Ma + Mw + Md + Mt - Iyy*theta_dot_dot)/(xach-xmg)

    print ('Lh', Lh)
    print ('IyyThetadotdot', Iyy*theta_dot_dot)

    CLh = (2*Lh)/(aero_vals().rho0*aero_vals().vstall**2*emp_vals().S_h)
    e0 = (2*CLto/(pi*wing_vals().A))*57.3
    deda = (2*aero_vals().cl_alpha_a_minus_h/(pi*wing_vals().A))
    e = (e0/57.3 + deda*aw/57.3) * 57.3

    print ('CLh', CLh)
    print ('e0', e0)
    print ('deda', deda)
    print ('e', e)


    ah = aw + ih - e
    te = (ah/57.3+(aero_vals().cl_h/aero_vals().cl_alpha_h))/(emp_vals().elevator_max_defl)
    ce_ch = (te*sqrt(0.7)/(0.8))**2

    print ('ah', ah)
    print ('te', te)
    print ('ce/ch', ce_ch)


    Vh = (aero_vals().l_h*emp_vals().S_h)/(wing_vals().S*wing_vals().MAC)
    Cmde = -aero_vals().cl_alpha_h*nh*Vh*be_bh*te
    CLde = aero_vals().cl_alpha_h*nh*(emp_vals().S_h/wing_vals().S)*be_bh*te
    CLhde = aero_vals().cl_alpha_h*te

    print ('Vh', Vh)
    print ('Cmde', Cmde)
    print ('CLde', CLde)
    print ('CLhde', CLhde)

    Cma = aero_vals().cl_alpha_a_minus_h*((xcg-xacwf)/wing_vals().MAC) - (aero_vals().cl_alpha_h*nh*(emp_vals().S_h/wing_vals().S)*(aero_vals().l_h/wing_vals().MAC)*(1-deda))
    q = 0.5*aero_vals().rho0*aero_vals().vinfcr**2
    CL1 = (2*m*g)/(aero_vals().rho0*aero_vals().vinfcr**2*wing_vals().S)

    print ('Cma', Cma)
    print ('q', q)
    print ('CL1', CL1)

    de = (-((((-T*(zt-zcg)/(q*wing_vals().S*wing_vals().MAC)) + Cm0)*aero_vals().cl_alpha_a_minus_h + (CL1-CL0)*Cma)/(aero_vals().cl_alpha_a_minus_h*Cmde - Cma*CLde)))*57.3

    Vc_list = np.arange(1,187,1)
    q_list_sea = []
    q_list_cruise = []
    CL1_list_sea = []
    CL1_list_cruise = []
    for i in range(len(Vc_list)):
        q_list_sea.append(0.5*aero_vals().rho0*Vc_list[i]**2)
        CL1_list_sea.append((2*m*g)/(aero_vals().rho0*Vc_list[i]**2*wing_vals().S))

    for i in range(len(Vc_list)):
        q_list_cruise.append(0.5*aero_vals().rho_cr*Vc_list[i]**2)
        CL1_list_cruise.append((2*m*g)/(aero_vals().rho_cr*Vc_list[i]**2*wing_vals().S))

    de_list_sea = []
    de_list_cruise = []

    for j in range(len(q_list_sea)):
        de1 = (-((((-T*(zt-zcg)/(q_list_sea[j]*wing_vals().S*wing_vals().MAC)) + Cm0)*aero_vals().cl_alpha_a_minus_h + (CL1_list_sea[j]-CL0)*Cma)/(aero_vals().cl_alpha_a_minus_h*Cmde - Cma*CLde))) * 57.3
        de_list_sea.append(de1)

    for j in range(len(q_list_cruise)):
        de1 = (-((((-T*(zt-zcg)/(q_list_cruise[j]*wing_vals().S*wing_vals().MAC)) + Cm0)*aero_vals().cl_alpha_a_minus_h + (CL1_list_cruise[j]-CL0)*Cma)/(aero_vals().cl_alpha_a_minus_h*Cmde - Cma*CLde))) * 57.3
        de_list_cruise.append(de1)


    plt.plot(Vc_list, de_list_sea)
    plt.plot(Vc_list, de_list_cruise)
    plt.xlabel('Velocity (m/s)')
    plt.ylabel(r'$\delta_E (deg)$')
    plt.xlim(0,70)
    plt.ylim(-25, 3)
    plt.gca().invert_yaxis()
    plt.grid()
    plt.gca().legend(('Sea level', 'Cruise altitude'), loc=2)
    #plt.title("Variation of elevator deflection with respect to aircraft velocity")
    plt.show()

print (elevator_sizing())