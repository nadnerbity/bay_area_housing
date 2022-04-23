#!/usr/bin/env python
"""Fit the travel time data using Gaussian Process Regression
"""


__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"


# Set up the imports to run the scrape.
import pandas as pd
import geopandas as gpd
import contextily as cx
from shapely.geometry import Point
from shapely.geometry import Polygon
from joblib import dump, load
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')
from redfin_functions import *
# import matplotlib.pyplot as plt
plt.ion()
plt.close('all')


def get_contour_verts(cn):
    contours = []
    # for each contour line
    for cc in cn.collections:
        paths = []
        # for each separate section of the contour line
        for pp in cc.get_paths():
            xy = []
            # for each segment of that section
            for vv in pp.iter_segments():
                xy.append(vv[0])
            paths.append(np.vstack(xy))
        contours.append(paths)

    return contours


def plot_data_on_map(LNG, LAT):
    data = {'LONGITUDE': LNG,
            'LATITUDE': LAT}
    df_h = pd.DataFrame(data)
    geometry = [Point(xy) for xy in zip(df_h['LONGITUDE'], df_h['LATITUDE'])]
    gdf_h = gpd.GeoDataFrame(df_h, geometry=geometry)
    gdf_h = gdf_h.set_crs(epsg=4326)
    gdf_h = gdf_h.to_crs(epsg=3857)

    shape_file = r'BayAreaCounties/geo_export_b749f330-e0bd-4f34-80b8-f9a7de8529af.shp'
    gdf = gpd.read_file(shape_file)  # Read file into a geodataframe
    gdf = gdf.to_crs(epsg=3857)
    gdf = gdf.set_index('county')

    fig, ax = plt.subplots(1, figsize=(7, 7))
    gdf.boundary.plot(ax=ax, edgecolor='blue', alpha=0.5)

    # Plot all houses
    gdf_h.plot(ax=ax, color='red', markersize=1)


# ------------------------ DATA IMPORT AND EXPORT -----------------------------
dir_to_collate = '/Users/brendan/Documents/Coding/RedfinTravelTime/data/March 28 2022'
# Load the data frame
lab_name = 'livermore'
gdf = load_data(lab_name)


gpr_dump_name = lab_name + '_gpr_march_28_2022.joblib'
y_scaler_dump_name = lab_name + '_y_scaler_march_28_2022.joblib'
x_scaler_dump_name = lab_name + '_x_scaler_march_28_2022.joblib'


# # Turn the data into np.arrays that are easier to handle instead of
# # typing the dataframe names over and over.
X = gdf[['LONGITUDE', 'LATITUDE']].values
Y = gdf['travel_time_with_traffic_s'].values
print('Fitting the 2D GP model...')

# Scale the data
x_scaler = StandardScaler()
y_scaler = StandardScaler()
X_s = x_scaler.fit_transform(X)
Y_s = y_scaler.fit_transform(Y.reshape(-1, 1)).reshape(len(Y),)
X_train, X_test, Y_train, Y_test = train_test_split(X_s, Y_s, test_size=0.2, random_state=42)

# Specify the kernel
kernel = C(np.mean(np.abs(Y_train))) + RBF((0.221, 0.137), (1e-5, 1e+2)) \
             + WhiteKernel(1.0, noise_level_bounds=(1e-10, 1e+0))
# kernel = DotProduct() + WhiteKernel()

gpr = GaussianProcessRegressor(kernel=kernel,
                               alpha=0.000433,
                               n_restarts_optimizer=1)

# Fit the known data
gpr.fit(X_train, Y_train)  # This takes about 5 minutes.

#  Save the fit GPR
print('Saving the GP model to ' + gpr_dump_name)
dump(gpr, dir_to_collate + '/' + gpr_dump_name)
dump(y_scaler, dir_to_collate + '/' + y_scaler_dump_name)
dump(x_scaler, dir_to_collate + '/' + x_scaler_dump_name)

# ------------------------ PLOTS -----------------------------
y_pred = gpr.predict(X_test)
plt.close(1)
plt.figure(1, facecolor='w')
plt.plot(Y_test, y_pred, '.')
plt.xlim([0, max(y_pred.max(), Y_test.max())])
plt.ylim([0, max(y_pred.max(), Y_test.max())])

