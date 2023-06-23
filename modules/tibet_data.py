"""
CAT Analysis Module for working with TibetSwap data
"""

import pandas as pd
import requests
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(__file__))
from utils import make_url


ANALYTICS_BASE_URL = "https://api.info.v2.tibetswap.io/"

base_url = ANALYTICS_BASE_URL

class Pairs:
    """
    Handle data about the available asset pairssys.path.append(os.path.dirname(__file__)).
    
    Assumes each token is paired with XCH.
    """
    
    def __init__(self, base_url=ANALYTICS_BASE_URL):
        self.base_url = base_url
        self.data = None
        
    def populate(self):
        url = make_url(self.base_url, 'pairs')
        response = requests.get(url)
        response.raise_for_status()
        self.data = pd.json_normalize(response.json())
        
    def refresh(self):
        self.populate()
        
    def get_data_item(self, entity='short_name', field='launcher_id', name='STDG'):
        if self.data is None:
            self.populate()
        return self.data[self.data[entity] == name][field].values[0]
    
    def get_launcher_id(self, token):
        return self.get_data_item(field='launcher_id', name=token)
    
    def get_xch_reserve(self, token):
        return self.get_data_item(field='xch_reserve', name=token).astype('float') / 1e12
    
    def get_token_reserve(self, token):
        return self.get_data_item(field='token_reserve', name=token).astype('float') / 1e3

    def get_liquidity(self, token):
        return self.get_data_item(field='liquidity', name=token).astype('float') / 1e3
    
    def get_transactions(self, token, lookback=7, op=None, limit=None):
        params = {}
        params['pair_launcher_id'] = self.get_launcher_id(token)
        if op is not None:
            params['operation'] = op
        if limit is not None:
            params['limit'] = limit
        url = make_url(base_url, 'transactions', params)
        response = requests.get(url)
        response.raise_for_status()
        df = pd.json_normalize(response.json())
        df['time'] = pd.to_datetime(df.timestamp, unit='s')
        start = datetime.now() - timedelta(days=lookback)
        return df[df.time > start].copy()
    
    def get_volume(self, token, lookback=7):
        df = self.get_transactions(token, lookback=lookback, op='SWAP')
        return df['state_change.xch'].abs().sum().astype('float') / 1e12
        
        
class Pair:
    """
    Get information about a particular asset pair.
    
    Assumes a token is paired with XCH.
    """
    
    def __init__(self, pairs, token_short_name):
        self.pairs = pairs
        self.token = token_short_name
        self.launcher_id = pairs.get_launcher_id(self.token)
        
    def refresh(self):
        self.pairs.refresh()
        # Will also need to refresh any token-specific caches, but there aren't any yet
        
    def get_transactions(self, lookback=7, op=None, limit=None):
        return self.pairs.get_transactions(self.token, lookback=7, op=op, limit=limit)
        
    def get_volume(self, lookback=7):
        return self.pairs.get_volume(self.token, lookback)
    
    def get_xch_reserve(self):
        return self.pairs.get_xch_reserve(self.token)

    def get_token_reserve(self):
        return self.pairs.get_token_reserve(self.token)

    def get_liquidity(self):
        return self.pairs.get_liquidity(self.token)

    def get_periodic_yield(self, lookback=7):
        return self.get_volume(lookback) * 0.0035 / self.get_xch_reserve()
    
    def get_annualized_yield(self, lookback=7):
        return (1 + self.get_periodic_yield(lookback)) ** (365.25 / lookback) - 1
    
    def get_price_impact_threshold(self, impact=0.02):
        return impact * self.get_xch_reserve() / 2
    
    def get_recovery_period(self, size=1, unit=7):
        return (2 * size / self.get_xch_reserve()) / self.get_periodic_yield(lookback=unit)

    def get_neutral_price(self):
        if self.token == 'USDS':
            return self.get_token_reserve/self.get_xch_reserve()
        else:
            return self.get_xch_reserve()/self.get_token_reserve()

    def get_inverse_price(self):
        return 1. / self.get_neutral_price()

    def get_xch_value_of_liquidity_units(self, n=1):
        return 2. * n * self.get_xch_reserve() / self.get_liquidity()
