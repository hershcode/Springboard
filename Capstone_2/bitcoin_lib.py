from datetime import datetime
from dateutil.parser import parse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.preprocessing import StandardScaler

def get_moving_averages():
    """This function computes the simple moving average and the exponential moving average
    """
    days = [15, 45, 90, 200]
    for day in days:
        data['sma{}_close'.format(day)] = data['close'].rolling(day).mean()
    for day in days:
        data['ema{}_close'.format(day)] = pd.Series.ewm(data['close'], span=day).mean()


def get_future_close():
    days = [5, 10]
    for day in days:
        data['{}d_future_close'.format(day)] = data['close'].shift(-day)
    for day in days:
        data['{}d_close_future_pct'.format(day)] =  data['{}d_future_close'.format(day)].pct_change(day)
    for day in days:
        data['{}d_close_pct'.format(day)] = data['close'].pct_change(day)


def get_rsi():
    windows = [15, 45, 90, 200]
    for window in windows:
        delta = data['close'].diff()
        up_days = delta.copy()
        up_days[delta<=0]=0.0
        down_days = abs(delta.copy())
        down_days[delta>0]=0.0
        RS_up = up_days.rolling(window).mean()
        RS_down = down_days.rolling(window).mean()
        data['rsi_{}d'.format(window)] = 100-100/(1+RS_up/RS_down)


def load_bitcoin_data():
    global data
    ### Load CSV file and transforming columns
    filename = "coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv"
    data = pd.read_csv(filename)
    data.columns = map(str.lower, data.columns)
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    data.rename(columns={'timestamp':'date'}, inplace=True)

    ### Setting index to the date and resampling
    data.index = data['date']
    data.fillna(method='ffill', inplace=True)
    data = data.resample('D').mean()

    ### Getting subset of data
    date = parse('2016-01-01')
    data = data.loc[date:].copy()

    ### Getting technical indicators
    get_moving_averages()
    get_rsi()
    get_future_close()

    data.drop(labels=['open', 'low', 'high'], axis=1, inplace=True)

    return data


####### Plotting functions
def plot(df, columns, xlabel, ylabel, title):

    sb.set()
    plt.figure(figsize=(14,6))

    for col in columns:
        df[col].plot()


    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(columns)
    plt.title(title)
    plt.show()

def correlation_heatmap(df):
    corr = df.corr()
    plt.figure(figsize=(20,14))
    sb.heatmap(data=corr)
    plt.title(label="Correlation Plot")
    plt.show()

def scatter_plot(df, x, y, xlabel, ylabel, title):
    plt.figure(figsize=(14,6))
    sb.scatterplot(x=x, y=y, data=df)
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel=ylabel)
    plt.title(label=title)
    plt.show()

def distribution(df, columns, title, subplots=False):
    plt.figure(figsize=(14, 10))

    if subplots == False:
        df[columns].plot.density()
        plt.title(label=title)
        plt.show()

    else:
        for count, column in enumerate(columns):
            index=count+1
            plt.subplot(2, 2, index)
            df[column].plot.density()
            plt.title(label=title[count])
        plt.show()

def scale(df, columns):

    scaler = StandardScaler().fit(df[columns].values)
    features = scaler.transform(df[columns].values)
    scaled_features = pd.DataFrame(features, columns=columns)

    return scaled_features
