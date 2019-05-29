import math
import sys
sys.path.insert(0, '../Aerodynamics/')
import aero
import aerodynamic_parameters
sys.path.insert(0, '../PowerElectrical/')
from isa import IsaCalculator
sys.path.insert(0, '../Airframe/')
import total_masses

class ThrustCalculator:

    """Preliminary required thrust calculation for one phase"""


    def __init__(self, velocity, altitude, duration, rateOfClimb=0.0, acceleration=0.0, driving=0):

        self.aero_vals = aerodynamic_parameters.aero_vals()
        self.wing_vals = aerodynamic_parameters.wing_vals()
        self.emp_vals = aerodynamic_parameters.emp_vals()

        self.mass_vals = total_masses.total_mass()

        self.mass = self.mass_vals.MTOW
        self.range = 400000
        self.mu = 0.015 #TODO take mu value for ground system

        self.velocity = velocity
        self.altitude = altitude
        self.rho, self.T, self.p = IsaCalculator(altitude)
        self.duration = duration

        self.drag = aero.drag(self.aero_vals.cd0, self.aero_vals.cl, self.wing_vals.b, self.wing_vals.MAC,
                              self.wing_vals.e, self.velocity, self.rho)
        self.acceleration = acceleration
        if driving != 0:
            self.friction = self.mass*9.80665*self.mu
        else:
            self.friction = 0.0
        self.thrust = self.drag + self.mass*self.acceleration + self.friction + rateOfClimb*self.mass*9.80665/velocity


# def takeoff_cl()
#     takeOff_t = ThrustCalculator(28.28, 0.0, 1500 / 2.5, 0, 0.8, 1)
#     takeOff_l = aero.Propellers(takeOff_t.thrust, takeOff_t.velocity,
#                                 takeOff_t.rho, takeOff_t.cl, 1)
#
#     return
#
# def climb_cl()
#
#     return
#
# def cruise_cl()
#
#     return



def main():
    #drive1_t = ThrustCalculator(29.0, 0.0, 50000.0/29.0, 0, 0, 1)

    takeOff_t = ThrustCalculator(25.0, 0.0, 1500 / 2.5, 0, 0.8, 1)
    takeOff_l = aero.Propellers(takeOff_t.thrust, takeOff_t.velocity,
                                takeOff_t.rho, takeOff_t.cl, 1)

    print(takeOff_l.lift_powered)
    print(takeOff_t.mass*9.80665)
    print(takeOff_l.v_wakeCP)
    print(takeOff_t.cl)
    print(takeOff_l.powerCP)
    print(takeOff_l.powerHLP)

    # iterating = True
    # while (iterating):
    #     takeOff_t = ThrustCalculator(36.0, 0.0, 1500/2.5, 0, 4.0/3.0, 1)
    #     takeOff_l = aero.Propellers(takeOff_t.thrust, takeOff_t.velocity,
    #                                       takeOff_t.rho, takeOff_t.cl, 0)
    #     if(takeOff_l.lift_powered < takeOff_t.mass*9.80665):


    #climb = ThrustCalculator(math.sqrt(2*takeOff.mass*9.80665/(takeOff.S*takeOff.rho*math.sqrt(3*math.pi*takeOff.cd0*takeOff.A*takeOff.e))), 750, 1500/7.44)

    #cruise = ThrustCalculator(69.4, 1500, 400000/69.4 + climb.duration)

    #reserve = ThrustCalculator(69.0, 1500, 45*60)

    #landStart = ThrustCalculator(31.0, 1500, 600)

    #landing = ThrustCalculator(31.0, 750, 1500/(31.0*sin(math.atan(1.0/3.0))))

    #drive2 = ThrustCalculator(29.0, 0.0, 50000.0 / 29.0, 0, 0, 1)

    return


if __name__ == "__main__":
    main()
