#!/usr/bin/env python
"""Build functions you'll need to make a bunch of cool plots
"""


__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"


# Set up the imports to run the scrape.
import pandas as pd
import geopandas as gpd
import contextily as cx
import numpy as np
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing
from shapely.ops import unary_union
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from joblib import load
from itertools import compress
plt.ion()
plt.close('all')


def load_data(name_of_data):
    """
    Load a data set by name.

    :param name_of_data: Name of data set to load. 'slac', 'berkeley' or 'livermore'
    :return: GeoPandas dataframe containing housing data
    """
    dir_to_collate = '/Users/brendan/Documents/Coding/RedfinTravelTime/data/March 28 2022'
    if name_of_data == 'slac':
        print('Loading SLAC data...')
        dump_file_name = 'SFH_with_travel_time.h5'
        # Load the data frame
        df = pd.read_hdf(dir_to_collate + '/' + dump_file_name)
        # Select only single family homes
        df = df.loc[df['PROPERTY TYPE'] == 'Single Family Residential']
        df = df.loc[df['SALE TYPE'] == 'MLS Listing']
        # Convert pandas DataFrame to GeoPandas DataFrame
        gdf = convert_df_to_gdf(df)
    elif name_of_data == 'berkeley':
        print('Loading Berkeley data...')
        dump_file_name = 'SFH_with_travel_time_Berkeley.h5'
        df = pd.read_hdf(dir_to_collate + '/' + dump_file_name)
        df = df.loc[df['PROPERTY TYPE'] == 'Single Family Residential']
        df = df.loc[df['SALE TYPE'] == 'MLS Listing']
        # Convert pandas DataFrame to GeoPandas DataFrame
        gdf = convert_df_to_gdf(df)
        # Rename the columns to make the functions that operate on the data
        # less name dependent
        gdf = gdf.rename(columns={
            "travel_time_with_traffic_Berkeley_s": "travel_time_with_traffic_s",
            "travel_time_Berkeley_s": "travel_time_s"
        })
    elif name_of_data == 'livermore':
        print('Loading Livermore data...')
        dump_file_name = 'SFH_with_travel_time_Livermore.h5'
        df = pd.read_hdf(dir_to_collate + '/' + dump_file_name)
        df = df.loc[df['PROPERTY TYPE'] == 'Single Family Residential']
        df = df.loc[df['SALE TYPE'] == 'MLS Listing']
        # Convert pandas DataFrame to GeoPandas DataFrame
        gdf = convert_df_to_gdf(df)
        # Rename the columns to make the functions that operate on the data
        # less name dependent
        gdf = gdf.rename(columns={
            "travel_time_with_traffic_Livermore_s": "travel_time_with_traffic_s",
            "travel_time_Livermore_s": "travel_time_s"
        })
    else:
        print('Invalid data request. Valid names are "slac", "berkeley" or "livermore"')
        return
    return gdf


def load_gpr_and_scalers(data_name):
    """
    Automate the process of loading a save Gaussian Process Regression based on lab location.

    :param data_name: The name of the data you wish to load. 'slac', 'berkeley' or 'livermore'
    :return: GPR and scalers from SKlearn used to fit to a data set
    """
    dir_to_collate = '/Users/brendan/Documents/Coding/RedfinTravelTime/data/March 28 2022'
    try:
        gpr = load(dir_to_collate + '/' + data_name + '_gpr_march_28_2022.joblib')
        y_scaler = load(dir_to_collate + '/' + data_name + '_y_scaler_march_28_2022.joblib')
        x_scaler = load(dir_to_collate + '/' + data_name + '_x_scaler_march_28_2022.joblib')
    except FileNotFoundError:
        raise FileNotFoundError(data_name + " is not a valid GPR. Only 'slac', 'berkeley' and 'livermore' will work.")
    return gpr, x_scaler, y_scaler


def get_contour_verts(cn):
    """
    Take in the output from matplotlibs contour function and return the contours that
    it would plot. Matplotlib has a good function for finding contours, may as well
    use it.

    example:
    cn = plt.contour(lng_grid_in, lat_grid_in, y_grid_in, [time_to_contour_in])
    contours = get_contour_verts(cn)

    :param cn: The output from matplotlib's contour plot function
    :return: list of contours from the contour plot
    """
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


def load_county_shape_file():
    """
    Open the shape files for the Bay Area counties.
    I guess Santa Cruz isn't in the bay area?
    :return: GeoPandas dataframe with the county shape polygons
    """
    # Open the shape files for the Bay Area counties.
    shape_file = r'/Users/brendan/Documents/Coding/RedfinTravelTime/BayAreaCounties/geo_export_b749f330-e0bd-4f34-80b8-f9a7de8529af.shp'
    gdf = gpd.read_file(shape_file)  # Read file into a geodataframe
    gdf = gdf.to_crs(epsg=3857)
    gdf = gdf.set_index('county')

    # Add in Santa Cruz, which isn't the Bay Area because ???
    shape_file_SC = r'/Users/brendan/Documents/Coding/RedfinTravelTime/BayAreaCounties/SC_County_Boundary/County_Boundary.shp'
    gdf_SC = gpd.read_file(shape_file_SC)  # Read file into a geodataframe
    gdf_SC = gdf_SC.to_crs(epsg=3857)
    gdf_SC['county'] = 'Santa Cruz'
    gdf_SC['objectid'] = 10.0
    gdf_SC['fipsstco'] = '06087'
    gdf_SC = gdf_SC.drop(labels=['OBJECTID', 'County_Bdy', 'SHAPE_Leng', 'SHAPE_Area'], axis=1)
    gdf_SC = gdf_SC.set_index('county')
    gdf = gpd.GeoDataFrame( pd.concat([gdf, gdf_SC], ignore_index=False))
    gdf = gdf.set_crs(epsg=3857)
    return gdf


def convert_lat_lng_to_gdf(lng, lat):
    """
    This function takes in two lists/arrays of shape (n,1) or (n,) and returns
    a geopandas dataframe suitable for plotting those points on a Bay Area map
    :param lng: longitude (about -121)
    :param lat: latitude (about 37)
    :return: GeoPandas dataframe
    """
    data = {'LONGITUDE': lng,
            'LATITUDE': lat}
    df_h = pd.DataFrame(data)
    geometry = [Point(xy) for xy in zip(df_h['LONGITUDE'], df_h['LATITUDE'])]
    gdf_h = gpd.GeoDataFrame(df_h, geometry=geometry)
    gdf_h = gdf_h.set_crs(epsg=4326)
    gdf_h = gdf_h.to_crs(epsg=3857)
    return gdf_h


def convert_df_to_gdf(df_in):
    """
    This function converts a Pandas dataframe with latitude and longitude points into a
    GeoPandas dataframe with geomapping data
    :param df_in: Dataframe to convert to GeoPandas dataframe
    :return: GeoPandas dataframe
    """
    try:
        df_in['LONGITUDE']
    except KeyError:
        print('Dataframe does not have key (column) called "LONGITUDE"')

    try:
        df_in['LATITUDE']
    except KeyError:
        print('Dataframe does not have key (column) called "LATITUDE"')

    geometry = [Point(xy) for xy in zip(df_in['LONGITUDE'], df_in['LATITUDE'])]
    gdf_h = gpd.GeoDataFrame(df_in, geometry=geometry)
    gdf_h = gdf_h.set_crs(epsg=4326)
    gdf_h = gdf_h.to_crs(epsg=3857)
    return gdf_h


def plot_bay_area_map(fig_num, data_name):
    """
    Generate the base map for the bay area on which to plot things.
    :param fig_num: A figure number to create
    :param data_name: Name of image to build, 'slac, 'berkeley' or 'livermore'
    The image will be centered on one of these labs
    :return: figure, axes
    """
    # Load and plot the shape file for counties
    gdf = load_county_shape_file()
    plt.close(fig_num)  # Close the figure if it is open
    fig = plt.figure(fig_num, figsize=(7, 7))
    ax = fig.add_subplot(111)
    gdf.boundary.plot(ax=ax, edgecolor='blue', alpha=0.5)

    # Add and center map
    if data_name == 'slac':
        gdf_h = convert_lat_lng_to_gdf([-122.204204], [37.421317])
        gdf_h.plot(ax=ax, color='black', markersize=50, marker='*')
        x_range = 70000  # these are range in epsg = 3857
        y_range = 75000
    elif data_name == 'berkeley':
        gdf_h = convert_lat_lng_to_gdf([-122.25297158693019], [37.8752010509367])
        gdf_h.plot(ax=ax, color='black', markersize=50, marker='*')
        x_range = 30000
        y_range = 30000
    elif data_name == 'livermore':
        gdf_h = convert_lat_lng_to_gdf([-121.71852305292059], [37.689547127607895])
        gdf_h.plot(ax=ax, color='black', markersize=50, marker='*')
        x_range = 70000
        y_range = 75000
    else:
        raise NameError("data_name must be 'slac', 'berkeley' or 'livermore'")
    # Zoom in around the lab of interest
    ax.set_xlim(gdf_h.geometry[0].x-x_range, gdf_h.geometry[0].x+x_range)
    ax.set_ylim(gdf_h.geometry[0].y-y_range, gdf_h.geometry[0].y+y_range)

    # Add the map underneath
    cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
    return fig, ax


def plot_gpd_data_on_map(gdf_in, axes_in, color_in):
    """
    Plot longitude and latitude data from a GeoPandas data frame on a map of the Bay Area
    :param gdf_in: a GeoPandas DataFrame
    :param axes_in: The axes on which to plot
    :param color_in: The color to use for the markers
    :return: nothing
    """
    if type(gdf_in) != gpd.geodataframe.GeoDataFrame:
        raise TypeError("Input must be GeoPandas DataFrame")

    # Plot all houses
    gdf_in.plot(ax=axes_in, color=color_in, markersize=1)


def plot_gpd_boundary_on_map(gdf_in, axes_in, color_in):
    """
    Plot longitude and latitude data from a GeoPandas data frame on a map of the Bay Area
    :param gdf_in: a GeoPandas DataFrame
    :param axes_in: The axes on which to plot
    :param color_in: The color to use for the markers
    :return: nothing
    """
    if type(gdf_in) != gpd.geodataframe.GeoDataFrame:
        raise TypeError("Input must be GeoPandas DataFrame")

    # Plot all houses
    gdf_in.boundary.plot(ax=axes_in, color=color_in)


def plot_data_on_map(lng, lat, axes_in, color_in):
    """
    This function takes a series of latitude and longitude points and plots them on a map
    :param lng: longitude (about -121 in the bay area)
    :param lat: latitude (about 37 in the bay area)
    :param axes_in: The axes on which to plot
    :param color_in: The color to use for the markers
    :return: nothing
    """
    gdf_h = convert_lat_lng_to_gdf(lng, lat)

    # Plot all houses
    gdf_h.plot(ax=axes_in, color=color_in, markersize=1)


def generate_time_contour(gdf_in, time_to_contour_in):
    """
    This function takes in a GeoPandas datafile that contains LATITUDE, LONGITUDE and
    travel_time_with_traffic as well a time for which to draw a contour. For example, if the GDF contains
    "travel_time_with_traffic" to SLAC and 600.0 it will return contours that show the location
    where it would take 600 seconds to drive to SLAC.

    This function can be quite slow.

    :param gdf_in: GeoPandas data frame
    :param time_to_contour_in: drive time used to calculate the contour
    :return: The drive time contour.
    """
    if type(time_to_contour_in) != float:
        raise TypeError("'time_to_contour_in' must be of type float")

    # Build a grid to map the data to. This allows you to build better contours
    lng_min = gdf_in.LONGITUDE.min()
    lng_max = gdf_in.LONGITUDE.max()
    lat_min = gdf_in.LATITUDE.min()
    lat_max = gdf_in.LATITUDE.max()
    nx = 2 ** 12
    lng = np.linspace(lng_min, lng_max, nx)
    lat = np.linspace(lat_min, lat_max, nx)
    lng, lat = np.meshgrid(lng, lat)
    z = griddata((gdf_in['LONGITUDE'].values, gdf_in['LATITUDE'].values), gdf_in['travel_time_with_traffic_s'].values,
                 (lng, lat),
                 method='cubic')
    cn = plt.contour(lng, lat, z, [time_to_contour_in])
    contours = get_contour_verts(cn)
    return contours


def generate_grid_from_gpr(gdf_in, gpr_in, x_scaler_in, y_scaler_in, data_name):
    """
    Build a grid and use the Gaussian Process Regression(gpr) to calculate the drive time from locations on
    that grid. This process is slow, because the GPR is slow, so want to do it as few times as possible.
    :param gdf_in: GeoPandas dataframe with longitude and latitudes. (to be removed)
    :param gpr_in: Gaussian process regressor from Sklearn
    :param x_scaler_in: X scaling function from sklearn
    :param y_scaler_in: Y scaling function from sklearn
    :return:
    """
    if data_name == 'slac':
        lng_min = -122.204204 - 0.6288207
        lng_max = -122.204204 + 0.6288207
        lat_min = 37.421317 - 0.5369822
        lat_max = 37.421317 + 0.5369822
    elif data_name == 'berkeley':
        lng_min = -122.2529716 - 0.2694946
        lng_max = -122.2529716 + 0.2694946
        lat_min = 37.8752011 - 0.2130325
        lat_max = 37.8752011 + 0.2130325
    elif data_name == 'livermore':
        lng_min = -121.7185231 - 0.6288206
        lng_max = -121.7185231 + 0.6288206
        lat_min = 37.6895471 - 0.5350646
        lat_max = 37.6895471 + 0.5350646
    else:
        raise NameError("data_name must be 'slac', 'berkeley' or 'livermore'")
    # Build a grid to map the data to. This allows you to build better contours
    # lng_min = gdf_in.LONGITUDE.min()
    # lng_max = gdf_in.LONGITUDE.max()
    # lat_min = gdf_in.LATITUDE.min()
    # lat_max = gdf_in.LATITUDE.max()
    nx = 2 ** 8
    lng = np.linspace(lng_min, lng_max, nx)
    lat = np.linspace(lat_min, lat_max, nx)
    lng, lat = np.meshgrid(lng, lat)

    lng_t = lng.reshape(nx ** 2, )
    lat_t = lat.reshape(nx ** 2, )
    X_grid = np.vstack((lng_t, lat_t)).T

    X_grid_s = x_scaler_in.transform(X_grid)
    y_grid_s = gpr_in.predict(X_grid_s)
    y_grid = y_scaler_in.inverse_transform(y_grid_s.reshape(-1, 1))
    y_grid = y_grid.reshape(nx, nx)
    return lat, lng, y_grid


def plot_time_contours_on_map(contours_in, axes_in, color_in):
    """
    Take in a list of data points that form a contour and draw them on supplied axes using the
    defined color.
    :param contours_in: Output from function get_contour_verts()
    :param axes_in: A matplotlib axes
    :param color_in: A color to draw the contour. i.e. 'black' or 'red'
    :return: nothing
    """
    tours = [LinearRing(a) for a in contours_in[0]]
    QA = gpd.GeoDataFrame(geometry=tours)

    QA = QA.set_crs(epsg=4326)
    QA = QA.to_crs(epsg=3857)
    QA.plot(ax=axes_in, color=color_in, markersize=1)


def generate_time_contours_from_grid(lng_grid_in, lat_grid_in, y_grid_in, time_to_contour_in):
    """
    This function takes in a grid of LATITUDE, LONGITUDE and y_grid_in (traveltime) as well a time for which to
    draw a contour. For example, if y_grid_in is travel time to slac and lng_grid_in, lat_grid_in from a grid around
    slac then passing time_to_contour_in of 600 will return contours that show locations where it takes 600 seconds
    to drive to slac.

    To prevent shapes from running into the ocean, this function uses county shape files to ensure the boundaries are
    only inside counties.

    :param lng_grid_in: grid of longitude values, numpy array of shape (n, n)
    :param lat_grid_in: grid of latitude values, numpy array of shape (n, n)
    :param y_grid_in:  grid of values, numpy array of shape (n, n)
    :param time_to_contour_in: value in 'y_grid_in' to draw a contour, float
    :return: GeoPandasData frame that contains a polygon of the contour
    """
    # Generate contours using matplotlib
    cn = plt.contour(lng_grid_in, lat_grid_in, y_grid_in, [time_to_contour_in])
    # Extract the contours from the matplotlib data
    contours = get_contour_verts(cn)

    # Turn the current contours set into Linear Rings
    tours = [LinearRing(a) for a in contours[0]]
    # Turn the LinearRings into polygons and load into a dataframe with the correct crs
    # polys = Polygon(tours[0])
    polys = [Polygon(i) for i in tours]
    # Keep only polygons with area larger than 0.01
    keep = [(i.area > 0.01) for i in polys]
    polys = list(compress(polys, keep))
    poly_gdf = gpd.GeoDataFrame(geometry=polys)
    poly_gdf = poly_gdf.set_crs(epsg=4326)
    poly_gdf = poly_gdf.to_crs(epsg=3857)

    # Load the county shape files
    gdf_c = load_county_shape_file()
    # Find the intersection between the counties and time contour
    temp = gdf_c.overlay(poly_gdf, how='intersection')
    # Now sum up all the intersection geometries
    polys = unary_union(temp.geometry.values)
    gpd_out = gpd.GeoDataFrame(geometry=[polys])
    gpd_out = gpd_out.set_crs(epsg=3857)
    return gpd_out


def gdf_is_within_plot_area(gdf_in):
    """
    Not sure why I wrote this.

    :param gdf_in:
    :return:
    """
    p1 = Point(-13657004.05236116, 4421528.091647129)
    p2 = Point(-13657004.05236116, 4564154.684093618)
    p3 = Point(-13531957.676081037, 4564154.684093618)
    p4 = Point(-13531957.676081037, 4421528.091647129)
    pointlist = [p1, p2, p3, p4, p1]
    poly = Polygon([[p.x, p.y] for p in pointlist])
    poly_gdf = gpd.GeoDataFrame(geometry=[poly])
    poly_gdf = poly_gdf.set_crs(epsg=3857)
    return gdf_in[gdf_in.geometry.within(poly_gdf.geometry[0])]


def draw_circle():
    """
    function that draws a circle of latitude and longitudes
    :return: two arrays of length Np of latitude and longitudes.
    """
    radius = 0.26
    x0 = -122.180313
    y0 = 37.407815
    Np = 2**5
    th = np.linspace(0, 2*np.pi, Np)
    x = radius * np.cos(th)
    y = radius * np.sin(th)
    return (x+x0), (y+y0)


def draw_qualifying_area():
    """
    Draw the "qualifying area" for Stanford housing program
    :return: GeoPandas dataframe containing qualifying area polygon
    """
    lats = [37.329680, 37.194948, 37.351051, 37.469241, 37.836964, 37.790179, 37.539977]
    lons = [-122.422681, -121.942596, -121.930055, -122.073697, -122.420304, -122.566955, -122.585027]
    polygon_geom = Polygon(zip(lons, lats))

    # You need a circle too.
    [lons, lats] = draw_circle()
    circle_geom = Polygon(zip(lons, lats))

    # Draw a polygon to cut the circle.
    lats = [37.329680, 37.194948, 37.044851, 37.095961, ]
    lons = [-122.422681, -121.942596, -121.907589, -122.492529]
    cut_polygon = Polygon(zip(lons, lats))

    # Combine the first two
    temp = circle_geom.union(polygon_geom)
    # Find the overlap of the cut polygon with the union of the first two polygons
    temp2 = temp.intersection(cut_polygon)
    temp = temp.difference(temp2)

    # Build a geopandas dataframe out of the geometry for easy plotting
    QA = gpd.GeoDataFrame(geometry=[temp])
    QA = QA.set_crs(epsg=4326)
    QA = QA.to_crs(epsg=3857)
    return QA

