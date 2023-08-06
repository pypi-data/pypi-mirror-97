"""
doublePlot.py

Created by Luca Camerani at 04/10/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np

x = range(1, 4)

fig, axs = plt.subplots(2)
fig.suptitle('Vertically stacked subplots')

for i in range(1, 10):
    axs[0].plot(x, np.random.rand(len(x)))
axs[1].plot(x, np.random.rand(len(x)))
