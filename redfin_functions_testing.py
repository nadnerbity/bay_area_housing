#!/usr/bin/env python
"""Test the redfin_functions routines.
"""


__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

# Set up the imports to run the scrape.
# import pandas as pd
# import geopandas as gpd
# import contextily as cx
# import numpy as np
# from shapely.geometry import Point
# from shapely.geometry import Polygon
# import matplotlib.pyplot as plt
# from scipy.interpolate import griddata
from redfin_functions import *
plt.ion()
plt.close('all')


# In order for ipython to reimport 'redfin_functions' you'll need to run the following in the console:
# %load_ext autoreload
# %autoreload 2

# ------------------------ DATA IMPORT -----------------------------
dir_to_collate = '/Users/brendan/Documents/Coding/RedfinTravelTime/data/March 28 2022'
dump_file_name = 'all_data.h5'
dump_file_name = 'SFH_with_travel_time.h5'

# Load the data frame
df = pd.read_hdf(dir_to_collate + '/' + dump_file_name)
# Select only single family homes
df = df.loc[df['PROPERTY TYPE'] == 'Single Family Residential']
df = df.loc[df['SALE TYPE'] == 'MLS Listing']
# df = df.loc[df['PRICE'] < 1000000.0]

# ------------------------ TEST SIMPLE PLOTTING -----------------------------
gdf = convert_df_to_gdf(df)
fig1, ax1 = plot_bay_area_map(1234)  # generate a bay area map
plot_gpd_data_on_map(gdf, ax1, 'red')  # Plot the housing data on it.

# ------------------------ TEST GENERATING CONVEX HULLS -----------------------------
# First find all points with a travel time smaller than 600 seconds


gpr, x_scaler, y_scaler = load_gpr_and_scalers()
print('Generating grid to make contours with')
lat_grid, lng_grid, y_grid = generate_grid_from_gpr(gdf, gpr, x_scaler, y_scaler)
print('Generating contours')
time_to_contour = 1200.0
gpd_cont = generate_time_contours_from_grid(lng_grid, lat_grid, y_grid, time_to_contour)
plot_gpd_boundary_on_map(gpd_cont, ax1, 'cyan')

