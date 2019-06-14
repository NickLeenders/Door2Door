# Aerodynamic people, make a program that edits the values in this class

import sys
sys.path.insert(0, '../PowerElectrical/')
from isa import IsaCalculator

from math import *

class aero_vals():
    def __init__(self):
        self.vh_over_v = 0.8  # TODO (v_h/v) factor
        self.cl_h = -0.8 # TODO lift coefficient from horizontal tail
        self.cl_alpha_h = 4.3 # TODO lift rate coefficient of horizontal tail
        self.cl_a_minus_h = 1.5  # TODO cl from aircraft less horizontal tail
        self.cl_alpha_a_minus_h = 6.3 # TODO lift rate coefficient of aircraft less tail
        self.cm_ac = -0.08# TODO moment coefficient around aerodynamic center
        self.cd0 =0.04794141815595157 # TODO drag coefficient at zero lift
        self.l_h = 2.4 # TODO distance wing ac to horizontal tail ac
        self.x_ac = 0.25 # TODO x distance of the ac
        self.mac_position = 2.241 # TODO Longitudinal position of the MAC
        self.downwash_factor = 0.395 # TODO (de/da) d_epsilon over d_alpha
        self.n_ult = 4.5 # TODO Ultimate load factor
        self.h= 1219.2 # altitude in meters
        self.b = 8.8

        self.mu = 1.8*10**-5  #
        self.rho0=1.225 #
        self.T0 = 288.15 #K
        self.rho_cr, self.T_cr, self.p_cr = IsaCalculator(self.h)
        self.vinfcr=250/3.6 # m/s
        self.gamma = 1.4  #-
        self.R = 287  # -
        self.Rey= 4229292
        self.Mach=0.24


        #self.rho= findrho(altitude)
        self.vinfcr = 250/3.6 # m/s
        self.vinf_takeoff = 39  # m/s
        self.vstall = self.vinf_takeoff/1.2 # m/s
        self.cl_cr=0.75 #TODO this should be initialised with a function,
        self.cl_takeoff=1.5            # so that the aero_vals object will have the correct Cl for the airspeed
        self.cl_climb=1.2
        self.cl_descent = 0.5
        self.roll_rate = 60*pi/180 # TODO Roll Rate Class I

        self.frontal_area = 2.4*1.7

class wing_vals():
    def __init__(self):
        self.S = 9.5288 #Surface Area
        self.b = 8.8 #Wing Span
        self.A = (self.b)**2/self.S #Aspect Ratio
        self.e = 0.8
        self.sweep_ang = -2.5 #Sweep Angle
        self.root_chord = 1.15 #Root Chord
        self.tip_chord = 1.01 #Tip Chord
        self.MAC= 1.08 #MAC chord
        self.tc= 0.18 #thickness chord ratio
        self.taper_ratio = self.tip_chord/self.root_chord # Taper Ratio
        self.MAC = self.root_chord - (2*(self.root_chord-self.tip_chord)*(0.5*self.root_chord+self.tip_chord)/(3*(self.root_chord+self.tip_chord))) #MAC length
        if self.taper_ratio == 1:
            self.y_MAC = self.b/4
        else:
            self.y_MAC = (self.root_chord - self.MAC)/(self.root_chord - self.tip_chord) * self.b/2 #Y position of the MAC
        self.ca_c = 0.2  # TODO chord aileron over chord wing (control/stability Aileron Sizing Tommy)
        self.aileron_effectiveness = 0.41  # TODO aileron effectiveness (control/stability Aileron Sizing Tommy)
        self.aileron_inner_perc = 0.74  # TODO Inner board Aileron Sizing (control/stability Aileron Sizing Tommy)
        self.aileron_outer_perc = 0.9  # TODO Outer board Aileron Sizing (control/stability Aileron Sizing Tommy)
        self.aileron_inner_pos = self.aileron_inner_perc * (self.b / 2)  # TODO Inner Board position Aileron
        self.aileron_outer_pos = self.aileron_outer_perc * (self.b / 2)  # TODO Outer Board position Aileron
        self.aileron_max_defl = 20 * pi / 180  # TODO Maxium Aileron Deflection

class emp_vals():
    def __init__(self):
        self.S_h = 1.4674 #Horizontal tail surface area
        self.b_h = 2.4 #Horizontal tail wing span
        self.c_h= 0.6113 #Horizontal tail wing chord Cr+Ct/2
        self.taper_h = 0.64 #Taper ratio horizontal tail
        self.A_h = (self.b_h)**2/self.S_h #Horizontal tail aspect ratio
        self.trh = 0.15 #Maximum Thickness of horizontal tail
        self.tch=0.10 # Thickness chord ratio horizontal tail
        self.num_htail = 1 #Number of horizontal tails
        
        self.S_v = 1.29 #Vertial tail surface area
        self.b_v = 1.2999 #Span of vertical tail surface
        self.c_v = 0.9946 #Chord of vertical tail surface Cr+Ct/2
        self.A_v = (self.b_v)**2/self.S_v #Vertical tail aspect ratio
        self.tcv= 0.10 # Thickness chord ratio vertical tail
        self.trv = 0.16 #Max thickness of vertical tail
        self.sweep_v = 0 #Sweep at 0.25c of vertical tail
        self.num_vtail = 1

