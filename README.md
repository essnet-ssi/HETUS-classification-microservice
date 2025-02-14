# HETUS-classification-microservice
This is the code of the microservice that predict the most probable HETUS activity (with assigned probabilities or scores) to each stop identified in the geotracker microservice.

This is performed through a model that exploits several information, such as place categories taxonomy, timing of the stop, country-specific indicators . Categories of place from the third party (Google Places or OpenStreetMap) are mapped to the HETUS classification of places, to connect them to HETUS activities.

The input data used for the activity prediction algorithm are:

- GPS points information
- Stop Attribute
- Map elements - Points of Interest (POI) inside the radius of the stop
- Profile of the user (age class, employment status)

## Testing the algorithm

Edit or confirm configuration parameters in the ADS/parameters.json file.

Run the Test_ADS.ipynb notebook.
