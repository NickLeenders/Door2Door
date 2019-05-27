import sys
sys.path.insert(0, '../Airframe/')
from masses_cg_positions import x_positions, z_positions, w_components

w_tail = w_components().w_tail
w_structure = w_components().w_structure
w_propeller = w_components().w_propeller
w_wing = w_components().w_wing
w_drivetrain = w_components().w_drivetrain
w_fuel = w_components().w_fuel
w_cell = w_components().w_cell
w_payload = w_components().w_payload
w_battery = w_components().w_battery
w_tank = w_components().w_tank

z_tail = z_positions().z_tail
z_structure = z_positions().z_structure
z_propeller = z_positions().z_propeller
z_wing = z_positions().z_wing
z_drivetrain = z_positions().z_drivetrain
z_fuel = z_positions().z_fuel
z_cell = z_positions().z_cell
z_payload = z_positions().z_payload
z_battery = z_positions().z_battery
z_tank = z_positions().z_tank

x_tail = x_positions().x_tail
x_structure = x_positions().x_structure
x_propeller = x_positions().x_propeller
x_wing = x_positions().x_wing
x_drivetrain = x_positions().x_drivetrain
x_fuel = x_positions().x_fuel
x_cell = x_positions().x_cell
x_payload = x_positions().x_payload
x_battery = x_positions().x_battery
x_tank = x_positions().x_tank


def function_OEW_CG():
    OEW_CG = (
                     x_tail * w_tail + x_structure * w_structure + x_propeller * w_propeller + x_wing * w_wing + x_drivetrain * w_drivetrain \
                     + x_cell * w_cell + x_battery * w_battery + x_tank * w_tank) / (w_tail + w_structure \
                                                                                     + w_propeller + w_wing + w_drivetrain + w_cell + w_battery + w_tank)
    return OEW_CG


def function_total_EOW_mass():
    mass_OEW_CG = (w_tail + w_structure + w_propeller + w_wing + w_drivetrain + w_cell + w_battery + w_tank)
    return mass_OEW_CG


def function_XCG():
    X_CG = (
                   x_tail * w_tail + x_structure * w_structure + x_propeller * w_propeller + x_wing * w_wing + x_drivetrain * w_drivetrain \
                   + x_fuel * w_fuel + x_cell * w_cell + x_payload * w_payload + x_battery * w_battery + x_tank * w_tank) / (
                   w_tail + w_structure \
                   + w_propeller + w_wing + w_drivetrain + w_fuel + w_cell + w_payload + w_battery + w_tank)
    return X_CG


def function_ZCG():
    get_values()
    X_CG = (
                   z_tail * w_tail + z_structure * w_structure + z_propeller * w_propeller + z_wing * w_wing + z_drivetrain * w_drivetrain \
                   + z_fuel * w_fuel + z_cell * w_cell + z_payload * w_payload + z_battery * w_battery + z_tank * w_tank) / (
                   w_tail + w_structure \
                   + w_propeller + w_wing + w_drivetrain + w_fuel + w_cell + w_payload + w_battery + w_tank)
    return (X_CG)
