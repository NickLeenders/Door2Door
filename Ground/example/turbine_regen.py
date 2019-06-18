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
    while i < 72:
        wind_speed.append(i)
        i+=1
        
    return wind_speed


def power_high(wind_speed):
    power = []
    rho = 1.225
    area = (0.576/2)**2 * math.pi
    eff = 0.25 #Theoretical limit is 59.6% average wind turbine is 35-45%
    for i in wind_speed:
        power_speed = rho * area * i**3 * eff
        power.append(power_speed)
    return power

def power_cruise(wind_speed):
    power = []
    rho = 1.225
    area = (1.524/2)**2 * math.pi
    eff = 0.25 #Theoretical limit is 59.6% average wind turbine is 35-45%
    for i in wind_speed:
        power_speed = rho * area * i**3 * eff
        power.append(power_speed)
    return power




def get_weather_data(filename='landing5.csv', **kwargs):

    if 'datapath' not in kwargs:
        kwargs['datapath'] = os.path.join(os.path.split(
            os.path.dirname(__file__))[0], 'example')
    file = os.path.join(kwargs['datapath'], filename)
    # read csv file
    weather_df = pd.read_csv(
        file, index_col=0, header=[0, 1],
        date_parser=lambda idx: pd.to_datetime(idx, utc=True))
    # change type of index to datetime and set time zone
    weather_df.index = pd.to_datetime(weather_df.index).tz_convert(
        'Europe/Berlin')
    # change type of height from str to int by resetting columns
    l0 = [_[0] for _ in weather_df.columns]
    l1 = [int(_[1]) for _ in weather_df.columns]
    weather_df.columns = [l0, l1]
    return weather_df



def initialize_wind_turbines():
   

    # specification of own wind turbine (Note: power values and nominal power
    # have to be in Watt)
    high_lift_turbine = {
        'name': 'high lift prop',
        'nominal_power': 27.5793914705218,  # in W
        'hub_height': 5,  # in m
        'rotor_diameter': 0.576,  # in m
        'power_curve': pd.DataFrame(
            data={'value': power_high(wind()),  # in W
                  'wind_speed': wind()})  # in m/s
    }
    # initialize WindTurbine object
    high_lift_turbine = WindTurbine(**high_lift_turbine)


    cruise_turbine = {
        'name': 'high lift prop',
        'nominal_power': 4000,  # in W
        'hub_height': 5,  # in m
        'rotor_diameter': 1.524,  # in m
        'power_curve': pd.DataFrame(
            data={'value': power_cruise(wind()),  # in W
                  'wind_speed': wind()})  # in m/s
    }
    # initialize WindTurbine object
    cruise_turbine = WindTurbine(**cruise_turbine)    


    return high_lift_turbine, cruise_turbine


def calculate_power_output(weather, high_lift_turbine, cruise_turbine):
    
    mc_my_turbine = ModelChain(high_lift_turbine).run_model(weather)

    high_lift_turbine.power_output = mc_my_turbine.power_output
    
    mc_my_turbine = ModelChain(cruise_turbine).run_model(weather)
    cruise_turbine.power_output = mc_my_turbine.power_output

    
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


def plot(high_lift_turbine, cruise_turbine):


    # plot or print turbine power output
    if plt:
        high_lift_turbine.power_output.plot(legend=True, label='High Lift Prop')
        cruise_turbine.power_output.plot(legend=True, label='Cruise Prop')

        plt.show()
    else:
        print(high_lift_turbine.power_output)
        print(cruise_turbine.power_output)
    total_power =  sum(cruise_turbine.power_output)
    total_energy = (total_power/3600)/1000
    print(total_energy)


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



def run_landing():
    weather = get_weather_data('landing5.csv')
    high_lift_turbine, cruise_turbine = initialize_wind_turbines()
    calculate_power_output(weather, high_lift_turbine, cruise_turbine)
    plot(high_lift_turbine, cruise_turbine)
    

if __name__ == "__main__":
    run_landing()