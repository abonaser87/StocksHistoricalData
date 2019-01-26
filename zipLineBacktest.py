
# coding: utf-8

# In[27]:


import pandas as pd
from collections import OrderedDict
import os
import pytz
from zipline.api import order, record, symbol, set_benchmark
import zipline
import matplotlib.pyplot as plt
from datetime import datetime

data = OrderedDict()

files = os.listdir("AdjDaily")
tickers=[]
for name in files:
    if name[0].isdigit():
        tickers.append(name.split('.')[0])
tickers=['1010']
def symbol_to_path(ticker, base_dir="AdjDaily"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(ticker)))

if 'TASI' not in tickers:  # add SPY for reference, if absent
    tickers.insert(0, 'TASI')
dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y')
for ticker in tickers:
    data[ticker] = pd.read_csv(symbol_to_path(ticker), index_col='Date',parse_dates=['Date'],date_parser=dateparse,na_values=['nan']
                )
    data[ticker] = data[ticker][['Close']]

# for ticker in tickers:
#     if ticker == 'TASI':
#         continue
#     print ticker
#     data[ticker].fillna(method="ffill", inplace=True)

panel = pd.Panel(data,major_axis=data['TASI'].index)
panel.minor_axis = ['close']
panel.major_axis = panel.major_axis.tz_localize(pytz.utc)
print(panel)
# panel.to_excel('panel.xlsx')
def initialize(context):
    set_benchmark(symbol('TASI'))


def handle_data(context, data):
    order(symbol('TASI'), 10)
    record(SPY=data.current(symbol('TASI'), 'price'))

perf = zipline.run_algorithm(start=datetime(2002, 1, 1, 0, 0, 0, 0, pytz.utc),
                      end=datetime(2003, 1, 1, 0, 0, 0, 0, pytz.utc),
                      initialize=initialize,
                      capital_base=100000,
                      handle_data=handle_data,
                      data=panel)
