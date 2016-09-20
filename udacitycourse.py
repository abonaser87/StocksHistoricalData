"""Slice and plot"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
# from sklearn import preprocessing, cross_validation, svm
# from sklearn.linear_model import LinearRegression
# import scipy as sp
# import scipy.optimize as scopt

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
    dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y')
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=['Date'],date_parser=dateparse, usecols=['Date', col ], na_values=['nan'])
        df_temp = df_temp.rename(columns={col: symbol})
        df = df.join(df_temp)
        if symbol == 'TASI':  # drop dates SPY did not trade
            df = df.dropna(subset=["TASI"])

    return df


def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def get_mean_volume(df,symbols):
    for symbol in symbols:
        print 'Mean Volume for' , symbol
        print df[symbol].mean()

    

def get_max_price(df,symbols):
    for symbol in symbols:
        print 'Max Close for' , symbol
        print df[symbol].max() , 'at ' , df[symbol].argmax()

def compute_daily_returns(df):
    daily_returns = (df/df.shift(1))-1 
    daily_returns = daily_returns[1:]
    # daily_returns.plot(kind="hist")
    plt.show()
    return daily_returns

def forecast(df):
    X = np.array(df.drop(['label'], 1))
    y = np.array(df['label'])
    X = preprocessing.scale(X)
    y = np.array(df['label'])
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
    clf = LinearRegression()
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print(confidence)
def dollar_avg(df):
    capital = 50000
    test = df.resample('Q')
    print test
    alloc = capital/ 4 / test
    print alloc
    print alloc.sum(axis=0).round()
    avg_price = capital / alloc.sum(axis=0).round()
    print avg_price
def stats(df,beta):
    dr = compute_daily_returns(df)
    cumlative_ret = (df[-1]/df[0])-1
    avg_daily = dr.mean()
    std_daily = dr.std()
    sharpe = math.sqrt(252) * dr.mean()/dr.std()
    print "Beta = ", beta
    print "Cumlative Return:" , cumlative_ret*100
    print "Avg. Daily Returns:", avg_daily*100
    print "Standard Deviation:",std_daily*100
    print "Sharpe Ratio:",sharpe 

def calc_alpha(port,tasi,beta):
    port_ret = (port[-1]/port[0])-1
    tasi_ret = (tasi[-1]/tasi[0])-1
    alpha = (port_ret*100)-(beta*tasi_ret*100)
    print "Alpha:",alpha

def calculate_pf_beta(df,alloc,symbols):
    betas = []
    daily_returns = compute_daily_returns(df)
    daily_returns = daily_returns.dropna()
    for symbol in symbols:
        beta,alpha = np.polyfit(daily_returns['TASI'],daily_returns[symbol],1)
        betas.append(beta)
    betas = np.array(betas)
    beta = sum(betas*alloc)
    return beta       

    
def test_run():
    # Define a date range
    dates = pd.date_range('01-01-2012', '31-07-2016')

    # Choose stock symbols to read

    symbols = ['TASI','1150','1120','2020','2330','3030','3040','3050','4001','4002','4008','4190','4200','4240','2270','6001','6002','4031','4110','4260','1820']
    alloc = [0,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05]
    # Get stock data
    df = get_data(symbols, dates,'Close')
    tasi = get_data(['TASI'],dates,'Close')
    beta = calculate_pf_beta(df,alloc,symbols)
    capital = 200000
    pos_val = normalize_data(df) * alloc * capital
    # shares = [x * capital for x in alloc] 
    # shares = np.asarray(shares / df.iloc[0])
    # total = np.asarray([a*b for a,b in zip(shares,divedend)])
    # total = total.sum()
    # print total
    port_val = pos_val.sum(axis=1)
    tasi_val = normalize_data(tasi) * capital
    tasi_port = tasi_val.sum(axis=1)
    print port_val[-1]
    print 'Portofolio Stats'
    stats(port_val,beta)
    print 'TASI Stats'
    stats(tasi_port,1)
    calc_alpha(port_val,tasi_port,beta)
    port_val.plot(title='Portofolio')
    tasi_port.plot(title='TASI')
    plt.show()

    # Forecasting
    # forecast_out = int(math.ceil(0.01 * len(df)))

    # df['label'] = df['4190'].shift(-forecast_out)
    # forecast(df)
    #dca = dollar_avg(df)
    # get_max_price(df,symbols)
    # daily_returns = compute_daily_returns(df)
    # daily_returns.plot(kind='scatter',x='TASI',y='4190')
    # beta_4300,alpha_4300 = np.polyfit(daily_returns['TASI'],daily_returns['4190'],1)
    # print beta_4300
    # print alpha_4300*252
    # plt.plot(daily_returns['TASI'],beta_4300*daily_returns['TASI']+alpha_4300,'-',color='r')
    
    # print daily_returns.corr(method='pearson')
    # df = get_data(symbols, dates,'Vol')
    # get_mean_volume(df,symbols)
    # plt.show()
    
    # Slice and plot
    #plot_selected(normalize_data(df), ['TASI', '4300'], '01-01-2015', '31-12-2015')



if __name__ == "__main__":
    test_run()