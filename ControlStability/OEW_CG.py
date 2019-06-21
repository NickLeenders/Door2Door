import sys

sys.path.insert(0, '../Airframe/')
sys.path.insert(0, '../Structure/')

from masses_cg_positions import x_positions, z_positions, w_components
from mass_calculation import wing_weight, emp_weight, MTOW, mass_iteration


# TODO Fix MTOW by actual MTOW iteration
w_tail = mass_iteration(MTOW)[2]
w_structure = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_structure
w_propeller = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_propeller
w_wing = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_wing
w_drivetrain = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_drivetrain
w_fuel = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_fuel
w_cell = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_cell
w_passenger = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_passenger
w_battery = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_battery
w_tank = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_tank
w_cargo = w_components(wing_weight(MTOW), emp_weight(MTOW)).w_cargo

z_tail = z_positions().z_tail
z_structure = z_positions().z_structure
z_propeller = z_positions().z_propeller
z_wing = z_positions().z_wing
z_drivetrain = z_positions().z_drivetrain
z_fuel = z_positions().z_fuel
z_cell = z_positions().z_cell
z_passenger = z_positions().z_passenger
z_battery = z_positions().z_battery
z_tank = z_positions().z_tank
z_cargo = z_positions().z_cargo

x_tail = x_positions().x_tail
x_structure = x_positions().x_structure
x_propeller = x_positions().x_propeller
x_wing = x_positions().x_wing
x_drivetrain = x_positions().x_drivetrain
x_fuel = x_positions().x_fuel
x_cell = x_positions().x_cell
x_passenger = x_positions().x_passenger
x_battery = x_positions().x_battery
x_tank = x_positions().x_tank
x_cargo = x_positions().x_cargo


def function_OEW_CG():
    OEW_CG = (
                     x_tail * w_tail + x_structure * w_structure + x_propeller * w_propeller + x_wing * w_wing + x_drivetrain * w_drivetrain \
                     + x_cell * w_cell + x_battery * w_battery + x_tank * w_tank) / (w_tail + w_structure \
                                                                                     + w_propeller + w_wing + w_drivetrain + w_cell + w_battery + w_tank)
    return OEW_CG


def function_total_EOW_mass():
    mass_OEW_CG = (w_tail + w_structure + w_propeller + w_wing + w_drivetrain + w_cell + w_battery + w_tank)
    print (w_wing)
    print (w_tail)
    return mass_OEW_CG


def function_XCG():
    X_CG = (
                   x_tail * w_tail + x_structure * w_structure + x_propeller * w_propeller + x_wing * w_wing + x_drivetrain * w_drivetrain \
                   + x_fuel * w_fuel + x_cell * w_cell + x_passenger[0] * w_passenger + 3 * x_passenger[
                       1] * w_passenger + x_battery * w_battery + x_tank * w_tank + x_cargo * w_cargo) / (
                   w_tail + w_structure \
                   + w_propeller + w_wing + w_drivetrain + w_fuel + w_cell + w_passenger*4 + w_battery + w_tank + w_cargo)
    return X_CG


def function_ZCG():
    X_CG = (
                   z_tail * w_tail + z_structure * w_structure + z_propeller * w_propeller + z_wing * w_wing + z_drivetrain * w_drivetrain \
                   + z_fuel * w_fuel + z_cell * w_cell + z_passenger * w_passenger + 3 * z_passenger * w_passenger + z_battery * w_battery + z_tank * w_tank + z_cargo * w_cargo) / (
                   w_tail + w_structure \
                   + w_propeller + w_wing + w_drivetrain + w_fuel + w_cell + w_passenger*4 + w_battery + w_tank + w_cargo)
    return (X_CG)

print (function_total_EOW_mass())
print (function_XCG())
print (function_ZCG())