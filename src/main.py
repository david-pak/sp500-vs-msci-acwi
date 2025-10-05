import pandas as pd

START_DATE = "02/1994"
END_DATE = "07/2025"

sp = pd.read_csv("../data/sp500_data.csv")
sp.index = sp["Date"]
acwi = pd.read_csv("../data/acwi_data.csv")
acwi.index = acwi["Date"]

sp_prices = sp["S&P 500"].loc[START_DATE : END_DATE]
acwi_prices = acwi["MSCI ACWI"].loc[START_DATE : END_DATE]

sp_rt = sp_prices.pct_change().dropna()
acwi_rt = acwi_prices.pct_change().dropna()