#global mapService, poiSearchRadius, UserSpeedMax ,radiusAccMax ,ActivityDurationMin ,NActivitySL, debug
# load JSON file containing parameters

import json
import pandas as pd


def Load():
    with open('parameters.json', 'r') as f:
        parameters = json.load(f)
    global mapService
    mapService = parameters['mapService']
    
    global poiSearchRadius
    poiSearchRadius = parameters['poiSearchRadius']
    
    global UserSpeedMax
    UserSpeedMax = parameters['UserSpeedMax']
    
    global radiusAccMax
    radiusAccMax = parameters['radiusAccMax'] #ATS Activity radius must be less than radiusAccMax
    
    global ActivityDurationMin
    ActivityDurationMin = parameters['ActivityDurationMin'] #ATS Activity duration must be greater than ActivityDurationMin
    
    global gpsSampleSize
    gpsSampleSize =parameters['gpsSampleSize'] # number of gps points used to calcualte the median distance from the poi
    
    global RadiusThresholdPoiStop
    RadiusThresholdPoiStop=parameters['RadiusThresholdPoiStop']
    
    global RadiusGPSThreshold
    RadiusGPSThreshold=parameters['RadiusGPSThreshold'] # gps.Accuracy<=RadiusGPSThreshold flter on GPS points accuracy

    global predMethod
    predMethod=parameters['predMethod'] # method used to predict activity: 'prob' if probabilistic, based on tables of activities, places, user, duration; 'direct' if it is not based on tables

    global DURATION_MODE
    DURATION_MODE=parameters['DURATION_MODE'] # actitivity duration distribution: lognorm | norm | uniform

    global TIMESLOT
    TIMESLOT=eval(parameters['TIMESLOT']) # True if the time slot is considered in the activity prediction, False otherwise

    print(parameters)
    print("Load model Parameters")
    
    #stop=ATS[(ATS.radius<=radiusAccMax)&(ATS.duration>=ActivityDurationMin)]