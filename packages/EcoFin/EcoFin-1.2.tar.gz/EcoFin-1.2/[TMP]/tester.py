"""
tester.py

Created by Luca Camerani at 08/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import json

from EcoFin.dataDownload.ticker import Ticker
from EcoFin.dataDownload.optionsManager import OptionManager

ticker = Ticker('MSFT')
opt_manager = OptionManager(ticker)

#data = opt_manager.downloadOptionChain()
#data = opt_manager.getExpirations()
opt_chain = opt_manager.getOptionChain()
print(opt_chain.getSummary())

#opt_chain.getChain().calls.to_excel('tmp.xlsx')
