from math import *
from OEW_CG import *
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, '../Airframe/')
sys.path.insert(0, '../Aerodynamics/')
from masses_cg_positions import x_positions, z_positions, w_components
from aerodynamic_parameters import aero_vals



def loading_diagram():
    " *** Cargo *** "
    cargo_cg = [function_OEW_CG()]
    cargo_mass = [function_total_EOW_mass()]

    cargo_cg.append((cargo_cg[0]*cargo_mass[0] + x_positions().x_cargo*w_components().w_cargo)/(cargo_mass[0] + w_components().w_cargo))
    cargo_mass.append(cargo_mass[0] + w_components().w_cargo)

    " *** Payload *** "

    payload_cg_fb = [cargo_cg[-1]]
    payload_cg_bf = [cargo_cg[-1]]

    payload_mass_fb = [cargo_mass[-1]]
    payload_mass_bf = [cargo_mass[-1]]

    cg_mass_update = 0
    mass_update = 0
    for i in range(len(x_positions().x_passenger)):
        payload_mass_fb.append(cargo_mass[-1] + mass_update + w_components().w_passenger[i])
        payload_cg_fb.append((cargo_cg[-1]*cargo_mass[-1] + cg_mass_update + x_positions().x_passenger[i]*w_components().w_passenger[i])/(cargo_mass[-1] + mass_update + w_components().w_passenger[i]))
        cg_mass_update = cg_mass_update + x_positions().x_passenger[i]*w_components().w_passenger[i]
        mass_update = mass_update + w_components().w_passenger[i]

    x_passenger = x_positions().x_passenger
    w_passenger = w_components().w_passenger
    x_passenger.reverse()
    w_passenger.reverse()

    cg_mass_update = 0
    mass_update = 0
    for i in range(len(x_passenger)):
        payload_mass_bf.append(cargo_mass[-1] + mass_update + w_passenger[i])
        payload_cg_bf.append((cargo_cg[-1]*cargo_mass[-1] + cg_mass_update + x_passenger[i]*w_passenger[i])/(cargo_mass[-1] + mass_update + w_passenger[i]))
        cg_mass_update = cg_mass_update + x_passenger[i]*w_passenger[i]
        mass_update = mass_update + w_passenger[i]

    " *** Fuel ***"
    fuel_cg = [payload_cg_fb[-1]]
    fuel_mass = [payload_mass_fb[-1]]

    fuel_cg.append((fuel_cg[0]*fuel_mass[0] + x_positions().x_fuel*w_components().w_fuel)/(fuel_mass[0] + w_components().w_fuel))
    fuel_mass.append(fuel_mass[0] + w_components().w_fuel)

    margin_min = min(cargo_cg + payload_cg_fb + fuel_cg)*0.98
    margin_max = max(cargo_cg + payload_cg_bf + fuel_cg)*1.02

    #convert values with respect to MAC
    cargo_cg_mac = (((np.array(cargo_cg)-aero_vals().mac_position)/aero_vals().mac_position))
    payload_cg_fb_mac = (((np.array(payload_cg_fb)-aero_vals().mac_position)/aero_vals().mac_position))
    payload_cg_bf_mac = (((np.array(payload_cg_bf)-aero_vals().mac_position)/aero_vals().mac_position))
    fuel_cg_mac = (((np.array(fuel_cg)-aero_vals().mac_position)/aero_vals().mac_position))
    margin_min_mac = (((np.array(margin_min)-aero_vals().mac_position)/aero_vals().mac_position))
    margin_max_mac = (((np.array(margin_max)-aero_vals().mac_position)/aero_vals().mac_position))

    plt.plot(cargo_cg_mac, cargo_mass, '-x')
    plt.plot(payload_cg_fb_mac, payload_mass_fb,'-x')
    plt.plot(payload_cg_bf_mac, payload_mass_bf,'-x')
    plt.plot(fuel_cg_mac, fuel_mass,'-x')
    plt.plot([margin_min_mac, margin_min_mac], [function_total_EOW_mass(), max(fuel_mass)],'-yx')
    plt.plot([margin_max_mac, margin_max_mac], [function_total_EOW_mass(), max(fuel_mass)],'-yx')


    plt.grid()
    plt.xlabel("c.g./mac")
    plt.ylabel("Mass [kg]")
    plt.title("Loading Diagram")
    plt.gca().legend(('Cargo','Passenger (F-B)','Passenger (B-F)', "Fuel", '2% Safety Margin'), loc=6)
    plt.show()


print (loading_diagram())