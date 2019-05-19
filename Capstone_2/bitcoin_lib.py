from datetime import datetime
from dateutil.parser import parse

import numpy as np
import pandas as pd

def get_moving_averages():
    """This function computes the simple moving average and the exponential moving average
    """
    days = [15, 30, 45, 60, 90, 200]
    for day in days:
        data['sma{}_close'.format(day)] = data['close'].rolling(day).mean()
    for day in days:
        data['ema{}_close'.format(day)] = pd.Series.ewm(data['close'], span=day).mean()


def get_future_close():
    days = [5, 10, 20, 30]
    for day in days:
        data['{}d_future_close'.format(day)] = data['close'].shift(-day)
    for day in days:
        data['{}d_close_future_pct'.format(day)] =  data['{}d_future_close'.format(day)].pct_change(day)
    for day in days:
        data['{}d_close_pct'.format(day)] = data['close'].pct_change(day)


def get_rsi():
    windows = [15, 30, 45, 60, 90, 200]
    for window in windows:
        delta = data['close'].diff()
        up_days = delta.copy()
        up_days[delta<=0]=0.0
        down_days = abs(delta.copy())
        down_days[delta>0]=0.0
        RS_up = up_days.rolling(window).mean()
        RS_down = down_days.rolling(window).mean()
        data['rsi_{}d'.format(window)] = 100-100/(1+RS_up/RS_down)


def load_bitcoin_data(filename, starting_date='2016-01-01'):
    global data
    ### Load CSV file and transforming columns
    data = pd.read_csv(filename)
    data.columns = map(str.lower, data.columns)
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    data.rename(columns={'timestamp':'date'}, inplace=True)

    ### Setting index to the date and resampling
    data.index = data['date']
    data.fillna(method='ffill', inplace=True)
    data = data.resample('D').mean()

    ### Getting subset of data
    date = parse(starting_date)
    data = data.loc[date:].copy()

    ### Getting technical indicators
    get_moving_averages()
    get_rsi()
    get_future_close()

    return data
