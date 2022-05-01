# Compare the travel times for different labs

import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')
from redfin_functions import *
import matplotlib.pyplot as plt
plt.ion()
plt.close('all')


# ------------------------ DATA IMPORT berkeley -----------------------------
data_name_to_load = 'slac'
# Load the data
gdf = load_data(data_name_to_load)
# Load the county shapes
gdf_c = load_county_shape_file()

# Load the GPR fit and scaler functions
gpr, x_scaler, y_scaler = load_gpr_and_scalers(data_name_to_load)

# Generate a grid in order to make contours
print('Generating grid to make contours with')
lat_grid, lng_grid, y_grid = generate_grid_from_gpr(gdf, gpr, x_scaler, y_scaler, data_name_to_load)

# Generate a time contour
print('Generating contours')
time_to_contour = 60.0*27.6
gpd_cont = generate_time_contours_from_grid(lng_grid, lat_grid, y_grid, time_to_contour)
# Find all the houses inside the time contour
in_boundary = gdf[gdf.geometry.within(gpd_cont.geometry[0])]

# Plot everything
fig1, ax1 = plot_bay_area_map(1234, data_name_to_load)  # generate a bay area map
plot_gpd_boundary_on_map(gpd_cont, ax1, 'black') # Plot the time contour on it
plot_gpd_data_on_map(in_boundary, ax1, 'red')  # Plot the housing data on it.

