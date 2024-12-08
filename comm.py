from adcdata import getAny
import math

def linkBudget(diameter, slantRange):
    # declare constants
    pt = 10 # Satellite Transmitter Power (in Decibel Watts, dBw)
    gt = 9 # Satellite Antenna Gain (in Decibel Isotopic, dBi)
    loss = 19.43 # Losses (in Decibels, db) 
    nr = 0.55 # Ground Station Antenna efficiency 
    sol = 0.136363636 # Speed of Light/Carrier Frequency (in meters, m)
    kb = -228.6 # Boltzmann Constant (in Decibel Watts per degree Kelvin per Hertz, dBW/K/Hz
    ts = 222 # System Noise Temperature (in degrees Kelvin, K)
    
    # mathy time
    firstSimple = (nr*(((math.pi * diameter) / sol) ** 2)) # simplify the first bunch of parenthisis
    secondSimple = ((4000*math.pi)*slantRange) / sol # simplify second bunch of parenthisis
    final = (10**((pt+gt-loss+10*math.log(firstSimple,10)-20*math.log(secondSimple,10)-kb-10*math.log(ts,10))/10))/1000 # plug in simplified portion into total formula
    return final

# def sorting(budgets):
#     print(str(budgets))
#     global prevBest
#     sortedList = []
#     items = list(budgets)
#     if(items[prevBest][1]>=10000):
#         sortedList.append(items[prevBest][1])
#         budgets.remove(prevBest)
#         other = []
#         other = items.sort(key=lambda x: x[1])
#         #other = sorted(budgets.items(), key = lambda x: x[1], reverse=True)
#         sortedList.append(other)
#     else:
#         sortedList = items.sort(key=lambda tup: tup[1])
#         #sortedList = sorted(budgets.items(), key = lambda x: x[1], reverse=True)
#     prevBest = sortedList[0][0]
#     return sortedList

def bestAntenna(actives, slants): # slant will be determined through data file
    """
    Returns the best antenna for the current position using the link budget.
    Higher link budget = better connection = better antenna

    End goal is to display the antennas based on best connection; Green light for best connection, then yellow for second best, and red for shouldn't be used.

    Colors will be decided based on order returned from this. the first antenna returned is green, second is yellow, last two are red (im not sure if we should include inactive antennas, but they shouldn't be used anyways so red shld work)

    TODO: make this a prioritized list 🙄
    things over 10k are thought as same as 10k
    eg:
    sattelites a,b,c , max 10
    a: 5
    b: 6
    c: 10

    c,b,a

    changes to:
    a: 15
    b: 6
    c: 10

    since a is over 10 and c is 10 + alr active, don't change active sattelite
    c,a,b
    """

    # antenna diameters
    d = 34 # diameter for every antenna except wpsa
    wpsaDiameter = 12 # diameter for wpsa antenna

    # antennas that are active
    # when reading from file, we will change the values based on if the antenna is currently available.
    # this will later be decided through reading the data file
    wpsaActive = actives[0]
    ds24Active = actives[1]
    ds34Active = actives[2]
    ds54Active = actives[3]

    budgets = { # dict of antennas as keys and link budget as value
        "wpsa": linkBudget(wpsaDiameter, slants[0]) if wpsaActive else 0, # python ternary operator basically a one line if statement using the link budget if it is active, otherwise setting it to 0
        "ds24": linkBudget(d, slants[1]) if ds24Active else 0, 
        "ds34": linkBudget(d, slants[2]) if ds34Active else 0,
        "ds54": linkBudget(d, slants[3]) if ds54Active else 0
    }

    # print(budgets)

    highToLow = sorted(budgets.items(), key = lambda x: x[1], reverse=True) # sorts the antennas by link budget, highest to low.
                                                                            # when using slant range 400k and ds24, ds34, and wpsa are active, it will return
                                                                            # [('ds24', 740.7264920372704), ('ds34', 740.7264920372704), ('wpsa', 92.27042807384723), ('ds54', 0)]
                                                                            # until slant range is read from data, every link budget will be the same 
                                                                            # other than wpsa since they all have the same diameter
    # highToLow = sorting(budgets.items())
    return highToLow

# print(bestAntenna(getAny(wpsar,101)))
# print(bestAntenna(74284.61081))

def main():
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
    gyrs = []

    for i in range(len(wpsa)):
    # for i in range():
        # initialize all actives to false at beginning of each iteration
        wpsaActive = False
        ds24Active = False
        ds34Active = False
        ds54Active = False

        # check data and fix activity
        wpsaActive = True if int(wpsa[i]) == 1 else False
        ds24Active = True if int(ds24[i]) == 1 else False
        ds34Active = True if int(ds34[i]) == 1 else False
        ds54Active = True if int(ds54[i]) == 1 else False


        bests = bestAntenna(                                                      # run best antenna by  
            [wpsaActive, ds24Active, ds34Active, ds54Active],                     # plugging in the active antennas
            [getAny(wpsar, i),getAny(ds24r, i),getAny(ds34r, i),getAny(ds54r, i)] # and the slant ranges of them
        )

        print(bests)
        gyr = (bests[0][0], bests[1][0], bests[2][0]) # [green light, yellow light, red light]
        gyrs.append(gyr)
    return gyrs

main()