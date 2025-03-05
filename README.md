# HETUS-classification-microservice
This is the code of the microservice that predict the most probable HETUS activity (with assigned probabilities or scores) to each stop identified in the geotracker microservice.

This is performed through a model that exploits several information, such as place categories taxonomy, timing of the stop, country-specific indicators . Categories of place from the third party (Google Places or OpenStreetMap) are mapped to the HETUS classification of places, to connect them to HETUS activities.

The input data used for the activity prediction algorithm are:

- GPS points information
- Stop Attribute
- Map elements - Points of Interest (POI) inside the radius of the stop
- Profile of the user (age class, employment status)

# Configuration parameters

The parameters to be set before run the algorithm are in the _./ADS/parameters.json_ file:

- mapService: the map service to be used, may be "GP" | "OSM", i.e. GooglePlaces or OpenStreetMap
- UseTUSdata: if True use probabilistic approach
- UseUserProfileInfo: if True use the user profile information (age class, occupation status) to predict activity
- AccuracyRadiusGPSMin (e.g. 20), minimum radius of the gps accuracy
- UserSpeedMax (e.g. 1.96), maximum speed of a user while walking
- DinamicPOISearchRadiusStep (e.g. 100), 
- GpsSampleSizeMax (e.g. 100), maximum number of gps points used to calcualte the median distance from the poi

## TUS (Time Usage Survey) Istat tables

- _./TUS_Istat/TUS_PLACE_COD_EN.csv_ : table of TUS place code, description of place and HETUS place associated
- _./TUS_Istat/HETUS_ACTIVITY_COD_EN.csv_ : table containing the HETUS activities and related descriptions
- _./TUS_Istat/GP2HETUS_MAP.csv_ : table of HETUS activities associated to GooglePlaces
- _./TUS_Istat/GP2TUS_PLACE_MAP.csv_ : table of TUS places associated to GooglePlaces
- _./TUS_Istat/OSM2TUS_PLACE_MAP.csv_ : table of TUS places associated to OpenStreetMap places
- _./TUS_Istat/Activity_Places_TUS_count2.csv_ : TUS table of activity, place, user profile, duration
- _./TUS_Istat/data_by_tslot/Activity_Places_TUS_TIME_SLOT.csv_ : TUS table of activity, place, user profile, duration, time slot

## Testing the algorithm

Edit or confirm configuration parameters in the _./ADS/parameters.json_ file.

Run the _./ADS/Test_ADS.ipynb_ notebook.
