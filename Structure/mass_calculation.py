import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.insert(0, '../Airframe/')
import masses_cg_positions
from total_masses import total_mass

sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import wing_vals, emp_vals, aero_vals

sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import wing_vals, emp_vals, aero_vals

MTOW = 1634


def roskam_convert(val, ty, to_roskam=True):
    '''Convert units to Roskam (from roskam if to_roskam=False). ty=1 for weight, 2 for distance , 3 for area , 4 for speed, 5 for angle. '''
    if ty == 1:
        if to_roskam:
            fin = val * 2.20462
        else:
            fin = val / 2.20462
    if ty == 2:
        if to_roskam:
            fin = val * 3.280084
        else:
            fin = val / 3.280084
    if ty == 3:
        if to_roskam:
            fin = val * 10.7639
        else:
            fin = val / 10.7639
    if ty == 4:
        if to_roskam:
            fin = val * 0.539957
        else:
            fin = val / 0.539957
    if ty == 5:
        if to_roskam:
            fin = val * 180 / np.pi
        else:
            fin = val * np.pi / 180

    return fin


def wing_weight(MTOW):
    W_tot = roskam_convert(MTOW, 1)

    S = roskam_convert(wing_vals().S, 3)
    n_ult = aero_vals().n_ult
    A = wing_vals().A
    W_w = (0.04674 * W_tot ** (0.397)) * (S ** 0.360) * (n_ult ** 0.397) * (A ** 1.712)
    W_w = roskam_convert(W_w, 1, to_roskam=False)
    return W_w


def emp_weight():
    W_tot = roskam_convert(total_mass().MTOW, 1)
    S_h = roskam_convert(emp_vals().S_h, 3)
    A_h = emp_vals().A_h
    trh = roskam_convert(emp_vals().trh, 2)
    S_v = roskam_convert(emp_vals().S_v, 3)
    A_v = emp_vals().A_v
    trv = roskam_convert(emp_vals().trv, 2)


if __name__ == "__main__":
    MTOW = [5, 1630]
    i = 1
    epsilon = 0.5
    while (MTOW[i] - MTOW[i - 1]) > epsilon:
        Wing_weight = wing_weight(MTOW[i])
        W_components = masses_cg_positions.w_components(Wing_weight)
        MTOW.append(total_mass(W_components).MTOW)
        i = i + 1

    print("MTOW = ", MTOW)
    print("Wing weight = ", wing_weight)
    iterations = np.arange(len(MTOW))
    plt.figure()
    plt.plot(iterations[1:], MTOW[1:], label='MTOW Iteration')
    plt.xticks([1, 2, 3, 4])
    plt.xlabel('Iteration')
    plt.ylabel('Mass [kg]')
    plt.show()