"""
tmp.py

Created by Luca Camerani at 29/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import time
import concurrent.futures
from tqdm import tqdm

def f(x):
    time.sleep(0.001)  # to visualize the progress
    return x**2

def run(f, my_iter):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(f, my_iter), total=len(my_iter)))
    return results

my_iter = range(100000)
run(f, my_iter)
