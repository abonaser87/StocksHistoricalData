import calendar
import os
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
import math

def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    plot_data(df.ix[start_index:end_index,columns])

def symbol_to_path(symbol, base_dir="googleHistorical/Daily"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def normalize_data(df):
    return df/df.ix[0,:]

def get_data(symbols, dates,col):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    # if 'TASI' not in symbols:  # add SPY for reference, if absent
    #     symbols.insert(0, 'TASI')
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
    for symbol in symbols:
        if symbol == 'SP':
            dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y')
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=['Date'],date_parser=dateparse, usecols=['Date', col ], na_values=['nan'])
        df_temp = df_temp.rename(columns={col: symbol})
        df = df.join(df_temp)

        if symbol == 'TASI':  # drop dates SPY did not tradenumpy-1.11.1+mkl-cp27-cp27m-win32.whl
            df = df.dropna(subset=["TASI"])

    return df

def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def compute_daily_returns(df):
    daily_returns = (df/df.shift(1))-1
    daily_returns = daily_returns[1:]
    #daily_returns.plot(kind="hist")
    #plt.show()
    return daily_returns

dates = pd.date_range('01-01-2004', '06-01-2017')
symbols = ['2020']
df = get_data(symbols, dates,'Close')
df = df.resample('M').mean()
N = (dates[-1] - dates[0]) / 365
N = str(N).split()[0]
returns = compute_daily_returns(df)
df = df[1:]
df['Gross Returns'] = 1 + returns
df = df.iloc[::-1]
xlookback = 8
holdingPeriod = 6
momentum = 1
tempIdx = 0
count = len(returns) - xlookback + 1
df['Mom'] = 'NaN'
i = 0
j = 0
lookback = xlookback
while i < count:
    j = i
    for idx, row in df.iterrows():
        if lookback > 0:
            if tempIdx == 0:
                tempIdx = df.iloc[j].name
            momentum = momentum * df['Gross Returns'].iloc[j]
            lookback -= 1
            j += 1
        else:
            momentum = momentum - 1
            # momentum = { 'Mom':momentum}
            df['Mom'].loc[tempIdx] = momentum
            momentum = 1
            tempIdx = 0
            lookback = xlookback
            break
    i += 1
df = df[:-lookback+1]
df = df.iloc[::-1]
buysignal =  df['Mom'] > 0
df['signal'] = np.where(buysignal,1,0)
df['postion']=0
holdingTrack = holdingPeriod
stock = '2020'
capital = 10000
postion = 0
trades = 0
CAGR = ((df[stock][-1] / df[stock][0]) ** (1 / float(N)) - 1) * 100
for idx,row in df.iterrows():
    if row['signal'] == 1 and holdingTrack == holdingPeriod:
        df['postion'].loc[idx] = 1
        postion = 1
    if holdingTrack == 0 :
        df['postion'].loc[idx] = -1
        holdingTrack = holdingPeriod
        postion = 0
    if postion == 1:
        holdingTrack -= 1
    if row['signal'] <= 0:
        continue
postion = 0
for index, row in df.iterrows():
    if row['postion'] == 1:
        postion = capital / row[stock]
        trades += 1
    if row['postion'] == -1:
        capital = postion * row[stock] - (postion * row[stock] * 0.0015 * 2)
        trades += 1
cagr = (((capital / 10000) ** (1 / float(N))) - 1) * 100
print df
print index, postion, capital
print trades, N, cagr, CAGR
