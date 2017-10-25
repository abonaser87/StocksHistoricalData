"""Slice and plot"""
import calendar
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime, timedelta
def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    plot_data(df.ix[start_index:end_index,columns])

def symbol_to_path(symbol, base_dir="Daily"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def normalize_data(df):
    return df/df.ix[0,:]

def get_data(symbols, dates,col):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'TASI' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'TASI')
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=['Date'],date_parser=dateparse, usecols=['Date', col ], na_values=['nan'])
        df_temp = df_temp.rename(columns={col: symbol})
        df = df.join(df_temp)

        if symbol == 'TASI':  # drop dates SPY did not tradenumpy-1.11.1+mkl-cp27-cp27m-win32.whl
            df = df.dropna(subset=["TASI"])

    return df

def priceIndex(df,firstDate,days):
    finalDate = pd.datetime.strptime(firstDate, '%Y-%m-%d') - timedelta(days=days)
    sixmonthprice = df.loc[finalDate]
    priceNow = df.loc[firstDate]
    print priceNow / sixmonthprice
if __name__ == "__main__":
    dates = pd.date_range('2016-01-02', '2017-06-22')
    symbols = [4190,2020,1810,3050,6004,6002,2110,4160,4003,2360,3040,4240,7020,1214,3020,1301,4004,8100,4001,1120,4002,8010,1330,3060,2270,1140,4260,4200,8140,2290]
    df = get_data(symbols, dates,'Close')
    # df = df.dropna(subset=["4270"])
    priceIndex(df,'2017-01-10',180)

