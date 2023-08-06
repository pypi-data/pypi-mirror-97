import os

__version__ = '0.1.8.dev1'

def set_token(api_token=None):
    if api_token is None:
        api_token = input('Please login to https://finlab-python.github.io/finlab/ and copy api token here: \n')
        os.environ['finlab_id_token'] = api_token

    os.environ['finlab_id_token'] = api_token

def get_token():

    if 'finlab_id_token' in os.environ:
        return os.environ['finlab_id_token']

    return None
