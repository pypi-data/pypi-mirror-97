"""
logo.py

Created by Luca Camerani at 10/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    mu = 0
    sigma = 0.2
    n = 10000

    x = np.random.normal(mu, sigma, n)
    y = np.random.normal(mu, sigma, n)

    fig, axs = plt.subplots(2, figsize=(4, 5), gridspec_kw={'height_ratios': [3, 1]})

    axs[0].set(aspect='equal')
    axs[0].scatter(x, y, alpha=.2)
    axs[0].axis('off')

    axs[1].text(.5, .05, "EcoFin", fontsize=40, ha='center', color="0.3")
    axs[1].axis('off')

    #plt.show()
    plt.savefig("../EcoFin/LOGO.svg", transparent=True)
