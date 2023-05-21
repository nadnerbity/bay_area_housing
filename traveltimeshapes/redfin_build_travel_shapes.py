#!/usr/bin/env python
"""Use the OSRM API to turn longitude and latitude data
into travel times to SLAC
"""


__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"


# Set up the imports to run the scrape.
import pandas as pd
import geopandas as gpd
import pickle

travelTimeFilename = 'travelTimeShapes.pkl'
dataID = 'argonne'

with open(travelTimeFilename, 'rb') as handle:
    oldGdf = pickle.load(handle)

# Load the new shape file
gdf = gpd.read_file(dataID + '_polygon.txt')
# Convert to the epsg of the new data to the epsg you've been using.
gdf = gdf.to_crs(epsg=3857)

# Load the query details for the new shape file
df = pd.read_json(dataID + '_request.txt')
# Normalize the data to all have their own column
df = pd.json_normalize(df.iloc[0].arrival_searches)
# Update the name of the shape
df.at[0, 'id'] = dataID

# Combine the two dataframes.
for col in df.columns:
    gdf[col] = df[col]

# Add the new shape to the file with all the shapes in them.
oldGdf = pd.concat([oldGdf, gdf], ignore_index=True)

# gdf.to_file(travelTimeFilename, driver='GeoJSON')
with open(travelTimeFilename, 'wb') as handle:
    pickle.dump(oldGdf, handle, protocol=pickle.HIGHEST_PROTOCOL)

