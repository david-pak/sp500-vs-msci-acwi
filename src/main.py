import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

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
sp_rt = sp_prices.pct_change().fillna(0.0)
acwi_rt = acwi_prices.pct_change().fillna(0.0)

#Calculate annual standard deviation
sp_std = sp_rt.std(ddof = 1) * math.sqrt(12)
acwi_std = acwi_rt.std(ddof = 1) * math.sqrt(12)

#Caculate cumulative wealth
sp_cwealth = (1 + sp_rt).cumprod()
acwi_cwealth = (1 + acwi_rt).cumprod()

#Combine cumulative wealth
both_cwealth = pd.concat([sp_cwealth, acwi_cwealth], axis = 1, join = "inner")
both_cwealth.index = pd.to_datetime(both_cwealth.index, format="%m/%Y")

#Calculate Compound Annual Growth Rate
sp_cagr = (sp_cwealth.iloc[-1]) ** (1 / TOTAL_YEARS) - 1
acwi_cagr = (acwi_cwealth.iloc[-1]) ** (1 / TOTAL_YEARS) - 1

#Calculate best/worst months
sp_bdate = sp_rt.idxmax()
sp_bvalue = sp_rt.loc[sp_bdate]
sp_wdate = sp_rt.idxmin()
sp_wvalue = sp_rt.loc[sp_wdate]

acwi_bdate = acwi_rt.idxmax()
acwi_bvalue = acwi_rt.loc[acwi_bdate]
acwi_wdate = acwi_rt.idxmin()
acwi_wvalue = acwi_rt.loc[acwi_wdate]

#Plot cumulative wealth of indicies
plt.figure(figsize = (10, 5))
plt.title("Growth of $1 from " + START_DATE + "-" + END_DATE)
plt.plot(both_cwealth.index, both_cwealth.iloc[:, 0].values, label = both_cwealth.columns[0])
plt.plot(both_cwealth.index, both_cwealth.iloc[:, 1].values, label = both_cwealth.columns[1])
plt.legend()

plt.xticks(rotation = 90)

plt.xlabel("Date")
plt.ylabel("Dollars")

plt.tight_layout()
plt.show()