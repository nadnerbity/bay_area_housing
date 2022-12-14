


# A first crack at trying to plot cost of housing as a function of time. This will lead to re-doing a lot of methods
# that import/export data but I want to know how to do the analysis before deciding on data IO

import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')
from redfin_functions import *
import matplotlib.pyplot as plt
plt.ion()
plt.close('all')

# ------------------------ DATA IMPORT -----------------------------
area_to_load = 'slac'
data_name_to_load = '02062022'
gdf = load_data_by_date(data_name_to_load)

# ------------------------ FIND HOUSES INSIDE SAN MATEO -----------------------------
# Load the county shapes
gdf_c = load_county_shape_file()

# Extract only houses in San Mateo
SM = gdf[gdf.geometry.within(gdf_c.loc['San Mateo'].geometry)]
fig1, ax1 = plot_bay_area_map(1233, area_to_load)  # generate a bay area map
plot_gpd_data_on_map(SM, ax1, 'red')  # Plot the housing data on it.

for index, row in gdf_c.iterrows():
    temp = gdf[gdf.geometry.within(gdf_c.loc[index].geometry)]
    print("Median home price in " + index + " is $" + str(temp.PRICE.median()))

# ------------------- FIND HOUSES INSIDE 27.6 MINUTE DRIVE --------------------------
# load the GPR to build the contour
gpr, x_scaler, y_scaler = load_gpr_and_scalers(area_to_load)
print('Generating grid to make contours with')
lat_grid, lng_grid, y_grid = generate_grid_from_gpr(gdf, gpr, x_scaler, y_scaler, area_to_load)
print('Generating contours')
time_to_contour = 60.0*27.6 # Convert 27.6 minutes to seconds
gpd_cont = generate_time_contours_from_grid(lng_grid, lat_grid, y_grid, time_to_contour)

# This takes a boundary in latitude and longitude that is 27.6 minutes from SLAC and keeps only the houses inside
# that boundary.
in_boundary = gdf[gdf.geometry.within(gpd_cont.geometry[0])]

fig1, ax1 = plot_bay_area_map(1234, area_to_load)  # generate a bay area map
plot_gpd_boundary_on_map(gpd_cont, ax1, 'black')
plot_gpd_data_on_map(in_boundary, ax1, 'red')  # Plot the housing data on it.

# ------------------- CREATE A DATAFRAM TO HOLD THE DATE DATA --------------------------

county_list = []
for index in gdf_c.iterrows():
    county_list.append(index[0])

column_names = ["date", "median_price_near_slac"]
column_names = column_names + county_list
df_by_date = pd.DataFrame(columns=column_names)
dates = ['28032022', '02062022', '21062022', '06072022', '15092022']
# gdf = load_data_by_date(data_name_to_load)

# The Dates are the rows, columns are locations of median prices.
for index in dates:
    A = [index]
    # Load the data of interest
    gdf = load_data_by_date(index)

    # Extract only the houses inside the 27.6 minute commute from SLAC
    in_boundary = gdf[gdf.geometry.within(gpd_cont.geometry[0])]
    A.append(in_boundary.PRICE.median())

    # Extract only houses in San Mateo
    for k in county_list:
        temp = gdf[gdf.geometry.within(gdf_c.loc[k].geometry)]
        A.append(temp.PRICE.median())

    # Calculate the median price in that range and save to data frame
    df_by_date.loc[len(df_by_date.index)] = A

