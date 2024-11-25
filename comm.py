from adcdata import getAny
import math
mins = []
mass = []
wpsa = []
wpsar = []
ds54 = []
ds54r = []
ds24 = []
ds24r = []
ds34 = []
ds34r = []
artemisPath= open("assets/NASA_ADC_Data_Update.csv", "r")  
for line in artemisPath:
    #get rids of the commas
    entries = line.split(",")
    #append to each array
    mins.append(entries[0])
    mass.append(entries[7])
    wpsa.append(entries[8])
    wpsar.append(entries[9])
    ds54.append(entries[10])
    ds54r.append(entries[11])
    ds24.append(entries[12])
    ds24r.append(entries[13])
    ds34.append(entries[14])
    ds34r.append(entries[15])
artemisPath.close() 

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

    End goal is to display the antennas based on best connection; Green light for best connection, then yellow for second best, and red for shouldn't be used.

    Colors will be decided based on order returned from this. the first antenna returned is green, second is yellow, last two are red (im not sure if we should include inactive antennas, but they shouldn't be used anyways so red shld work)

    TODO: read from data file to get active antennas AND slant range
    """

    # antenna diameters
    d = 34 # diameter for every antenna except wpsa
    wpsaDiameter = 12 # diameter for wpsa antenna

    # antennas that are active
    # when reading from file, we will change the values based on if the antenna is currently available.
    # this will later be decided through reading the data file
    ds24Active = False
    ds34Active = False
    ds54Active = False
    wpsaActive = True

    budgets = { # dict of antennas as keys and link budget as value
        "ds24": linkBudget(d, slant) if ds24Active else 0, # python ternary operator basically a one line if statement using the link budget if it is active, otherwise setting it to 0
        "ds34": linkBudget(d, slant) if ds34Active else 0,
        "ds54": linkBudget(d, slant) if ds54Active else 0,
        "wpsa": linkBudget(wpsaDiameter, slant) if wpsaActive else 0
    }

    # print(budgets)

    highToLow = sorted(budgets.items(), key = lambda x: x[1], reverse=True) # sorts the antennas by link budget, highest to low.
                                                                            # when using slant range 400k and ds24, ds34, and wpsa are active, it will return
                                                                            # [('ds24', 740.7264920372704), ('ds34', 740.7264920372704), ('wpsa', 92.27042807384723), ('ds54', 0)]
                                                                            # until slant range is read from data, every link budget will be the same 
                                                                            # other than wpsa since they all have the same diameter
    return highToLow

# print(bestAntenna(getAny(wpsar,101)))
# print(bestAntenna(74284.61081))

for i in range(len(wpsa)):
    wpsaActive = False
    ds24Active = False
    ds34Active = False
    ds54Active = False
    # print(int(wpsa[i]) == 1)
    # print(int(ds24[i]) == 1)
    # print(int(ds34[i]) == 1)
    # print(int(ds54[i]) == 1)

    wpsaActive = True if int(wpsa[i]) == 1 else False
    ds24Active = True if int(ds24[i]) == 1 else False
    ds34Active = True if int(ds34[i]) == 1 else False
    ds54Active = True if int(ds54[i]) == 1 else False

    if wpsaActive == True:
        print(bestAntenna(getAny(wpsar, i)))
        # print(wpsar[i])
    if ds24Active == True:
        print(bestAntenna(getAny(ds24r, i)))
        # pass
    if ds34Active == True:
        print(bestAntenna(getAny(ds34r, i)))
        # pass
    if ds54Active == True:
        print(bestAntenna(getAny(ds54r, i)))
        # pass


    # print(wpsaActive, ds24Active, ds34Active, ds54Active)

    break

