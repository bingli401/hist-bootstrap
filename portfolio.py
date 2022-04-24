#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 22:51:21 2022

@author: bingli
"""

import pandas as pd
from DataHandling import DataHandling

class EqPortfolio:
    
    def __init__(self, balance_current, portfolio_comp, price_current, retn_hist):
        #self.security_name = []
        self.balance = balance_current
        self.components = portfolio_comp
        #self.weights = weights_current
        self.price = price_current
        #self.fx = fx_current
        self.retn_hist = retn_hist
        #self.return_hist = pd.DataFrame()
        #self.fx_hist = pd.DataFrame()
        
        
    def adjust_fx_return(self):
       # assert self.retn_hist.columns == self.components['Ticker']
       for i, security in enumerate(self.components['Ticker'].tolist()):
           fx_ticker = self.components.iloc[[i]]['FX Ticker'].tolist()
           if not pd.isnull(fx_ticker):
               #pd.DataFrame(df.values*df2.values, columns=df.columns, index=df.index)
               #adjusted return = (p_t * fx_t ) / (p_t-1 * fx_t-1) - 1
               self.retn_hist[[security]] = (self.retn_hist[[security]].values + 1) * (self.retn_hist[fx_ticker].values + 1) - 1
       
        
        
        
        
        
        
    