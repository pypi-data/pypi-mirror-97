"""
surfaceFromDF.py

Created by Luca Camerani at 11/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm

dpu = pu[pu.Reputation < 5000]

X = dpu[['Age', 'TimeOnSite']]
y = dpu['Reputation']

X = sm.add_constant(X)
est = sm.OLS(y, X).fit()

xx1, xx2 = np.meshgrid(np.linspace(X.Age.min(), X.Age.max(), 100),
                       np.linspace(X.TimeOnSite.min(), X.TimeOnSite.max(), 100))

# plot the hyperplane by evaluating the parameters on the grid
Z = est.params[0] + est.params[1] * xx1 + est.params[2] * xx2

# create matplotlib 3d axes
fig = plt.figure(figsize=(12, 8))
ax = Axes3D(fig, azim=-115, elev=15)

# plot hyperplane
surf = ax.plot_surface(xx1, xx2, Z, cmap=plt.cm.RdBu_r, alpha=0.6, linewidth=0)

# plot data points - points over the HP are white, points below are black
resid = y - est.predict(X)
ax.scatter(X[resid >= 0].Age, X[resid >= 0].TimeOnSite, y[resid >= 0], color='black', alpha=0.4, facecolor='white')
ax.scatter(X[resid < 0].Age, X[resid < 0].TimeOnSite, y[resid < 0], color='black', alpha=0.4)

# set axis labels
ax.set_xlabel('Age')
ax.set_ylabel('TimeOnSite')
ax.set_zlabel('Reputation')
