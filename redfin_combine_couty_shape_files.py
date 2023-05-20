#!/usr/bin/env python
"""Combine all the county shape files from different sources into one file that is easier to load.
"""

# Version 0.1: First shot at combining all the shape files
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

import os
import geopandas as gpd
import pandas as pd
import pickle

file_path = os.path.abspath(os.path.dirname(__file__))
# Open the shape files for the Bay Area counties.
shape_file = file_path + '/Counties/geo_export_b749f330-e0bd-4f34-80b8-f9a7de8529af.shp'
gdf = gpd.read_file(shape_file)  # Read file into a geodataframe
gdf = gdf.to_crs(epsg=3857)
gdf = gdf.set_index('county')

# Add in Santa Cruz, which isn't the Bay Area because ???
# shape_file_SC = r'/Users/brendan/Documents/Coding/RedfinTravelTime/Counties/SC_County_Boundary/County_Boundary.shp'
shape_file_SC = file_path + '/Counties/SC_County_Boundary/County_Boundary.shp'
gdf_SC = gpd.read_file(shape_file_SC)  # Read file into a geodataframe
gdf_SC = gdf_SC.to_crs(epsg=3857)
gdf_SC['county'] = 'Santa Cruz'
gdf_SC['objectid'] = 10.0
gdf_SC['fipsstco'] = '06087'
gdf_SC = gdf_SC.drop(labels=['OBJECTID', 'County_Bdy', 'SHAPE_Leng', 'SHAPE_Area'], axis=1)
gdf_SC = gdf_SC.set_index('county')
gdf = gpd.GeoDataFrame(pd.concat([gdf, gdf_SC], ignore_index=False))
gdf = gdf.set_crs(epsg=3857)

gdf = gdf.drop('objectid', axis=1)

shape_file_IL = file_path + '/Counties/IL_BNDY_County/IL_BNDY_County_Py.shp'
gdf_IL = gpd.read_file(shape_file_IL)
gdf_IL = gdf_IL.to_crs(epsg=3857)
gdf_IL = gdf_IL.rename(columns={'COUNTY_NAM': 'county', 'CO_FIPS': 'fipsstco'})
gdf_IL = gdf_IL.set_index('county')
# Add the state number (17) and convert the FIPS to the appropriate format
gdf_IL['fipsstco'] = gdf_IL['fipsstco'].apply(lambda x : '17{:03d}'.format(x))
gdf = gpd.GeoDataFrame(pd.concat([gdf, gdf_IL], ignore_index=False))
gdf = gdf.set_crs(epsg=3857)


save_file_name = file_path + '/Counties/' + 'all_counties.pkl'
with open(save_file_name, 'wb') as handle:
    pickle.dump(gdf, handle, protocol=pickle.HIGHEST_PROTOCOL)


