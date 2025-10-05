import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

def period_returns(prices):
    rt = prices.pct_change().fillna(0.0)
    #print(rt)
    return rt
    
def standard_deviation(period_returns):
    stdv = period_returns.std(ddof = 1) * math.sqrt(12)
    #print(stdv)
    return stdv
    
def cumulative_wealth(period_returns):
    cwealth = (1 + period_returns).cumprod()
    #print(cwealth)
    return cwealth

def cagr(cwealth, years):
    cagr_val = cwealth.iloc[-1] ** (1 / years) - 1
    #print(cagr_val)
    return cagr_val

def best_month(period_returns):
    best_date = period_returns.idxmax()
    best_value = period_returns.loc[best_date]
    #print(best_date, best_value)
    return (best_date, best_value)

def worst_month(period_returns):
    worst_date = period_returns.idxmin()
    worst_value = period_returns.loc[worst_date]
    #print(worst_date, worst_value)
    return (worst_date, worst_value)
    
def max_drawdown(cwealth):
    peak = cwealth.cummax()
    drawdown = (cwealth / peak) - 1
    #print(min(drawdown))
    return min(drawdown)

START_DATE = "02/1992"
END_DATE = "07/2025"

sm, sy = map(int, START_DATE.split('/'))
em, ey = map(int, END_DATE.split('/'))

TOTAL_YEARS = ((ey - sy) * 12 + (em - sm) + 1) / 12

sp = pd.read_csv("../data/sp500_data.csv")
sp.index = sp["Date"]
acwi = pd.read_csv("../data/acwi_data.csv")
acwi.index = acwi["Date"]

#Extract prices
sp_prices = sp["S&P 500"].loc[START_DATE : END_DATE]
acwi_prices = acwi["MSCI ACWI"].loc[START_DATE : END_DATE]

#Calculate period returns
sp_rt = period_returns(sp_prices)
acwi_rt = period_returns(acwi_prices)

#Calculate annual standard deviation
sp_std = standard_deviation(sp_rt)
acwi_std = standard_deviation(acwi_rt)

#Caculate cumulative wealth
sp_cwealth = cumulative_wealth(sp_rt)
acwi_cwealth = cumulative_wealth(acwi_rt)

#Combine cumulative wealth
both_cwealth = pd.concat([sp_cwealth, acwi_cwealth], axis = 1, join = "inner")
both_cwealth.index = pd.to_datetime(both_cwealth.index, format="%m/%Y")

#Calculate Compound Annual Growth Rate
sp_cagr = cagr(sp_cwealth, TOTAL_YEARS)
acwi_cagr = cagr(acwi_cwealth, TOTAL_YEARS)

#Calculate best/worst months
sp_best = best_month(sp_rt)
sp_worst = worst_month(sp_rt)
acwi_best = best_month(acwi_rt)
acwi_worst = worst_month(acwi_rt)

#Calculate max drawdown
sp_mdd = max_drawdown(sp_cwealth)
acwi_mdd = max_drawdown(acwi_cwealth)

#Plot cumulative wealth of indicies
plt.figure(figsize = (10, 5))
plt.title("Growth of $1 from " + START_DATE + "-" + END_DATE)
plt.plot(both_cwealth.index, both_cwealth.iloc[:, 0].values, label = both_cwealth.columns[0])
plt.plot(both_cwealth.index, both_cwealth.iloc[:, 1].values, label = both_cwealth.columns[1])
plt.legend()
plt.xlabel("Date")
plt.ylabel("Dollars")
plt.tight_layout()
plt.show()