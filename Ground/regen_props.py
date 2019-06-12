# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:22:49 2019

@author: ttweedy
"""
import math

def wind():
    wind_speed = []
    i=0
    while i < 31:
        wind_speed.append(i)
        i+=2
        
    return wind_speed
print(wind())

def power(wind_speed):
    power = []
    rho = 1.225
    area = (0.576/2)**2 * math.pi
    eff = 0.2
    for i in wind_speed:
        power_speed = rho * area * i**3 * eff
        power.append(power_speed)
    return power
print(power(wind()))
        
    