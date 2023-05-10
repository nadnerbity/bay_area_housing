# Plot houses that 2x SLAC associate staff scientist can afford


from scipy.optimize import fsolve
from mortgage_calcs import *
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')
from redfin_functions import *

plt.ion()
plt.close('all')

# ------------------------ DATA IMPORT -----------------------------

counties = load_county_shape_file()
gdf = load_data_by_date('17042023')
# Select only single family homes
gdf = gdf.loc[gdf['PROPERTY TYPE'] == 'Single Family Residential']
gdf = gdf.loc[gdf['SALE TYPE'] == 'MLS Listing']
# Remove <=2 bedroom listings, these aren't family friendly
gdf = gdf.loc[gdf['BEDS'] > 2.0]
# Remove <=1 bathroom listings, these aren't family friendly
gdf = gdf.loc[gdf['BATHS'] > 1.0]

fig1, ax1 = plot_bay_area_map(1234, 'chicago')  # generate a chicago map

dupage = gdf[gdf.geometry.within(counties.loc['DUPAGE'].geometry)]
kane = gdf[gdf.geometry.within(counties.loc['KANE'].geometry)]

plot_gpd_data_on_map(gdf, ax1, 'red')
plot_gpd_data_on_map(dupage, ax1, 'blue')


