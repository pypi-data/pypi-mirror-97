"""
IV.py

Created by Luca Camerani at 08/11/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""
import matplotlib.pyplot as plt

from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.blackScholesModel import BSM
from EcoFin.options.optionChain import OptionChain
from EcoFin.stat.interpolation import interpolateNaN

ticker = Ticker('MSFT')
optionChain = OptionChain(ticker)

r = optionChain.getRiskFreeRate()


ticker = optionChain.getTicker()
underliyngPrice = optionChain.getSpotPrice()
chain = optionChain.getChain()
date = optionChain.getDate()
maturity = optionChain.getMaturity()
strikeList = optionChain.getStikeList()
forwardPrice = optionChain.getForwardPrice()


contracts = chain.puts

IVs = []
for index, contract in contracts.iterrows():
    strike = contract['strike']
    marketPrice = contract['avgPrice']
    option = BSM(underliyngPrice, strike, r, None, maturity.days)

    IV = option.getImpliedVolatility(marketPrice, 'call')
    IVs.append(IV)

    print(' • Strike: {}'.format(strike))
    print(' • Underlying: {}'.format(underliyngPrice))
    print(' • Market Price: {}'.format(marketPrice))
    print(' • r: {}'.format(r))
    print(' • Maturity: {}'.format(maturity))
    print(' -> IV: {}'.format(IV))

fig, axs = plt.subplots(2)
axs[0].plot(contracts['strike'], interpolateNaN(IVs), label='computed')
axs[0].plot(contracts['strike'], contracts['impliedVolatility'], label='source')
axs[0].legend()

axs[1].plot(contracts['strike'], contracts['avgPrice'], label='Market Price')
