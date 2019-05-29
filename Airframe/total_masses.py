from masses_cg_positions import w_components


def MTOW_calculate():
    MTOW = w_components().w_tail + w_components().w_structure + w_components().w_propeller + w_components().w_wing + w_components().w_drivetrain + w_components().w_fuel + w_components().w_cell + w_components().w_payload + w_components().w_passenger + w_components().w_battery + w_components().w_tank + w_components().w_cargo
    return MTOW


def OEW_calculate():
    OEW = w_components().w_tail + w_components().w_structure + w_components().w_propeller + w_components().w_wing + w_components().w_drivetrain + w_components().w_cell + w_components().w_passenger + w_components().w_battery + w_components().w_tank + w_components().w_cargo
    return OEW


class total_mass():
    def __init__(self):
        self.MTOW = MTOW_calculate()
        self.OEW = OEW_calculate()
