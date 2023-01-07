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
name_of_data = '28112022'
dir_to_data = '/Users/brendan/Documents/Coding/RedfinTravelTime/data/' + name_of_data + '/' + name_of_data + '.h5'
df = pd.read_hdf(dir_to_data)
# Select only single family homes
df = df.loc[df['PROPERTY TYPE'] == 'Condo/Co-op']
df = df.loc[df['SALE TYPE'] == 'MLS Listing']
# Convert pandas DataFrame to GeoPandas DataFrame
gdf = convert_df_to_gdf(df)
# Rename the HOA column to get rid of the '/'
gdf = gdf.rename(columns={'HOA/MONTH': 'HOAperMonth'})

#
# # This throws a warning that will need to be fixed.
gdf = add_required_salary_to_dataframe(gdf, 0, 0.062/12, 0.0115/12, 0.01/12)


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
#

# (gdf.BATHS.values >= 2.0)
# Keep only 2+2 or larger, we are looking for things for a family.
# in_bdy = gdf.loc[(gdf.BATHS.values >= 2.0) & (gdf.BEDS.values >= 2.0)]

# # Extract only houses within a 27.6 minute boundary of SLAC
# in_bdy = in_bdy[in_bdy.geometry.within(gpd_cont.geometry[0])]

OneAndOne = gdf.loc[(gdf.BATHS.values >= 1.0) & (gdf.BEDS.values >= 1.0)];
OneAndOne = OneAndOne[OneAndOne.geometry.within(gpd_cont.geometry[0])]

TwoAndTwo = gdf.loc[(gdf.BATHS.values >= 2.0) & (gdf.BEDS.values >= 2.0)]
TwoAndTwo = TwoAndTwo[TwoAndTwo.geometry.within(gpd_cont.geometry[0])]


scale_value = 1e6
plt.close(3456)
plt.figure(3456)
ax1 = plt.subplot(211)
plt.hist(OneAndOne.required_salary.values,
         50,
         density=False,
         facecolor='r',
         alpha=0.75)
plt.xlim([0, 600])
plt.ylim([0, 22])
ax1.set_title('1+1 Condos', fontsize=18)

ax2 = plt.subplot(212)
plt.hist(TwoAndTwo.required_salary.values,
         50,
         density=False,
         facecolor='b',
         alpha=0.75)
plt.xlim([0, 600])
plt.ylim([0, 22])
ax2.set_title('2+2 Condos', fontsize=18)
ax2.set_xlabel('Required Yearly Salary [1000 $]', fontsize=18)

plt.tight_layout()



