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


def bestAntenna(slant): # slant will be determined through data file, for now it is just a parameter to make this simpler
    """
    Returns the best antenna for the current position using the link budget.
    Higher link budget = better connection = better antenna
    TODO: read from data file to get active antennas AND slant range
    """

    # antenna diameters
    d = 34 # diameter for every antenna except wpsa
    wpsaDiameter = 12 # diameter for wpsa antenna

    # antennas that are active
    # this will later be decided through reading the data file
    dss24Active = False
    dss34Active = False
    dss54Active = False
    wpsaActive = False

    budgets = { # dict of antennas as keys and link budget as value
        "dss24": linkBudget(d, slant) if dss24Active else 0, # python ternary operator basically a one line if statement using the link budget if it is active, otherwise setting it to 0
        "dss34": linkBudget(d, slant) if dss34Active else 0,
        "dss54": linkBudget(d, slant) if dss54Active else 0,
        "wpsa": linkBudget(wpsaActive, slant) if wpsaActive else 0
    }

    print(budgets)

    best = max(budgets, key=budgets.get)
    bestBudget = budgets[best]

    return [best, bestBudget] # returns a list that has antenna name for the best current antenna and the link budget for that antenna 
                              # example: ['dss24', 740.7264920372704]

  
    


print(bestAntenna(400000))