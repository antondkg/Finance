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
startYear = 2018
startMonth = 1
startDay = 1

# create a datetime object with info above
start = dt.datetime(startYear, startMonth, startDay)

# current date time
now = dt.datetime.now()

# fetch data from yfinance
df = pdr.get_data_yahoo(stock, start, now)

#print(df)
# Set the moving average range number

# Red Blue strategy
# Set the moving averages to be used to calculate the bands
emasUsed = [3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60]
for x in emasUsed:
    ema = x
    df["Ema_" + str(ema)] = round(df.iloc[:, 4].ewm(span = ema, adjust = False).mean(), 2)


df = df.iloc[60:]

# Loop through each of the days and calculate the Min & Max
pos = 0 # open = 1 or close = 0
percentChange = []
for num, i in enumerate(df.index):
    cmin = min(df["Ema_3"][i], df["Ema_5"][i], df["Ema_8"][i], df["Ema_10"][i], df["Ema_12"][i], df["Ema_15"][i])
    cmax = max(df["Ema_30"][i], df["Ema_35"][i], df["Ema_40"][i], df["Ema_45"][i], df["Ema_50"][i], df["Ema_60"][i])

    close = df["Adj Close"][i]

    # if the min is higher than then max open position
    if cmin > cmax:
        if pos == 0:
            bp = close
            pos = 1
            print("buying now at: " + str(bp))
    # if the min is lower than the max then close position
    elif cmin < cmax:
        if pos == 1:
            pos = 0
            sp = close
            print("Selling now at: " + str(sp))
            pc = (sp/bp - 1) * 100
            percentChange.append(pc)

    # edge case for if i have an open position at the end
    if (num == df["Adj Close"].count() - 1 and pos == 1):
        pos = 0
        sp = close
        print("Selling now at: " + str(sp))
        pc = (sp/bp - 1) * 100
        percentChange.append(pc)

    end = df["Adj Close"][i]
    start = df["Adj Close"][0]
print(percentChange)

## KPI

gains = 0
ng = 0
losses = 0
nl = 0
totalR = 1

for p in percentChange:
    if p > 0:
        gains += p
        ng += 1
    else:
        losses += p
        nl += 1
    totalR = totalR * ((p / 100) + 1)

totalR = round((totalR - 1) * 100, 2)

if ng > 0:
    avgGain = gains / ng
    maxR = str(max(percentChange))
else:
    avgGain = 0
    maxR = "undefined"

if (nl > 0):
    avgLoss = losses/nl
    maxL = str(min(percentChange))
    ratio = str(-avgGain/avgLoss)
else:
    avgLoss = 0
    maxR = "undefined"
    ration = "inf"

if (ng > 0 or nl > 0):
    battingAvg = ng / (ng + nl)
else:
    battingAvg = 0

print()
print("Results for " + stock + " going back to " + str(df.index[0]))
print("Emas used: " +str(emasUsed))
print("battingAvg: " + str(battingAvg))
print("Gain / Loss Ratio: " + str(ratio))
print("Average Gain: " + str(avgGain))
print("Average Loss: " + str(avgLoss))
print("Max Return: " + str(maxR))
print("Max Loss: " + str(maxL))
print("Total Return over " + str(ng + nl) + " trades: " + str(totalR) + "%")
print("Holding Asset: " + str((end / start - 1) * 100) + "%")