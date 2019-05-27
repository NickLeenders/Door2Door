from math import *
from OEW_CG import *
import matplotlib.pyplot as plt
import numpy as np


x_payload = [2.46, 2.66]
w_payload = [80, 270]
x_fuel = 0.5
w_fuel = 90
x_cargo = 4.8
w_cargo = 40
mac = 1.3

" *** Cargo *** "
cargo_cg = [function_OEW_CG()]
cargo_mass = [function_total_EOW_mass()]

cargo_cg.append((cargo_cg[0]*cargo_mass[0] + x_cargo*w_cargo)/(cargo_mass[0] + w_cargo))
cargo_mass.append(cargo_mass[0] + w_cargo)

" *** Payload *** "

payload_cg_fb = [cargo_cg[-1]]
payload_cg_bf = [cargo_cg[-1]]

payload_mass_fb = [cargo_mass[-1]]
payload_mass_bf = [cargo_mass[-1]]

cg_mass_update = 0
mass_update = 0
for i in range(len(x_payload)):
    payload_mass_fb.append(cargo_mass[-1] + mass_update + w_payload[i])
    payload_cg_fb.append((cargo_cg[-1]*cargo_mass[-1] + cg_mass_update + x_payload[i]*w_payload[i])/(cargo_mass[-1] + mass_update + w_payload[i]))
    cg_mass_update = cg_mass_update + x_payload[i]*w_payload[i]
    mass_update = mass_update + w_payload[i]

x_payload.reverse()
w_payload.reverse()

cg_mass_update = 0
mass_update = 0
for i in range(len(x_payload)):
    payload_mass_bf.append(cargo_mass[-1] + mass_update + w_payload[i])
    payload_cg_bf.append((cargo_cg[-1]*cargo_mass[-1] + cg_mass_update + x_payload[i]*w_payload[i])/(cargo_mass[-1] + mass_update + w_payload[i]))
    cg_mass_update = cg_mass_update + x_payload[i]*w_payload[i]
    mass_update = mass_update + w_payload[i]

" *** Fuel ***"
fuel_cg = [payload_cg_fb[-1]]
fuel_mass = [payload_mass_fb[-1]]

fuel_cg.append((fuel_cg[0]*fuel_mass[0] + x_fuel*w_fuel)/(fuel_mass[0] + w_fuel))
fuel_mass.append(fuel_mass[0] + w_fuel)

margin_min = min(cargo_cg + payload_cg_fb + fuel_cg)*0.98
margin_max = max(cargo_cg + payload_cg_bf + fuel_cg)*1.02

#convert values with respect to MAC
cargo_cg_mac = (((np.array(cargo_cg)-mac)/mac)*100)
payload_cg_fb_mac = (((np.array(payload_cg_fb)-mac)/mac)*100)
payload_cg_bf_mac = (((np.array(payload_cg_bf)-mac)/mac)*100)
fuel_cg_mac = (((np.array(fuel_cg)-mac)/mac)*100)
margin_min_mac = (((np.array(margin_min)-mac)/mac)*100)
margin_max_mac = (((np.array(margin_max)-mac)/mac)*100)

# plt.plot(cargo_cg, cargo_mass, '-x')
# plt.plot(payload_cg_fb, payload_mass_fb,'-x')
# plt.plot(payload_cg_bf, payload_mass_bf,'-x')
# plt.plot(fuel_cg, fuel_mass,'-x')
# plt.plot([margin_min, margin_min], [1100, max(fuel_mass)],'-x')
# plt.plot([margin_max, margin_max], [1100, max(fuel_mass)],'-x')

plt.plot(cargo_cg_mac, cargo_mass, '-x')
plt.plot(payload_cg_fb_mac, payload_mass_fb,'-x')
plt.plot(payload_cg_bf_mac, payload_mass_bf,'-x')
plt.plot(fuel_cg_mac, fuel_mass,'-x')
plt.plot([margin_min_mac, margin_min_mac], [1100, max(fuel_mass)],'-x')
plt.plot([margin_max_mac, margin_max_mac], [1100, max(fuel_mass)],'-x')


plt.grid()
plt.xlabel("Center of Gravity (C.G.)")
plt.ylabel("Mass [kg]")
plt.title("Loading Diagram Eagle")
plt.gca().legend(('Cargo','Passenger (F-B)','Passenger (B-F)', "Fuel", '2% Safety Margin', '2% Safety Margin'))
plt.show()


