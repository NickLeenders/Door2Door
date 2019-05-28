# Aerodynamic people, make a program that edits the values in this class
class aero_vals():
    def __init__(self):
        self.vh_over_v = 1  # TODO (v_h/v) factor
        self.cl_h = 2  # TODO lift coefficient from horizontal tail
        self.cl_alpha_h = 4.7 # TODO lift rate coefficient of horizontal tail
        self.cl_a_minus_h = 1.5  # TODO cl from aircraft less horizontal tail
        self.cl_alpha_a_minus_h = 6.66 # TODO lift rate coefficient of aircraft less tail
        self.chord = 1.2  # TODO chord from the main wing
        self.cm_ac = -0.30 # TODO moment coefficient around aerodynamic center
        self.l_h = 2.6 # TODO distance wing ac to horizontal tail ac
        self.x_ac = 2 # TODO x distance of the ac
        self.mac = 2.2 # TODO mean aerodynamic chord
        self.downwash_factor = 0.19 # TODO (de/da) d_epsilon over d_alpha
