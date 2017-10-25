"""Slice and plot"""
import calendar
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
# from sklearn import preprocessing, cross_validation, svm
# from sklearn.linear_model import LinearRegression
import scipy as sp
import scipy.optimize as scopt
import cvxopt as opt
from cvxopt import blas, solvers

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

def get_divdend(symbols,dates):
    df = pd.DataFrame(index=dates)
    if 'TASI' in symbols:
        symbols.pop(0)
    for symbol in symbols:
        df_temp=pd.read_csv("divdend.csv",index_col='Date', usecols=['Date', symbol ], na_values=['0'])
        df = df.join(df_temp)
    df=df.fillna(0)
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
    capital = 4000 * 12 * 4
    test = df.resample('M')
    alloc = [1,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125]
    alloc[:] = [x*4000 for x in alloc]
    alloc = alloc / test
    print alloc
    print alloc.sum(axis=0).round()
    avg_price = 27500 / alloc.sum(axis=0).round()
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

def negative_sharpe_ratio_n_minus_1_stock(weights,returns,risk_free_rate):
    """
    Given n-1 weights, return a negative sharpe ratio
    """
    weights2 = sp.append(weights, 1-np.sum(weights))
    return -sharpe_ratio(returns, weights2, risk_free_rate)

def optimize_portfolio(returns, risk_free_rate):
    """ 
    Performs the optimization
    """
    # start with equal weights
    w0 = np.ones(returns.columns.size-1,dtype=float) * 1.0 / returns.columns.size
    # minimize the negative sharpe value
    w1 = scopt.fmin(negative_sharpe_ratio_n_minus_1_stock,w0, args=(returns, risk_free_rate))
    # build final set of weights
    final_w = sp.append(w1, 1 - np.sum(w1))
    # and calculate the final, optimized, sharpe ratio
    final_sharpe = sharpe_ratio(returns, final_w, risk_free_rate)
    return (final_w, final_sharpe)

def calc_annual_returns(daily_returns):
    grouped = np.exp(daily_returns.groupby(lambda date: date.year).sum())-1
    return grouped        

def sharpe_ratio(returns, weights = None, risk_free_rate = 0):
    n = returns.columns.size
    if weights is None: weights = np.ones(n)/n
    # get the portfolio variance
    var = calc_portfolio_var(returns, weights)
    # and the means of the stocks in the portfolio
    means = returns.mean()
    # and return the sharpe ratio
    return (means.dot(weights) - risk_free_rate)/np.sqrt(var)

def calc_portfolio_var(returns, weights=None):
    if weights is None: 
        weights = np.ones(returns.columns.size) / \
        returns.columns.size
    sigma = np.cov(returns.T,ddof=0)
    var = (weights * sigma * weights.T).sum()
    return var

def optimal_portfolio(returns):
    n = len(returns)
    returns = np.asmatrix(returns)
    print returns
    N = 100
    mus = [10**(5.0 * t/N - 1.0) for t in range(N)]
    
    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(returns))
    pbar = opt.matrix(np.mean(returns, axis=1))
    
    # Create constraint matrices
    G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n ,1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)
    
    # Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] 
                  for mu in mus]
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER
    returns = [blas.dot(pbar, x) for x in portfolios]
    risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    m1 = np.polyfit(returns, risks, 2)
    x1 = np.sqrt(m1[2] / m1[0])
    # CALCULATE THE OPTIMAL PORTFOLIO
    wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    return np.asarray(wt), returns, risks

def dailystratTest(N,df,stock):
    df = normalize_data(df)
    CAGR = ((df[stock][-1] / df[stock][0]) ** (1 / float(N)) - 1) * 100
    for index, row in df.iterrows():
        # Check for the old weekend
        if index < pd.to_datetime('2013-06-29',dayfirst=True):
            if calendar.day_name[index.weekday()] == 'Wednesday':
                df.set_value(index,'postion',1)
            if calendar.day_name[index.weekday()] == 'Tuesday':
                df.set_value(index, 'postion', -1)
            # The current weekend
        else:
            if calendar.day_name[index.weekday()] == 'Thursday':
                df.set_value(index,'postion',1)
            if calendar.day_name[index.weekday()] == 'Wednesday':
                df.set_value(index, 'postion', -1)
    capital = 1000000
    postion = 0
    trades = 0
    print df['postion']
    for index, row in df.iterrows():
        if row['postion'] == 1:
            postion = capital / row[stock]
            trades += 1
        if row['postion'] == -1:
            capital = postion * row[stock] - (postion * row[stock] * 0.0015 * 2)
            trades += 1
    cagr = (((capital / 1000000) ** (1 / float(N))) - 1) * 100
    print index, postion, capital
    print trades, N, cagr , CAGR


def test_run():
    # Define a date range
    dates = pd.date_range('2017-01-01', '2017-06-22 ')
    N= (dates[-1]-dates[0])/365
    N = str(N).split()[0]

    # Choose stock symbols to read
    symbols = ['TASI','4190','6004','4160','2360','8210','3050','4240','3040','2110','4009','1810','2330','2020','4008','6002','8010','1820','4031','4200','3060','8180','4260','4001','2270','4030','4006','2320','3010','4002','4110']
    alloc = [0,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033,0.033]

    # Get stock data
    stock = 'TASI'
    df = get_data(symbols, dates,'Close')

    # Divdended
    # dailystratTest(N,df, stock)
    # MovingAvgTest(N, df, stock)
    # OptPort(df)
    # dca = dollar_avg(df)
    # BetaAlpha(dates, df, symbols)
    backtest(alloc, dates, df, symbols)


def backtest(alloc, dates, df, symbols):
    tasi = get_data(['TASI'], dates, 'Close')
    beta = calculate_pf_beta(df, alloc, symbols)
    capital = 200000
    pos_val = normalize_data(df) * alloc * capital
    port_val = pos_val.sum(axis=1)
    tasi_val = normalize_data(tasi) * capital
    tasi_port = tasi_val.sum(axis=1)
    print 'Portofolio Stats'
    stats(port_val, beta)
    print 'TASI Stats'
    stats(tasi_port, 1)
    calc_alpha(port_val, tasi_port, beta)
    ax = port_val.plot(label='Portofolio')
    tasi_port.plot(label='TASI',ax=ax)
    ax.legend(loc="upper right")
    plt.show()


def BetaAlpha(dates, df, symbols):
    get_max_price(df, symbols)
    daily_returns = compute_daily_returns(df)
    daily_returns.plot(kind='scatter', x='TASI', y='4190')
    beta_4300, alpha_4300 = np.polyfit(daily_returns['TASI'], daily_returns['4190'], 1)
    print beta_4300
    print alpha_4300 * 252
    plt.plot(daily_returns['TASI'], beta_4300 * daily_returns['TASI'] + alpha_4300, '-', color='r')
    print daily_returns.corr(method='pearson')
    df = get_data(symbols, dates, 'Vol')
    get_mean_volume(df, symbols)
    plt.show()
    # Slice and plot
    plot_selected(normalize_data(df), ['TASI', '4300'], '01-01-2015', '31-12-2015')


def OptPort(df):
    print 'Optimization'
    df = df.drop('TASI',1)
    df = normalize_data(df)
    dr = compute_daily_returns(df)
    annual_returns = calc_annual_returns(dr)
    ar = annual_returns.mean().transpose()
    print ar
    weights, returns, risks = optimal_portfolio(ar)
    print weights
    # Forecasting
    forecast_out = int(math.ceil(0.01 * len(df)))
    df['label'] = df['4190'].shift(-forecast_out)
    forecast(df)


def MovingAvgTest(N, df, stock):
    # calculate the stock CAGR
    df = df.resample('M')
    CAGR = ((df[stock][-1] / df[stock][0]) ** (1 / float(N)) - 1) * 100
    # Moving Average
    df['MA'] = pd.rolling_mean(df[stock], window=6)
    buysignal = df[stock] > df['MA']
    df['signal'] = np.where(buysignal, 1.0, 0)
    df['postions'] = df['signal'].diff()
    print df
    capital = 10000
    postion = 0
    trades = 0
    for index, row in df.iterrows():
        if row['postions'] == 1:
            postion = capital / row[stock]
            trades += 1
        if row['postions'] == -1:
            capital = postion * row[stock] - (postion * row[stock] * 0.0015 * 2)
            trades += 1
    cagr = (((capital / 10000) ** (1 / float(N))) - 1) * 100
    print index, postion, capital
    print trades, N, cagr, CAGR
    # ax = df[stock].plot(label=stock)
    # df['MA'].plot(label='200 MA',ax=ax)
    # ax.legend(loc="upper right")
    # plt.show()

if __name__ == "__main__":
    test_run()