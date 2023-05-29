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
name_of_data = '28112022'
dir_to_data = '/Users/brendan/Documents/Coding/RedfinTravelTime/data/' + name_of_data + '/' + name_of_data + '.h5'
df = pd.read_hdf(dir_to_data)
# Select only single family homes
df = df.loc[df['PROPERTY TYPE'] == 'Condo/Co-op']
df = df.loc[df['SALE TYPE'] == 'MLS Listing']
# Convert pandas DataFrame to GeoPandas DataFrame
gdf = convert_df_to_gdf(df)
# # Rename the HOA column to get rid of the '/'
# gdf = gdf.rename(columns={'HOA/MONTH': 'HOAperMonth'})
#
# #
# # # This throws a warning that will need to be fixed.
# gdf = add_required_salary_to_dataframe(gdf, 0, 0.062/12, 0.0115/12, 0.01/12)


# ------------------- PLOT 27.6 MINUTE DRIVE --------------------------
data_name_to_load = 'slac'
# generate a bay area map
fig1, ax1 = plot_bay_area_map(1234, 'slac')

# load the GPR to build the contour
gpr, x_scaler, y_scaler = load_gpr_and_scalers(data_name_to_load)
print('Generating grid to make contours with')
lat_grid, lng_grid, y_grid = generate_grid_from_gpr(gdf, gpr, x_scaler, y_scaler, data_name_to_load)
print('Generating contours')
time_to_contour = 60.0*27.6
gpd_cont = generate_time_contours_from_grid(lng_grid, lat_grid, y_grid, time_to_contour)

plot_gpd_boundary_on_map(gpd_cont, ax1, 'black')

