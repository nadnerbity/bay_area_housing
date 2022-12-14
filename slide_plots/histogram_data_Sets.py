# Plot houses that 2x SLAC associate staff scientist can afford


from scipy.optimize import fsolve
from mortgage_calcs import *
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')
from redfin_functions import *

plt.ion()
plt.close('all')


def principal_to_income(r, n):
    return (1-(1+r)**-n)/40/r


# ------------------------ DATA IMPORT -----------------------------

gdf_28112022 = load_data_by_date('28112022')

# Select only single family homes
gdf_28112022 = gdf_28112022.loc[gdf_28112022['PROPERTY TYPE'] == 'Single Family Residential']
gdf_28112022 = gdf_28112022.loc[gdf_28112022['SALE TYPE'] == 'MLS Listing']
# Remove <=2 bedroom listings, these aren't family friendly
gdf_28112022 = gdf_28112022.loc[gdf_28112022['BEDS'] > 2.0]
# Remove <=1 bathroom listings, these aren't family friendly
gdf_28112022 = gdf_28112022.loc[gdf_28112022['BATHS'] > 1.0]
# Keep only house less than $2.5M
gdf_28112022 = gdf_28112022.loc[gdf_28112022['PRICE'] < 2500000.0]

gdf_28032022 = load_data_by_date('28032022')

# Select only single family homes
gdf_28032022 = gdf_28032022.loc[gdf_28032022['PROPERTY TYPE'] == 'Single Family Residential']
gdf_28032022 = gdf_28032022.loc[gdf_28032022['SALE TYPE'] == 'MLS Listing']
# Remove <=2 bedroom listings, these aren't family friendly
gdf_28032022 = gdf_28032022.loc[gdf_28032022['BEDS'] > 2.0]
# Remove <=1 bathroom listings, these aren't family friendly
gdf_28032022 = gdf_28032022.loc[gdf_28032022['BATHS'] > 1.0]
# Keep only house less than $2.5M
gdf_28032022 = gdf_28032022.loc[gdf_28032022['PRICE'] < 2500000.0]

# ------------------- PLOT 27.6 MINUTE DRIVE --------------------------
data_name_to_load = 'slac'
# generate a bay area map
fig1, ax1 = plot_bay_area_map(1234, 'slac')

# load the GPR to build the contour
gpr, x_scaler, y_scaler = load_gpr_and_scalers(data_name_to_load)
print('Generating grid to make contours with')
lat_grid, lng_grid, y_grid = generate_grid_from_gpr(gdf_28112022, gpr, x_scaler, y_scaler, data_name_to_load)
print('Generating contours')
time_to_contour = 60.0*27.6
gpd_cont = generate_time_contours_from_grid(lng_grid, lat_grid, y_grid, time_to_contour)
plot_gpd_boundary_on_map(gpd_cont, ax1, 'black')

# Extract only houses within a 27.6 minute boundary of SLAC
in_bdy_28112022 = gdf_28112022[gdf_28112022.geometry.within(gpd_cont.geometry[0])]
in_bdy_28032022 = gdf_28032022[gdf_28032022.geometry.within(gpd_cont.geometry[0])]
plot_gpd_data_on_map(in_bdy_28112022, ax1, 'red')


plt.close(3456)
plt.figure(3456)
ax = plt.subplot(211)
plt.hist(in_bdy_28032022.PRICE.values,
         50,
         density=False,
         facecolor='r',
         alpha=0.75)
plt.xlim([0.5e6, 2.5e6])
plt.ylim([0, 20])
ax.set_title('March 28th 2022', fontsize=18)

ax = plt.subplot(212)
plt.hist(in_bdy_28112022.PRICE.values,
         50,
         density=False,
         facecolor='b',
         alpha=0.75)
plt.xlim([0.5e6, 2.5e6])
plt.ylim([0, 20])
ax.set_title('November 28th 2022', fontsize=18)

plt.tight_layout()



