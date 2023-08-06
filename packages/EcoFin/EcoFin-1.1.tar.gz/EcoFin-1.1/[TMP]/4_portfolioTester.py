"""
4_portfolioTester.py

Created by Luca Camerani at 07/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

from EcoFin.assetAllocation.performance import Performance
from EcoFin.utils import utils

# -------------------------[Set-up]-------------------------
ticker_list = [line.rstrip('\n') for line in open(r'../Tesi/INDEXs/DJIA.txt')]
maturity_min = 15

base_path = r'../Tesi/Export/BackTest_C'
start_date = 0

# Strategy set-up
direction = 'OPS_[OI]'      # Direction driver
force = None#'VIX_[CBOE]'        # In None, don't use force driver
polarize = False             # True or False: polarize direction component
buy_only = True             # Set a buy only strategy that ignore negative signals

# Portfolio set-up
w_limit = 5           # Rank best N ticker based on strategy
leverage = None     # Strategy leverage (1 is no leverage, None is auto-compensation)
# ----------------------------------------------------------

base = ['SpotPrice']
data = {b: {} for b in base + [direction, force]}
if None in data.keys():
    del data[None]

for tick in tqdm(ticker_list, desc='Importing data'):
    try:
        # Import data and clean-up
        source = pd.read_excel(r'{}/{}/backTest_[{}].xlsx'.format(base_path, tick, maturity_min), engine='openpyxl')
        source = source.loc[source['Date'] >= start_date, ~source.columns.str.contains('^Unnamed')]
        source.set_index(pd.to_datetime(source['Date'], format='%Y%m%d'), drop=True, inplace=True)

        for driver in data.keys():
            data[driver][tick] = source[driver]
    except:
        pass

# Merge (concatenate) data and create dataframes
for driver in data.keys():
    data[driver] = pd.concat(data[driver], axis=1)

    # ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌[Normalize direction data]❌❌❌❌❌❌❌❌❌❌❌
    if driver == direction:
        data[driver] = data[driver].sub(data[driver].mean(axis=1), axis=0)
    # ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌

# Generate strategy signals
# ⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕[SET-UP]⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕
if polarize:
    limit = 0 if buy_only else -1
    data[direction] = utils.polarizeTable(data[direction], under=limit)

if force is None:
    force_v = 1
else:
    force_v = data[force]

data['signals'] = data[direction] * force_v
# ⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕[SET-UP]⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕

if w_limit is not None:
    mask = pd.DataFrame(np.sort(data['signals'].values, axis=1), index=data['signals'].index,
                        columns=data['signals'].columns).iloc[:, -w_limit]
    data['signals'] = (data['signals'] >= pd.DataFrame(
        data=np.array([mask, ] * data['signals'].shape[1]).T,
        index=data['signals'].index,
        columns=data['signals'].columns)).astype(int)
    data['signals'][data['signals'] > 0] = 1

if buy_only:
    data['signals'][data['signals'] < 0] = 0

# Compute weights
data['weights'] = data['signals'].div(data['signals'].abs().sum(axis=1), axis=0)

# Compute ln-returns of benchmark and strategy
if leverage is None: leverage = data['SpotPrice'].shape[1]
data['lnReturns'] = np.log(data['SpotPrice'].shift(-1) / data['SpotPrice'])
data['strategy'] = data['lnReturns'] * data['weights'] * leverage

# Compute performance metrics
performance = Performance(data['lnReturns'].mean(axis=1), data['strategy'].mean(axis=1), r=0.019)
performance.printPerformanceSummary()

# =====================================================================================
#                       FROM HERE NO DATA MANIPULATION
# =====================================================================================

# Create plot framework
fig, axs = plt.subplots(2, figsize=(15, 8), sharex=True)
fig.suptitle('Strategy tester', fontsize=16)

# Plot strategy return vs. benchmark (data)
axs[0].set_title('data returns')
axs[0].plot(data['lnReturns'].mean(axis=1).cumsum(), label='Benchmark')
axs[0].plot(data['strategy'].mean(axis=1).cumsum(), label='Strategy')
axs[0].set(ylabel='Cumulated ln-returns ($X_t$)')
axs[0].legend()

# Plot number of assets in portfolio
ax2 = axs[0].twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:gray'
ax2.set_ylabel('Assets count', color=color)  # we already handled the x-label with ax1
ax2.plot(data['weights'].index, data['weights'].ne(0).sum(axis=1), linewidth=.5, color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Plot evolution of weights
positive = data['weights'][data['weights'] >= 0].fillna(0)
negative = data['weights'][data['weights'] < 0].fillna(0)

axs[1].set_title('Weights evolution')
axs[1].stackplot(data['weights'].index, positive.T)
axs[1].stackplot(data['weights'].index, negative.T)
axs[1].plot(data['weights'].sum(axis=1), linewidth=1, linestyle="dotted",
            color='black', alpha=.6, label='Avg. ($\mu$)')
axs[1].set(xlabel=r'days ($t$)', ylabel=r'data weights')

axs[1].legend()

with pd.ExcelWriter('{}/portfolio.xlsx'.format(base_path)) as writer:
    data['lnReturns'].to_excel(writer, sheet_name='lnReturns', index=True)
    data['signals'].to_excel(writer, sheet_name='Signals', index=True)
    data['weights'].to_excel(writer, sheet_name='Weights', index=True)
    data['strategy'].to_excel(writer, sheet_name='Strategy', index=True)

plt.show()
