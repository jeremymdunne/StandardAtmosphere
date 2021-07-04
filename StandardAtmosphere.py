"""
Standard Atmosphere

Collection of functions intended to simplify the process of determining the
pressure, temperature, density, etc. of Earth's atmosphere at a given altitude

Author: Jeremy Dunne
Date: 6/19/2021

Data Source: https://www.engineeringtoolbox.com/standard-atmosphere-d_604.html
"""
import warnings
import math
# exceptions
class DefaultStandardAtmosphereWarning(Warning):
    def __init__(self, expression=None):
        self.text = "Standard Atmosphere Warning: "

class AltitudeOutOfBoundsWarning(DefaultStandardAtmosphereWarning):
    def __init__(self, expression):
        super().__init__()
        self.text += " altitude out of bounds, proceeding wit"

# Look-up table from engineeringtoolbox
standard_atmosphere_lookup = {
    'altitude': [-1000, 0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000,
        9000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 60000, 70000,
        80000], # meters
    'temperature': [21.5, 15, 8.5, 2, -4.49, -10.98, -17.47, -23.96, -30.45,
        -36.94, -43.42, -49.9, -56.5, -56.5, -51.6, -46.64, -22.8, -2.5, -26.13,
        -53.57, -74.51], # °C
    'pressure': [11.39, 10.13, 8.988, 7.95, 7.012, 6.166, 5.405, 4.722, 4.111,
        3.565, 3.08, 2.65, 1.211, 0.5529, 0.2549, 0.1197, 0.0287, 0.007978,
        0.002196, 0.00052, 0.00011], # 10^4 N/m^2
    'density': [1.347, 1.225, 1.112, 1.007, 0.9093, 0.8194, 0.7364, 0.6601,
        0.59, 0.5258, 0.4671, 0.4135, 0.1948, 0.08891, 0.04008, 0.01841,
        0.003996, 0.001027, 0.0003097, 0.00008283, 0.00001846], # kg/m^3
    'dynamic_viscosity': [1.821, 1.789, 1.758, 1.726, 1.694, 1.661, 1.628,
        1.595, 1.561, 1.527, 1.493, 1.458, 1.422, 1.422, 1.448, 1.475, 1.601,
        1.704, 1.584, 1.438, 1.321] # 10^-5 N s/m^2
}


##
# get_index
# get the first index in a data set which is larger than the value
#
# @param value value to search for
# @param sorted (smallest to largets) data set
# @return index of the next largest index. None if out of index
def get_index(value, data):
    if(value > data[-1]):
        return None
    if(value < data[0]):
        return 0
    i = 1
    while(data[i] < value):
        i += 1
    return i

##
# linear_interpolate
# linearly interpolate data
#
# @param target_x target x value to interpolate from
# @param x_data array of x data
# @param y_data array of y data
# @return linearly interpolated y value at the target_x
def linear_interpolate(target_x, x_data, y_data):
    # find the target index
    index = get_index(target_x, x_data)
    if(index is None):
        index = len(x_data) - 1
    if(index == 0):
        index = 1
    x_n1 = x_data[index]
    x_n = x_data[index - 1]
    y_n1 = y_data[index]
    y_n = y_data[index - 1]
    # linear estimation
    slope = (y_n1 - y_n)/(x_n1-x_n)
    value = y_n + slope * (target_x - x_n)
    return value

##
# get_pressure
# get the pressure at the given altitude
#
# @param altitude altitude to get the pressure at, in meters
# @return pressure at the altitude, in pascals
def get_pressure(altitude):
    # check the bounds
    if(altitude < standard_atmosphere_lookup['altitude'][0] or altitude > standard_atmosphere_lookup['altitude'][-1]):
        # print an error
        print("StandardAtmosphere get_pressure() altitude out of bounds, proceeding with best available data")
    pressure = linear_interpolate(altitude, standard_atmosphere_lookup['altitude'], standard_atmosphere_lookup['pressure'])
    if(pressure < 0):
        pressure = 0
    # convert to pa
    pressure = pressure * math.pow(10,4)
    return pressure

##
# get_temperature
# get the temperature at the given altitude
#
# @param altitude altitude to get the temperature at, in meters
# @return temperature at the altitude, in °C
def get_temperature(altitude):
    # check bounds
    if(altitude < standard_atmosphere_lookup['altitude'][0] or altitude > standard_atmosphere_lookup['altitude'][-1]):
        # print an error
        print("StandardAtmosphere get_temperature() altitude out of bounds, proceeding with best available data")
    temperature = linear_interpolate(altitude, standard_atmosphere_lookup['altitude'], standard_atmosphere_lookup['temperature'])
    # no real bounds
    return temperature

##
# get_density
# get the density at the given altitude
#
# @param altitude altitude to get the density at, in meters
# @return density at the altitude, in kg/m^3
def get_density(altitude):
    # check bounds
    if(altitude < standard_atmosphere_lookup['altitude'][0] or altitude > standard_atmosphere_lookup['altitude'][-1]):
        # print an error
        print("StandardAtmosphere get_density() altitude out of bounds, proceeding with best available data")
    density = linear_interpolate(altitude, standard_atmosphere_lookup['altitude'], standard_atmosphere_lookup['density'])
    # lower bound
    if(density < 0):
        density = 0
    return density

##
# get_dynamic_viscocity
# get the dynamic viscocity at the given altitude
#
# @param altitude altitude to get the dynamic viscocity at, in meters
# @return dynamic viscocity at the altitude, in N s/m^2
def get_dynamic_viscocity(altitude):
    # check bounds
    if(altitude < standard_atmosphere_lookup['altitude'][0] or altitude > standard_atmosphere_lookup['altitude'][-1]):
        # print an error
        print("StandardAtmosphere get_dynamic_viscocity() altitude out of bounds, proceeding with best available data")
    viscocity = linear_interpolate(altitude, standard_atmosphere_lookup['altitude'], standard_atmosphere_lookup['dynamic_viscosity'])
    # lower bound
    if(viscocity < 0):
        viscocity = 0
    # adjust
    viscocity = viscocity * math.pow(10,-5)
    return viscocity

##
# get_standard_atmosphere
# get standard atmosphere data at a given altitude
#
# @param altitude altitude to get data at, in meters
# @return dict with standard atmosphere data
def get_standard_atmosphere(altitude):
    dict = {}
    dict['pressure'] = get_pressure(altitude)
    dict['temperature'] = get_temperature(altitude)
    dict['dynamic_viscosity'] = get_dynamic_viscocity(altitude)
    dict['density'] = get_density(altitude)
    dict['altitude'] = altitude
    return dict

if __name__ == '__main__':
    print(get_standard_atmosphere(1259))
