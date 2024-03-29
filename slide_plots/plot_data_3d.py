# A first crack at trying to plot cost of housing as a function of time. This will lead to re-doing a lot of methods
# that import/export data but I want to know how to do the analysis before deciding on data IO

import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')
from redfin_functions import *
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
plt.ion()
plt.close('all')

# ------------------------ DATA IMPORT -----------------------------
area_to_load = 'slac'
data_name_to_load = '02062022'
gdf = load_data_by_date(data_name_to_load)

# Cut out some outliers >$5M houses
gdf_t = gdf[gdf.PRICE < 5e6]
# gdf_t = gdf.iloc[1:10]

# # Cluster the data to make it easier to plot
# N = 2**8
# model = KMeans(n_clusters = N)
# AA = np.vstack((gdf_t['LONGITUDE'].values, gdf_t['LATITUDE'].values, gdf_t['PRICE'])).T
# model.fit(AA)
# BB = model.predict(AA)
#
# gdf_g = gdf_t.groupby(by=BB)
# kmeans_data = np.zeros((N,3))
#
# for i in range(N):
#     kmeans_data[i, 0] = gdf_g.get_group(i).LONGITUDE.mean()
#     kmeans_data[i, 1] = gdf_g.get_group(i).LATITUDE.mean()
#     kmeans_data[i, 2] = gdf_g.get_group(i).PRICE.mean()

# X = kmeans_data[:, 0]
# Y = kmeans_data[:, 1]
# B = np.zeros_like(X)
# T = kmeans_data[:, 2]
# width = depth = 1e-2

gdf_f = gdf_t.sample(frac=0.1)
X = gdf_f.LONGITUDE.values
Y = gdf_f.LATITUDE.values
B = np.zeros_like(X)
T = gdf_f.PRICE.values
width = depth = 1e-2

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(111, projection='3d')
ax1.bar3d(X, Y, B, width, depth, T)


# # ------------------------ FIND HOUSES INSIDE SAN MATEO -----------------------------
# # Load the county shapes
# gdf_c = load_county_shape_file()
#
# # Extract only houses in San Mateo
# SM = gdf[gdf.geometry.within(gdf_c.loc['San Mateo'].geometry)]
# fig1, ax1 = plot_bay_area_map(1234, area_to_load)  # generate a bay area map
# plot_gpd_data_on_map(SM, ax1, 'red')  # Plot the housing data on it.
#
# for index, row in gdf_c.iterrows():
#     temp = gdf[gdf.geometry.within(gdf_c.loc[index].geometry)]
#     print("Median home price in " + index + " is $" + str(temp.PRICE.median()))
#
# # ------------------- FIND HOUSES INSIDE 27.6 MINUTE DRIVE --------------------------
# # load the GPR to build the contour
# gpr, x_scaler, y_scaler = load_gpr_and_scalers(area_to_load)
# print('Generating grid to make contours with')
# lat_grid, lng_grid, y_grid = generate_grid_from_gpr(gdf, gpr, x_scaler, y_scaler, area_to_load)
# print('Generating contours')
# time_to_contour = 60.0*27.6
# gpd_cont = generate_time_contours_from_grid(lng_grid, lat_grid, y_grid, time_to_contour)
#
# in_boundary = gdf[gdf.geometry.within(gpd_cont.geometry[0])]
#
# fig1, ax1 = plot_bay_area_map(1234, area_to_load)  # generate a bay area map
# plot_gpd_boundary_on_map(gpd_cont, ax1, 'black')
# plot_gpd_data_on_map(in_boundary, ax1, 'red')  # Plot the housing data on it.

