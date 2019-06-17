import math
import numpy
import matplotlib.pyplot as plt

cd0=0.055133
k=0.040858857



y=numpy.arange(-0.5, 1.5,0.01)
#x=numpy.arange(-0.5, 1.5,0.01)


x=cd0+k*(y-0.1)**2


#y=cd0+k*(x-0.1)**2

print(x)
print(y)
plt.plot(x,y)
plt.ylabel('CL [-]')
plt.xlabel('CD [-]')
plt.xlim()
plt.show()