"""
intertemp_test.py

Created by Luca Camerani at 10/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np
import time

from datetime import datetime
from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.stat.utils import weightedAvg, weightedStd

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=None)

date1 = 1551398400
date2 = 1554076800

print("Query for dates: \n * {}\n * {}\n\n".format(date1, date2))

# ----------------------------------------------------------
start = time.time()

for now in range(date1, date2, 86400): # Go on, day by day
    print('Try with: {}'.format(datetime.utcfromtimestamp(now).strftime('%a %d-%m-%Y')))
    try:
        optionManager.setNow(now)

        i = 0   # <- Time To Maturity curve
        exp = optionManager.getExpirations()[i]
        optionChain = optionManager.getOptionChain(exp=exp)

        print("-------- {}: [{} → {}] --------\n\n".format(datetime.utcfromtimestamp(now).strftime('%a %d-%m-%Y'),
                                     datetime.utcfromtimestamp(optionChain.getChainDate()).strftime('%a %d-%m-%Y'),
                                     datetime.utcfromtimestamp(optionChain.getChainExpiration()).strftime('%a %d-%m-%Y')))


        """
        ticker_info = ticker.getInfo()

        forwardPrice = optionChain.getForwardPrice()

        deepOptionChain = DeepOptionChain(optionChain)
        data = deepOptionChain.getDeepOptionChain()

        data['weights'] = data.loc[:, ['openInterest_call', 'openInterest_put']].sum(axis=1) / \
                          np.nansum(data.loc[:, ['openInterest_call', 'openInterest_put']].to_numpy())

        summary = {'Mean': weightedAvg(data['spreadSummary'], data['weights']),
                   'Std': weightedStd(data['spreadSummary'], data['weights'])}
        #print(' → {}: {}'.format(now, summary))
        """
    except:
        print("-------- Exception: no data found for the date --------\n\n")
        pass

print('Total time: {}'.format(time.time() - start))
