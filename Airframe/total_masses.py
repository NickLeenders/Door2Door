def MTOW_calculate(w_components):
    MTOW = w_components.w_tail + w_components.w_structure + w_components.w_propeller + w_components.w_wing + w_components.w_drivetrain + w_components.w_fuel + w_components.w_cell + 4.0 * w_components.w_passenger + w_components.w_battery + w_components.w_tank + w_components.w_cargo
    return MTOW


def OEW_calculate(w_components):
    OEW = w_components.w_tail + w_components.w_structure + w_components.w_propeller + w_components.w_wing + w_components.w_drivetrain + w_components.w_cell + w_components.w_passenger + w_components.w_battery + w_components.w_tank + w_components.w_cargo
    return OEW


class total_mass():
    def __init__(self, w_components):
        self.MTOW = MTOW_calculate(w_components)
        self.OEW = OEW_calculate(w_components)
