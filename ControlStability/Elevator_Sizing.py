from math import *
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../Airframe/')
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals, wing_vals


#Parameters Required For Calculation

defl_max = -25

g = 9.80665
Iyy = 1825
theta_dot_dot = 12/57.3
mu = 0.04
T = 3927.303

m = 1930
Sh = 9.5288*0.24

dCLflap = 0.5
CL0 = 0.24
CD0to = 0.038

Cm0 = 0.05
aw = 2
ih = -1
nh = 0.96
be_bh = 1.0

xmg = 5.0
xcg = 2.5544
xach = 4.73
xacwf = 2.511
zd = 1.037
zmg = 0.15
zt = 1.7
zcg = 1.037
h = 1.7
h0 = 1.037

def elevator_sizing():
    # Calculation

    k = 1/(pi*wing_vals().e*wing_vals().A)
    CLc = 2*m*g/(aero_vals().rho_cr*aero_vals().vinfcr**2*wing_vals().S)
    CLto = CLc + dCLflap
    CDto = CD0to + k*CLto**2

    Dto = 0.5*aero_vals().rho0*aero_vals().vstall**2*wing_vals().S*CDto
    #Lto = 0.5*aero_vals().rho0*aero_vals().vstall**2*wing_vals().S*CLto
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

    Lh = (Mlwf + Macwf + Ma + Mw + Md + Mt - Iyy*theta_dot_dot)/(xach-xmg)

    print (Lh)

    CLh = (2*Lh)/(aero_vals().rho0*aero_vals().vstall**2*Sh)
    e0 = (2*CLto/(pi*wing_vals().A))*57.3
    deda = (2*aero_vals().cl_alpha_a_minus_h/(pi*wing_vals().A))
    e = (e0/57.3 + deda*aw/57.3) * 57.3
    # print (CLh)
    # print (e0)
    # print (deda)
    # print (e)


    ah = aw + ih - e
    te = (ah/57.3+(aero_vals().cl_h/aero_vals().cl_alpha_h))/(defl_max/57.3)
    ce_ch = (te*sqrt(0.7)/(0.8))**2
    # print(ah)
    print (te)
    print (ce_ch)

    Vh = (aero_vals().l_h*Sh)/(wing_vals().S*wing_vals().MAC)
    Cmde = -aero_vals().cl_alpha_h*nh*Vh*be_bh*te
    CLde = aero_vals().cl_alpha_h*nh*(Sh/wing_vals().S)*be_bh*te
    CLhde = aero_vals().cl_alpha_h*te

    # print (Vh)
    # print (Cmde)
    # print (CLde)
    # print (CLhde)


    Cma = aero_vals().cl_alpha_a_minus_h*((xcg-xacwf)/wing_vals().MAC) - (aero_vals().cl_alpha_h*nh*(Sh/wing_vals().S)*(aero_vals().l_h/wing_vals().MAC)*(1-deda))
    q = 0.5*aero_vals().rho0*aero_vals().vinfcr**2
    CL1 = (2*m*g)/(aero_vals().rho0*aero_vals().vinfcr**2*wing_vals().S)
    # print (Cma)
    # print (q)
    # print (CL1)
    de = (-((((-T*(zt-zcg)/(q*wing_vals().S*wing_vals().MAC)) + Cm0)*aero_vals().cl_alpha_a_minus_h + (CL1-CL0)*Cma)/(aero_vals().cl_alpha_a_minus_h*Cmde - Cma*CLde)))*57.3
    # print (de)

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

    Vc_list_knot1 = np.array(Vc_list)/0.5144
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
    plt.xlabel('Speed (m/s)')
    plt.ylabel(r'$\delta_E (deg)$')
    plt.xlim(0,70)
    plt.ylim(-40, 3)
    plt.grid()
    plt.gca().legend(('Sea level', 'Cruise altitude'), loc=6)
    plt.title("Variation of elevator deflection with respect to aircraft speed")
    plt.show()

print (elevator_sizing())