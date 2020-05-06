import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename as aof

yf.pdr_override()
start = dt.datetime(2017, 12, 1)
now = dt.datetime.now()

# UI element to choose the Excel file

root = Tk()
ftypes = [(".xls", "*.xlsx"),(".xls", "*.xlsm"), (".xls", "*.xls")]
ttl = "Title"
dir1 = '/Users/antoniogoncalves'
filepath = aof(initialdir = dir1, title = ttl, filetypes = ftypes)

# set the file path for list of stocks to analyze
#filepath = r"/Users/antoniogoncalves/Google Drive/Development/Finance/RichardStocks.xlsx"


# convert excel data into pandas dataframe
stockList = pd.read_excel(filepath)
stockList = stockList.head()

# export the list into a pandas df
exportList = pd.DataFrame(columns = ["Stock", "RS_Rating", "50 Day MA", "150 Day MA", "200 Day MA", "52 Week High", "52 Week Low"])

# Iterate through each of the stocks
for i in stockList.index:
    stock = str(stockList["Symbol"][i])
    RS_Rating = stockList["RS Rating"][i]

    # Check to see if yfinance has the data for the specified stocks
    try:
        df = pdr.get_data_yahoo(stock, start, now)

        # calculate the Moving averages
        smaUsed = [50, 150, 200]

        for sma in smaUsed:
            df["SMA_" + str(sma)]\
             = round(df["Adj Close"].rolling(window = sma).mean(), 2)

        # get the most recent close value loc = end
        currClose = df["Adj Close"][-1]

        # get the most recent 50 day Moving Average
        ma_50 = df["SMA_50"][-1]
        ma_150 = df["SMA_150"][-1]
        ma_200 = df["SMA_200"][-1]

        # find 52 Week High & Low
        low52Week = min(df["Adj Close"][-260:])
        high52Week = max(df["Adj Close"][-260:])
        # 200 Day Moving Average for past 20 trading days

        try:
            ma_200_20 = df["SMA_200"][-20]
        except Exception:
            ma_200_20 = 0
       ######## Trading Conditions ####################################################
        #region
        # Condition 1: Current Price > 150 SMA and > 200 SMA
        if (currClose > ma_150 and currClose > ma_200):
            cond_1 = True
        else:
            cond_1 = False

        # Condition 2: 150 SMA and > 200 SMA
        if (ma_150 > ma_200):
            cond_2 = True
        else:
            cond_2 = False

        # Condition 3: 200 SMA trending up for at least 1 month
        # (ideally 4-5 months)
        if (ma_200 > ma_200_20):
            cond_3 = True
        else:
            cond_3 = False

        # Condition 4: 50 SMA > 150 SMA and 50 SMA > 200 SMA
        if (ma_50 > ma_150 and ma_50 > ma_200):
            cond_4 = True
        else:
            cond_4 = False


        # Condtition 5: Current Price > 50 SMA
        if (currClose > ma_50):
            cond_5 = True
        else:
            cond_5 = False

        # Condition 6: Current Price is at least 30% above 52 week low
        if (currClose >= low52Week * 1.3):
            cond_6 = True
        else:
            cond_6 = False

        # Condition 7: Current Price is within 25% of 52 week high
        if (currClose >= high52Week * 0.75):
            cond_7 = True
        else:
            cond_7 = False

        # Condition 8: IBD RS Rating > 70 and the higher the better
        if (RS_Rating > 70):
            cond_8 = True
        else:
            cond_8 = False

        #endregion
        #### Check if all conditions are true
        if (cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6\
            and cond_7 and cond_8):
            export = pd.DataFrame({"Stock": stock, "RS_Rating": RS_Rating, "50 Day MA": ma_50, "150 Day MA": ma_150, "200 Day MA": ma_200, "52 Week High" : high52Week, "52 Week Low" : low52Week}, index = [0])
            exportList = exportList.append(export)

    except Exception:
        print("No data on " + stock)

print(exportList)

# original file path and adding the name
newFile = os.path.dirname(filepath) + "/ScreenOutput/" + str(dt.datetime.now()) + ".xlsx"
# new writer object
writer = pd.ExcelWriter(newFile)
# export dataframe to the excel
exportList.to_excel(writer, "Sheet1")
writer.save()
