import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

# setting up the yfinance to be read on DataFrame
yf.pdr_override()

# ask user for stock input
stock = input("Enter a stock ticker: ")

# set up the start and end date for the data fetch
startYear = 2019
startMonth = 1
startDay = 1

# create a datetime object with info above
start = dt.datetime(startYear, startMonth, startDay)

# current date time
now = dt.datetime.now()

# fetch data from yfinance
df = pdr.get_data_yahoo(stock, start, now)

# Set the moving average range number
ma = 50

# set up a string witht the chosen moving average
smaString = "Sma_" + str(ma)

# calculate the moving average: 4th column = Adj Close
df[smaString] = df.iloc[:, 4].rolling(window = ma).mean()

# deletes the first 50 rows of NaN vals
df = df.iloc[ma:]
print(df)

numH = 0
numL = 0

# looping over each index to find when Closed higher that Moving Average
for i in df.index:
    if (df["Adj Close"][i]) > df[smaString][i]:
        print("the close is higher")
        numH += 1
    else:
        print("the close is lower")
        numL += 1

print(numH)
print(numL)







