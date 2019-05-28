from numpy import *
m = 1558.
g = 9.81
W = m*g
H = 914.4
t = 120.
rho = 1.225
RC = H/t
CD0 = 0.07
b = 8.8
c = 1.2
S = b*c
A = b**2/S
e = 0.85
K = 1/(pi*A*e)


CLopt = sqrt(3*CD0*pi*A*e)
CD = CD0+K*CLopt**2
Vopt = sqrt(2*W/(rho*S*CLopt))

Pa = RC*W + CD*0.5*rho*Vopt**3*S

print (Pa)