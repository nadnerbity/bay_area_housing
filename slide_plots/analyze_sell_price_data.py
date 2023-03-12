# Plot houses that 2x SLAC associate staff scientist can afford


from scipy.optimize import fsolve
from mortgage_calcs import *
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')
from redfin_functions import *

plt.ion()
plt.close('all')

dir_to_data = '/Users/brendan/Documents/Coding/RedfinTravelTime/data/stanford_circle_redfin_2023-02-16-06-22-33.csv'
df = pd.read_csv(dir_to_data)
# Select only single family homes
df = df.loc[df['PROPERTY TYPE'] == 'Single Family Residential']
df = df.loc[df['SALE TYPE'] == 'MLS Listing']
# Convert pandas DataFrame to GeoPandas DataFrame
gdf = convert_df_to_gdf(df)
gdf = gdf.rename(columns={'HOA/MONTH': 'HOAperMonth'})
gdf = gdf.rename(columns={'DAYS ON MARKET': 'DaysOnMarket'})



# scale_value = 1e6
# plt.close(3457)
# plt.figure(3457)
# ax1 = plt.subplot(211)
# plt.hist(in_bdy_28032022.required_salary.values,
#          50,
#          density=False,
#          facecolor='r',
#          alpha=0.75)
# plt.xlim([0, 600])
# plt.ylim([0, 22])
# ax1.set_title('March 28th 2022', fontsize=18)
#
# ax2 = plt.subplot(212)
# plt.hist(in_bdy_28112022.required_salary.values,
#          50,
#          density=False,
#          facecolor='b',
#          alpha=0.75)
# plt.xlim([0, 600])
# plt.ylim([0, 22])
# ax2.set_title('November 28th 2022', fontsize=18)
# ax2.set_xlabel('Required Yearly Salary [1000 $]', fontsize=18)
#
# plt.tight_layout()
#
#
# plt.figure(34)
# plt.plot(in_bdy_28112022.PRICE, in_bdy_28112022.DaysOnMarket, 'bo')
# plt.xlabel('Price [$]', fontsize=18)
# plt.ylabel('Days On Market [Days]', fontsize=18)
#
# temp = in_bdy_28112022[in_bdy_28112022['DaysOnMarket'] <= 200]
#
# plt.figure(45)
# plt.hist(temp.DaysOnMarket,
#          40,
#          density=False,
#          facecolor='b',
#          alpha=0.75)
# plt.xlabel('Days On Market [Days]', fontsize=18)
# plt.ylabel('Count [1]', fontsize=18)
# plt.tight_layout()
