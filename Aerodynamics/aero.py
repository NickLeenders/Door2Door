import sys
import math
import numpy as np
import sys
from aerodynamic_parameters import wing_vals
sys.path.insert(0, '../Aerodynamics/')
import aerodynamic_parameters
sys.path.insert(0, '../PowerElectrical/')
import power

def drag(cd0, cl, b, c, e, v, rho):
    cdw = 0.018 #cd0 + (cl**2)/(math.pi*(b/c)*e)

    lf=5.5 #length fuselage
    df=(2.4+1.5)*(2.0/math.pi) #'diameter fuselage'
    lambdaf=lf/df #ratio
    ln=2.3 #nose to circular distance
    #taper=wing_vals().taper_ratio
    #tct=0.18
    #tcr=0.18
    #Sexpw=S-1.2*2.4
    cfe=0.0045
    S = wing_vals().S


    taperh=1.0
    tcth=0.12
    tcrh=0.12
    Sexph=3.84

    taperv=1.0
    tctv = 0.12
    tcrv = 0.12
    Sexpv = 1.2*1.5

    Swetf=math.pi*df*lf*((0.5+0.135*ln/lf)**(2/3))*(1.015+0.3/(lambdaf**1.5))
    Swetv = 2 * Sexpv * (1 + 0.25 * tcrv * (1 + taperv * tctv / tcrv) / (1 + taperv))
    Sweth = 2 * Sexph * (1 + 0.25 * tcrh * (1 + taperh * tcth / tcrh) / (1 + taperh))

    CD0=cfe*(Sweth+Swetv+Swetf)/(S)
    cd=CD0+cdw
    d = cd * S * 0.5 * 1.09 * 69.4** 2

    return d

def propEfficiency(BHP, V, rho, Dp, Nv):
    """This routine estimates the propeller efficiency for a constant speed propeller,

    by iterating the propulsive disk equations with a user supplied viscous profile efficiency."""

    #Input variables:

    #   BHP = Engine watts --> horse power at condition in BHP

    #   V   = Velocity at condition in m/s --> ft/s

    #   H   = Pressure Altitude in m --> ft

    #   Dp = Propeller diameter in m --> ft

    #   Nv = User entered viscous profile efficiency


    #Convert input
    BHP = BHP / 745.7 #Convert to HP
    Dp = Dp * 3.28084 #Convert to feet
    V = V * 3.28084   #Convert to ft/s
    Dp = Dp * 3.28084 #Convert to feet

    #Presets
    A = 3.14159265358979*(Dp ** 2.0)/4.0                  #Prop area (ftˆ2)

    rho = rho*0.00194032    #Air density at pressure alt

    Np = 0.5                                            #Initial propeller efficiency

    #Check the value of V to prevent a function crash
    if (V == 0.0):
        PropEfficiency = 0.0
        return PropEfficiency

    #Iterate to get a solution
    Delta = 0.0
    while (Delta < 0.0001):
        T = Np*BHP*550.0 / V                          #Thrust (lbf)

        w = 0.5*(math.sqrt(V*V + 2*T / (rho*A)) - V)  #Induced velocity (ft/s)

        Ni = 1.0 / (1.0 + w / V)                            #Ideal efficiency

        Npnew = Nv * Ni                                 #New efficiency

        Delta = abs(Np - Npnew)                         #Difference

        Np = Npnew                                     #Set a new Np before next iteration

    PropEfficiency = Np

    return PropEfficiency

class Propellers:

    # Yuneec Power Drive 20
    #
    numberHLP = 8
    diameterHLP = 0.576
    maxpowerHLP = 20000
    #efficiencyHLP = 0.75
    weightHLP = 16.36 + 8.2 #Prop + engine

    #Yuneec Power Drive 60
    #
    numberCP = 2
    diameterCP = 1.524
    maxpowerCP = 60000
    #efficiencyCP = 0.8
    weightCP = 30.0 + 30.0 #Prop + engine

    b = 8.8
    c_avg = 1.2
    S = b * c_avg
    A = b / c_avg



    def __init__(self, thrust, v_infty, rho, cl, stol=0):
        self.efficiencyHLP = propEfficiency(self.maxpowerHLP, v_infty, rho, self.diameterHLP, 0.87)
        self.efficiencyCP = propEfficiency(self.maxpowerCP, v_infty, rho, self.diameterCP, 0.9)
        if (stol==0):
            self.powerCP = self.maxpowerCP*self.efficiencyCP
            coefficientsCP = [1, -2, 1, 2 * self.powerCP / (
                    (v_infty ** 3) * rho * math.pi * self.diameterCP ** 2)]
            self.a_CP = np.roots(coefficientsCP)
            self.a_CP = float(np.real(self.a_CP[np.isreal(self.a_CP)]))
            self.v_wakeCP = (1 - 2 * self.a_CP) * v_infty
            self.thrustCP = self.numberCP * rho * 0.5 * math.pi * ((self.diameterCP**2)/4)*(self.v_wakeCP ** 2 - v_infty ** 2)
            if (self.thrustCP > thrust):
                self.v_wakeCP = math.sqrt(((8.0 * thrust) / (
                        self.numberCP * rho * math.pi * (self.diameterCP ** 2))) + v_infty ** 2)
                self.a_CP = (v_infty - self.v_wakeCP) / (2.0 * v_infty)
                self.thrustCP = self.numberCP * rho * (1.0 / 8.0) * math.pi * (self.diameterCP ** 2) * (
                        self.v_wakeCP ** 2 - v_infty ** 2)
                self.powerCP = self.thrustCP * v_infty * (1.0 - self.a_CP) / self.numberCP
                self.v_wakeHLP = v_infty
                self.a_HLP = 0.0
                self.thrustHLP = 0.0
                self.powerHLP = 0.0
            else:
                self.v_wakeHLP = math.sqrt(((8.0 * (thrust - self.thrustCP)) / (
                        self.numberHLP * rho * math.pi * (self.diameterHLP ** 2))) + v_infty ** 2)
                self.a_HLP = (v_infty - self.v_wakeHLP) / (2.0 * v_infty)
                self.thrustHLP = self.numberHLP * rho * (1.0 / 8.0) * math.pi * (self.diameterHLP ** 2) * (
                        self.v_wakeHLP ** 2 - v_infty ** 2)
                self.powerHLP = self.thrustHLP*v_infty*(1.0 - self.a_HLP) / self.numberHLP
            assert self.powerHLP <= self.maxpowerHLP*self.efficiencyHLP, "Not enough propeller power for these thrust values"
        elif (stol==1):
            self.powerHLP = self.maxpowerHLP*self.efficiencyHLP
            coefficientsHLP = [1, -2, 1, 2 * self.maxpowerHLP * self.efficiencyHLP / (
                    (v_infty ** 3) * rho * math.pi * self.diameterHLP ** 2)]
            self.a_HLP = np.roots(coefficientsHLP)
            self.a_HLP = float(np.real(self.a_HLP[np.isreal(self.a_HLP)]))
            self.v_wakeHLP = (1 - 2 * self.a_HLP) * v_infty
            self.thrustHLP = self.numberHLP*rho*0.5*math.pi*((self.diameterHLP**2)/4)*(self.v_wakeHLP**2 - v_infty**2)
            if (self.thrustHLP > thrust):
                self.v_wakeHLP = math.sqrt(((8.0 * thrust) / (
                        self.numberHLP * rho * math.pi * (self.diameterHLP ** 2))) + v_infty ** 2)
                self.a_HLP = (v_infty - self.v_wakeHLP) / (2.0 * v_infty)
                self.thrustHLP = self.numberHLP * rho * (1.0 / 8.0) * math.pi * (self.diameterHLP ** 2) * (
                        self.v_wakeHLP ** 2 - v_infty ** 2)
                self.powerHLP = self.thrustHLP * v_infty * (1.0 - self.a_HLP) / self.numberHLP
                self.v_wakeCP = v_infty
                self.a_CP = 0.0
                self.thrustCP = 0.0
                self.powerCP = 0.0
            else:
                self.v_wakeCP = math.sqrt(((8.0*(thrust - self.thrustHLP)) / (self.numberCP * rho * math.pi * (self.diameterCP ** 2))) + v_infty**2)
                self.a_CP = (v_infty - self.v_wakeCP) / (2.0*v_infty)
                self.thrustCP = self.numberCP * rho * (1.0/8.0) * math.pi * (self.diameterCP**2) * (self.v_wakeCP ** 2 - v_infty ** 2)
                self.powerCP = self.thrustCP*v_infty*(1.0-self.a_CP) / self.numberCP
                #self.powerCPalt1 = -self.numberCP*(1.0/8.0)*math.pi*(self.diameterCP**2)*rho*(v_infty**2 - self.v_wakeCP**2)*v_infty*(1.0-self.a_CP)
                #self.powerCPalt2 = -self.numberCP*0.5*rho*math.pi*(self.diameterCP**2)*(v_infty**3)*self.a_CP*(1-self.a_CP)**2
            assert self.powerCP <= self.maxpowerCP*self.efficiencyCP, "Not enough propeller power for these thrust values"


        self.lift_powered = cl*0.5*rho*(self.numberHLP*self.diameterHLP*self.c_avg*self.v_wakeHLP**2 +
                                       self.numberCP*0.5*self.diameterCP*self.c_avg*self.v_wakeCP**2 +
                                       (self.b - self.numberHLP*self.diameterHLP - self.numberCP*0.5*self.diameterCP)*self.c_avg*v_infty**2)



def main():
    takeOff_t = power.ThrustCalculator(28.28, 0.0, 1500 / 2.5, 0, 0.8, 1)

    return

if __name__ == "__main__":
    main()
