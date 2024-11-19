#creating functions that can be used throughout all the files
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
        
def getAny(arr, num):
    #artemisPath= open("NASA_ADC_Data_Update.csv", "r") 
    #arr = []
    # for line in artemisPath:
    #     entries = line.split(",")
    #     if is_float(entries[column]):
    #         arr.append(entries[column])
    #     else:
    #         arr.append("")
    if is_float(arr[num]):
        return float(arr[num])
    else:
        return 0