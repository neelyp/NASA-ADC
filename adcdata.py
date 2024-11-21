#creating functions that can be used throughout all the files
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
        
def getAny(arr, num):
    if is_float(arr[num]):
        return float(arr[num])
    else:
        return 0