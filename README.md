# HETUS-classification-microservice
This is the code of the microservice that predict the most probable HETUS activity (with assigned probabilities or scores) to each stop identified in the geotracker microservice.

This is performed through a model that exploits several information, such as place categories taxonomy, timing of the stop, country-specific indicators . Categories of place from the third party (Google Places or OpenStreetMap) are mapped to the HETUS classification of places, to connect them to HETUS activities.

The input data used for the activity prediction algorithm are:

- GPS points information
- Stop Attribute
- Map elements - Points of Interest (POI) inside the radius of the stop
- Profile of the user (age class, employment status)

# Configuration parameters

The parameters to be set before run the algorithm are in the ADS/parameters.json file:

- mapService: the map service to be used, may be "GP" | "OSM", i.e. GooglePlaces or OpenStreetMap
- radiusAccMax (e.g. 12000)
- poiSearchRadius (e.g. 50)
- ActivityDurationMin (e.g. 300 seconds), the minimum duration for an activity
- UserSpeedMax (e.g. 1.96), tha maximum speed of a user while walking
- gpsSampleSize (e.g. 100)
- RadiusThresholdPoiStop": 50,
- RadiusGPSThreshold": 20,
- predMethod ("direct" | "prob"), method used to predict activity: 'prob' if probabilistic, based on tables of activities, places, user, duration; 'direct' if it is not 
             based on tables
- DURATION_MODE  ("lognorm" | "norm" | "uniform"), actitivity duration distribution
- TIMESLOT" ("False"|"True), True if the time slot is considered in the activity prediction, False otherwise

## Testing the algorithm

Edit or confirm configuration parameters in the ADS/parameters.json file.

Run the Test_ADS.ipynb notebook.
