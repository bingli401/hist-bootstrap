#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 22:42:27 2022

@author: bingli
"""

import os
import getpass
import argparse
import logging
import numpy as np
import pandas as pd
from datetime import date
from portfolio import EqPortfolio
from DataHandling import DataHandling
from RiskEngine import HistSimulation

def main():
    
    # define main's arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--valdate', type=str, default='2022-03-31', help='valuation date in yyyy-mm-dd.')
    parser.add_argument('--portfolio', type=str, default='portfolio_input.txt', help='A file containing necessary portfolio information. ')
    parser.add_argument('--startdate', type=str, default='2017-01-01', help='Start date of historical data used for historical simulation.')
    parser.add_argument('--enddate', type=str, default='2022-01-01', help='End date of historical data used for historical simulation in yyyy-mm-dd.')
    parser.add_argument('--balance', type=float, default=1000000000, help='Notional of the portfolio as of valuation date in yyyy-mm-dd.')
    parser.add_argument('--numsim', type=int, default=5000, help='Number of simulations.')
    parser.add_argument('--conflvl', type=float, default=0.99, help='Confidence level for risk metrics.')
    
    args = parser.parse_args()
    
    val_date = args.valdate
    portfolio_file = args.portfolio
    hist_start_date = args.startdate
    hist_end_date = args.enddate
    balance = args.balance
    num_sim = args.numsim
    confidence_lvl = args.conflvl
    
    # set up the logging
    dir_path = os.path.dirname(os.path.realpath(__file__))
    datestr = date.today().strftime('%Y%m%d')
    logging.basicConfig(level=logging.INFO,
                        datefmt='%m-%d %H:%M',
                        filename=dir_path+'/log_' + datestr + '.log',
                        filemode='w')
    console = logging.StreamHandler()
    #console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)-6s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
    
    logging.info('=============== Program starts ===================')
    logging.info('>>> OS user: '+ getpass.getuser())
    logging.info('>>> Valuation date: '+ val_date)
    logging.info('>>> Hist start date: '+ hist_start_date)
    logging.info('>>> Hist end date: '+ hist_end_date)
    logging.info('>>> Portfolio file: '+ portfolio_file)
    logging.info('>>> Portfolio balance: '+ str(balance))
    
    # read portfolio file
    logging.info('>>> Read portfolio file: ' + portfolio_file)
    portfolio_input = pd.read_csv(portfolio_file, sep='\t')
    
    # download raw data from yahoo finance
    logging.info('>>> Download data from yahoo finance and compute return.')
   
    tickers_all = portfolio_input['Ticker'].to_list()+portfolio_input['FX Ticker'].to_list()
    prices_hist = DataHandling.download_price(tickers=tickers_all, 
                                         start_date=hist_start_date, 
                                         end_date=val_date)
    

    
    
    prices_current = prices_hist.loc[[val_date],]
    prices_hist = prices_hist.loc[hist_start_date:hist_end_date,]
    

    
    # not FX adjusted
    retn_hist = DataHandling.linear_return(prices_hist)


    # create my portfolio 
    myPort = EqPortfolio(balance_current=balance,
                         portfolio_comp=portfolio_input,
                         price_current = prices_current,
                         retn_hist = retn_hist)
    # adjust fx in return
    myPort.adjust_fx_return()

    logging.info('>>> Construct my portfolio succefully.')
    
    # create my risk engine
    logging.info('>>> Running Risk Engine - might take a few seconds to min.')

    myRiskEngine = HistSimulation(portfolio=myPort, 
                                  num_sim=num_sim, 
                                  num_stitches=4, 
                                  subwindow_length=65,
                                  confidence_lvl=confidence_lvl)
    
    myRiskEngine.hist_bootstrap()
    cum_retns = myRiskEngine.hist_simulation()

    logging.info('>>> Running Risk Engine - Done.')
    logging.info('>>> Risk Reporting:')
    
    myRiskEngine.risk_report(cum_retns)
    
    # rolling 
    logging.info('>>> For justification purpose only:')
    cum_retns_roll = myRiskEngine.rolling_hist(260)
    myRiskEngine.risk_report(cum_retns_roll)    
    
    logging.info('=============== Program completed ===================')
if __name__ == "__main__":
    main()



    
    