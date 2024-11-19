#make global
mins = []
rx = []
ry  = []
rz = []
vx = []
vy = [] 
vz = []
mass = []
wpsa = []
wpsar = []
ds54 = []
ds54r = []
ds24 = []
ds24r = []
ds34 = []
ds34r = []
def createLists():
    artemisPath= open("assets/NASA_ADC_Data_Update.csv", "r") 
    mins = []
    rx = []
    ry  = []
    rz = []
    vx = []
    vy = []
    vz = []
    mass = []
    wpsa = []
    wpsar = []
    ds54 = []
    ds54r = []
    ds24 = []
    ds24r = []
    ds34 = []
    ds34r = []
   
    for line in artemisPath:
        #get rids of the commas
        entries = line.split(",")
        #append to each array
        mins.append(entries[0])
        rx.append(entries[1])
        ry.append(entries[2])
        rz.append(entries[3])
        vx.append(entries[4])
        vy.append(entries[5])
        vz.append(entries[6])
        mass.append(entries[7])
        wpsa.append(entries[8])
        wpsar.append(entries[9])
        ds54.append(entries[10])
        ds54r.append(entries[11])
        ds24.append(entries[12])
        ds24r.append(entries[13])
        ds34.append(entries[14])
        ds34r.append(entries[15])
#creating functions that can be used throughout all the files
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def getMins(num):
    artemisPath= open("assets/NASA_ADC_Data_Update.csv", "r") 
    mins = []
    for line in artemisPath:
        entries = line.split(",")
        if is_float(entries[0]):
            mins.append(entries[0])
        else:
            mins.append("")
    return float(mins[num])

def getRx(num):
    artemisPath= open("assets/NASA_ADC_Data_Update.csv", "r") 
    rx = []
    for line in artemisPath:
        entries = line.split(",")
        print(str(len(entries)))
    #     if is_float(entries[1]):
    #         rx.append(entries[1])
    #     else:
    #         rx.append("")
    # return float(rx[num])

def getRy(num):
    createLists()
    return float(ry[num])
def getRz(num):
    createLists()
    return float(rz[num])
def getVx(num):
    createLists()
    return float(vx[num])
def getVy(num):
    createLists()
    return float(vy[num])
def getVz(num):
    createLists()
    return float(vz[num])
def getMass(num):
    createLists()
    return float(mass[num])
def getWpsa(num):
    createLists()
    return float(wpsa[num])
def getWpsar(num):
    createLists()
    return float(wpsar[num])
def getDs54(num):
    createLists()
    return float(ds54[num])
def getDs54r(num):
    createLists()
    return float(ds54r[num])
def getDs24(num):
    createLists()
    return float(ds24[num])
def getDs24r(num):
    createLists()
    return float(ds54r[num])
def getDs34(num):
    createLists()
    return float(ds54[num])