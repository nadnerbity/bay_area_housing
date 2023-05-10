#!/usr/bin/env python
"""Loop through all the saved redfin data, perform some simple additions and save
the data as one file.
"""

# Version 0.0: Original version from 2019
# Version 0.1: Re-written 3 years later to switch to Redfin which has a more permissive API


__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"


# Set up the imports to run the scrape.
import pandas as pd
import numpy as np
import time
import datetime
import os

daymonyear = '17042023'
dir_to_collate = '/Users/brendan/Documents/Coding/RedfinTravelTime/data/' + daymonyear
dump_file_name = daymonyear + '.h5'

# List files in the directory of interest
files = os.listdir(dir_to_collate)
# Build a list of only files that end in 'csv', it is ~*~pythonic~*~
files = [k for k in files if (k[-3:] == 'csv')]

# Load all the data into a dataframe
df = pd.read_csv(dir_to_collate + '/' + files[0])
for k in range(1, len(files)):
    df = pd.concat([df, pd.read_csv(dir_to_collate + '/' + files[k])], ignore_index=True)

# Split off the redfin ID
f = lambda x: x.split('/')[-1]
df['redfin_id'] = df['URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON ' \
                     'PRICING)'].apply(f)

# Add in a column for the date this analysis occurred
df['date_created'] = datetime.datetime.now()

# Save the data to an hdf5 file.
df.to_hdf(dir_to_collate + '/' + dump_file_name, key='df', mode='w')
