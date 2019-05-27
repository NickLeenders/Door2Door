from math import *


x_tail = 5.4
x_structure = 3
x_propeller = 2.5
x_wing = 2.8
x_drivetrain = 3.97
x_fuel = 0.5
x_cell = 0.5
x_payload = 2.61
x_battery = 2.61
x_tank = 0.5

z_tail = 1.4
z_structure = 1.2
z_propeller = 1.4
z_wing = 1.4
z_drivetrain = 0.15
z_fuel = 0.5
z_cell = 0.5
z_payload = 0.6
z_battery = 0.15
z_tank = 0.5

w_tail = 20.71
w_structure = 385.5112
w_propeller = 260
w_wing = 162.488
w_drivetrain = 30
w_fuel = 90
w_cell = 63.29
w_payload = 360
w_battery = 75
w_tank = 108

def function_OEW_CG():
    OEW_CG = (x_tail*w_tail + x_structure*w_structure + x_propeller*w_propeller + x_wing*w_wing + x_drivetrain*w_drivetrain \
          + x_cell*w_cell + x_battery*w_battery + x_tank*w_tank)/(w_tail + w_structure \
          + w_propeller + w_wing + w_drivetrain + w_cell + w_battery + w_tank)
    return OEW_CG
def function_total_EOW_mass():
    mass_OEW_CG = (w_tail + w_structure + w_propeller + w_wing + w_drivetrain + w_cell + w_battery + w_tank)
    return mass_OEW_CG

def function_XCG():
    X_CG = (x_tail*w_tail + x_structure*w_structure + x_propeller*w_propeller + x_wing*w_wing + x_drivetrain*w_drivetrain \
          + x_fuel*w_fuel + x_cell*w_cell + x_payload*w_payload + x_battery*w_battery + x_tank*w_tank)/(w_tail + w_structure \
          + w_propeller + w_wing + w_drivetrain + w_fuel + w_cell + w_payload + w_battery + w_tank)
    return X_CG

def function_ZCG():
    X_CG = (z_tail*w_tail + z_structure*w_structure + z_propeller*w_propeller + z_wing*w_wing + z_drivetrain*w_drivetrain \
          + z_fuel*w_fuel + z_cell*w_cell + z_payload*w_payload + z_battery*w_battery + z_tank*w_tank)/(w_tail + w_structure \
          + w_propeller + w_wing + w_drivetrain + w_fuel + w_cell + w_payload + w_battery + w_tank)
    return (X_CG)


