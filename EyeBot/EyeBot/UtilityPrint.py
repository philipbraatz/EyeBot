debug_level = "all"

def log(message,type="TEMP"):
    #print("logging..."+type)
    if (type == 'temp' or type == 't') and (debug_level =="all" or debug_level == 'temp'):
        print("\ntest value: "+message+"----------\n")
    elif type == 'debug' or type == 'd' and (debug_level =="all" or debug_level == 'debug' or debug_level == 'temp'):
        print("->"+message)
    elif type == "user" or type == 'u' and (True):#all debug levels
        print(": "+message)