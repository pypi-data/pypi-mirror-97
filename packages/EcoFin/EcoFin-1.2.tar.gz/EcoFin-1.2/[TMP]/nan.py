"""
nan.py

Created by Luca Camerani at 11/10/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np

a = np.full(5, np.nan)

print(len(a))
print(sum(np.isnan(a).astype(int)))
