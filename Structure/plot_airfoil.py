import numpy as np 
import csv
import matplotlib.pyplot as plt
import scipy.interpolate as spin


def wingbox(frontsparheight, backsparheight):
	#Import and read data of airfoil
	with open('naca633618-il.csv', 'r') as f:
		point = np.array(list(csv.reader(f, delimiter=',')))
		
		x_coordinates = [float(x[0]) for x in point]
		y_coordinates = [float(x[1]) for x in point] 
	
	#Interpolate lower part airfoil
	ius = spin.InterpolatedUnivariateSpline(x_coordinates[25:51], y_coordinates[25:51])
	xi = np.arange(0,1150,1)
	ylower = ius(xi)
	
	#reverse data point, otherwise interpolation wont work
	x_coordinates = x_coordinates[::-1]
	y_coordinates = y_coordinates[::-1]
	
	#Interpolate upper part 
	ius = spin.InterpolatedUnivariateSpline(x_coordinates[25:51], y_coordinates[25:51])
	yupper = ius(xi)
	
	#Determine height of the spars of the wingbox and frontspar location
	height = [x for x in ((0 - ylower) + yupper)]

	for i in xi:
		a = height[i] - frontsparheight
		
		if a >= 0:
			Frontsparlocation = i
			break

	#Determine Backspar location of the wingbox using same height as frontspar
	for i in xi[::-1]:
		a = height[i] - backsparheight
		
		if a >= 0:
			Backsparlocation = i
			break

	#Determine width of the wingbox
	Width = xi[Backsparlocation] - xi[Frontsparlocation] 

	#Determine middle spar for fastening is the spar with maximum height
	Middlesparlocation = np.argmax(height)

	Middlesparheight = (yupper[np.argmax(height)] + (0 - ylower[np.argmax(height)]))

	#Determine Airfoil contour size 
	contour = 0
	for i in xi[1:]:
		delta_x = xi[i] - xi[i-1]
		delta_ylower = ylower[i] - ylower[i-1]
		delta_yupper = yupper[i] - yupper[i-1]

		a = np.sqrt((delta_ylower*delta_ylower)+(delta_x*delta_x)) + np.sqrt((delta_yupper*delta_yupper)+(delta_x*delta_x))
		
		contour = contour + a

	#Plot figure 
	plt.figure(num=None, figsize=(10, 2), dpi=125, facecolor='w', edgecolor='k')
	plt.axis([-50,1200,-90,160])
	plt.scatter(x_coordinates,y_coordinates)
	plt.plot(xi,ylower, 'y')
	plt.plot(xi,yupper, 'y')
	plt.plot((xi[Frontsparlocation], xi[Frontsparlocation]), (ylower[Frontsparlocation], yupper[Frontsparlocation]), 'k-')
	plt.plot((xi[Backsparlocation], xi[Backsparlocation]), (ylower[Backsparlocation], yupper[Backsparlocation]), 'k-')
	plt.plot((xi[Middlesparlocation], xi[Middlesparlocation]), (ylower[Middlesparlocation], yupper[Middlesparlocation]), 'k-')

	#Horizontal lines in airfoil
	plt.plot(xi[Frontsparlocation:Backsparlocation],ylower[Frontsparlocation:Backsparlocation], 'k')
	plt.plot(xi[Frontsparlocation:Backsparlocation],yupper[Frontsparlocation:Backsparlocation], 'k')

	#For plotting square wingbox
	#plt.plot((xi[Frontsparlocation], xi[Backsparlocation]), (ylower[Frontsparlocation], ylower[Backsparlocation]), 'k-')
	#plt.plot((xi[Frontsparlocation], xi[Backsparlocation]), (yupper[Frontsparlocation], yupper[Backsparlocation]), 'k-')
	
	#For plotting maximum height line
	#plt.plot((xi[np.argmax(height)], xi[np.argmax(height)]), (ylower[np.argmax(height)], yupper[np.argmax(height)]), 'k-')
	plt.show()

	#return values important
	print 'width',Width, 'mm'
	print 'space for motor and shaft', Frontsparlocation, 'mm'
	return Width, Middlesparheight, contour

#Fibre orientation is 0 / 30 / -30 / 0 degrees (the 30degrees Modulus is taken from Gurit pdf)

def YoungsModulusLayer(E_fibre, E_honey, Nr_layers, Fibre_thick):
	#E_fibre youngs modulus fibre in line with fibres
	#E_honey youngs modulus of honeycomb material
	#Nr_layers is defined as the amount of layers on each side of the honeycomb
	#Fibre and Honeycomb thickness in mm

	#VolumeHoney = Honeycomb_thick / ((Nr_layers * Fibre_thick * 2.) + Honeycomb_thick)
	VolumeFibre = (Nr_layers * Fibre_thick * 2.) / ((Nr_layers * Fibre_thick * 2.)) #+ Honeycomb_thick)

	E_Panel = ((0.238 * E_fibre * VolumeFibre) + (E_fibre * VolumeFibre)) / 2 #+ (E_honey * VolumeHoney)
	return format(E_Panel, '.2f')


def MassOfComposite(Density, Fibre_thick, Nr_layers, frontsparheight, backsparheight):
	#Area_wingbox_ribs = 
	#Nr_ribs

	wingb = wingbox(frontsparheight, backsparheight)
	Area_wingbox_spars = 3.2 * (frontsparheight + backsparheight + wingb[1]) 
	Area_airfoil = wingb[2] * 3.2 

	Area_wingbox = Area_airfoil + (Area_wingbox_spars) #+ (Area_wingbox_ribs * Nr_ribs)

	Mass = Nr_layers * Fibre_thick * Area_wingbox * Density

	return int(Mass)


print 'Youngs Modulus =', YoungsModulusLayer(141.5, 4.61e-5, 4, 1), 'GPa'

print 'Mass', MassOfComposite(1.55, 0.5, 4, 180.0, 180.0), 'gram'


