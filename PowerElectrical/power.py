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
    totalPower = thrust*velocity/0.9 #transmission efficiency = 0.9
    return totalPower

def tankSizing(pressure, volumeHydrogen, yieldStrength, density, safetyFactor):
    radiusHydrogen = (volumeHydrogen*3.0/(4.0*math.pi))**(1.0/3.0)
    thickness = pressure*radiusHydrogen*safetyFactor/(2.0*yieldStrength)
    mass = density*(4.0/3.0)*math.pi*((radiusHydrogen + thickness)**3 - (radiusHydrogen)**3)
    return mass, thickness

def cellPotential(i, p_atm):
    ###Constants
    #Faraday's constant
    F = 96485.33212 # C/mol
    #Gas constant
    R = 8.314462618 # J/(K mol)
    #Entropy of reaction
    ds = -163.28 # J / (mol K)

    ###Cell specs
    #Operational temperature
    T = 333.15 #K
    #Partial pressures
    P_a = 1.51 #atm
    P_c = p_atm #atm
    X_h2 = 1.0
    X_o2 = 0.21

    ###Model F's fitting parameters
    b = 0.06642 #V/decade
    i_loss = 0.001225 #A cm^2
    i_0 = 3.7980 #A cm^2
    resistance = 0.1083 #ohm cm^2
    m = 0.005248 #V
    n = 2.2421 #cm^2 / A

    V_rev = 1.229 - ds/(2.0*F)*(T - 298.15) - (R*T/(2.0*F))*math.log(1.0/((P_a*X_h2)*(P_c*X_o2)**0.5))

    V = V_rev - b*math.log((i + i_loss)/i_0) - resistance*i - m*math.exp(n*i)

    return V

def cellSizing(powerReq, i, p_atm):
    A_cell = powerReq/(cellPotential(i, p_atm)*i) #cm^2
    return A_cell*0.0001 #m^2

def fuelCalc():

    MTOW = mass_calculation.mass_iteration(1630.0)[0]
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

    for t in np.arange(5*dt, 39.0/acc, dt):
        takeOff_t = ThrustCalculator(MTOW - massHydrogen, acc*t, 0.0, dt, 0, acc, 1)
        takeOff_l = aero.Propellers(takeOff_t.thrust, takeOff_t.velocity,
                                    takeOff_t.rho, takeOff_t.aero_vals.cl_takeoff, 1)
        takeOff_power.append((takeOff_l.powerHLP * takeOff_l.numberHLP +
                      takeOff_l.powerCP * takeOff_l.numberCP))
        takeOff_energy.append((takeOff_l.powerHLP * takeOff_l.numberHLP +
                       takeOff_l.powerCP * takeOff_l.numberCP) * takeOff_t.duration)
        massHydrogen = massHydrogen + ((takeOff_power[-1]/0.6)/SED_hydrogen)*dt

    power.append(sum(takeOff_power)/len(takeOff_power))
    energy.append(sum(takeOff_energy))
    print("####Take-off####")
    print("Altitude: ", takeOff_t.altitude, "Velocity: ", takeOff_t.velocity)
    print("HLP eff: ", takeOff_l.efficiencyHLP, "CP eff: ", takeOff_l.efficiencyCP)

    #CLIMB
    climb_t = ThrustCalculator(MTOW - massHydrogen, math.sqrt(2*(MTOW - massHydrogen)*9.80665/(takeOff_t.wing_vals.S*takeOff_t.rho*math.sqrt(3*math.pi*takeOff_t.aero_vals.cd0*takeOff_t.wing_vals.A*takeOff_t.wing_vals.e))), 750.0, 1500.0/7.44, 7.44)
    climb_l = aero.Propellers(climb_t.thrust, climb_t.velocity,
                                climb_t.rho, climb_t.aero_vals.cl_cr, 0)
    power.append((climb_l.powerHLP * climb_l.numberHLP +
                   climb_l.powerCP * climb_l.numberCP))
    energy.append((climb_l.powerHLP * climb_l.numberHLP +
                   climb_l.powerCP * climb_l.numberCP) * climb_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * climb_t.duration
    print("####Climb####")
    print("Altitude: ", climb_t.altitude, "Velocity: ", climb_t.velocity)
    print("HLP eff: ", climb_l.efficiencyHLP, "CP eff: ", climb_l.efficiencyCP)

    #CRUISE
    cruise_t = ThrustCalculator(MTOW - massHydrogen, 69.4, 1500, 400000.0/69.4)
    cruise_l = aero.Propellers(cruise_t.thrust, cruise_t.velocity,
                              cruise_t.rho, cruise_t.aero_vals.cl_cr, 0)
    power.append((cruise_l.powerHLP * cruise_l.numberHLP +
                   cruise_l.powerCP * cruise_l.numberCP))
    energy.append((cruise_l.powerHLP * cruise_l.numberHLP +
                   cruise_l.powerCP * cruise_l.numberCP) * cruise_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * cruise_t.duration
    print("####Cruise####")
    print("Altitude: ", cruise_t.altitude, "Velocity: ", cruise_t.velocity)
    print("HLP eff: ", cruise_l.efficiencyHLP, "CP eff: ", cruise_l.efficiencyCP)

    #RESERVE
    reserve_t = ThrustCalculator(MTOW - massHydrogen, 69.0, 1500.0, 45*60)
    reserve_l = aero.Propellers(reserve_t.thrust, reserve_t.velocity,
                               reserve_t.rho, reserve_t.aero_vals.cl_cr, 0)
    power.append((reserve_l.powerHLP * reserve_l.numberHLP +
                   reserve_l.powerCP * reserve_l.numberCP))
    energy.append((reserve_l.powerHLP * reserve_l.numberHLP +
                   reserve_l.powerCP * reserve_l.numberCP) * reserve_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * reserve_t.duration
    print("####Reserve####")
    print("Altitude: ", reserve_t.altitude, "Velocity: ", reserve_t.velocity)
    print("HLP eff: ", reserve_l.efficiencyHLP, "CP eff: ", reserve_l.efficiencyCP)

    #DESCENT
    landStart_t = ThrustCalculator(MTOW - massHydrogen, 31.0, 1500.0, 600)
    landStart_l = aero.Propellers(landStart_t.thrust, landStart_t.velocity,
                               landStart_t.rho, landStart_t.aero_vals.cl_takeoff, 1)
    power.append((landStart_l.powerHLP * landStart_l.numberHLP +
                   landStart_l.powerCP * landStart_l.numberCP))
    energy.append((landStart_l.powerHLP * landStart_l.numberHLP +
                   landStart_l.powerCP * landStart_l.numberCP) * landStart_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * landStart_t.duration
    print("####Descent####")
    print("Altitude: ", landStart_t.altitude, "Velocity: ", landStart_t.velocity)
    print("HLP eff: ", landStart_l.efficiencyHLP, "CP eff: ", landStart_l.efficiencyCP)

    #LANDING
    landing_t = ThrustCalculator(MTOW - massHydrogen, 39.0, 750.0, 1928.0/(31.0*math.sin(math.atan(1.0/3.0))))
    landing_l = aero.Propellers(landing_t.thrust, landing_t.velocity,
                                  landing_t.rho, landing_t.aero_vals.cl_takeoff, 1)
    power.append((landing_l.powerHLP * landing_l.numberHLP +
                   landing_l.powerCP * landing_l.numberCP))
    energy.append((landing_l.powerHLP * landing_l.numberHLP +
                   landing_l.powerCP * landing_l.numberCP) * landing_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * landing_t.duration
    print("####Landing####")
    print("Altitude: ", landing_t.altitude, "Velocity: ", landing_t.velocity)
    print("HLP eff: ", landing_l.efficiencyHLP, "CP eff: ", landing_l.efficiencyCP)
    print("Thrust when landing:")
    print(landing_l.thrustCP)
    print(landing_l.thrustHLP)

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
    colors = ['blue', 'gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'black', 'red', 'purple']

    #Energy Bar Chart
    plt.figure(0)
    plt.bar(ind, energy, label='Energy', color=colors)
    plt.xticks(ind, ('Drive 1', 'Take-off', 'Climb', 'Cruise', 'Reserve', 'Descent', 'Landing', 'Drive 2'))
    plt.xlabel('Phase')
    plt.ylabel('Energy [kW-h]')
    plt.title("Total Energy Required in Each Phase")

    #Energy breakdown pie chart
    plt.figure(1)
    labels = 'Drive 1', 'Take-off', 'Climb', 'Cruise', 'Reserve', 'Descent', 'Landing', 'Drive 2'
    patches, texts = plt.pie(energy, colors=colors)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.title("Total Energy Required in Each Phase")

    #Power bar chart
    plt.figure(2)
    plt.bar(ind, power, label='Power', color=colors)
    plt.xticks(ind, ('Drive 1', 'Take-off', 'Climb', 'Cruise', 'Reserve', 'Descent', 'Landing', 'Drive 2'))
    plt.xlabel('Phase')
    plt.ylabel('Power [kW]')
    plt.title("Total Power Required in Each Phase")

    # Power breakdown pie chart
    plt.figure(3)
    labels = 'Drive 1', 'Take-off', 'Climb', 'Cruise', 'Reserve', 'Descent', 'Landing', 'Drive 2'
    patches, texts = plt.pie(power, colors=colors)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.title("Total Power Required in Each Phase")

    print("Total energy: ", sum(energy))
    print("Maximum power: ", max(power))

    #Find phase with max power usage:
    index_max = min(range(len(power)), key=power.__getitem__)
    switch = {0: drive1_t,
              1: takeOff_t,
              2: climb_t,
              3: cruise_t,
              4: reserve_t,
              5: landStart_t,
              6: landing_t,
              7: drive2_t
    }
    maxPowerPhase = switch[index_max]

    print("Power per phase: ")
    for i in range(8):
        print(power[i])

    #Size fuel cell for several possible current densities i [A / cm^2]
    V = []
    A = []
    I = np.linspace(0.10, 1.5, 30)
    for i in I:
        V.append(cellPotential(i, maxPowerPhase.p))
        A.append(cellSizing(max(power), i, maxPowerPhase.p))

    plt.figure(4)
    fig, ax1 = plt.subplots()
    ax1.plot(I, V, 'bo', label='Voltage [V]')
    ax1.set_ylabel('Voltage [V]', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ax2.plot(I, A, 'r+', label='Cell Area [m^2]')
    ax2.set_ylabel('Cell Area [m^2]', color='r')
    ax2.tick_params('y', colors='r')

    plt.xlabel('Current Density [A/cm^2]')
    plt.title("H2 Fuel Cell Sizing at Max Power Condition")

    plt.show()

    materials = ["epoxy", "al2o3", "aluminum"]
    yieldStrength = [738.0E6, 252.0E6, 505.0E6]
    density = [1.58E3, 3.4E3, 2.61E3]

    for i in range(3):
        print("Structural tank mass if using ", materials[i])
        print(tankSizing(200000, massHydrogen / 70.8, yieldStrength[i], density[i], 2.0)[0])
        print(tankSizing(200000, massHydrogen/70.8, yieldStrength[i], density[i], 2.0)[1])

    return #massHydrogen


if __name__ == "__main__":
    fuelCalc()
