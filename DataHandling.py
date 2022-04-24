#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 23:00:03 2022

@author: bingli
"""
import pandas as pd
import yfinance as yf
import logging


class DataHandling:
    @staticmethod
    def download_price(tickers, start_date, end_date):
        # tickers is a list of ticker
        # date is in format 'yyyy-mm-dd'
        # fetch the Close price only
        
        tickers_nonan = [x for x in tickers if pd.isnull(x) == False]
        
        data = yf.download(tickers_nonan, start=start_date, end=end_date)['Close']
        '''
        if():
            raise Exception()
        '''
        return data
        
    @staticmethod        
    def linear_return(price):
        # price is a dataframe
        # if price is 0, there will be na return, for now, simply drop
        retn = price.pct_change().dropna()
        return retn
        
    @staticmethod
    def cumulative_return(retn):
        # note the 1st time step's cumulative return is not 1 (not the current day)
        return (retn+1).cumprod()
    
    
               
        