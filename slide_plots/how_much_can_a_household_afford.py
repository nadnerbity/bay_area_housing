# Calculate how much a household can afford


from mortgage_calcs import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import sys
sys.path.insert(1, '/Users/brendan/Documents/Coding/RedfinTravelTime')

plt.ion()
plt.close('all')


def monthly_payment(p0, r, n):
    return r*p0 / (1-(1+r)**(-n))


def principal_to_income(r, n):
    return (1-(1+r)**-n)/40/r


# ------------------------ COST VS INTEREST -----------------------------
nx = 2**4
interest_rate = np.linspace(0.01, 0.10, nx)


# ------------------------ HOME PRICE VS SALARY -----------------------------
nx = 2**5
yearly_salary = np.linspace(100000.0, 600000.0, nx)

# Calculate what can a given salary can afford at 3% interest
home_value_3 = [fsolve(how_much_can_afford, [3*g], args=(g, 0, 0.03/12, 0.0115/12, 0.01/12))[0]/1000 for g in
                yearly_salary]
home_value_3 = np.array(home_value_3)

# Calculate what can a given salary can afford at 5% interest
home_value_5 = np.array([fsolve(how_much_can_afford, [3*g], args=(g, 0, 0.05/12, 0.0115/12, 0.01/12))[0]/1000 for
                        g in yearly_salary])

# Calculate what can a given salary can afford at 7% interest
home_value_7 = np.array([fsolve(how_much_can_afford, [3*g], args=(g, 0, 0.07/12, 0.0115/12, 0.01/12))[0]/1000 for
                        g in yearly_salary])

# ------------------------ PLOTS -----------------------------
# Plot monthly cost and required yearly interest rate VS income
after_DP = 0.8
plt.close(456)
fig = plt.figure(456)
ax1 = fig.add_subplot(111)
ax1.plot(100*interest_rate, monthly_payment(after_DP*1825000, interest_rate/12, 360), 'k',
         linestyle="dashdot")
ax1.plot(100*interest_rate, monthly_payment(after_DP*2388000, interest_rate/12, 360), 'k--')
ax1.plot(100*interest_rate, monthly_payment(after_DP*2750000, interest_rate/12, 360), 'k-')
plt.axvline(x=6.35, color='r')
ax1.set_xlabel('Yearly Interest Rate [%]', fontsize=20)
ax1.set_ylabel('Monthly Payment [$]', fontsize=20)
ax1.legend(['$1.83 Million - Santa Clara', '$2.39 Million - San Mateo', '$2.75 Million - SLAC'])
ax1.text(6.5, 6000, 'Current Interest \n Rate + Taxes',
         color='red',
         fontsize=15)

limits = ax1.get_ylim()
ax2 = ax1.twinx()
ax2.plot(100*interest_rate, (40/1000)*monthly_payment(after_DP*2750000, interest_rate/12, 360), 'k-')
ax2.set_ylabel('Yearly Income [1000 $]', fontsize=20)
ax2.set_ylim(limits[0]*40/1000, limits[1]*40/1000)

plt.tight_layout()

fig = plt.figure(457)
ax1 = fig.add_subplot(111)
ax1.plot(yearly_salary/1000, home_value_3 + 100, 'k-')
ax1.plot(yearly_salary/1000, home_value_5 + 100, 'k--')
ax1.plot(yearly_salary/1000, home_value_7 + 100, 'k', linestyle='dashdot')
ax1.set_xlabel('Household Yearly Salary [1000 $]', fontsize=20)
ax1.set_ylabel('Maximum House Price [1000 $]', fontsize=18)
ax1.legend(['3% Interest Rate', '5%', '7%'], loc='lower right')
# Add in slac salaries
plt.axhline(y=1825, color='r')  # Santa Clara
ax1.text(100, 1825+25, 'Santa Clara', color='red', fontsize=15)
plt.axhline(y=2388, color='r')  # San Mateo
ax1.text(100, 2388+25, 'San Mateo', color='red', fontsize=15)
plt.axhline(y=2750, color='r')  # Near SLAC
ax1.text(100, 2750+25, 'Near SLAC', color='red', fontsize=15)


plt.tight_layout()
