import math
import sys
sys.path.insert(0, '../PowerElectrical/')
from isa import IsaCalculator
import numpy as np

def thermalControl(h, cabinSA, k, Ti):
    """Calculates the power required to heat the cabin.
    Inputs:
    h: altitude (m)
    cabinV: volume of cabin (m^3)
    cabinSA: cabin surface area (m^2)
    k: outer skin material's heat transfer coefficient (W/ m^2 K)
    Ti: desired interior temp (celsius)"""
    dT = Ti - isa.IsaCalculator(h)[1]
    reqPower = 2.0*cabinSA*k*dT
    return

def main():
    cabinSA = math.pi*(1.3)**2.0
    k = 4.5


    return

if __name__ == "__main__":
    main()