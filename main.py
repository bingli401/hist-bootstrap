#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 22:42:27 2022

@author: bingli
"""

import os
import argparse
import logging
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from portfolio import EqPortfolio
from DataHandling import DataHandling
from RiskEngine import HistSimulation
from RiskEngine import RiskMetrics

def main():
        
    # arguments
    val_date = '2022-03-31'
    portfolio_file = 'portfolio_input.txt'
    hist_start_date = '2017-01-01'
    hist_end_date = '2022-01-01'
    balance = 1000000000
    num_sim = 5000
    
    # read portfolio file
    
    portfolio_input = pd.read_csv(portfolio_file, sep='\t')
    
    # download raw data from yahoo finance
    
    tickers_all = portfolio_input['Ticker'].to_list()+portfolio_input['FX Ticker'].to_list()
    prices_hist = DataHandling.download_price(tickers=tickers_all, 
                                         start_date=hist_start_date, 
                                         end_date=val_date)
    
    # filling missing data (using basic forward fill ) 
    # and then remvoe remaining na (first few rows if there is nan)
    [prices_hist[col].fillna(method='ffill', inplace=True) for col in prices_hist.columns.to_list()]
    prices_hist.dropna(inplace=True)
    
    
    prices_current = prices_hist.loc[[val_date],]
    prices_hist = prices_hist.loc[hist_start_date:hist_end_date,]
    

    
    # non FX adjusted
    retn_hist = DataHandling.linear_return(prices_hist)

    
    
    # create my portfolio 
    myPort = EqPortfolio(balance_current=balance,
                         portfolio_comp=portfolio_input,
                         price_current = prices_current,
                         retn_hist = retn_hist)
    
    myPort.adjust_fx_return()
    
    # create my risk engine
    myRiskEngine = HistSimulation(portfolio=myPort, 
                                  num_sim=num_sim, 
                                  num_stitches=4, 
                                  subwindow_length=65)
    
    myRiskEngine.hist_bootstrap()
    cum_retns = myRiskEngine.hist_simulation()
    
    myRiskEngine.risk_report(cum_retns)
    
    # rolling 
    print('\nrolling: \n')
    cum_retns_roll = myRiskEngine.rolling_hist(260)
    myRiskEngine.risk_report(cum_retns_roll)    
    
    
    
    print()
if __name__ == "__main__":
    main()



    
    