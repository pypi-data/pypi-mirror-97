import requests
import datetime
import pandas as pd
from io import BytesIO
from . import get_token, set_token
from . import dataframe

cache = {}
cache_time = {}
stock_names = {}

def get(dataset, use_cache=True):

    global stock_names

    # use cache if possible
    now = datetime.datetime.now()
    if (use_cache and (dataset in cache) and
        (now - cache_time[dataset] < datetime.timedelta(days=1))):
        return cache[dataset]

    api_token = get_token()

    # request for auth url
    request_args = {
        'api_token': api_token,
        'bucket_name':'finlab_tw_stock_item',
        'blob_name': dataset.replace(':', '#') + '.feather'
    }

    url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_generate_data_url'
    auth_url = requests.get(url, request_args)

    # download and parse dataframe
    res = requests.get(auth_url.text)
    df = pd.read_feather(BytesIO(res.content))

    # set date as index
    if 'date' in df:
        df.set_index('date', inplace=True)

        # if column is stock name
        if (df.columns.str.find(' ') != -1).all():

            # save new stock names
            new_stock_names = df.columns.str.split(' ')
            new_stock_names = dict(zip(new_stock_names.str[0], new_stock_names.str[1]))
            stock_names = {**stock_names, **new_stock_names}

            # remove stock names
            df.columns = df.columns.str.split(' ').str[0]

            # combine same stock history according to sid
            df = df.transpose().groupby(level=0).mean().transpose()


        df = dataframe.FinlabDataFrame(df)


    # save cache
    if use_cache:
        cache[dataset] = df
        cache_time[dataset] = now

    return df
