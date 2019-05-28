import isa
import math
import Aerodynamics.aero as aero

class ThrustCalculator:
    """Preliminary required thrust calculation for one phase"""
    b = 8.8
    c_avg = 1.2
    S = b*c_avg
    A = b/c_avg
    cd0 = 0.07
    e = 0.8
    mass = 1558
    mu = 0.015
    range = 400000

    def __init__(self, velocity, altitude, duration, rateOfClimb=0.0, acceleration=0.0, driving=0):
        self.velocity = velocity
        self.altitude = altitude
        self.rho, self.T, self.p = isa.IsaCalculator(altitude)
        self.duration = duration
        if abs(rateOfClimb) < 1.0E-5:
            self.cl = (self.mass*9.80665)/(self.S*0.5*self.rho*self.velocity**2)
        elif rateOfClimb > 1.0E-5:
            self.cl = math.sqrt(3*math.pi*self.cd0*self.A*self.e)
        self.drag = aero.drag(self.cd0, self.cl, self.b, self.c_avg, self.e, self.velocity, self.rho)
        self.acceleration = acceleration
        if driving != 0:
            self.friction = self.mass*9.80665*self.mu
        else:
            self.friction = 0.0
        self.thrust = self.drag + self.mass*self.acceleration + self.friction + rateOfClimb*self.mass*9.80665/velocity


def main():
    #drive1_t = ThrustCalculator(29.0, 0.0, 50000.0/29.0, 0, 0, 1)

    takeOff_t = ThrustCalculator(36.0, 0.0, 1500 / 2.5, 0, 0.8, 1)
    takeOff_l = aero.Propellers(takeOff_t.thrust, takeOff_t.velocity,
                                takeOff_t.rho, takeOff_t.cl, 1)

    print(takeOff_l.lift_powered)
    print(takeOff_t.mass*9.80665)
    # iterating = True
    # while (iterating):
    #     takeOff_t = ThrustCalculator(36.0, 0.0, 1500/2.5, 0, 4.0/3.0, 1)
    #     takeOff_l = aero.Propellers(takeOff_t.thrust, takeOff_t.velocity,
    #                                       takeOff_t.rho, takeOff_t.cl, 0)
    #     if(takeOff_l.lift_powered < takeOff_t.mass*9.80665):


    #climb = ThrustCalculator(2*takeOff.mass*9.80665/(takeOff.S*takeOff.rho*math.sqrt(3*math.pi*takeOff.cd0*takeOff.A*takeOff.e)), 750, 1500/7.44)

    #cruise = ThrustCalculator(69.4, 1500, 400000/69.4 + climb.duration)

    #reserve = ThrustCalculator(69.0, 1500, 45*60)

    #landStart = ThrustCalculator(31.0, 1500, 600)

    #landing = ThrustCalculator(31.0, 750, 1500/(31.0*sin(math.atan(1.0/3.0))))

    #drive2 = ThrustCalculator(29.0, 0.0, 50000.0 / 29.0, 0, 0, 1)

    return


if __name__ == "__main__":
    main()
