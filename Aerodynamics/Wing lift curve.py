import math
import numpy
import matplotlib.pyplot as plt

M_inf= 0.24
A= 8.8/1.08
eta= 0.95
sweep= 0.91144687 * math.pi / 180

beta=math.sqrt(1-M_inf**2)
slope=(2*math.pi*A)/(2+math.sqrt(4+((A*beta)/eta)**2*(1+(math.tan(sweep/beta**2))**2)))
slope2= slope*math.pi/180+0.02372
CLmax=1.575
astal=(CLmax/slope-(+4*math.pi/180))*(180/math.pi)

print "hoi", astal
print slope2

#alphalist=numpy.arange(-4,astal,0.5)
#y=slope2*alphalist
#x=alphalist
x1=[-5,10,13,13.5,14, 14.621,15,15.5]
y1=[-0.18,1.2,1.476,1.5, 1.52, 1.575,1.476, 1.2]

x= [-5,10,13, 13.5, 14 ,14.25, 14.5, 14.621, 14.741, 14.85, 15,15.5]
y = [-0.18,1.2,1.476, 1.516, 1.561, 1.569, 1.574, 1.575, 1.574, 1.570, 1.566 , 1.495]
x2= [-5,10,13, 13.5, 14 ,14.25, 14.5, 14.621, 14.741, 14.85, 15,15.5]
y2= [0.08,1.5,1.776, 1.816, 1.861, 1.869, 1.874, 1.875, 1.874, 1.870, 1.866 , 1.795]
print(x)
print(y)
z=numpy.polyfit(x,y,5)
p=numpy.poly1d(z)
plt.plot(x,p(x))
plt.plot(x2,y2)
plt.ylabel('CL [-]')
plt.xlabel('alpha [deg]')
plt.xlim()
plt.show()