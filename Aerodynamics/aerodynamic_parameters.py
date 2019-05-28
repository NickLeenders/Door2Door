# Aerodynamic people, make a program that edits the values in this class
from math import *

class aero_vals():
    def __init__(self):
        self.vh_over_v = 1  # TODO (v_h/v) factor
        self.cl_a = 4.5 # TODO airfoil lift curve slope
        self.cl_h = 2  # TODO lift coefficient from horizontal tail
        self.cl_alpha_h = 4.7 # TODO lift rate coefficient of horizontal tail
        self.cl_a_minus_h = 1.5  # TODO cl from aircraft less horizontal tail
        self.cl_alpha_a_minus_h = 6.66 # TODO lift rate coefficient of aircraft less tail
        self.chord = 1.2  # TODO chord from the main wing
        self.cm_ac = -0.30 # TODO moment coefficient around aerodynamic center
        self.cd_zero = 0.05 # TODO CD0
        self.l_h = 2.6 # TODO distance wing ac to horizontal tail ac
        self.x_ac = 2 # TODO x distance of the ac
        self.mac = 2.2 # TODO mean aerodynamic chord
        self.downwash_factor = 0.19 # TODO (de/da) d_epsilon over d_alpha
        self.surface_area = 10.56 # TODO Wing Surface Area
        self.wingspan = 8.8 # TODO Wing Span
        self.roll_rate = 60*pi/180 # TODO Roll Rate Class I
        self.taper_ratio = 0.9 # TODO taper ratio
        self.ca_c = 0.2  # TODO chord aileron over chord wing (control/stability Aileron Sizing Tommy)
        self.aileron_effectiveness = 0.41 # TODO aileron effectiveness (control/stability Aileron Sizing Tommy)
        self.ar_wing = 7.33 # TODO aspect ratio main wing
        self.aileron_inner_perc = 0.7 # TODO Inner board Aileron Sizing (control/stability Aileron Sizing Tommy)
        self.aileron_outer_perc = 0.9 # TODO Outer board Aileron Sizing (control/stability Aileron Sizing Tommy)
        self.aileron_inner_pos = self.aileron_inner_perc*(self.wingspan/2) # TODO Inner Board position Aileron
        self.aileron_outer_pos = self.aileron_outer_perc*(self.wingspan/2) # TODO Outer Board position Aileron
        self.aileron_max_defl = 25*pi/180 # TODO Maxium Aileron Deflection
        self.cruise_speed = 240/3.6 # TODO Cruise Speed