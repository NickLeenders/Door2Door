from math import *
import numpy as np
import matplotlib.pyplot as plt

#Parameters Required For Calculation

defl_max = -25

g = 9.80665
Iyy = 150000
theta_dot_dot = 12/57.3

e = 0.88
A = 8
m = 20000
Vc = 360*0.5144
Pc = 0.549
P0 = 1.225
S = 70
Sh = 16
lh = 11.3 + 0.5
C = 2.96
Vs = 43.73
Vr = Vs
mu = 0.04
T = 56000

dCLflap = 0.5
CL0 = 0.24
CD0to = 0.038
Cmacwf = 0.05
CLa = 5.7
CLaw = 5.7
CLawf = CLaw
CLah = 4.3
Cm0 = 0.05
aw = 2
ih = -1
nh = 0.96
be_bh = 1.0

xmg = 1.1
xcg = 0.0
xach = 11.3
xacwf = 0.8
zd = 1.9
zt = 2.0
zt1 = -0.3
zcg = 1.7
h = 0.8
h0 = 0.5

# Calculation

k = 1/(pi*e*A)
CLc = 2*m*g/(Pc*Vc**2*S)
CLto = CLc + dCLflap
CDto = CD0to + k*CLto**2

Dto = 0.5*P0*Vr**2*S*CDto
Lto = 0.5*P0*Vr**2*S*CLto

Macwf = 0.5*P0*Vr**2*Cmacwf*S*C

Ff = mu*(m*g - Lto)
a = (T-Dto-Ff)/m

#Calculation pitching moments in the take-off rotation

Mw = -m*g*(xmg-xcg)
Md = Dto*(zd)
Mt = -T*(zt)
Mlwf = Lto*(xacwf)
Ma = m*a*(zcg)

Lh = (Mlwf + Macwf + Ma + Mw + Md + Mt - Iyy*theta_dot_dot)/xach

CLh = (2*Lh)/(P0*Vr**2*Sh)
e0 = (2*CLto/(pi*A))*57.3
deda = (2*CLaw/(pi*A))
e = (e0/57.3 + deda*aw/57.3) * 57.3

ah = aw + ih - e
te = (ah/57.3+(CLh/CLah))/(defl_max/57.3)
ce_ch = (te*sqrt(0.7)/(0.8))**2

Vh = (lh*Sh)/(S*C)
Cmde = -CLah*nh*Vh*be_bh*te
CLde = CLah*nh*(Sh/S)*be_bh*te
CLhde = CLah*te


Cma = CLawf*((h-h0)/C) - (CLah*nh*(Sh/S)*(lh/C)*(1-deda))
q = 0.5*P0*Vc**2
CL1 = (2*m*g)/(P0*Vc**2*S)

de = -((((T*zt1/(q*S*C)) + Cm0)*CLa + (CL1-CL0)*Cma)/(CLa*Cmde - Cma*CLde))

#plot
Vc_list = np.arange(1,187,1)
q_list = []
CL1_list = []
for i in range(len(Vc_list)):
    q_list.append(0.5*P0*Vc_list[i]**2)
    CL1_list.append((2*m*g)/(P0*Vc_list[i]**2*S))


Vc_list_knot1 = np.array(Vc_list)/0.5144
de_list = []

for j in range(len(q_list)):
    de1 = (-((((T*zt1/(q_list[j]*S*C)) + Cm0)*CLa + (CL1_list[j]-CL0)*Cma)/(CLa*Cmde - Cma*CLde))) * 57.3
    de_list.append(de1)

plt.plot(Vc_list_knot1, de_list)
plt.xlim(50,360)
plt.ylim(-25, 3)
plt.show()