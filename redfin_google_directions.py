#!/usr/bin/env python
"""Use the google map API to turn longitude and latitude data
into travel times to SLAC
"""


__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"


# Set up the imports to run the scrape.
import pandas as pd
import numpy as np
import googlemaps
from datetime import datetime
from datetime import timezone
import pytz
import matplotlib.pyplot as plt
from tqdm import tqdm
plt.ion()
plt.close('all')


def get_drive_time(origin_in, destination_in, depart_time_in):
    """
    Query the google maps api for drive times in traffic.

    :param origin_in: origin latitude and longitude coordinates e.g. '37.5,-122.2'

    :param destination_in: destination latitude and longitude coordinates e.g. '37.5,-122.2'

    :param depart_time_in: time (in the future) to get directions
    This is 'epoch time' which is integer seconds since midnight 1/1/1970 UTC.
    Datetime can be used to convert from a date and time in a timezone to epoch time:
    depart_time = int(datetime(2022, 4, 20, 8, 0, 0).astimezone(pytz.timezone("America/Los_Angeles")).timestamp())

    :return a: The distance traveled in meters
    :return b: The travel time without traffic, in seconds
    :return c: The travel time with traffic, in seconds
    :return directions: The complete google API output, for testing purposes
    """
    directions = gmaps.directions(origin=origin_in,
                                  destination=destination_in,
                                  mode="driving",
                                  departure_time=depart_time_in,
                                  traffic_model="best_guess")
    # I'm going to spell out exactly what I'm extracting
    try:
        aa = directions[0]['legs'][0]['distance']['value']  # Distance traveled in meters
    except:
        aa = np.nan

    try:
        bb = directions[0]['legs'][0]['duration']['value']  # Travel time in seconds
    except:
        bb = np.nan

    try:
        cc = directions[0]['legs'][0]['duration_in_traffic']['value']  # Travel time in traffic in seconds
    except:
        cc = np.nan

    return aa, bb, cc


def convert_epoch_to_ca(epoch_time):
    """
    Converts from epoch time, seconds since 1/1/1970 UTC to a datetime element in California time.
    :param epoch_time: time in seconds since 1/1/1970 UTC, converts to int
    :return: datetime element with timezone info for 'America/Los_Angeles'
    """
    return datetime.fromtimestamp(int(epoch_time)).astimezone(pytz.timezone("America/Los_Angeles"))


def convert_ca_to_epoch(ca_datetime):
    """
    Takes a naive datetime element, assumes it is California time, and converts that to epoch time.
    :param ca_datetime: datetime object for date+time, assumed to be in california
    :return: integer seconds since midnight 1/1/1970 UTC
    """
    if type(ca_datetime) != datetime:
        raise TypeError("Input time must be of type datetime")
    return int(datetime(2022, 4, 20, 7, 45, 0).astimezone(pytz.timezone("America/Los_Angeles")).timestamp())


# Create new `pandas` methods which use `tqdm` progress
# (can use tqdm_gui, optional kwargs, etc.)
tqdm.pandas()

# ------------------------ SETUP THE GMAP API -----------------------------
api_file = '/Users/brendan/Documents/Coding/RedfinTravelTime/google_api/google_api_key.txt'
api_key = open(api_file).read()
gmaps = googlemaps.Client(key=api_key, queries_per_second=10)
slac_latlng = '37.421317,-122.204204'
livermore_latlng = '37.689547127607895,-121.71852305292059'
berkeley_latlng = '37.8752010509367,-122.25297158693019'
home_latlng = '37.395723,-122.012859'
hayward_latlng = '37.628641,-122.072809'

# ------------------------ DATA IMPORT -----------------------------
dir_to_collate = '/Users/brendan/Documents/Coding/RedfinTravelTime/data/March 28 2022'
read_file_name = 'all_data.h5'
dump_file_name = 'SFH_with_travel_time_Berkeley.h5'

# Load a data frame
print("Loading and setting up dataframe...")
df = pd.read_hdf(dir_to_collate + '/' + read_file_name)
# Select only single family homes
df = df.loc[df['PROPERTY TYPE'] == 'Single Family Residential']
df = df.loc[df['SALE TYPE'] == 'MLS Listing']
# Combine the lat and long into a string that google maps API can use
df['google_loc'] = df.apply(lambda x: str(x.LATITUDE)+','+str(x.LONGITUDE), axis=1)
df = df.reset_index()
# Create columns to add data to
df['distance_Berkeley_m'] = ""
df['travel_time_Berkeley_s'] = ""
df['travel_time_with_traffic_Berkeley_s'] = ""

# ------------------------ TEST AN API CALL -----------------------------
# ------------------------ DRIVING -----------------------------
# Request driving directions
# Simple example
# Convert Wednesday April 6th 2022 at 8 AM Pacific to unix epoch time
# time_to_depart = int(datetime(2022, 4, 20, 8, 0, 0).astimezone(pytz.timezone("America/Los_Angeles")).timestamp())
# a, b, c, directions_result = get_drive_time(home_latlng, slac_latlng, time_to_depart)
print("Calling google maps API and processing %5i entries" % df.shape[0])
depart_datetime = datetime(2022, 4, 20, 7, 45, 0)
depart_time = convert_ca_to_epoch(depart_datetime)
df[['distance_Berkeley_m', 'travel_time_Berkeley_s', 'travel_time_with_traffic_Berkeley_s']] = \
    df.progress_apply(lambda x: get_drive_time(x.google_loc, berkeley_latlng, depart_time), axis=1,
                      result_type='expand')

# Save the data to an hdf5 file.
print("Saving dataframe...")
# Add on when the travel time was checked and for what day the travel time was checked
df['date_travel_time_added'] = datetime.now()
df['travel_time_start_time'] = depart_datetime
df.to_hdf(dir_to_collate + '/' + dump_file_name, key='df', mode='w')



