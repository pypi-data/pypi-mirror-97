"""
plotColor.py

Created by Luca Camerani at 12/10/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np

size = 20

x = np.arange(0, size)
y = np.random.random(size)

plt.plot(x, y)

top = [x if x >= .8 else np.nan for x in y]
bottom = [x if x <= .2 else np.nan for x in y]

plt.plot(x, top, 'v', color='red')
plt.plot(x, bottom, '^', color='green')

plt.show()
