# Compare the travel times for different labs
# This file plots how much down payment assistance is required to get various incomes into housing around SLAC

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
lab = ['slac', 'berkeley', 'livermore', 'fermilab', 'argonne', 'slac']
N = [2, 8, 1, 3, 6, 10]
NN = 0
dateToLoad = '17042023'
# dateToLoad = '28032022'

# Load the travel time shape
# fig1, ax1 = plot_bay_area_map(1234, lab[NN])
# plot_gpd_boundary_on_map(travelTimeShape.iloc[[N[NN]]], ax1, 'black')

NN = 7
fig1, ax1 = plot_bay_area_map(1234, travelTimeShape.iloc[NN].id)
plot_gpd_boundary_on_map(travelTimeShape.iloc[[NN]], ax1, 'black')

# Load the housing data
gdf = load_data_by_date(dateToLoad)
# Select only single family homes
gdf = gdf.loc[gdf['PROPERTY TYPE'] == 'Single Family Residential']
gdf = gdf.loc[gdf['SALE TYPE'] == 'MLS Listing']
# Remove <=2 bedroom listings, these aren't family friendly
gdf = gdf.loc[gdf['BEDS'] > 2.0]
# Remove <=1 bathroom listings, these aren't family friendly
gdf = gdf.loc[gdf['BATHS'] > 1.0]
gdf = gdf.loc[gdf['PRICE'] < 6000000]



# Split out only the houses inside the travel time boundary
inside = gdf[gdf.geometry.within(travelTimeShape.iloc[NN].geometry)]

# Plot the data!
plot_gpd_data_on_map(gdf, ax1, 'blue')
# Plot the data!
plot_gpd_data_on_map(inside, ax1, 'red')

# Apply the function that calcs how much household income is required to pay for a house and not be cost of housing
# burdened.

M = 2**6
salaries = np.linspace(50000, 750000, M)




dp = lambda s: fsolve(how_much_can_afford, [3*s],
                     args=(s, 1.0, 0.03/12, 0.01/12, 0.01/12))[0] / 1000
A = [dp(b) for b in salaries]

inside = inside.sort_values('PRICE')

p_1 = inside.iloc[0].PRICE
p_25th = inside.iloc[int(len(inside)/4)].PRICE
slac_median = inside.PRICE.median()

plt.close(673)
plt.figure(673, figsize=(10,6))
plt.plot(salaries/1000, [i if (i>0) else 0 for i in (p_1/1000 - A)], 'k')
plt.plot(salaries/1000, [i if (i>0) else 0 for i in (p_25th/1000 - A)], 'r')
plt.plot(salaries/1000, [i if (i>0) else 0 for i in (slac_median/1000 - A)], 'b')
plt.xlabel('Household Salary [1000s $]', fontsize=20)
plt.ylabel('Down Payment [1000s $]', fontsize=20)
plt.title('Down Payment Necessary to be Affordable', fontsize=20)
plt.legend(('SLAC Cheapest: $' + str(p_1),
            '25th Percentile: $' + str(p_25th),
            'SLAC Median: $' + str(slac_median)),
           fontsize=18)
plt.tight_layout()


# Stuff I probably don't need but hate to delete. I guess I should rely on git?
# downpayment_help_needed_for_given_salary_and_home_price(800000, 1000000, 100000, 0.02/12, 0.01/12, 0.01/12, 0)
# Will return the
# dp = lambda y, z: fsolve(downpayment_help_needed_for_given_salary_and_home_price, [10000],
#                      args=(y, z, 0.07/12, 0.01/12, 0.01/12, 0))[0] / 1000

# def dp_help_by_price(sals, price):
#     # A = [dp(price, b) for b in sals]
#     A = [dp(b) for b in sals]
#     # A = [c if (c < price/1000) else price/1000 for c in A] #cute
#     for i in range(len(A)):
#         if A[i] < 0:
#             A[i] = 0
#         elif A[i] > price/1000:
#             A[i] = price/1000
#         else:
#             A[i] = A[i]
#     return A

# dp_help_25percentile = dp_help_by_price(salaries, p_25th)
# dp_help_SLAC_median = dp_help_by_price(salaries, slac_median)

