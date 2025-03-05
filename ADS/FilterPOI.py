#
import pandas as pd
import numpy as np
from geopy.distance import geodesic,great_circle
from matplotlib import pyplot as plt


def FilterPOI(gps,pois,RadiusStep):
    # FILTER ONLY POI tagged with a tus place
    #display(pois)
    pois["TUS_PLACE"]=pois.TUS_PLACE.astype(str)
    pois=pois[pois.TUS_PLACE.str.isdigit()]  

    StopCenter=gps[["Longitude", 	"Latitude"]].mean()
    
    def distance(x):
        row=x
        try:
            distance = great_circle( (StopCenter[1],StopCenter[0]), (row.lat,row.lon)).meters    
        except:
            return np.nan
        #
        return (distance)
        
    pois["distance"]=pois.apply(distance,axis=1)
    
    RadiusThreshold=RadiusStep
    while (True):        
        poisFilter=pois[pois["distance"]<=RadiusThreshold]        
        print("with radius",RadiusThreshold,"found",len(poisFilter))
        if (len(poisFilter)>0)|(RadiusThreshold>10000):
            break
        RadiusThreshold+=RadiusStep
    
    return poisFilter


