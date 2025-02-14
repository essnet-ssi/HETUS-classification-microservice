
import json
import pandas as pd

def Read(filename) :
    global gps,pois,stop,STOPradius,profile
    # 1 READ INPUT JSON   
    g= open (filename,"r")      
    ADS_in=(json.load(g))
    g.close()
        

    # 3 GET GPS POINT FILTERING VELOCITY (UserSpeedMax) E ACCURACY (RadiusGPSThreshold parameter)   
    gps=pd.DataFrame(ADS_in["gps"])     
   
    
    # 4 GET POINTS OF INTERESTS
    pois=pd.DataFrame(ADS_in["pois"])    
    #display(pois)
    MapServicePoisNumber = len(pois)


    # 5 GET STOP INFO FROM INPUT JSON
    stop=pd.DataFrame([ADS_in["stop"]])
    STOPradius=stop.iloc[0].radius #??  --- > STOPradius = stop?


    # 5.1 GET TIME SLOT 
    #codFascia=TimeSlotFromStop.getTimeSlotFromStop(ADS_in)

    # 6b GET PROFILE INFO FROM INPUT JSON
    profile=pd.DataFrame([ADS_in["profile"]])