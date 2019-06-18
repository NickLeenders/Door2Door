# For the structures guys: Please make your modules update the values in these class so Control and other people can use them.
import numpy as np
import sys

sys.path.insert(0, '../PowerElectrical/')
from power import IsaCalculator


class x_positions:
    def __init__(self):
        self.x_tail = 5.0
        self.x_structure = 2.75
        self.x_propeller = 2.5
        self.x_wing = 2.875
        self.x_drivetrain = 0.51
        self.x_fuel = 3.490
        self.x_cell = 1.725
        self.x_payload = 2.61
        self.x_passenger = [2.00, 2.80]  # c.g. position front passenger and back passengers (1-3 configuration)
        self.x_battery = 2.61
        self.x_tank = 3.490
        self.x_cargo = 4.27
        self.x_wheel_fr = 0.86775
        self.x_wheel_bk = 4.984


class y_positions:
    def __init__(self):
        self.y_prop_position = [1.5, 2.1, 2.7, 3.3,
                                4.4]  # centerline of main body to tip of the wing for one side symmetric


class z_positions:
    def __init__(self):
        # TODO All not exact distances
        self.z_tail = 1.163
        self.z_structure = 1.2
        self.z_propeller = 1.7
        self.z_wing = 1.7
        self.z_drivetrain = 0.15
        self.z_fuel = 0.5
        self.z_cell = 0.5
        self.z_passenger = 0.7
        self.z_battery = 0.35
        self.z_tank = 0.7
        self.z_cargo = 0.5


class w_components:
    def __init__(self, wing_weight, emp_weight):
        self.w_tail = emp_weight
        self.w_structure = 385.5112  # TODO not done yet
        self.w_propeller = 316.48  # 16.36kg (8x), 30kg (2x) and including motor that are 8.2kg (8x), 30kg (2x)
        self.w_wing = wing_weight
        self.w_drivetrain = 158.75  # Includes ground motor and converter
        self.w_fuel = 16.66
        self.w_cell = 63.29
        self.w_payload = 360
        self.w_passenger = 80.0  # TODO add seat weight to this
        self.w_battery = 75  # TODO not done yet
        self.w_tank = 45.39  # Done
        self.w_cargo = 40
