# Analyze the effect landed has on housing affordability


import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')
from redfin_functions import *
from mortgage_calcs import *
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
plt.ion()
plt.close('all')

# ------------------------ DATA IMPORT -----------------------------
data_name_to_load = 'slac'
gdf = load_data(data_name_to_load)
gdf = gdf.loc[gdf['PROPERTY TYPE'] == 'Single Family Residential']
gdf = gdf.loc[gdf['SALE TYPE'] == 'MLS Listing']

# Build the 26.7 minute contour
# load the GPR to build the contour
gpr, x_scaler, y_scaler = load_gpr_and_scalers(data_name_to_load)
print('Generating grid to make contours with')
lat_grid, lng_grid, y_grid = generate_grid_from_gpr(gdf, gpr, x_scaler, y_scaler, data_name_to_load)
print('Generating contours')
time_to_contour = 60.0*27.6
gpd_cont = generate_time_contours_from_grid(lng_grid, lat_grid, y_grid, time_to_contour)

# Grab the bottom 10%
# Max affordable home without landed:
max_price = fsolve(how_much_can_afford, [3*230000], args=(230000, 76000, 0.061/12, 0.0115/12, 0.01/12))[0]
gdf_2x_ass = gdf[gdf['PRICE'] < max_price]
# Max with landed
max_price = fsolve(how_much_can_afford, [3*230000], args=(230000, 0, 0.051/12, 0.0115/12, 0.01/12))[0]
gdf_2x_ass_landed = gdf[gdf['PRICE'] < max_price]

fig1, ax1 = plot_bay_area_map(1543, data_name_to_load)  # generate a bay area map
plot_gpd_boundary_on_map(gpd_cont, ax1, 'black')
plot_gpd_data_on_map(gdf_2x_ass_landed, ax1, 'blue')
plot_gpd_data_on_map(gdf_2x_ass, ax1, 'red')
plt.axis('off')
plt.tight_layout()


# -------------------------- NOTES -------------------------------
# Some Landed spot checks
# How much can a household making $230k/year afford without landed, if they somehow managed 20% down
# This function outputs close to zero when you have the home costs + income balanced
# Entering a zero in the third spot means 20% down
# how_much_can_afford(979000, 230000, 0, 0.051/12, 0.0115/12, 0.01/12)
# Up the interest rate by 1% to include PMI
# how_much_can_afford(979000, 230000, 0, 0.061/12, 0.0115/12, 0.01/12)

# This optimization process solves the transcendental equation of determining the maximum loan that can be afforded
# given taxes rates, down payment and salary
# Start by assuming 100k down, 230k/year, 5.1% mortgage interest + 1% PMI, 1.15% local taxes and 1% maintenance
# fsolve(how_much_can_afford, [3*230000], args=(230000, 100000, 0.061/12, 0.0115/12, 0.01/12))[0]
# fsolve(how_much_can_afford, [3*230000], args=(230000, 0, 0.051/12, 0.0115/12, 0.01/12))[0]
# fsolve(how_much_can_afford, [3*230000], args=(230000, 0, 0.051/12, 0.0115/12, 0.01/12))[0]
# fsolve(how_much_can_afford, [3*230000], args=(230000, 240000, 0.051/12, 0.0115/12, 0.01/12))[0]
