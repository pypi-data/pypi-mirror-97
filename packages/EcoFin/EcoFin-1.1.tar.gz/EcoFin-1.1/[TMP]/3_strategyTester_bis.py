"""
10_strategyTester.py

Created by Luca Camerani at 27/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tqdm import tqdm

# -------------------------[Set-up]-------------------------
ticker_list = [line.rstrip('\n') for line in open(r'../INDEXs/DJIA.txt')]
maturity_min = 15

base_path = r'../Export/BackTest'
start_date = 0
weights = 'OI'
# ----------------------------------------------------------

output = {}
portfolio = {'bench_ret': pd.DataFrame(), 'strategy': pd.DataFrame(), 'strategy_ret': pd.DataFrame()}
for tick in tqdm(ticker_list, desc='Compute backtest strategy'):
    try:
        # Import data and clean-up
        data = pd.read_excel(r'{}/{}/backTest_[{}].xlsx'.format(base_path, tick, maturity_min), engine='openpyxl')
        data = data.loc[data['Date'] >= start_date, ~data.columns.str.contains('^Unnamed')]
        data.set_index(pd.to_datetime(data['Date'], format='%Y%m%d'), inplace=True)

        # Normalize indicators
        for t, row in data.iterrows():
            data.loc[t, 'OPS_Norm'] = data.loc[t, 'OPS_[{}]'.format(weights)] - data.loc[data.index < t,
                                                                                'OPS_[{}]'.format(weights)].mean()
            data.loc[t, 'IVS_Norm'] = data.loc[t, 'IVS_[{}]'.format(weights)] - data.loc[data.index < t,
                                                                                'IVS_[{}]'.format(weights)].mean()
            data.loc[t, 'PCD_Norm'] = data.loc[t, 'PCD'] - data.loc[data.index < t, 'PCD'].mean()
            data.loc[t, 'OIR_Norm'] = data.loc[t, 'OIR_[{}]'.format(weights)]

        # Create signals framework
        signals = pd.DataFrame(
            columns=['SpotPrice', 'OPS_signal', 'IVS_signal', 'OIR_signal', 'PCD_signal', 'LnReturn', 'strategy'], index=data.index)

        signals['SpotPrice'] = data['SpotPrice']
        signals['LnReturn'] = np.log(data['SpotPrice'].shift(-1) / data['SpotPrice'])
        
        factor = {'buy': 1,
                  'sell': -1} # by putting 0 is buy-only

        signals.loc[data['OPS_Norm'] > 0, 'OPS_signal'] = factor['buy']
        signals.loc[data['OPS_Norm'] <= 0, 'OPS_signal'] = factor['sell']

        signals.loc[data['IVS_Norm'] > 0, 'IVS_signal'] = factor['buy']
        signals.loc[data['IVS_Norm'] <= 0, 'IVS_signal'] = factor['sell']

        signals.loc[data['OIR_Norm'] > 0.5, 'OIR_signal'] = factor['buy']
        signals.loc[data['OIR_Norm'] <= 0.5, 'OIR_signal'] = factor['sell']

        signals.loc[data['PCD_Norm'] > 0, 'PCD_signal'] = factor['buy']
        signals.loc[data['PCD_Norm'] <= 0, 'PCD_signal'] = factor['sell']

        # Set-up force factor
        signals['force'] = data['VIX_[CBOE]']

        # Create strategy from signals and data
        # ⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕[STRATEGY SET-UP]⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕
        l = 8

        signals['strategy'] = signals['OPS_signal'] * signals['force']
        #signals['strategy'] = signals[['OPS_signal', 'IVS_signal', 'OIR_signal']].sum(axis=1) * signals['force']
        # ⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕

        # Add strategy returns
        portfolio['bench_ret'] = pd.concat([portfolio['bench_ret'], signals['LnReturn'].rename(tick)], axis=1)
        portfolio['strategy'] = pd.concat([portfolio['strategy'], signals['strategy'].rename(tick)], axis=1)

        output[tick] = pd.merge(data, signals, left_index=True, right_index=True)
    except Exception as e:
        print('\nError [{}]: {}'.format(tick, e))
        pass

# compute strategy global returns
portfolio['strategy_ret'] = portfolio['strategy'] * portfolio['bench_ret'] * l

fig, axs = plt.subplots(3, figsize=(15, 8), sharex=True)
fig.suptitle('Strategy tester', fontsize=16)

# Plot returns and signals
axs[0].set_title('Benchmark returns')
axs[1].set_title('Signals')
for tick in output.keys():
    axs[0].plot(np.cumsum(portfolio['bench_ret'][tick]), label=tick)
    axs[1].scatter(portfolio['strategy'][tick].index,
                   portfolio['strategy'][tick], alpha=.3, label=tick)

axs[0].set(ylabel=r'ln-returns ($X_t$)')
axs[0].legend(ncol=4)

# Plot strategy return vs. benchmark (portfolio)
axs[2].set_title('Portfolio returns')
axs[2].plot(np.cumsum(portfolio['bench_ret'].sum(axis=1)), label='Benchmark')
axs[2].plot(np.cumsum(portfolio['strategy_ret'].sum(axis=1)), label='Strategy')
axs[2].set(xlabel=r'Time ($t$)', ylabel=r'ln-returns ($X_t$)')
axs[2].legend()

# Compute performance metrics
SR_b = portfolio['bench_ret'].sum(axis=1).sum() / portfolio['bench_ret'].sum(axis=1).std()
SR_s = portfolio['strategy_ret'].sum(axis=1).sum() / portfolio['strategy_ret'].sum(axis=1).std()

print('Sharpe-Ratio:\n • Benchmark: {}\n • Strategy: {}'.format(SR_b, SR_s))

plt.show()
