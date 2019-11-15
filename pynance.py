"""
Creación de objetos financieros como los son los bonos y las acciones, además se crea
el objeto Portfolio en el que se mostrará características básicas.
"""

import scipy.optimize as sco
import matplotlib.pyplot as plt
import numpy as np

class Portfolio:
    """Clase que contiene toda la cartera de activos"""

    def __init__(self, returns):

        self.returns = returns
        self.cols_num = returns.shape[1]
        self.cov = returns.cov()
        self.corr = returns.corr()

    def return_avg(self, weights):
        """Calcula el retorno del portafolio"""
        return_port = weights @ self.returns.transpose()
        return np.sum(return_port)

    def risk(self, weights):
        """Calcula el riesgo del portafolio"""

        risk = weights @ self.cov @ weights.transpose()
        return np.sqrt(risk)

    def sharpe_ratio(self, weights):
        """Calcula el ratio de sharpe
        S = return / std"""

        return self.return_avg(weights) / self.risk(weights)

    def min_variance(self):
        """Calcula los pesos que resultan en el mínimo riesgo para el
        inversionista"""

        bounds = [(0, 1) for i in range(self.cols_num)]
        constr = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})

        result = sco.minimize(self.risk,
                              x0=self.cols_num * [1. / self.cols_num],
                              bounds=bounds,
                              method='SLSQP',
                              constraints=constr)

        return result['x']

    def max_return(self):
        """Calcula la cartera que brinda el máximo retorno al
        inversionista"""

        bounds = [(0, 1) for i in range(self.cols_num)]
        constr = ({"type": "eq", "fun": lambda x: 1 - np.sum(x)})

        result = sco.minimize(lambda x: -self.return_avg(x),
                              x0=self.cols_num * [1. / self.cols_num],
                              bounds=bounds,
                              method='SLSQP',
                              constraints=constr)

        return result['x']

    def max_sharpe_ratio(self):
        """Calcula los pesos que brindan el mayor índice de sharp
        S = return_avg / std"""

        bounds = [(0, 1) for i in range(self.cols_num)]
        constr = ({"type": "eq", "fun": lambda x: 1 - np.sum(x)})
        result = sco.minimize(lambda x: -self.sharpe_ratio(x),
                              x0=self.cols_num * [1. / self.cols_num],
                              bounds=bounds,
                              method='SLSQP',
                              constraints=constr)

        return result["x"]

    def efficient_frontier(self, show=True):
        """Retorna la frontera eficiente y si se desea graficarla"""

        w_shr = self.max_sharpe_ratio()
        ret_sh = self.return_avg(w_shr)
        std_sh = self.risk(w_shr)

        w_min = self.min_variance()  # Los pesos para obtener la mínima varianza
        w_max = self.max_return()  # Los pesos para el máximo retorno.

        # Retorno del peso de mínima varianza.
        ret_min = self.return_avg(w_min)
        ret_max = self.return_avg(w_max)  # Retorno del peso de máximo retorno.

        ran_ret = np.linspace(ret_min, ret_max)
        bounds = [(0, 1) for i in range(self.cols_num)]
        ran_std = np.zeros((50, 1))

        for i, ret in enumerate(ran_ret):
            constr = ({"type": "eq",
                       "fun": lambda x, y=ret: self.return_avg(x) - y},
                      {"type": "eq",
                       "fun": lambda x: np.sum(x) - 1})

            w_i = sco.minimize(self.risk,
                               x0=self.cols_num * [1. / self.cols_num],
                               method='SLSQP',
                               bounds=bounds,
                               constraints=constr)["x"]

            ran_std[i] = self.risk(w_i)

        ret, std = self.random_portfolios(5000, show=False)

        if show:
            plt.scatter(std,
                        ret,
                        s=10,
                        label="Portafolios aleatorios")
            plt.scatter(ran_std[0], ret_min, marker="*",
                        s=400, label="Mínima varianza")
            plt.scatter(std_sh, ret_sh, marker="*", s=400,
                        label="Máximo ratio de Sharpe")
            plt.scatter(ran_std[-1], ret_max, marker="*",
                        s=400, label="Máximo retorno")
            plt.plot(ran_std,
                     ran_ret,
                     linestyle="--",
                     linewidth=3,
                     color="black",
                     label="Frontera eficiente")

            plt.xlabel("Volatilidad")
            plt.ylabel("Retorno promedio")
            plt.title("Frontera eficiente del portafolio")
            plt.legend()
            plt.show()

        return ran_std

    def random_portfolios(self, num_portfolio, show=True):
        """Generater random weights to create portfolios and plot
        in a graphic"""

        random_ws = list()

        # Genera pesos aleatorios cuya suma es igual a 1.
        for _ in range(num_portfolio):
            r_w = np.random.random(self.cols_num)
            r_w /= np.sum(r_w)
            random_ws.append(r_w)

        random_ws = np.array(random_ws)

        # Obtiene tanto los retornos promedios y la volatilidad de cada peso
        # aleatorio generado.
        ret_random = list(map(self.return_avg, random_ws))
        std_random = list(map(self.risk, random_ws))

        if show:
            plt.scatter(std_random, ret_random)
            plt.title("Perfomance de portafolios aleatorios")
            plt.show()

        return ret_random, std_random
