from adcdata import *
import math


def linkBudget(diameter, slantRange):
    # declare constants
    pt = 10 # Satellite Transmitter Power (in Decibel Watts, dBw)
    gt = 9 # Satellite Antenna Gain (in Decibel Isotopic, dBi)
    loss = 19.43 # Losses (in Decibels, db) 
    nr = 0.55 # Ground Station Antenna efficiency 
    sol = 0.136363636 # Speed of Light/Carrier Frequency (in meters, m)
    kb = -228.6 # Boltzmann Constant (in Decibel Watts per degree Kelvin per Hertz, dBW/K/Hz
    ts = 22 # System Noise Temperature (in degrees Kelvin, K)
    
    # mathy time
    firstSimple = (nr*(((math.pi * diameter) / sol) ** 2)) # simplify the first bunch of parenthisis
    secondSimple = ((4000*math.pi)*slantRange) / sol # simplify second bunch of parenthisis
    final = (10**((pt+gt-loss+10*math.log(firstSimple,10)-20*math.log(secondSimple,10)-kb-10*math.log(ts,10))/10))/1000 # plug in simplified portion into total formula
    return final

print(linkBudget(34,400000))