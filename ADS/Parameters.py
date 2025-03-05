#global mapService, poiSearchRadius, UserSpeedMax ,radiusAccMax ,ActivityDurationMin ,NActivitySL, debug
# load JSON file containing parameters

import json
import pandas as pd


def Load():
    with open('parameters.json', 'r') as f:
        parameters = json.load(f)
    global mapService
    mapService = parameters['mapService']
    
    #global poiSearchRadius
    #spoiSearchRadius = parameters['poiSearchRadius']
    
    global UserSpeedMax
    UserSpeedMax = parameters['UserSpeedMax']
    
    #global radiusAccMax
    #radiusAccMax = parameters['radiusAccMax'] #ATS Activity radius must be less than radiusAccMax
    
    #global ActivityDurationMin
    #ActivityDurationMin = parameters['ActivityDurationMin'] #ATS Activity duration must be greater than ActivityDurationMin
    
    global GpsSampleSizeMax
    GpsSampleSizeMax =parameters['GpsSampleSizeMax'] # number of gps points used to calcualte the median distance from the poi
    
    global DinaminPOISearchRadiusStep
    DinaminPOISearchRadiusStep=parameters['DinamicPOISearchRadiusStep']
    
    global AccuracyRadiusGPSMin
    AccuracyRadiusGPSMin=parameters['AccuracyRadiusGPSMin'] # gps.Accuracy<=RadiusGPSThreshold flter on GPS points accuracy

    global UseTUSdata
    UseTUSdata=parameters['UseTUSdata']   # method used to predict activity: 'prob' if probabilistic, 
                                                # based on tables of activities, places, user, duration; 
                                                # 'NoTUS' if it is not based on tables

    global DURATION_MODE
    DURATION_MODE="lognorm" #parameters['DURATION_MODE'] # actitivity duration distribution: lognorm | norm | uniform

    global TIMESLOT    
    if UseTUSdata==True:
        TIMESLOT=True# eval(parameters['TIMESLOT']) # True if the time slot is considered in the activity prediction, False otherwise
    else:
        TIMESLOT=False


    global UseUserProfileInfo
    UseUserProfileInfo=parameters["UseUserProfileInfo"]
    
    print(parameters)
    print("Load model Parameters")

    #"DURATION_MODE": "lognorm",
    #"TIMESLOT": "False"
    
    #stop=ATS[(ATS.radius<=radiusAccMax)&(ATS.duration>=ActivityDurationMin)]