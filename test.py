"""xº
Script para hacer los test de la librería pynance.
"""

import pynance as fy

def main():
    """Realizar los test"""
    #Características del instrumento A.
    r_a = 0.1
    sd_a = 0.12

    #Características del instrumeno B
    r_b = 0.25
    sd_b = 0.3

    #Peso del instrumento A en el portafolio
    weights = 0.1
    corr = -1

    stock_a = fy.Asset(r_a, sd_a)
    stock_b = fy.Asset(r_b, sd_b)

    portfolio = fy.Portfolio(stock_a, stock_b, weights, corr)
    figure = portfolio.show_yields([-1, -0.75, -0.2, 0.4, 1])
    figure.savefig("images/yields.png")
    print(portfolio.description())

if __name__ == "__main__":
    main()
