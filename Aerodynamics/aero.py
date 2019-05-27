import math
import numpy as np


def drag(cd0, cl, b, c, e, v, rho):
    cd = cd0 + (cl**2)/(math.pi*(b/c)*e)
    d = cd*b*c*0.5*rho*v**2
    return d

class Propellers:

    numberHLP = 8
    diameterHLP = 0.576
    maxpowerHLP = 14400
    efficiencyHLP = 0.8

    numberCP = 2
    diameterCP = 1.524
    maxpowerCP = 48120
    efficiencyCP = 0.8

    b = 8.8
    c_avg = 1.2
    S = b * c_avg
    A = b / c_avg



    def __init__(self, thrust, v_infty, rho, cl, stol=0):

        if (stol=0):
            self.powerCP = self.maxpowerCP*self.efficiencyCP
            coefficientsCP = [1, -2, 1, 2 * self.maxpowerCP * self.efficiencyCP / (
                    (v_infty ** 3) * rho * math.pi * self.diameterCP ** 2)]
            a_CP = np.roots(coefficientsCP)
            a_CP = float(np.real(a_CP[np.isreal(a_CP)]))
            self.v_wakeCP = (1 - 2 * a_CP) * v_infty
            self.v_wakeHLP = math.sqrt((thrust - self.numberCP*0.5*rho*math.pi*((self.diameterCP**2)/4)*(
                    self.v_wakeCP**2 - v_infty**2))/(self.numberHLP*0.5*rho*math.pi*((self.diameterHLP**2)/4)) +
                                       v_infty**2)
            a_HLP = (v_infty - self.v_wakeHLP)/v_infty
            self.powerHLP = 2.0*rho*self.A*(v_infty**3)*a_HLP*(1 - a_HLP)**2
            assert self.powerHLP <= self.maxpowerHLP*self.efficiencyHLP, "Not enough propeller power for these thrust values"
        elif (stol=1):
            self.powerHLP = self.maxpowerHLP*self.efficiencyHLP
            coefficientsHLP = [1, -2, 1, 2 * self.maxpowerHLP * self.efficiencyHLP / (
                    (v_infty ** 3) * rho * math.pi * self.diameterHLP ** 2)]
            a_HLP = np.roots(coefficientsHLP)
            a_HLP = float(np.real(a_HLP[np.isreal(a_HLP)]))
            self.v_wakeHLP = (1 - 2 * a_HLP) * v_infty
            self.v_wakeCP = math.sqrt((thrust - self.numberHLP * 0.5 * rho * math.pi * ((self.diameterHLP ** 2) / 4) * (
                    self.v_wakeHLP ** 2 - v_infty ** 2)) / (self.numberCP * 0.5 * rho * math.pi * (
                        (self.diameterCP ** 2) / 4)) +
                                       v_infty ** 2)
            a_CP = (v_infty - self.v_wakeCP) / v_infty
            self.powerCP = 2.0 * rho * self.A * (v_infty ** 3) * a_CP * (1 - a_CP) ** 2
            assert self.powerCP <= self.maxpowerCP, "Not enough propeller power for these thrust values"

        self.lift_noPower = cl*self.S*0.5*rho*v_infty**2
        self.lift_powered = cl*0.5*rho(numberHLP*diameterHLP*c_avg*v_wakeHLP**2 +
                                       numberCP*0.5*diameterCP*c_avg*v_wakeCP**2 +
                                       (b - numberHLP*diameterHLP - numberCP*0.5*diameterCP)*c_avg*v_infty**2)
        self.cl_effective = cl*(self.lift_powered/self.lift_noPower)
