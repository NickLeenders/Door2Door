import math
import sys
sys.path.insert(0, '../Aerodynamics/')
import aero
import aerodynamic_parameters
sys.path.insert(0, '../PowerElectrical/')
from isa import IsaCalculator
#sys.path.insert(0, '../Airframe/')
#import total_masses
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, '../Structure/')
import mass_calculation

class ThrustCalculator:

    """Preliminary required thrust calculation for one phase"""


    def __init__(self, mass, velocity, altitude, duration, rateOfClimb=0.0, acceleration=0.0, driving=0):

        self.aero_vals = aerodynamic_parameters.aero_vals()
        self.wing_vals = aerodynamic_parameters.wing_vals()
        self.emp_vals = aerodynamic_parameters.emp_vals()
        self.mass = mass
        self.range = 400000
        self.mu = 0.015 #TODO take mu value for ground system

        self.velocity = velocity
        self.altitude = altitude
        self.rho, self.T, self.p = IsaCalculator(altitude)
        self.duration = duration

        if (self.velocity > 40.0):
            self.drag = aero.drag(self.aero_vals.cd0, self.aero_vals.cl_cr, self.wing_vals.b, self.wing_vals.MAC,
                              self.wing_vals.e, self.velocity, self.rho)
        else:
            self.drag = aero.drag(self.aero_vals.cd0, self.aero_vals.cl_takeoff, self.wing_vals.b, self.wing_vals.MAC,
                                  self.wing_vals.e, self.velocity, self.rho)
        self.acceleration = acceleration
        if driving != 0:
            self.friction = self.mass*9.80665*self.mu
        else:
            self.friction = 0.0
        self.thrust = self.drag + self.mass*self.acceleration + self.friction

def enginePower(thrust, velocity):
    backWheelDiameter = 0.63 #m
    frontWheelDiameter = 0.5245 #m
    backWheelRPM = velocity*60.0/(math.pi*backWheelDiameter)
    frontWheelRPM = velocity * 60.0 / (math.pi * frontWheelDiameter)
    totalPower = 2.0*math.pi*thrust*(2.0*frontWheelRPM + backWheelRPM)/60.0
    return totalPower

def main():

    MTOW = mass_calculation.mass_iteration(1630.0)
    SED_hydrogen = (120.0+142.0)*1.0E6/2.0 #Taking average between 120 MJ/kg and 142 MJ/kg

    power = []
    energy = []
    massHydrogen = 0.0

    #DRIVE 1
    drive1_t = ThrustCalculator(MTOW - massHydrogen, 29.0, 0.0, 50000.0/29.0, 0, 0, 1)
    power.append(enginePower(drive1_t.thrust, drive1_t.velocity))
    energy.append(power[-1]*drive1_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * drive1_t.duration

    #TAKE-OFF
    dt = 1.0
    acc = 1.1
    takeOff_power = []
    takeOff_energy = []

    for t in np.arange(0, 39.0/acc, dt):
        takeOff_t = ThrustCalculator(MTOW - massHydrogen, acc*dt, 0.0, dt, 0, acc, 1)
        takeOff_l = aero.Propellers(takeOff_t.thrust, takeOff_t.velocity,
                                    takeOff_t.rho, takeOff_t.aero_vals.cl_takeoff, 1)
        takeOff_power.append((takeOff_l.powerHLP * takeOff_l.numberHLP +
                      takeOff_l.powerCP * takeOff_l.numberCP))
        takeOff_energy.append((takeOff_l.powerHLP * takeOff_l.numberHLP +
                       takeOff_l.powerCP * takeOff_l.numberCP) * takeOff_t.duration)
        massHydrogen = massHydrogen + ((takeOff_power[-1]/0.6)/SED_hydrogen)*dt

    power.append(sum(takeOff_power)/len(takeOff_power))
    energy.append(sum(takeOff_energy))

    #CLIMB
    climb_t = ThrustCalculator(MTOW - massHydrogen, math.sqrt(2*(MTOW - massHydrogen)*9.80665/(takeOff_t.wing_vals.S*takeOff_t.rho*math.sqrt(3*math.pi*takeOff_t.aero_vals.cd0*takeOff_t.wing_vals.A*takeOff_t.wing_vals.e))), 750.0, 1500.0/7.44, 7.44)
    climb_l = aero.Propellers(climb_t.thrust, climb_t.velocity,
                                climb_t.rho, climb_t.aero_vals.cl_cr, 0)
    power.append((climb_l.powerHLP * climb_l.numberHLP +
                   climb_l.powerCP * climb_l.numberCP))
    energy.append((climb_l.powerHLP * climb_l.numberHLP +
                   climb_l.powerCP * climb_l.numberCP) * climb_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * climb_t.duration

    #CRUISE
    cruise_t = ThrustCalculator(MTOW - massHydrogen, 69.4, 1500, 400000.0/69.4)
    cruise_l = aero.Propellers(cruise_t.thrust, cruise_t.velocity,
                              cruise_t.rho, cruise_t.aero_vals.cl_cr, 0)
    power.append((cruise_l.powerHLP * cruise_l.numberHLP +
                   cruise_l.powerCP * cruise_l.numberCP))
    energy.append((cruise_l.powerHLP * cruise_l.numberHLP +
                   cruise_l.powerCP * cruise_l.numberCP) * cruise_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * cruise_t.duration

    #RESERVE
    reserve_t = ThrustCalculator(MTOW - massHydrogen, 69.0, 1500.0, 45*60)
    reserve_l = aero.Propellers(reserve_t.thrust, reserve_t.velocity,
                               reserve_t.rho, reserve_t.aero_vals.cl_cr, 0)
    power.append((reserve_l.powerHLP * reserve_l.numberHLP +
                   reserve_l.powerCP * reserve_l.numberCP))
    energy.append((reserve_l.powerHLP * reserve_l.numberHLP +
                   reserve_l.powerCP * reserve_l.numberCP) * reserve_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * reserve_t.duration

    #DESCENT
    landStart_t = ThrustCalculator(MTOW - massHydrogen, 31.0, 1500.0, 600)
    landStart_l = aero.Propellers(landStart_t.thrust, landStart_t.velocity,
                               landStart_t.rho, landStart_t.aero_vals.cl_takeoff, 1)
    power.append((landStart_l.powerHLP * landStart_l.numberHLP +
                   landStart_l.powerCP * landStart_l.numberCP))
    energy.append((landStart_l.powerHLP * landStart_l.numberHLP +
                   landStart_l.powerCP * landStart_l.numberCP) * landStart_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * landStart_t.duration

    #LANDING
    landing_t = ThrustCalculator(MTOW - massHydrogen, 31.0, 750.0, 1928.0/(31.0*math.sin(math.atan(1.0/3.0))))
    landing_l = aero.Propellers(landing_t.thrust, landing_t.velocity,
                                  landing_t.rho, landing_t.aero_vals.cl_takeoff, 1)
    power.append((landing_l.powerHLP * landing_l.numberHLP +
                   landing_l.powerCP * landing_l.numberCP))
    energy.append((landing_l.powerHLP * landing_l.numberHLP +
                   landing_l.powerCP * landing_l.numberCP) * landing_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * landing_t.duration

    # DRIVE 2
    drive2_t = ThrustCalculator(MTOW - massHydrogen, 29.0, 0.0, 50000.0 / 29.0, 0, 0, 1)
    power.append(enginePower(drive2_t.thrust, drive2_t.velocity))
    energy.append(power[-1] * drive2_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * drive2_t.duration

    print("Hydrogen mass: ", massHydrogen)
    print("Hydrogen volume: ", massHydrogen/70.8)

    for i in range(0, len(energy)):
        energy[i] = energy[i]/(3.6E6)
        power[i] = power[i] / (1000.0)

    ind = np.arange(len(energy))
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'black', 'red']

    #Energy Bar Chart
    plt.figure(0)
    plt.bar(ind, energy, label='Energy', color=colors)
    plt.xticks(ind, ('Take-off', 'Climb', 'Cruise', 'Reserve', 'Descent', 'Landing'))
    plt.xlabel('Phase')
    plt.ylabel('Energy [kW-h]')
    plt.title("Total Energy Required in Each Phase")

    #Energy breakdown pie chart
    plt.figure(1)
    labels = 'Take-off', 'Climb', 'Cruise', 'Reserve', 'Descent', 'Landing'
    patches, texts = plt.pie(energy, colors=colors)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.title("Total Energy Required in Each Phase")

    #Power bar chart
    plt.figure(2)
    plt.bar(ind, power, label='Power', color=colors)
    plt.xticks(ind, ('Take-off', 'Climb', 'Cruise', 'Reserve', 'Descent', 'Landing'))
    plt.xlabel('Phase')
    plt.ylabel('Power [kW]')
    plt.title("Total Power Required in Each Phase")

    # Power breakdown pie chart
    plt.figure(3)
    labels = 'Take-off', 'Climb', 'Cruise', 'Reserve', 'Descent', 'Landing'
    patches, texts = plt.pie(power, colors=colors)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.title("Total Power Required in Each Phase")

    plt.show()

    print("Total energy: ", sum(energy))
    print("Maximum power: ", max(power))

    return


if __name__ == "__main__":
    main()
