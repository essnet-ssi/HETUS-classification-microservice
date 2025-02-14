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

def scorePOI_X(gps,pois,gpsSampleSize):
    #print ("len(gps):",len(gps))
    gps=gps.sample(n=min(gpsSampleSize,len(gps)))
    def distance(x):
        row=x
        try:
            #distance = geodesic( (row.Latitude,row.Longitude), (row.lat,row.lon), ellipsoid='WGS-84').meters
            distance = great_circle( (row.Latitude,row.Longitude), (row.lat,row.lon)).meters
    
        except:
            return np.nan
        #
        return 1/(distance)*(1/(row.Accuracy))
        
    
    gps['key'] = 1
    pois['key'] = 1
    cartesian_df = pd.merge(gps, pois, on='key').drop('key', axis=1)
    gps=gps.drop('key', axis=1)
    pois=pois.drop('key', axis=1)
    cartesian_df["distance"]=cartesian_df.apply(distance,axis=1)
    result = cartesian_df.groupby(['lat','lon'])['distance'].median().rename('scorePoi')
    result=result.sort_values(ascending=False).reset_index()
    result=pd.merge(result,pois,on=["lat","lon"])
    #display(result)
    return result


