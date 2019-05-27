# Aerodynamic people, make a program that edits the values in this class
class aero_vals():
    def __init__(self):
        self.vh_over_v = 1  # (v_h/v) factor
        self.cl_h = 2  # lift coefficient from horizontal tail
        self.cl_alpha_h = 2.1 # lift rate coefficient of horizontal tail
        self.cl_a_minus_h = 1.5  # cl from aircraft less horizontal tail
        self.cl_alpha_a_minus_h = 1.6 # lift rate coefficient of aircraft less tail
        self.chord = 1.2  # chord from the main wing
        self.cm_ac = 1 # moment coefficient around aerodynamic center
        self.l_h = 2.6 # distance wing ac to horizontal tail ac
        self.x_ac = 2 # x distance of the ac
        self.mac = 1.3 # mean aerodynamic chord
        self.downwash_factor = 0.15 # (de/da) d_epsilon over d_alpha
