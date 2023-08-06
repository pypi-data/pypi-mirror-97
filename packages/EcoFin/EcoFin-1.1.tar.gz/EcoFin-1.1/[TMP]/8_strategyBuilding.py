"""
8_strategyBuilding.py

Created by Luca Camerani at 17/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tick = 'MSFT'
path = r"G:\Il mio Drive\Uni\ECOFIN\TESI\EcoFin Library\Export\BackTest\{}\intertempAnalysis_[5].xlsx".format(tick)

data = pd.read_excel(path, engine='openpyxl')

signal = 'OIR_[ATM]'
percentile = 0.85

for t, row in data.iterrows():
    data.loc[t, '{}_Norm'.format(signal)] = data.loc[t, signal]# - data.loc[0:t, signal].mean()
    data.loc[t, 'u_perc'] = np.percentile(data.loc[0:t, '{}_Norm'.format(signal)], percentile * 100)
    data.loc[t, 'l_perc'] = np.percentile(data.loc[0:t, '{}_Norm'.format(signal)], (1-percentile) * 100)

data['return'] = data['SpotPrice'].shift(-1) / data['SpotPrice'] - 1
data['logReturn'] = np.log(data['return'] + 1)

data['L_strategy'] = 0
data.loc[data['{}_Norm'.format(signal)] > 0, 'L_strategy'] = data['logReturn']

data['LS_strategy'] = 0
data.loc[data['{}_Norm'.format(signal)] > 0.5, 'LS_strategy'] = data['logReturn']
data.loc[data['{}_Norm'.format(signal)] <= 0.5, 'LS_strategy'] = -data['logReturn']

data['filter_strategy'] = 0
data.loc[data['{}_Norm'.format(signal)] >= data.u_perc, 'filter_strategy'] = data['logReturn']
data.loc[data['{}_Norm'.format(signal)] <= data.l_perc, 'filter_strategy'] = -data['logReturn']

print(data)

print(np.sum(data.logReturn))
print(np.sum(data.L_strategy))
print(np.sum(data.LS_strategy))
print(np.sum(data.filter_strategy))

plt.plot(data.index, np.cumsum(data.logReturn), label='Return')
plt.plot(data.index, np.cumsum(data.L_strategy), label='Long only')
plt.plot(data.index, np.cumsum(data.LS_strategy), label='Long and Short')
plt.plot(data.index, np.cumsum(data.filter_strategy), label='Percentile')
plt.legend()
