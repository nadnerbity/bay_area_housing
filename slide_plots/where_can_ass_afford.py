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
data_name_to_load = 'slac'
gdf = load_data(data_name_to_load)


# Select only single family homes
gdf = gdf.loc[gdf['PROPERTY TYPE'] == 'Single Family Residential']
gdf = gdf.loc[gdf['SALE TYPE'] == 'MLS Listing']
# Remove <=2 bedroom listings, these aren't family friendly
gdf = gdf.loc[gdf['BEDS'] > 2.0]
# Remove <=1 bathroom listings, these aren't family friendly
gdf = gdf.loc[gdf['BATHS'] > 1.0]


fig1, ax1 = plot_bay_area_map(1234, 'slac')  # generate a bay area map

# 5.1% is 30-year fixed rate on 4/17/22, 1.15% is average property taxes
interest_rate = 0.051+0.0115
# (1/0.8) is to include the down payment
# 1000 convert to $ from k$
# 2*135 is two Staff Scientists at SLAC
# max_price = (1/0.8)*1000*2*135*principal_to_income(interest_rate/12, 360)
max_price = fsolve(how_much_can_afford, [3*270000], args=(270000, 0, 0.051/12, 0.0115/12, 0.01/12))[0]
gdf_ss = gdf[gdf['PRICE'] <= max_price]
gdf_ss = gdf_ss.sort_values('travel_time_with_traffic_s')
plot_gpd_data_on_map(gdf_ss, ax1, 'blue')  # Plot the housing data on it.

# 2*115 is two Associate Staff Scientists at SLAC
# max_price = (1/0.8)*1000*2*115*principal_to_income(interest_rate/12, 360)
max_price = fsolve(how_much_can_afford, [3*230000], args=(230000, 0, 0.051/12, 0.0115/12, 0.01/12))[0]
gdf_ass = gdf[gdf['PRICE'] <= max_price]
gdf_ass = gdf_ass.sort_values('travel_time_with_traffic_s')
plot_gpd_data_on_map(gdf_ass, ax1, 'red')  # Plot the housing data on it.
ax1.axis('off')

# ------------------- PLOT 27.6 MINUTE DRIVE --------------------------
# load the GPR to build the contour
gpr, x_scaler, y_scaler = load_gpr_and_scalers(data_name_to_load)
print('Generating grid to make contours with')
lat_grid, lng_grid, y_grid = generate_grid_from_gpr(gdf, gpr, x_scaler, y_scaler, data_name_to_load)
print('Generating contours')
time_to_contour = 60.0*27.6
gpd_cont = generate_time_contours_from_grid(lng_grid, lat_grid, y_grid, time_to_contour)
plot_gpd_boundary_on_map(gpd_cont, ax1, 'black')



# temp = gdf_is_within_plot_area(gdf_ss)
# nx = 2**4
# interest_rate = np.linspace(0.01, 0.10, nx)
# # ------------------------ PLOTS -----------------------------
# # Plot ratio of principal to income for various interest rates
# plt.close(745)
# fig = plt.figure(745)
# ax1 = fig.add_subplot(111)
# ax1.plot(100*interest_rate, principal_to_income(interest_rate/12, 360), 'k')
# ax1.set_xlabel('Yearly Interest Rate [%]', fontsize=20)
# ax1.set_ylabel('Principal / Income [1]', fontsize=20)
# plt.tight_layout()
