#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 23:39:26 2022

@author: bingli
"""
import random
import numpy as np
import pandas as pd
from DataHandling import DataHandling
from portfolio import EqPortfolio

class HistSimulation:
    
    def __init__(self, portfolio, num_sim, num_stitches, subwindow_length):
        self.portfolio = portfolio
        self.num_sim = num_sim
        self.num_stitches = num_stitches
        self.tot_timesteps = portfolio.retn_hist.shape[0]
        self.subwindow_length = subwindow_length
        self.bootstrap_indices = []
        
        
    def hist_bootstrap(self):
        self.bootstrap_indices = [self.hist_bootstrap_onepath() for j in range(self.num_sim)]
        
        
        
    def hist_bootstrap_onepath(self):
        if self.tot_timesteps > self.subwindow_length:            
            population = range(self.tot_timesteps - self.subwindow_length)
            indx_start = random.sample(population, self.num_stitches)
        
        elif self.tot_timesteps == self.subwindow_length:
            indx_start = [0]
        else:
            raise Exception('>>> Error: tot_timesteps cannot be smaller than subwindow_length.')
            
        l = []
        [l.extend(list(range(x, x+self.subwindow_length))) for x in indx_start]
        
        return l
        
    def hist_simulation(self):
        #for s, security in enumerate(self.portfolio.components['Ticker']):
        #    balance_security = self.portfolio.balance * self.portfolo.components.iloc[[s]]['Weight'] 
        cum_retns_port = []
        for i, bootstr_index in enumerate(self.bootstrap_indices):
            # get all the weights of securities and save it to a matrix of num x 1
            weights = self.portfolio.components[['Weights']]
            
            # get all the returns of securities based on bootstrap indices
            # filter only security return and make sure the order
            retns = self.portfolio.retn_hist.iloc[bootstr_index][self.portfolio.components['Ticker'].tolist()]
            
            # compute cumulative return
            cum_retns = DataHandling.cumulative_return(retns)
            
            # The order of weights and return should already be in line
            # matrix multiplication of cum_retns * weights, which will be the total potfolio cumulative return
            cum_retns_port.append(np.dot(cum_retns, weights).flatten())
        

        return cum_retns_port
        

    def rolling_hist(self, time_window):
        cum_retns_port = []
        for i in range(0, self.tot_timesteps-time_window):
            weights = self.portfolio.components[['Weights']]
            retns = self.portfolio.retn_hist.iloc[i:(i+time_window-1)][self.portfolio.components['Ticker'].tolist()]
            cum_retns = DataHandling.cumulative_return(retns)
            cum_retns_port.append(np.dot(cum_retns, weights).flatten())
            
            
        return cum_retns_port
    
    
    
    def risk_report(self, cum_retns):
        # pick the last day's return from each simulation
        one_year_end_retn_dist = []
        [one_year_end_retn_dist.append(one_year_cum_retn[-1] - 1) for one_year_cum_retn in cum_retns]
        
        etl_99pct = RiskMetrics.etl(one_year_end_retn_dist, 0.01)
        basic_stats_retn = RiskMetrics.basic_stats(one_year_end_retn_dist)
        print('ETL 99% : ' + str(etl_99pct))
        print('Mean : ' + str(basic_stats_retn['mean']))
        print('stdev : ' + str(basic_stats_retn['stdev']))
    
        # alternative tail risk - etl of maximum lost
        one_year_maxloss_dist = []
        [one_year_maxloss_dist.append(np.min(one_year_cum_retn-1)) for one_year_cum_retn in cum_retns]
    
        etl_maxloss_99pct = RiskMetrics.etl(one_year_maxloss_dist, 0.01)
        basic_stats_maxloss = RiskMetrics.basic_stats(one_year_maxloss_dist)
        print('ETL max-loss 99% : ' + str(etl_maxloss_99pct))    
        print('Mean : ' + str(basic_stats_maxloss['mean']))
        print('stdev : ' + str(basic_stats_maxloss['stdev']))
    
        
class RiskMetrics:
    @staticmethod
    def etl(retn_distribution, tail_pct):
        d = int(np.floor(len(retn_distribution) * tail_pct))
        retn_distribution.sort()
        return np.average(retn_distribution[0:d])
    @staticmethod    
    def basic_stats(retn_distribution):
        mean = np.average(retn_distribution)
        stdev = np.std(retn_distribution)
        return {'mean': mean, 'stdev': stdev}
        
        
    