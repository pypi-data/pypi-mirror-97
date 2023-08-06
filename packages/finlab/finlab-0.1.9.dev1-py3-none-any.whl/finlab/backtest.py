import copy
import math
import pandas as pd
import numpy as np
from .report import Report

def sim(price, buy, sell, resample=None, *arg1, weight=None, benchmark=None, **arg2):

    # resample dates
    if isinstance(resample, str):
        dates = pd.date_range(buy.index[0], buy.index[-1], freq=resample)
    elif resample is None:
        dates = None

    # calculate position using buy and sell
    positions = calculate_position(price, buy, sell, dates, weight)
    positions = positions[(positions.sum(axis=1) != 0).cumsum() != 0]
    returns = calculate_capital(price, positions, *arg1, **arg2)
    return Report(returns, positions, benchmark)

def rebalance_dates(freq):
    if isinstance(freq, str):
        def f(start_date, end_date):
            return pd.date_range(start_date, end_date, freq=freq)
        return f
    elif isinstance(freq, pd.Series):
        def f(start_date, end_date):
            return pd.to_datetime(freq.loc[start_date, end_date].index)
    return f

def adjust_dates_to_index(creturn, dates):

    def to_buesiness_day(d):
        if d <= creturn.index[-1]:
            i = creturn.index.get_loc(d, method='bfill')
            ret = creturn.index[i]
        else:
            ret = None#creturn.index[-1]
        return ret

    return pd.DatetimeIndex(pd.Series(dates).apply(to_buesiness_day).dropna()).drop_duplicates()

def calculate_position(price, buy, sell, resample=None, weight=None):

    '''
    signalIn and signalOut are pandas dataframe, which indicate a stock should be
    bought or not.
    '''

    if sell is not None:
        buy &= price.notna()
        sell |= price.isna()

    position = pd.DataFrame(np.nan, index=buy.index, columns=buy.columns)
    position[buy.fillna(False)] = 1
    if sell is not None:
        position[sell.fillna(False)] = 0
        position = position.ffill()
    position = position.fillna(0)
    position = position.div(position.abs().sum(axis=1), axis=0).fillna(0)

    if resample is not None:
        dates = adjust_dates_to_index(price, resample)
        position = position.reindex(price.index, method='ffill')\
            .reindex(dates, method='ffill')\
            .reindex(price.index, method='ffill').astype(float)

    ret = position.reindex(sorted(price.index | position.index), method='ffill').reindex_like(price).fillna(0)

    if weight is not None:
        if isinstance(weight, pd.DataFrame):
            ret *= weight.reindex(ret.index, method='ffill').fillna(0)
        elif isinstance(weight, pd.Series):
            ret.div(1/ret.sum(), axis=0)
        elif isinstance(weight, float):
            ret = (ret != 0).clip(None, weight)

    return ret

import numpy as np
def create_transaction_history(price, position, dfs = {}):

    orgKeys = list(dfs.keys())
    y = position.shift()
    yy = position.shift(2)
    buy = (yy == 0) & (y > 0)
    sell = (yy > 0) & (y == 0)

    priceOpen = price

    buyPrice = (priceOpen * buy).dropna(axis='index', how='all')

    sellPrice = (priceOpen * sell)
    sellDates = sell.apply(lambda s: s.index)

    sellPrice[sell == False] = np.nan
    sellDates[sell == False] = np.nan

    sellPrice = sellPrice.bfill()
    sellDates = sellDates.bfill()

    sellPrice = sellPrice[buy].dropna(axis='index', how='all')
    sellDates = sellDates[buy].dropna(axis='index', how='all')

    buyPrice[buy == False] = np.nan
    sellPrice[buy == False] = np.nan
    sellDates[buy == False] = np.nan

    for name, df in dfs.items():
        dfs[name] = df.reindex_like(position, method='ffill').shift()[buy]

    dfs['buy_price'] = buyPrice
    dfs['sell_price'] = sellPrice
    dfs['sell_date'] = sellDates

    newdfs = {}
    for name, df in dfs.items():
        uns = df.unstack()
        uns = uns[~uns.isnull()]
        uns = uns.swaplevel()
        newdfs[name] = uns
    profolio = pd.DataFrame(newdfs).reset_index()
    profolio = profolio.rename(columns = {'date':'buy_date'})

    keys = ['stock_id','buy_date', 'buy_price', 'sell_date', 'sell_price'] + list(orgKeys)
    dfs.clear()
    return profolio[keys]

def calculate_capital(price, position, fee_ratio=1.425/1000, tax_ratio=3/1000, mode='long'):

    # calculate stock return
    adj_close = price.copy()
    position[adj_close.ffill().shift().isna() & adj_close.notna()] = 0

    # calculate position adjust dates
    periods = (position.diff().abs().sum(axis=1) > 0).cumsum()
    indexes = pd.Series(periods.index).groupby(periods.values).last()

    # calculate periodic returns
    selected_adj = (adj_close.shift(-2)/adj_close.shift(-1)).replace([np.inf, -np.inf], 1).clip(0.9 ,1.1).groupby(periods).cumprod()
    selected_adj[(position == 0) | (selected_adj == 0)] = np.nan
    ret = (selected_adj.fillna(1) * position).sum(axis=1) + (1 - position.sum(axis=1))

    # calculate cost
    pdiff = position.diff()
    pdiff[pdiff > 0] *= (fee_ratio)
    pdiff[pdiff < 0] *= (fee_ratio + tax_ratio)
    cost = pdiff.abs().sum(axis=1).shift()
    cost = cost.fillna(0)

    # calculate cummulation returns
    s = (pd.Series(ret.groupby(periods).last().values, indexes).reindex(ret.index).fillna(1).shift().cumprod() * ret)

    # consider cost
    cap = ((s.shift(-1) / s).shift(3) * (1-cost)).cumprod().fillna(1)

    return cap[cap.shift().fillna(1) != 1.0]
