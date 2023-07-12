#!/usr/bin/env python
"""Build functions you'll need to calculate quantities associated with a mortgage
"""

__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

import numpy as np
from scipy.optimize import fsolve


def principal_to_income(r, n):
    return (1 - (1 + r) ** -n) / 40 / r


def monthly_payment(r=(0.04 / 12.0), p=1000000.0, n=360.0):
    """
    A function to calculate the monthly payment for a loan.

    :param r: interest rate per N
    :param p: initial loan value
    :param n: total number of payments
    """
    return (r * p) / (1.0 - (1.0 + r) ** (-n))


def interest_paid_by_month(i=1, r=(0.04 / 12.0), p=1000000.0, n=360.0):
    """
    A function to calculate the interest paid on payment i.
    i.e. how much of the ith payment is interest

    :param i: payment number
    :param r: interest rate per N
    :param p: initial loan value
    :param n: total number of payments
    """
    c = monthly_payment(r, p, n)
    return (p * r - c) * (1 + r) ** (i - 1) + c


def principal_paid_by_month(i=1, r=(0.04 / 12.0), p=1000000.0, n=360.0):
    """
    A function to calculate the principal paid on payment i.
    i.e. how much of the ith payment is principal

    :param i: payment number
    :param r: interest rate per N
    :param p: initial loan value
    :param n: total number of payments
    """
    c = monthly_payment(r, p, n)
    return (c - p * r) * (1 + r) ** (i - 1)


def total_principal_paid(i=1, r=(0.04 / 12.0), p=1000000.0, n=360.0):
    """
    A function to calculate the total principal paid after payment i

    :param i: number of payments made
    :param r: interest rate per N
    :param p: initial loan value
    :param n: total number of payments
    """
    c = monthly_payment(r, p, n)
    return (c - p * r) * ((1 + r) ** i - 1) / r


def total_interest_paid(i=1, r=(0.04 / 12.0), p=1000000.0, n=360.0):
    """
    A function to calculate the total principal paid after payment i

    :param i: number of payments made
    :param r: interest rate per N
    :param p: initial loan value
    :param n: total number of payments
    """
    c = monthly_payment(r, p, n)
    return (p * r - c) * ((1 + r) ** i - 1) / r + i * c


def net_after_selling(i=1, r=(0.04 / 12.0), p=1000000.0, n=360.0, ps=1000000.0, rt=(0.0115 / 12)):
    """
    A function to calculate the net to the owner after selling a home at price ps.
    Assumes 20% down.
    Assumes 3% paid to buy and 3% paid to sell
    Assumes 1% property taxes per year
    Assumes 1% to maintain per year

    :param i: number of payments made before selling
    :param r: interest rate per N (usually per month)
    :param p: initial purchase price
    :param n: total number of payments
    :param ps: sale price
    :param rt: monthly tax rate
    """
    # Split the calculation up to describe the terms
    temp = 1.00 * ps  # 0% of the sale price goes to a realtor
    temp = temp - 0.80 * p + total_principal_paid(i, r, 0.8 * p,
                                                  n)  # Subtract off the loan amount, add in principal paid
    temp = temp - 0.03 * p  # Buyer paid 3% to a realtor
    temp = temp - i * rt * p  # Property taxes
    temp = temp - i * 0.01 / 12.0 * p  # Maintenance

    # return 0.97*ps - (0.8*p - total_principal_paid(i, r, p, n)) - 0.03*p - i*0.01/12.0*p - i*0.01/12.0*p
    return temp


def net_after_selling_landed(i=1,
                             r=(0.04 / 12.0),
                             pi=1000000.0,
                             n=360.0,
                             ps=1000000.0,
                             rt=(0.0115 / 12),
                             d=50000.0,
                             dl=50000.0):
    """
    A function to calculate the net to the owner after selling a home at price ps after i payments.
    Assumes 0% paid to buy and 0% paid to sell
    Assumes 1% to maintain per year

    :param i: number of payments made before selling
    :param r: interest rate per N (usually per month)
    :param pi: initial purchase price
    :param n: total number of payments
    :param ps: sale price
    :param rt: monthly tax rate
    :param d: down payment from person
    :param dl: down payment from landed
    returns: Net to homeowner, total principal paid, total taxes paid
    """
    # Split the calculation up to describe the terms
    temp = 1.00 * ps  # 0% of the sale price goes to a realtor
    temp = temp - (pi - d - dl)  # Subtract off the initial loan amount, less down payments
    princ_paid = total_principal_paid(i, r, (pi - d - dl), n)
    temp = temp + princ_paid  # Add back in the principal paid
    temp = temp - 0.00 * pi  # Buyer paid 0% to a realtor
    temp = temp - i * rt * pi  # Subtract off the amount paid in property taxes
    temp = temp - i * 0.00 / 12.0 * pi  # Maintenance
    paid_to_landed = dl * (1 + 2.5 * (ps - pi) / pi)
    temp = temp - paid_to_landed  # Landed's cut, including getting their down payment back

    return temp, princ_paid, i * rt * pi, paid_to_landed


def calc_rate_of_return(p=1000000.0, ps=1100000.0, n=12.0):
    """
    Calculate the average rate of return over n intervals

    :param p: initial purchase price
    :param ps: sale price
    :param n: total number of intervals (years, months)
    """
    return np.exp(np.log(ps / p) / n) - 1


def calc_sale_price(p=1000000.0, n=12.0, a=0.02):
    """
    Calculate the sale price given n instances of growth a.
    A property that appreciates 1% a year and sold after 10 years would use
    n = 10, a = 0.01

    :param p: initial purchase price
    :param n: total number of intervals (years, months)
    :param a: price change rate per n
    """
    return p * (1 + a) ** n


def calc_taxes_on_income(s):
    if s <= 19900.0:
        t = 0.1 * s
    elif 19900.0 < s <= 81050.0:
        t = 1990.0 + 0.12 * (s - 19990.0)
    elif 81050 < s <= 172750.0:
        t = 9328.0 + 0.22 * (s - 81050.0)
    elif 172750 < s <= 329850.0:
        t = 29502.0 + 0.24 * (s - 172750.0)
    elif 329850 < s <= 418850.0:
        t = 67206.0 + 0.32 * (s - 329850.0)
    elif 418850 < s <= 628300.0:
        t = 95686.0 + 0.35 * (s - 418850.0)
    elif 628300 < s:
        t = 168993.50 + 0.37 * (s - 628300.0)
    else:
        t = 0

    return t


def standard_deduction_or_mid(ss, pp, rr):
    """
    This function returns how much money married, filing jointly can recoup when using mortgage interest deduction
    on their Federal taxes.
    :param ss: Yearly income
    :param pp: Principal on mortgage
    :param rr: Monthly interest rate
    :return: amount of money saved if mortgage interest deduction is worth it, 0 if it isn't
    """
    # Calculate the interest paid in the first year.
    if pp > 750000:
        interest_paid = total_interest_paid(i=12, r=rr, p=750000, n=360.0)
    else:
        interest_paid = total_interest_paid(i=12, r=rr, p=pp, n=360.0)
    # print('Interest paid is : ', str(interest_paid))

    # Calculate Federal taxes when taking the standard deduction
    sd = calc_taxes_on_income(ss - 25100)
    # print('Taxes when taking SD : ', str(sd))

    # Calculate Federal taxes when taking the mortgage interest deduction
    mid = calc_taxes_on_income(ss - interest_paid)
    # print('Taxes when taking MID : ', str(mid))

    if interest_paid > 25100:
        return sd - mid
    else:
        return 0


def how_much_can_afford(x, s, d, r, rt, rm):
    """
    Function used to solve for how much a family can afford based on their income. This function is used with an
    optimizer.
    It starts with HUD defined maximum housing costs (30% salary before taxes) and adds in any money that might come
    from using the mortgage interest deduction and subtracts off the cost of the mortgage, taxes and maintenance.
    Thus, if it returns 0 the household is paying exactly 30% of their before tax income on housing. If it returns a
    negative number they are spending more than 30%, if it returns a positive number they are spending less than 30%.

    :param x: Price of house
    :param s: Yearly salary of family
    :param d: House down payment in dollars
    :param r: monthly interest rate
    :param rt: monthly tax rate
    :param rm: monthly maintenance rate
    :return: Monthly money remaining that HUD says can safely be used for housing. If this is zero you're at the HUD
    recommended 30%. If this number is negative you're paying more than 30%. If this number is positive you're paying less than 30%.
    """
    if d == 0:
        # If d == 0, then assume 20% down payment
        return (0.3 / 12) * s + (1 / 12) * standard_deduction_or_mid(s, 0.8 * x, r) - monthly_payment(r, 0.8 * x,
                                                                                                      360.0) - x * (
                           rt + rm)
    else:
        return (0.3 / 12) * s + (1 / 12) * standard_deduction_or_mid(s, x - d, r) - monthly_payment(r, x - d,
                                                                                                    360.0) - x * (
                           rt + rm)


def salary_needed_for_given_house_price(s, x, d, r, rt, rm, hoa):
    """
        Function used to solve for how much salary is required to by a house of value x.
        This is the same as 'how_much_can_afford' with the first two variables switched for use to scipy.fsolve
        It starts with HUD defined maximum housing costs (30% salary before taxes) and adds in any money that might come
        from using the mortgage interest deduction and subtracts off the cost of the mortgage, taxes and maintenance.

        :param x: Price of house
        :param s: Yearly salary of family
        :param d: House down payment in dollars
        :param r: monthly interest rate
        :param rt: monthly tax rate
        :param rm: monthly maintenance rate
        :param hoa: Any (monthly) HOA fees that may be required. This can also be used to add any monthlies (or
        reduce monthlies by making negative this value negative)
        :return: Money remaining that HUD says can safely be used for housing. If this is zero you're at the HUD
        recommended 30%. If this number is negative you're paying more than 30%. If this number is positive you're paying less than 30%.
        """
    if d == 0:
        # If d == 0, then assume 20% down payment
        return (0.3 / 12) * s + (1 / 12) * standard_deduction_or_mid(s, 0.8 * x, r) - monthly_payment(r, 0.8 * x,
                                                                                                      360.0) - x * (
                       rt + rm) - hoa
    else:
        return (0.3 / 12) * s + (1 / 12) * standard_deduction_or_mid(s, x - d, r) - monthly_payment(r, x - d,
                                                                                                    360.0) - x * (rt +
                                                                                                                  rm) - hoa


def add_required_salary_to_dataframe(df_in, d, r, rt, rm):
    """
    Function to add a column to a pandas dataframe based on the price of a house and interest and tax rates.

    :param df_in: Dataframe to add the column 'required_salary' to
    :param d: House down payment in dollars
    :param r: monthly interest rate
    :param rt: monthly tax rate
    :param rm: monthly maintenance rate
    :return:
    """
    if hasattr(df_in, 'HOAperMonth'):
        a = lambda y: fsolve(salary_needed_for_given_house_price, [450000],
                             args=(y.PRICE, d, r, rt, rm, y.HOAperMonth))[0] / 1000
    else:
        a = lambda y: fsolve(salary_needed_for_given_house_price, [450000],
                             args=(y.PRICE, d, r, rt, rm, 0))[0] / 1000

    df_in['required_salary'] = df_in.apply(a, axis=1)
    return df_in


def downpayment_help_needed_for_given_salary_and_home_price(d, x, s, r, rt, rm, hoa):
    """
    Function used to solve for how much down payment assistance is required to make a house price x affordable on a salary s.
    This is the same as 'salary_needed_for_given_house_price' with the first and third variables switched for use to scipy.fsolve
    It starts with HUD defined maximum housing costs (30% salary before taxes) and adds in any money that might come
    from using the mortgage interest deduction and subtracts off the cost of the mortgage, taxes and maintenance.

    :param d: House down payment in dollars
    :param x: Price of house
    :param s: Yearly salary of family
    :param r: monthly interest rate
    :param rt: monthly tax rate
    :param rm: monthly maintenance rate
    :param hoa: Any (monthly) HOA fees that may be required. This can also be used to add any monthlies (or
    reduce monthlies by making negative this value negative)
    :return: Money remaining that HUD says can safely be used for housing. If this is zero you're at the HUD
    recommended 30%. If this number is negative you're paying more than 30%. If this number is positive you're paying less than 30%.
    """
    return salary_needed_for_given_house_price(s, x, d, r, rt, rm, hoa)