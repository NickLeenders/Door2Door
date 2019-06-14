import numpy as np 
import csv
import matplotlib.pyplot as plt
import scipy.interpolate as spin
from mpl_toolkits import mplot3d
import mpl_toolkits.mplot3d.axes3d as axes3d

def wingbox(frontsparheight, backsparheight):
	#Import and read data of airfoil
	with open('naca633618-il_root.csv', 'r') as f:
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

	#Determine tip wingbox
	with open('naca633618-il_tip.csv', 'r') as f:
		point = np.array(list(csv.reader(f, delimiter=',')))
		
		x_coordinates_tip = [float(x[0]) for x in point]
		y_coordinates_tip = [float(x[1]) for x in point] 
	
	#Interpolate lower part airfoil
	ius = spin.InterpolatedUnivariateSpline(x_coordinates_tip[25:51], y_coordinates_tip[25:51])
	xi_tip = np.arange(0,1010,1)
	ylower_tip = ius(xi_tip)
	
	#reverse data point, otherwise interpolation wont work
	x_coordinates_tip = x_coordinates_tip[::-1]
	y_coordinates_tip = y_coordinates_tip[::-1]
	
	#Interpolate upper part 
	ius = spin.InterpolatedUnivariateSpline(x_coordinates_tip[25:51], y_coordinates_tip[25:51])
	yupper_tip = ius(xi_tip)


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

	#For plotting the electric motor
	plt.plot((xi[(Frontsparlocation - 2)], xi[(Frontsparlocation - 2)]), (ylower[(Frontsparlocation - 2)], yupper[(Frontsparlocation - 2)]), 'r')
	plt.plot((xi[(Frontsparlocation - 130)], xi[(Frontsparlocation - 130)]), (ylower[(Frontsparlocation - 2)], yupper[(Frontsparlocation - 2)]), 'r')
	plt.plot((xi[(Frontsparlocation - 2)], xi[(Frontsparlocation - 130)]), (ylower[(Frontsparlocation - 2)], ylower[(Frontsparlocation - 2)]), 'r')
	plt.plot((xi[(Frontsparlocation - 2)], xi[(Frontsparlocation - 130)]), (yupper[(Frontsparlocation - 2)], yupper[(Frontsparlocation - 2)]), 'r')

	#For plotting square wingbox
	#plt.plot((xi[Frontsparlocation], xi[Backsparlocation]), (ylower[Frontsparlocation], ylower[Backsparlocation]), 'k-')
	#plt.plot((xi[Frontsparlocation], xi[Backsparlocation]), (yupper[Frontsparlocation], yupper[Backsparlocation]), 'k-')
	
	#For plotting maximum height line
	#plt.plot((xi[np.argmax(height)], xi[np.argmax(height)]), (ylower[np.argmax(height)], yupper[np.argmax(height)]), 'k-')
	

	#plotting tip section
	#plt.scatter(x_coordinates_tip,y_coordinates_tip)
	plt.plot(xi_tip,ylower_tip, 'g')
	plt.plot(xi_tip,yupper_tip, 'g')

	plt.show()

	#make surface 3D model of wing
	#z_final = np.array([0, 3200])
	#y_final = np.resize(np.array(xi),(1150,1))
	
	#make 3d model of wing
	z_coordinates = np.zeros(2300)  
	z_coordinates_tip = [x for x in np.zeros(2020) +320]
	x_final = np.array(z_coordinates).tolist() + np.array(z_coordinates_tip).tolist()
	y_final = np.array(xi).tolist() + np.array(xi).tolist() + np.array(xi_tip).tolist() + np.array(xi_tip).tolist()
	z_final = np.array(yupper).tolist() + np.array(ylower).tolist() + np.array(yupper_tip).tolist() + np.array(ylower_tip).tolist()
	
	
	#ax = plt.axes(projection='3d')
	#ax.scatter3D(x_final, y_final, z_final, c=z_final, cmap='Greens')

	#plt.show()

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

#Calculates the mass when composite plate is considered, all sides and spars have same thickness
def MassOfComposite(Density, Fibre_thick, Honeycomb_thick, Nr_layers, frontsparheight, backsparheight, MaximumBending):
	#Area_wingbox_ribs = 
	#Nr_ribs

	#runs the wingbox function to get width, airfoil circumference and drawings
	wingb = wingbox(frontsparheight, backsparheight)

	#runs the DoesItHoldBending formula to check what the max ben. stress occuring is
	thickness = (Fibre_thick * Nr_layers * 2) + Honeycomb_thick
	bending = 2.5 * DoesItHoldBending(MaximumBending, frontsparheight/1000., backsparheight/1000., thickness/1000., wingb[0]/1000.)

	#Calculate the area of all the plates and airfoil, so easily multiplied with length
	#Three spars are used, the middle one is on the location with the most space between upper and lower airfoil
	Area_wingbox_spars = 3200 * (frontsparheight + backsparheight + wingb[1]) 
	Area_wingbox_spars = 3200 * (frontsparheight + backsparheight + wingb[1]) 
	Area_airfoil = wingb[2] * 3200

	Area_wingbox = Area_airfoil + (Area_wingbox_spars) #+ (Area_wingbox_ribs * Nr_ribs)

	#Calculates mass not taking ribs and fastening bolts or adhesive into account
	Mass = Nr_layers * Fibre_thick * Area_wingbox * Density/1e6

	return int(Mass), bending

#Calculates the mass when metal plate is considered
def MassOfMetal(Density, thickness, frontsparheight, backsparheight, MaximumBending):
	#Area_wingbox_ribs = 
	#Nr_ribs = 

	#runs the wingbox function to get width, airfoil circumference and drawings
	wingb = wingbox(frontsparheight, backsparheight)

	#runs the DoesItHoldBending formula to check what the max ben. stress occuring is
	bending = 1.5 * DoesItHoldBending(MaximumBending, frontsparheight/1000., backsparheight/1000., thickness/1000., wingb[0]/1000.)
	
	#Calculate the area of all the plates and airfoil, so easily multiplied with length
	#Three spars are used, the middle one is on the location with the most space between upper and lower airfoil
	Area_wingbox_spars = 3200 * (frontsparheight + backsparheight + wingb[1]) 
	Area_airfoil = wingb[2] * 3200

	Area_wingbox = Area_airfoil + (Area_wingbox_spars) #+ (Area_wingbox_ribs * Nr_ribs)

	#Calculates mass not taking ribs and fastening bolts or adhesive into account
	Mass = thickness * Area_wingbox * Density/1e6

	return int(Mass), bending 

#calculates the bendingstress occuring at maximum condition in the wingbox
def DoesItHoldBending(MaximumBending, frontsparheight, backsparheight, thickness, Width):
	y_halfheight = ((backsparheight + frontsparheight) / 4)
	y_fullheight = ((backsparheight + frontsparheight) / 2)

	#Determines Iyy area moment from the centre point, where the bending moments is assumed to act
	Iyy_Topsurface = format(((1/12) * (Width ** 3) * thickness) + (Width * thickness * (y_halfheight **2)),'.15f')
	#Iyy_Sidesurface = format(((1/12) * (thickness ** 3) * Width) + (Width * thickness * (y_halfheight **2)),'.15f')

	Iyy = (2 * float(Iyy_Topsurface)) #+ (2 * float(Iyy_Sidesurface))
	stress = (float(MaximumBending) * float(y_halfheight)) / float(Iyy)
	return stress / 1e6


print 'Youngs Modulus =', YoungsModulusLayer(141.5, 4.61e-5, 4, 1), 'GPa'

#MassOfMetal(Density, thickness, frontsparheight, backsparheight, MaximumBending)
a = MassOfMetal(2.810, 4, 180.0, 180.0, 42000.)

print 'Mass Metal', a[0], 'Kg'
print 'Stress Metal', a[1], 'MPa'

#MassOfComposite(Density, Fibre_thick, Honeycomb_thick, Nr_layers, frontsparheight, backsparheight, MaximumBending)
a = MassOfComposite(1.550, 0.5, 5, 8, 180.0, 180.0, 42000.)

print 'Mass Composite', a[0], 'Kg'
print 'Stress Composite', a[1], 'MPa'

