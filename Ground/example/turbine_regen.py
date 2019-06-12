
## Using windpowerlib ##

import os
import pandas as pd

try:
    from matplotlib import pyplot as plt
except ImportError:
    plt = None

from windpowerlib import ModelChain
from windpowerlib import WindTurbine

# You can use the logging package to get logging messages from the windpowerlib
# Change the logging level if you want more or less messages
import logging
logging.getLogger().setLevel(logging.DEBUG)

import math

def wind():
    wind_speed = []
    i=0
    while i < 31:
        wind_speed.append(i)
        i+=2
        
    return wind_speed
print(wind())

def power(wind_speed):
    power = []
    rho = 1.225
    area = (1.524/2)**2 * math.pi
    eff = 0.05 #Theoretical limit is 59.6% average wind turbine is 35-45%
    for i in wind_speed:
        power_speed = rho * area * i**3 * eff
        power.append(power_speed)
    return power
print(power(wind()))



def initialize_wind_turbines():
   

    # specification of own wind turbine (Note: power values and nominal power
    # have to be in Watt)
    high_lift_turbine = {
        'name': 'high lift prop',
        'nominal_power': 27.5793914705218,  # in W
        'hub_height': 5,  # in m
        'rotor_diameter': 0.576,  # in m
        'power_curve': pd.DataFrame(
            data={'value': [p * 1 for p in [
                      0.0, 0.12768236791908238, 1.021458943352659, 3.447423933815225, 8.171671546821273, 15.9602959898853, 27.5793914705218, 43.79505219624526, 65.37337237457018, 93.08044621301106, 127.6823679190824, 169.94523170029868, 220.6351317641744, 280.51816231822403, 350.36041756996207, 430.92799172690303]],  # in W
                  'wind_speed': [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]})  # in m/s
    }
    # initialize WindTurbine object
    high_lift_turbine = WindTurbine(**high_lift_turbine)


    cruise_turbine = {
        'name': 'high lift prop',
        'nominal_power': 193.0677,  # in W
        'hub_height': 5,  # in m
        'rotor_diameter': 1.524,  # in m
        'power_curve': pd.DataFrame(
            data={'value': [p * 1 for p in [
                      0.0, 0.8938319931279862, 7.15065594502389, 24.133463814455627, 57.20524756019112, 111.72899914099828, 193.06771051564502, 306.58437364289927, 457.64198048152895, 651.6035229903019, 893.8319931279863, 1189.6903828533495, 1544.5416841251601, 1963.7488889021859, 2452.674989143194, 3016.682976806954]],  # in W
                  'wind_speed': [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]})  # in m/s
    }
    # initialize WindTurbine object
    cruise_turbine = WindTurbine(**cruise_turbine)    


    return high_lift_turbine, cruise_turbine


def calculate_power_output(weather, high_lift_turbine, cruise_turbine):
    
    # power output calculation for my_turbine
    # initialize ModelChain with default parameters and use run_model method
    # to calculate power output
    mc_my_turbine = ModelChain(high_lift_turbine).run_model(weather)
    # write power output time series to WindTurbine object
    high_lift_turbine.power_output = mc_my_turbine.power_output
    
    mc_my_turbine = ModelChain(cruise_turbine).run_model(weather)
    # write power output time series to WindTurbine object
    cruise_turbine.power_output = mc_my_turbine.power_output

    # power output calculation for e126
    # own specifications for ModelChain setup
    modelchain_data = {
        'wind_speed_model': 'logarithmic',  # 'logarithmic' (default),
                                            # 'hellman' or
                                            # 'interpolation_extrapolation'
        'density_model': 'ideal_gas',  # 'barometric' (default), 'ideal_gas' or
                                       # 'interpolation_extrapolation'
        'temperature_model': 'linear_gradient',  # 'linear_gradient' (def.) or
                                                 # 'interpolation_extrapolation'
        'power_output_model': 'power_curve',  # 'power_curve' (default) or
                                              # 'power_coefficient_curve'
        'density_correction': True,  # False (default) or True
        'obstacle_height': 0,  # default: 0
        'hellman_exp': None}  # None (default) or None
    # initialize ModelChain with own specifications and use run_model method
    # to calculate power output


    return


def plot_or_print(high_lift_turbine, cruise_turbine):


    # plot or print turbine power output
    if plt:
        high_lift_turbine.power_output.plot(legend=True, label='High Lift Prop')
        cruise_turbine.power_output.plot(legend=True, label='Cruise Prop')

        plt.show()
    else:
        print(high_lift_turbine.power_output)
        print(cruise_turbine.power_output)


    # plot or print power curve
    if plt:
        if high_lift_turbine.power_curve is not None:
            high_lift_turbine.power_curve.plot(x='wind_speed', y='value', style='*',
                                  title='High Lift Turbine Power Curve')
            plt.show()
        if cruise_turbine.power_curve is not None:
            cruise_turbine.power_curve.plot(x='wind_speed', y='value', style='*',
                                        title='Cruise Turbine Power Curve')
            plt.show()



def run_example():

    weather = get_weather_data('weather.csv')
    high_lift_turbine, cruise_turbine = initialize_wind_turbines()
    calculate_power_output(weather, high_lift_turbine, cruise_turbine)
    plot_or_print(high_lift_turbine, cruise_turbine)
    

if __name__ == "__main__":
    run_example()
