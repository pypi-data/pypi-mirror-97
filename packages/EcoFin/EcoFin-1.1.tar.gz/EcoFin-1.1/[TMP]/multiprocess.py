"""
7_backTester.py

Created by Luca Camerani at 12/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import concurrent.futures
import os
import pandas as pd
import shutil

from datetime import datetime
from tqdm import tqdm
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.options.optionChainSynopsis import OptionChainSinopsys

# -------------------------[Set-up]-------------------------
ticker_list = ['AAPL', 'MSFT', 'CSCO', 'PM', 'BA', 'MS', 'FDX', 'AEP', 'PFE', 'SNPS']

# 1Y
date1 = 1546300800
date2 = 1577664000

# 1M
"""
date1 = 1546300800
date2 = 1548892800
"""

maturity_curve = 2
shift_returns = 1
# ----------------------------------------------------------

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
        for tick in ticker_list:
            e.submit(execute, tick)

def execute(tick: str):
    ticker = Ticker(tick)
    ticker_info = ticker.getInfo()

    optionManager = OptionManager(ticker)

    output = pd.DataFrame({'Date': [], 'Exp': [],
                           'Maturity': [], 'ForwardPrice': [], 'SpotPrice': [],
                           'OPS': [], 'OPS_Std': [],
                           'IVS': [], 'IVS_Std': [],
                           'NAP': []}, index=[])

    for now in tqdm(range(date1, date2, 86400), desc=tick): # Compute day by day
        try:
            optionManager.setNow(now)

            exp = optionManager.getExpirations()[maturity_curve]
            optionChain = optionManager.getOptionChain(exp=exp)

            ticker_info = ticker.getInfo()

            deepOptionChain = DeepOptionChain(optionChain, computeIV=True, progressBar=False)
            synopsis = OptionChainSinopsys(deepOptionChain)

            OPS = synopsis.computeOptionPriceSpread()
            IVS = synopsis.computeImpliedVolatilitySpread()
            NAP = synopsis.computeNoArbitragePrice()

            summary = {'Date': optionChain.getChainDate(),
                       'Exp': optionChain.getChainExpiration(),
                       'Maturity': optionChain.getTimeToMaturity().days,
                       'ForwardPrice': optionChain.getForwardPrice(),
                       'SpotPrice': optionChain.getSpotPrice(),
                       'OPS': OPS.mean,
                       'OPS_Std': OPS.std,
                       'IVS': IVS.mean,
                       'IVS_Std': IVS.std,
                       'NAP': NAP.value,
                       'NAP_Ret': NAP.ret,
                       }

            output = output.append(pd.DataFrame(summary, index=[datetime.utcfromtimestamp(optionChain.getChainDate())]))
        except:
            pass

    output['Return'] = (output['SpotPrice'].shift(-shift_returns) / output['SpotPrice'] - 1)

    # ----------------------[EXPORT BLOCK]--------------------------------
    path = '../Export/TESI/[{}]_({})'.format(ticker.ticker, ticker_info.longName)
    if not os.path.exists(path):
        os.makedirs(path)

    with pd.ExcelWriter('{}/intertempAnalysis_[{}].xlsx'.format(path, maturity_curve)) as writer:
        output.to_excel(writer, sheet_name='Results', index=False)
    # ----------------------[EXPORT BLOCK]--------------------------------

if __name__ == "__main__":
    main()
