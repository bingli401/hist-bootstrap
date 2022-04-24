#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 22:51:21 2022

@author: bingli
"""

import pandas as pd
import numpy as np
import logging
from DataHandling import DataHandling

class EqPortfolio:
    # Equity portfolio class
    # Only suitable for equity alike portfolios 
    
    def __init__(self, balance_current, portfolio_comp, price_current, retn_hist):

        self.balance = balance_current
        self.components = portfolio_comp
        self.price = price_current
        self.retn_hist = retn_hist
        
        # simply not allow leverage
        if not np.sum(portfolio_comp['Weights']) == 1:
            logging.info('>>> Error: portfolio weights do not sum to 100%.')
            raise Exception('>>> Error: portfolio weights do not sum to 100%.')
        
    def adjust_fx_return(self):
        # loop through each security, if the security has FX ticker attached to it, adjust the return
        for i, security in enumerate(self.components['Ticker'].tolist()):
            fx_ticker = self.components.iloc[[i]]['FX Ticker'].tolist()
            if not pd.isnull(fx_ticker):
                #adjusted return = (p_t * fx_t ) / (p_t-1 * fx_t-1) - 1
                self.retn_hist[[security]] = (self.retn_hist[[security]].values + 1) * (self.retn_hist[fx_ticker].values + 1) - 1
       
        
        
        
        
        
        
    