# For the structures guys: Please make your modules update the values in these class so Control and other people can use them.
import numpy as np
import sys
sys.path.insert(0, '../Structure/')
#from Mass_calculation import wing_weight
import Mass_calculation
class x_positions():
    def __init__(self):
        self.x_tail = 5.4
        self.x_structure = 3
        self.x_propeller = 2.5
        self.x_wing = 2.8
        self.x_drivetrain = 3.97
        self.x_fuel = 0.5
        self.x_cell = 0.5
        self.x_payload = 2.61
        self.x_battery = 2.61
        self.x_tank = 0.5


class z_positions():
    def __init__(self):
        self.z_tail = 1.4
        self.z_structure = 1.2
        self.z_propeller = 1.4
        self.z_wing = 1.4
        self.z_drivetrain = 0.15
        self.z_fuel = 0.5
        self.z_cell = 0.5
        self.z_payload = 0.6
        self.z_battery = 0.15
        self.z_tank = 0.5


class w_components():
    def __init__(self):
        self.MTOW = 1634
        self.w_tail = 20.71
        self.w_structure = 385.5112
        self.w_propeller = 260
        self.w_wing = wing_weight()
        self.w_drivetrain = 30
        self.w_fuel = 90
        self.w_cell = 63.29
        self.w_payload = 360
        self.w_battery = 75
        self.w_tank = 108
