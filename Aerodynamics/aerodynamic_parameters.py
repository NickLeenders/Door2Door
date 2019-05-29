# Aerodynamic people, make a program that edits the values in this class

import sys
pi=3.1415
sys.path.insert(0, '../PowerElectrical/')
from isa import IsaCalculator

from math import *


class aero_vals():
    def __init__(self):
        self.vh_over_v = 1  # TODO (v_h/v) factor
        self.cl_h = -0.5  # TODO lift coefficient from horizontal tail
        self.cl_a = 4.5 # TODO airfoil lift curve slope
        self.cl_alpha_h = 3.82 # TODO lift rate coefficient of horizontal tail
        self.cl_a_minus_h = 1.5  # TODO cl from aircraft less horizontal tail
        self.cl_alpha_a_minus_h = 4.9 # TODO lift rate coefficient of aircraft less tail
        self.chord = 1.2  # TODO chord from the main wing
        self.cm_ac = -0.30 # TODO moment coefficient around aerodynamic center
        self.cd0 = 0.05 # TODO drag coefficient at zero lift
        self.l_h = 2.6 # TODO distance wing ac to horizontal tail ac
        self.x_ac = 0.1 # TODO x distance of the ac
        self.mac_position = 2.2 # TODO Longitudinal position of the MAC
        self.downwash_factor = 0.3835 # TODO (de/da) d_epsilon over d_alpha
        self.n_ult = 4.5 # TODO Ultimate load factor
        self.h= 1219.2 # altitude in meters
        self.rho0=1.225 # kg/m^3
        self.T0=288.15 # K

        self.rho, self.T, self.p = IsaCalculator(self.h)
        self.vinfcr=250/3.6 # m/s
        self.vstall = 20.0 # m/s
        self.vinf_takeoff = 25.2  # m/s

        #self.rho= findrho(altitude)
        self.vinfcr = 240/3.6 # m/s
        self.vstall = 20.0 # m/s
        self.vinf_takeoff = 1.2 * self.vstall  # m/s

        self.lapse = 0.0065  # degree/m
        self.g = 9.80665  # m/s^2
        self.R = 287  # J/kg
        self.gamma = 1.4  # -
        self.mu = 1.8 * 10 ** -5  # kg/ms(at 15 celsius but alsmost doesn't change)
        self.cl=1.5
        self.b = 8.8  # Wing Span
        self.roll_rate = 60*pi/180 # TODO Roll Rate Class 
        self.ca_c = 0.2  # TODO chord aileron over chord wing (control/stability Aileron Sizing Tommy)
        self.aileron_effectiveness = 0.41 # TODO aileron effectiveness (control/stability Aileron Sizing Tommy)
        self.ar_wing = 7.33 # TODO aspect ratio main wing
        self.aileron_inner_perc = 0.7 # TODO Inner board Aileron Sizing (control/stability Aileron Sizing Tommy)
        self.aileron_outer_perc = 0.9 # TODO Outer board Aileron Sizing (control/stability Aileron Sizing Tommy)
        self.aileron_inner_pos = self.aileron_inner_perc*(self.b/2) # TODO Inner Board position Aileron
        self.aileron_outer_pos = self.aileron_outer_perc*(self.b/2) # TODO Outer Board position Aileron
        self.aileron_max_defl = 25*pi/180 # TODO Maxium Aileron Deflection

class wing_vals():
    def __init__(self):
        self.S = 10.56 #Surface Area
        self.b = 8.8 #Wing Span
        self.A = (self.b)**2/self.S #Aspect Ratio
        self.sweep_ang = 0 #Sweep Angle
        self.taper_ratio = 1 #Taper Ratio
        self.root_chord = 1.2 #Root Chord
        self.tip_chord = self.root_chord * self.taper_ratio #Tip Chord
        self.MAC = self.root_chord - (2*(self.root_chord-self.tip_chord)*(0.5*self.root_chord+self.tip_chord)/(3*(self.root_chord+self.tip_chord))) #MAC length
        if self.taper_ratio == 1:
            self.y_MAC = self.b/4
        else:
            self.y_MAC = (self.root_chord - self.MAC)/(self.root_chord - self.tip_chord) * self.b/2 #Y position of the MAC
        
class emp_vals():
    def __init__(self):
        self.S_h = 2.88 #Horizontal tail surface area
        self.b_h = 2.4 #Horizontal tail wing span
        self.A_h = (self.b_h)**2/self.S_h #Horizontal tail aspect ratio
        self.trh = 0.15 #Maximum Thickness of horizontal tail
        self.num_htail = 1 #Number of horizontal tails
        
        self.S_v = 1.2 #Vertial tail surface area
        self.b_v = 1 #Span of vertical tail surface
        self.A_v = (self.b_v)**2/self.S_v #Vertical tail aspect ratio
        self.trv = 0.16 #Max thickness of vertical tail
        self.sweep_v = 0 #Sweep at 0.25c of vertical tail
        self.num_vtail = 1
