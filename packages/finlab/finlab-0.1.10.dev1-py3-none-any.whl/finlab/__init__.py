import os

__version__ = '0.1.10.dev1'

def set_token(api_token=None):
    if api_token is None:
        print('Go to this URL in a browser: https://finlab-python.github.io/finlab/api_token')
        api_token = input('Enter your api_token:\n')
        os.environ['finlab_id_token'] = api_token

    os.environ['finlab_id_token'] = api_token

def get_token():

    if 'finlab_id_token' not in os.environ:
        set_token()

    return os.environ['finlab_id_token']
