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
import os, sys

file_path = os.path.abspath(os.path.dirname(__file__))
base = '/'.join(file_path.split('/')[:-1])
sys.path.insert(1, base)
sys.path.insert(1, base + 'traveltimeshapes')
from redfin_functions import *

travelTimeShape = load_travel_time_shapes()

lab = 'slac'
fig1, ax1 = plot_bay_area_map(1234, lab)

plot_gpd_boundary_on_map(travelTimeShape[travelTimeShape['id'] == lab], ax1, 'red')

gdf = load_data_by_date('17042023')
plot_gpd_data_on_map(gdf, ax1, 'blue')

# Split out only the houses inside the travel time polygon
inside = gdf[gdf.geometry.within(travelTimeShape[travelTimeShape['id'] == lab].geometry)]
plot_gpd_data_on_map(inside, ax1, 'black')