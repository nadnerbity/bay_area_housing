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
import json
import os


def loadSingleDataFile(fileToLoad):
    # Load the combined json file into memory
    with open(fileToLoad) as json_file:
        data = json.load(json_file)
    # Convert the geojson component to a pandas data frame.
    gdf = gpd.GeoDataFrame.from_features(data[1])
    gdf = gdf.set_crs(epsg=4326)
    gdf = gdf.to_crs(epsg=3857)

    # Load the request details into a pandas dataframe
    df = pd.DataFrame(data[0])
    # Normalize the data to all have their own column
    df = pd.json_normalize(df.iloc[0].arrival_searches)

    # Combine the two dataframes.
    for col in df.columns:
        gdf[col] = df[col]

    return gdf


# Load the data file by file.
N = 0
files = os.listdir()
for f in files:
    if f.endswith(".json"):
        temp = loadSingleDataFile(f)
        if N == 0:
            gdf = temp
            N += 1
        else:
            gdf = pd.concat([gdf, temp], ignore_index=True)

# Save the data to a pickle file to make loading it easier.
travelTimeFilename = 'travelTimeShapes.pkl'

with open(travelTimeFilename, 'wb') as handle:
    pickle.dump(gdf, handle, protocol=pickle.HIGHEST_PROTOCOL)

