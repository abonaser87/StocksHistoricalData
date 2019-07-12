

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

def symbol_to_path(symbol, base_dir="AdjDaily"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates,col):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'TASI' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'TASI')
    dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y')
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=['Date'],date_parser=dateparse, usecols=['Date', col ], na_values=['nan'])
        df_temp = df_temp.rename(columns={col: symbol})
        df = df.join(df_temp)

        if symbol == 'TASI':  # drop dates SPY did not trad
            df = df.dropna(subset=["TASI"])

    return df

def load_df():
    dates = pd.date_range('01/01/2002', '01/01/2017')
    N= (dates[-1]-dates[0])/365
    N = str(N).split()[0]
    files = os.listdir("AdjDaily")
    symbols=[]
    for name in files:
        if name[0].isdigit():
            symbols.append(name.split('.')[0])
    df = get_data(symbols, dates, 'Close')
    df.to_pickle('database.pkl')
    return df
def normalize_data(df):
    return df/df.ix[0,:]

def compute_daily_returns(df):
    daily_returns = (df/df.shift(1))-1
    daily_returns = daily_returns[1:]
    return daily_returns

def stats(df,period):
    if period == 'W':
        p = 52.0
    if period == 'M':
        p = 12.0
    if period == 'D':
        p = 365.0
    cagr = (df.iloc[-1]/df.iloc[0])**(1.0/(len(df)/p)) - 1.0
    dr = compute_daily_returns(df)
    sharpe = np.sqrt(p) * dr.mean() / dr.std()
    print ' CAGR(%) = ' + str(cagr * 100)
    print ' Sharpe ratio = ' + str(sharpe)

def multi_period_return(period_returns):
    return np.prod(period_returns + 1) - 1

try:
    df = pd.read_pickle('database.pkl')
except:
    print 'No pkl'
    df = load_df()
df = df.resample('M').mean()
df = df.dropna(subset=["TASI"])
tasi = df['TASI'].copy()
df = df.drop('TASI',axis=1)

returns = compute_daily_returns(df)

lookback = 11
holdPeriod = 3
test = returns.rolling(lookback).apply(multi_period_return)
test = test[lookback:]
mask = test.iloc[0].isnull()
test = test.loc[:,~mask]
print test
sorteddf = test.sort_values(by=test.index.values[0], ascending=False, axis=1)
print sorteddf