# Python to output the scissor plot

import sys
import matplotlib.pyplot as plt

sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import aero_vals


def control_curve(x_cg):
    sh_over_s = (1 / ((aero_vals().cl_h / aero_vals().cl_a_minus_h) * (
            aero_vals().l_h / aero_vals().chord) * aero_vals().vh_over_v ** 2)) * x_cg - ((
                        aero_vals().cm_ac / aero_vals().chord - aero_vals().x_ac) / (
                        (aero_vals().cl_h / aero_vals().cl_a_minus_h) * (
                        aero_vals().l_h / aero_vals().chord) * aero_vals().vh_over_v ** 2))
    return sh_over_s


def stability_curve(x_cg):
    stability_margin = 0.05
    sh_over_s = 1 / ((aero_vals().cl_alpha_h / aero_vals().cl_alpha_a_minus_h) * (
            aero_vals().l_h / aero_vals().chord) * (
                             1 - aero_vals().downwash_factor) * aero_vals().vh_over_v ** 2) * x_cg - (
                        aero_vals().x_ac - stability_margin) / (
                        (aero_vals().cl_h / aero_vals().cl_a_minus_h) * (
                        aero_vals().l_h / aero_vals().chord) * (
                                1 - aero_vals().downwash_factor) * aero_vals().vh_over_v ** 2)
    return sh_over_s


def create_plot(x_cg):
    first_curve = stability_curve(x_cg)
    second_curve = control_curve(x_cg)
    plt.plot(x_cg, second_curve)
    plt.plot(x_cg, first_curve)
    plt.show()
    pass
