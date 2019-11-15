# coding=utf-8

"""
Script para hacer los test de la librería pynance.
"""

import numpy as np
import pandas as pd
import pynance as fy

def main():
    """Main function"""

    arrays = {}
    for i in range(10):
        arr = 0.05*np.random.random(100) - 0.02
        arrays["serie_{0}".format(i)] = arr

    returns = pd.DataFrame(arrays, index=[i for i in range(100)])

    port = fy.Portfolio(returns)
    port.efficient_frontier()

if __name__ == "__main__":
    main()

