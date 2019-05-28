# Aerodynamic people, make a program that edits the values in this class
class aero_vals():
    def __init__(self):
        self.vh_over_v = 1  # TODO (v_h/v) factor
        self.cl_h = -0.5  # TODO lift coefficient from horizontal tail
        self.cl_alpha_h = 3.82 # TODO lift rate coefficient of horizontal tail
        self.cl_a_minus_h = 1.5  # TODO cl from aircraft less horizontal tail
        self.cl_alpha_a_minus_h = 4.9 # TODO lift rate coefficient of aircraft less tail
        self.chord = 3.8  # TODO chord from the main wing
        self.cm_ac = -0.30 # TODO moment coefficient around aerodynamic center
        self.l_h = 2.6 # TODO distance wing ac to horizontal tail ac
        self.x_ac = 0.1 # TODO x distance of the ac
        self.mac = 2.2 # TODO mean aerodynamic chord
        self.downwash_factor = 0.3835 # TODO (de/da) d_epsilon over d_alpha
