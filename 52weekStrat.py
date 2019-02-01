

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
    cagr = (df.iloc[-1]/df.iloc[0])**(1.0/(len(full)/p)) - 1.0
    dr = compute_daily_returns(df)
    sharpe = np.sqrt(p) * dr.mean() / dr.std()
    print ' CAGR(%) = ' + str(cagr * 100)
    print ' Sharpe ratio = ' + str(sharpe)

try:
    df = pd.read_pickle('database.pkl')
except:
    print 'No pkl'
    df = load_df()
df = df.resample('W').mean()
df = df.dropna(subset=["TASI"])
tasi = df['TASI'].copy()
df = df.drop('TASI',axis=1)

# Slice the dataframe to Weeks
data = OrderedDict()
j=52
i=1
k=0
while k <= len(df):
    data['Week'+str(i)] = df[k:j]
    k=j
    j+=52
    i+=1
# Rank from Lowest to highest 52Weeks Returns
i=1
pctReturn = OrderedDict()
while i <= len(data):
    mask = data['Week'+str(i)].iloc[0].isnull()
    data['Week'+str(i)] = data['Week'+str(i)].loc[:,~mask]
    data['Week'+str(i)] = data['Week'+str(i)].fillna(method='ffill')
    data['Week'+str(i)].to_excel('Week'+str(i)+'.xlsx')
    data['Week'+str(i)].min().to_excel('Min Week'+str(i)+'.xlsx')
    pctReturn['Week'+str(i)] = (data['Week'+str(i)].iloc[-1] / data['Week'+str(i)].min())-1
    pctReturn['Week'+str(i)]= pctReturn['Week'+str(i)].sort_values()
    i+=1

# Divide to Quartiles and get the last week price
w=1
qNum=1
q=4
j=0
k=1
quartiles = OrderedDict()

while w <= len(pctReturn):
    numInQuartile = np.round(len(pctReturn['Week'+str(w)])/float(q))
    i=0
    while qNum <= q:
        x = int(numInQuartile*qNum)
        quartiles['Week'+str(w)+'Q'+str(qNum)] = [pctReturn['Week'+str(w)][int(j):x].index]
        qNum+=1
        j+=numInQuartile
#     qNum=1
#     while i < len(pctReturn['Week'+str(w)]):
#         price = data['Week'+str(w)][pctReturn['Week'+str(w)].index[i]].iloc[-1]
#         index = pctReturn['Week'+str(w)].index[i]
#         quartiles['Week'+str(w)+'Q'+str(qNum)].loc[index]=price

#         if k == numInQuartile:
#             qNum+=1
#             k=0
#         if qNum > q:
#             qNum=q
#         i+=1
#         k+=1
    w+=1
    qNum=1
    j=0
    k=1

# Construct Portfolios
capital = 100000
w=2
qNum=1
portfolios = OrderedDict()
while w <= len(data):
    test = pd.DataFrame()
    while qNum <= q:
        if w > 2 :
            capital = portfolios['Week'+str(w-1)]['Q'+str(qNum)].iloc[-1]
        stocks = quartiles['Week' + str(w-1) + 'Q'+str(qNum)][0]
        cond = [c for c in data['Week'+str(w)].columns if c not in stocks]
        df_temp = normalize_data(data['Week'+str(w)].drop(cond,axis=1)).dropna(axis=1) * (1.0/len(stocks)) * capital
        df_temp = df_temp.sum(axis=1)
        df_temp = df_temp.rename('Q'+str(qNum))
        df_temp = df_temp.to_frame()
        test = test.join(df_temp, how='outer')
        portfolios['Week'+str(w)] = test
        qNum+=1
    w+=1
    qNum=1


from matplotlib import style
style.use('ggplot')

# Merge the years to get full data for four quartiles
full = pd.DataFrame()
for port in portfolios:
    full = full.append(portfolios[port])

capital = 100000
tasi = normalize_data(tasi) * capital

cagr = stats(full,'W')
print cagr
tasiCagr = stats(tasi,'W')
print tasiCagr

yearlyRtns = compute_daily_returns(full.resample('Y').mean())
print yearlyRtns * 100
tasiYearlRtns = compute_daily_returns(tasi.resample('Y').mean())
print tasiYearlRtns *100
