# 2- al punto 2 ci deve essere un input che prevede  (Pieter come ci passiamo i dati tra blocchi funzionali?)
#   {X_i},T     - i punti gps associati allo stop   -alternativa- se non è possibile passare i punti gps può passare una matrice di covarianza ed il centroide tempo e durata dello stop
#   {POI_j}     - i poi associati ad un centroide ed radius che ci passa il blocco funzionale-1 il POI contiene lat lon tag
#   UserProfile - dati associati allo user OCCUPAZIONE CLASSE ETA
#
# l'algoritmo - calcola scorePOI_X monotono. P({X_i}|POI_j)
# lo score si può calcolare in due maniere median,bidimentionalGaussian
# median -> scorePOI_X(j) = mediana(Acc{X_i}/distanza({X_i},POI_j)) 
#
#


# 2- al punto 2 ci deve essere un input che prevede  (Pieter come ci passiamo i dati tra blocchi funzionali?)
#   {X_i},T     - i punti gps associati allo stop   -alternativa- se non è possibile passare i punti gps può passare una matrice di covarianza ed il centroide tempo e durata dello stop
#   {POI_j}     - i poi associati ad un centroide ed radius che ci passa il blocco funzionale-1 il POI contiene lat lon tag
#   UserProfile - dati associati allo user OCCUPAZIONE CLASSE ETA
#
# l'algoritmo - calcola scorePOI_X monotono. P({X_i}|POI_j)
# lo score si può calcolare in due maniere median,bidimentionalGaussian
# median -> scorePOI_X(j) = mediana(Acc{X_i}/distanza({X_i},POI_j)) 
#
#
import pandas as pd
import numpy as np
from geopy.distance import geodesic,great_circle
from matplotlib import pyplot as plt





def FilterPOI(gps,pois,RadiusThresholdStep):

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
    
    for RadiusThreshold in range(0,100,RadiusThresholdStep):
        print(RadiusThreshold,RadiusThresholdStep)
        poisFilter=pois[pois["distance"]<=RadiusThreshold]
        
        #print("with radius",RadiusThreshold,"found",len(poisFilter))
        if len(poisFilter)>0:
            break

    #print ("pois Filtered:",len(poisFilter))
    
    return poisFilter


