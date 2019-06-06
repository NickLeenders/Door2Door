# Python to output the scissor plot

import sys
import matplotlib.pyplot as plt

sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals, wing_vals
from Loading_Diagram import *
from OEW_CG import *


def control_curve(x_cg_mac):
    sh_over_s = (1 / ((aero_vals().cl_h / aero_vals().cl_a_minus_h) * (
            aero_vals().l_h / wing_vals().MAC) * aero_vals().vh_over_v ** 2)) * x_cg_mac + (
                        aero_vals().cm_ac / wing_vals().MAC - aero_vals().x_ac) / (
                        (
                                aero_vals().cl_h / aero_vals().cl_a_minus_h) * (
                                aero_vals().l_h / wing_vals().MAC) * aero_vals().vh_over_v ** 2)
    return sh_over_s


def stability_curve(x_cg_mac):
    stability_margin = 0.06
    sh_over_s = 1 / ((aero_vals().cl_alpha_h / aero_vals().cl_alpha_a_minus_h) * (
            aero_vals().l_h / wing_vals().MAC) * (
                             1 - aero_vals().downwash_factor) * aero_vals().vh_over_v ** 2) * x_cg_mac - (
                        aero_vals().x_ac - stability_margin) / (
                        (aero_vals().cl_h / aero_vals().cl_a_minus_h) * (
                        aero_vals().l_h / wing_vals().MAC) * (
                                1 - aero_vals().downwash_factor) * aero_vals().vh_over_v ** 2)
    return sh_over_s


def create_plot(x_cg):
    first_curve = stability_curve(x_cg)
    second_curve = control_curve(x_cg)
    plt.xlabel("c.g./mac")
    plt.ylabel(r'$S_h/S$')
    plt.title("Scissor Plot")
    plt.plot(x_cg, second_curve)
    plt.plot(x_cg, first_curve)
    plt.plot([loading_diagram()[0], loading_diagram()[0]], [0, 1.0],'-yx')
    plt.plot([loading_diagram()[1], loading_diagram()[1]], [0, 1.0],'-yx')
    plt.axis([0, 0.4, 0, 1.0])
    plt.grid()
    plt.show()
    pass



