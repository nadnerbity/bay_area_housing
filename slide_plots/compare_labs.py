# Compare the travel times for different labs

import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')
from redfin_functions import *
from mortgage_calcs import *
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
plt.ion()
plt.close('all')

# Load the shape files for travel time
travelTimeShape = load_travel_time_shapes()

# Encode the location in the traveltime shapes to make them selectable by number. There has to be a better way to do
# this.
lab = ['slac', 'berkeley', 'livermore', 'fermilab', 'argonne']
N = [2, 8, 1, 3, 6]
NN = 4

fig1, ax1 = plot_bay_area_map(1234, lab[NN])
plot_gpd_boundary_on_map(travelTimeShape.iloc[[N[NN]]], ax1, 'black')

dateToLoad = '17042023'
gdf = load_data_by_date(dateToLoad)
# Select only single family homes
gdf = gdf.loc[gdf['PROPERTY TYPE'] == 'Single Family Residential']
gdf = gdf.loc[gdf['SALE TYPE'] == 'MLS Listing']
# Remove <=2 bedroom listings, these aren't family friendly
gdf = gdf.loc[gdf['BEDS'] > 2.0]
# Remove <=1 bathroom listings, these aren't family friendly
gdf = gdf.loc[gdf['BATHS'] > 1.0]
gdf = gdf.loc[gdf['PRICE'] < 6000000]

# Plot the data!
plot_gpd_data_on_map(gdf, ax1, 'blue')

# Split out only the houses inside the travel time boundary
inside = gdf[gdf.geometry.within(travelTimeShape.iloc[N[NN]].geometry)]

a = lambda y: fsolve(salary_needed_for_given_house_price, [450000],
                     args=(y.PRICE, y.PRICE*0.2, 0.07/12, 0.025/12, 0.01/12, 0))[0] / 1000

inside['required_salary'] = inside.apply(a, axis=1)
inside = inside.sort_values('required_salary')
plot_gpd_data_on_map(inside, ax1, 'red')
ax1.set_title(lab[NN] + ' date:' + dateToLoad, fontsize=20)

plt.close(37)
plt.figure(37)
ax1 = plt.subplot(211)
plt.hist(inside.PRICE.values/1e6,
         50,
         density=False,
         facecolor='b',
         alpha=0.75)
plt.xlabel('Price [$M]', fontsize=20)
plt.ylabel('N [1]', fontsize=20)
plt.xlim([0, 3.0])

ax2 = plt.subplot(212)
plt.hist(inside.required_salary.values,
         50,
         density=False,
         facecolor='b',
         alpha=0.75)
plt.xlabel('Required Yearly Salary [$k]', fontsize=20)
plt.ylabel('N [1]', fontsize=20)
plt.xlim([0, 800])
plt.tight_layout()


correlation = "{:.4f}".format(inside['PRICE'].corr(inside['DaysOnMarket']))
plt.close(567)
plt.figure(567)
plt.scatter(inside.DaysOnMarket, inside.PRICE)
plt.xlim([0, 45])
plt.xlabel('Days on Market [days]', fontsize=18)
plt.ylabel('Price [$]', fontsize=18)
plt.title('Correlation: ' + correlation, fontsize=18)
plt.tight_layout()

