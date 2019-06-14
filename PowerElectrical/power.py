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
from mpl_toolkits.mplot3d import axes3d
from matplotlib import style

class ThrustCalculator:

    """Preliminary required thrust calculation for one phase"""


    def __init__(self, mass, velocity, v_wakeCP, v_wakeHLP, altitude, duration, rateOfClimb=0.0, acceleration=0.0, driving=0):

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

        self.v_wakeCP = v_wakeCP
        self.v_wakeHLP = v_wakeHLP

        if (self.velocity > 40.0 and driving==0):
            self.drag = aero.drag(1, self.velocity, self.v_wakeCP, self.v_wakeHLP, self.rho)[0]
        elif (driving==0):
            self.drag = aero.drag(2, self.velocity, self.v_wakeCP, self.v_wakeHLP, self.rho)[0]
        elif (driving==1):
            self.drag = aero.drag(0, self.velocity, self.v_wakeCP, self.v_wakeHLP, self.rho)[0]

        self.acceleration = acceleration

        if driving != 0:
            self.friction = self.mass*9.80665*self.mu
        else:
            self.friction = 0.0
        self.thrust = self.drag + self.mass*self.acceleration + self.friction

def enginePower(thrust, velocity):
    totalPower = thrust*velocity/0.9 #transmission efficiency = 0.9
    return totalPower

def heatCapacityH2(T):
    # heat capacity in J/(g*K):
    C = 14.43877 - 1.691*T + 0.10687*T*T - 0.00174*T*T*T
    return C

def tankSizing(pressure, massHydrogen, volumeHydrogen, yieldStrength, density, safetyFactor, missionDuration, thermalConductivity, densityFoam):
    radiusHydrogen = (volumeHydrogen*3.0/(4.0*math.pi))**(1.0/3.0)
    #structural tank:
    thickness = pressure*radiusHydrogen*safetyFactor/(2.0*yieldStrength)
    mass = density*(4.0/3.0)*math.pi*((radiusHydrogen + thickness)**3 - (radiusHydrogen)**3)
    #foam insulator:
    SA = 4.0*math.pi*(radiusHydrogen + thickness)**2
    Thot = 80.0 + 273.15
    Tcold = 16.0
    Q_max = massHydrogen*1000.0*heatCapacityH2(Tcold)*3.5/missionDuration
    thicknessI = thermalConductivity*SA*(Thot - Tcold)/Q_max
    massI = densityFoam * (4.0 / 3.0) * math.pi * ((radiusHydrogen + thickness + thicknessI) ** 3 - (radiusHydrogen + thickness) ** 3)
    #total (w/o liner for now):
    massTotal = mass + massI
    thicknessTotal = thickness + thicknessI
    return massTotal, thicknessTotal, mass, thickness, massI, thicknessI, radiusHydrogen

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
    drive1_t = ThrustCalculator(MTOW - massHydrogen, 29.0, 29.0, 29.0, 0.0, 50000.0/29.0, 0, 0, 1)
    power.append(enginePower(drive1_t.thrust, drive1_t.velocity))
    energy.append(power[-1]*drive1_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * drive1_t.duration

    #TAKE-OFF
    dt = 1.0
    acc = 1.1
    takeOff_power = []
    takeOff_energy = []

    for t in np.arange(5*dt, 35.0/acc, dt):
        takeOff_t = ThrustCalculator(MTOW - massHydrogen, acc*t, acc*t, acc*t, 0.0, dt, 0, acc, 1)
        takeOff_l = aero.Propellers(takeOff_t.thrust, takeOff_t.velocity,
                                    takeOff_t.rho, takeOff_t.aero_vals.cl_takeoff, 1)
        temp = takeOff_t
        temp.thrust = 0.0
        while (abs(takeOff_t.thrust - temp.thrust) > 0.005):
            temp = takeOff_t
            takeOff_t = ThrustCalculator(MTOW - massHydrogen, acc * t, takeOff_l.v_wakeCP, takeOff_l.v_wakeHLP, 0.0, dt, 0, acc, 1)
            takeOff_l = aero.Propellers(takeOff_t.thrust, takeOff_t.velocity,
                                        takeOff_t.rho, takeOff_t.aero_vals.cl_takeoff, 1)
        print("#########################")
        print("Take-off:")
        print("Weight: ", (MTOW - massHydrogen)*9.80665)
        print("Lift: ", takeOff_l.lift_powered)

        takeOff_power.append((takeOff_l.powerHLP * takeOff_l.numberHLP +
                      takeOff_l.powerCP * takeOff_l.numberCP))
        takeOff_energy.append((takeOff_l.powerHLP * takeOff_l.numberHLP +
                       takeOff_l.powerCP * takeOff_l.numberCP) * takeOff_t.duration)
        massHydrogen = massHydrogen + ((takeOff_power[-1]/0.6)/SED_hydrogen)*dt

    power.append(sum(takeOff_power)/len(takeOff_power))
    energy.append(sum(takeOff_energy))
    print("Altitude: ", takeOff_t.altitude, "Velocity: ", takeOff_t.velocity)
    print("HLP eff: ", takeOff_l.efficiencyHLP, "CP eff: ", takeOff_l.efficiencyCP)
    print("HLP thrust: ", takeOff_l.thrustHLP, "CP thrust: ", takeOff_l.thrustCP)
    print("Wake velocity CP: ", takeOff_l.v_wakeCP, " Wake velocity HLP: ", takeOff_l.v_wakeHLP)

    #CLIMB
    climb_t = ThrustCalculator(MTOW - massHydrogen, 45.0, 45.0, 45.0, 750.0, 1500.0/7.44, 7.44)
    climb_l = aero.Propellers(climb_t.thrust, climb_t.velocity,
                                climb_t.rho, climb_t.aero_vals.cl_takeoff, 1)
    temp = climb_t
    temp.thrust = 0.0
    while (abs(climb_t.thrust - temp.thrust) > 0.005):
        temp = climb_t
        climb_t = ThrustCalculator(MTOW - massHydrogen, 45.0, climb_l.v_wakeCP, climb_l.v_wakeHLP, 750.0, 1500.0/7.44, 7.44)
        climb_l = aero.Propellers(climb_t.thrust, climb_t.velocity,
                                    climb_t.rho, climb_t.aero_vals.cl_takeoff, 1)
    print("#########################")
    print("Climb:")
    print("Weight: ", (MTOW - massHydrogen)*9.80665)
    print("Lift: ", climb_l.lift_powered)

    power.append((climb_l.powerHLP * climb_l.numberHLP +
                   climb_l.powerCP * climb_l.numberCP))
    energy.append((climb_l.powerHLP * climb_l.numberHLP +
                   climb_l.powerCP * climb_l.numberCP) * climb_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * climb_t.duration
    print("Altitude: ", climb_t.altitude, "Velocity: ", climb_t.velocity)
    print("HLP eff: ", climb_l.efficiencyHLP, "CP eff: ", climb_l.efficiencyCP)
    print("HLP thrust: ", climb_l.thrustHLP, "CP thrust: ", climb_l.thrustCP)

    #CRUISE
    cruise_t = ThrustCalculator(MTOW - massHydrogen, 69.4, 69.4, 69.4, 1500, 400000.0/69.4)
    cruise_l = aero.Propellers(cruise_t.thrust, cruise_t.velocity,
                              cruise_t.rho, cruise_t.aero_vals.cl_cr, 0)
    temp = cruise_t
    temp.thrust = 0.0
    while (abs(cruise_t.thrust - temp.thrust) > 0.005):
        temp = cruise_t
        cruise_t = ThrustCalculator(MTOW - massHydrogen, 69.4, cruise_l.v_wakeCP, cruise_l.v_wakeHLP, 1500.0, 400000.0/69.4)
        cruise_l = aero.Propellers(cruise_t.thrust, cruise_t.velocity,
                                  cruise_t.rho, cruise_t.aero_vals.cl_cr, 0)
    print("#########################")
    print("Cruise:")
    print("Weight: ", (MTOW - massHydrogen)*9.80665)
    print("Lift: ", cruise_l.lift_powered)

    power.append((cruise_l.powerHLP * cruise_l.numberHLP +
                   cruise_l.powerCP * cruise_l.numberCP))
    energy.append((cruise_l.powerHLP * cruise_l.numberHLP +
                   cruise_l.powerCP * cruise_l.numberCP) * cruise_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * cruise_t.duration
    print("Altitude: ", cruise_t.altitude, "Velocity: ", cruise_t.velocity)
    print("HLP eff: ", cruise_l.efficiencyHLP, "CP eff: ", cruise_l.efficiencyCP)
    print("HLP thrust: ", cruise_l.thrustHLP, "CP thrust: ", cruise_l.thrustCP)

    #RESERVE
    reserve_t = ThrustCalculator(MTOW - massHydrogen, 69.4, 69.4, 69.4, 1500.0, 45.0*60.0)
    reserve_l = aero.Propellers(reserve_t.thrust, reserve_t.velocity,
                               reserve_t.rho, reserve_t.aero_vals.cl_cr, 0)
    temp = reserve_t
    temp.thrust = 0.0
    while (abs(reserve_t.thrust - temp.thrust) > 0.005):
        temp = reserve_t
        reserve_t = ThrustCalculator(MTOW - massHydrogen, 69.4, reserve_l.v_wakeCP, reserve_l.v_wakeHLP, 1500.0, 45.0*60.0)
        reserve_l = aero.Propellers(reserve_t.thrust, reserve_t.velocity,
                                  reserve_t.rho, reserve_t.aero_vals.cl_cr, 0)
    print("#########################")
    print("Reserve:")
    print("Weight: ", (MTOW - massHydrogen)*9.80665)
    print("Lift: ", reserve_l.lift_powered)
    power.append((reserve_l.powerHLP * reserve_l.numberHLP +
                   reserve_l.powerCP * reserve_l.numberCP))
    energy.append((reserve_l.powerHLP * reserve_l.numberHLP +
                   reserve_l.powerCP * reserve_l.numberCP) * reserve_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * reserve_t.duration
    print("Altitude: ", reserve_t.altitude, "Velocity: ", reserve_t.velocity)
    print("HLP eff: ", reserve_l.efficiencyHLP, "CP eff: ", reserve_l.efficiencyCP)
    print("HLP thrust: ", reserve_l.thrustHLP, "CP thrust: ", reserve_l.thrustCP)

    #DESCENT
    landStart_t = ThrustCalculator(MTOW - massHydrogen, 31.0, 31.0, 31.0, 1500.0, 600)
    landStart_l = aero.Propellers(landStart_t.thrust, landStart_t.velocity,
                               landStart_t.rho, landStart_t.aero_vals.cl_descent, 0)
    temp = landStart_t
    temp.thrust = 0.0
    while (abs(landStart_t.thrust - temp.thrust) > 0.005):
        temp = landStart_t
        landStart_t = ThrustCalculator(MTOW - massHydrogen, 31.0, landStart_l.v_wakeCP, landStart_l.v_wakeHLP, 1500.0, 600.0)
        landStart_l = aero.Propellers(landStart_t.thrust, landStart_t.velocity,
                                  landStart_t.rho, landStart_t.aero_vals.cl_descent, 0)
    print("#########################")
    print("Descent:")
    print("Weight: ", (MTOW - massHydrogen)*9.80665)
    print("Lift: ", landStart_l.lift_powered)
    power.append((landStart_l.powerHLP * landStart_l.numberHLP +
                   landStart_l.powerCP * landStart_l.numberCP))
    energy.append((landStart_l.powerHLP * landStart_l.numberHLP +
                   landStart_l.powerCP * landStart_l.numberCP) * landStart_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * landStart_t.duration
    print("Altitude: ", landStart_t.altitude, "Velocity: ", landStart_t.velocity)
    print("HLP eff: ", landStart_l.efficiencyHLP, "CP eff: ", landStart_l.efficiencyCP)
    print("HLP thrust: ", landStart_l.thrustHLP, "CP thrust: ", landStart_l.thrustCP)

    #LANDING
    landing_t = ThrustCalculator(MTOW - massHydrogen, 35.0, 35.0, 35.0, 750.0, (MTOW - massHydrogen)/(31.0*math.sin(math.atan(1.0/3.0))))
    landing_l = aero.Propellers(landing_t.thrust, landing_t.velocity,
                                  landing_t.rho, landing_t.aero_vals.cl_takeoff, 1)
    temp = landing_t
    temp.thrust = 0.0
    while (abs(landing_t.thrust - temp.thrust) > 0.005):
        temp = landing_t
        landing_t = ThrustCalculator(MTOW - massHydrogen, 35.0, landing_l.v_wakeCP, landing_l.v_wakeHLP, 750.0, (MTWO - massHydrogen)/(31.0*math.sin(math.atan(1.0/3.0))))
        landing_l = aero.Propellers(landing_t.thrust, landing_t.velocity,
                                  landing_t.rho, landing_t.aero_vals.cl_takeoff, 1)
    print("#########################")
    print("Landing:")
    print("Weight: ", (MTOW - massHydrogen)*9.80665)
    print("Lift: ", landing_l.lift_powered)
    power.append((landing_l.powerHLP * landing_l.numberHLP +
                   landing_l.powerCP * landing_l.numberCP))
    energy.append((landing_l.powerHLP * landing_l.numberHLP +
                   landing_l.powerCP * landing_l.numberCP) * landing_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * landing_t.duration
    print("Altitude: ", landing_t.altitude, "Velocity: ", landing_t.velocity)
    print("HLP eff: ", landing_l.efficiencyHLP, "CP eff: ", landing_l.efficiencyCP)
    print("HLP thrust: ", landing_l.thrustHLP, "CP thrust: ", landing_l.thrustCP)

    #DRIVE 2
    drive2_t = ThrustCalculator(MTOW - massHydrogen, 29.0, 29.0, 29.0, 0.0, 50000.0 / 29.0, 0, 0, 1)
    power.append(enginePower(drive2_t.thrust, drive2_t.velocity))
    energy.append(power[-1] * drive2_t.duration)
    massHydrogen = massHydrogen + ((power[-1] / 0.6) / SED_hydrogen) * drive2_t.duration

    print("######################")
    print("Hydrogen mass: ", massHydrogen)
    print("Hydrogen volume: ", massHydrogen/66.5)

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

    print("#######################")
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

    plt.figure(5)
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

    missionDuration = 0.0
    for i in range(8):
        missionDuration += switch[i].duration

    materials = ["Carbon Fiber", "Al2O3 Laminate", "Aluminum 8091"]
    yieldStrength = [738.0E6, 252.0E6, 505.0E6]
    density = [1.58E3, 3.4E3, 2.61E3]

    materialsI = ["Melamine Foam", "Aerogel", "Expanded PS Foam"]
    thermalConductivity = [0.032, 0.011, 0.033]
    densityFoam = [9.0, 70.0, 18.0]

    style.use('ggplot')
    fig = plt.figure()
    ax13d = fig.add_subplot(111, projection='3d')

    structuralMaterials = []
    insulatingMaterials = []
    tankMasses = []
    tankThicknesses = []

    for i in range(len(materials)):
        for j in range(len(materialsI)):
            print("#########################")
            print("If using ", materials[i], " for structure and ", materialsI[j], " for insulation")
            tankSize = tankSizing(220000, massHydrogen, massHydrogen / 66.5, yieldStrength[i], density[i], 2.0, missionDuration,
                       thermalConductivity[j], densityFoam[j])
            print("Total tank mass:")
            print(tankSize[0], " kg")
            print("Total tank thickness: ")
            print(tankSize[1]*1000.0, " mm")

            structuralMaterials.append(i)
            insulatingMaterials.append(j)
            tankMasses.append(tankSize[0])
            tankThicknesses.append(tankSize[1]*1000.0)


            print("Structural tank mass:")
            print(tankSize[2], " kg")
            print("Structural tank thickness: ")
            print(tankSize[3]*1000.0, " mm")
            print("Insulating tank mass:")
            print(tankSize[4], " kg")
            print("Insulating tank thickness: ")
            print(tankSize[5]*1000.0, " mm")

    print("Internal Radius of tank (hydrogen):")
    print(tankSize[6] * 1000.0, " mm")

    colors3D = ['gold', 'lightcoral', 'lightskyblue', 'gold', 'lightcoral', 'lightskyblue', 'gold', 'lightcoral', 'lightskyblue']

    dx = 0.5*np.ones(len(structuralMaterials))
    dy = 0.5*np.ones(len(insulatingMaterials))
    ax13d.bar3d(structuralMaterials, insulatingMaterials, np.zeros(len(structuralMaterials)), dx, dy, tankMasses, color=colors3D)
    #ax13d.set_xlabel('Structural Material')
    #ax13d.set_ylabel('Insulating Material')
    ax13d.set_zlabel('Tank Mass [kg]')
    plt.xticks(np.arange(3), materials, rotation=10)
    plt.yticks(0.7 + np.arange(3), materialsI, rotation=-20)
    plt.title("Tank Masses for Material Selection")

    fig = plt.figure()
    ax13d = fig.add_subplot(111, projection='3d')

    dx = 0.5 * np.ones(len(structuralMaterials))
    dy = 0.5 * np.ones(len(insulatingMaterials))
    ax13d.bar3d(structuralMaterials, insulatingMaterials, np.zeros(len(structuralMaterials)), dx, dy, tankThicknesses, colors3D)
    # ax13d.set_xlabel('Structural Material')
    # ax13d.set_ylabel('Insulating Material')
    ax13d.set_zlabel('Tank Thickness [mm]')
    plt.xticks(np.arange(3), materials, rotation=10)
    plt.yticks(0.7 + np.arange(3), materialsI, rotation=-20)
    plt.title("Tank Thicknesses for Material Selection")

    plt.show()
    return


if __name__ == "__main__":
    fuelCalc()
