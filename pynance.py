"""
Creación de objetos financieros como los son los bonos y las acciones, además se crea
el objeto Portfolio en el que se mostrará características básicas.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style

style.use("seaborn")

class Bond:
    """Creación del bono en el que se necestia el valor nominal del bono, la tasa de
    interés con el que se trabajará con el bono, la tasa cupón del bono y el tiempo
    por el cual estará funcionando el bono

    Keyword arguments:

    vn: Valor Nominal, puede ser de tipo 'int' o 'float'.

    r: Tasa de interés, el valor tiene que estar en puntos decimales y no en valor
    porcentual.

    rc: Tasa cupón cuyo valor debe estar en puntos decimales y no en valor porcentual.

    t: Tiempo del bono que debe ser de tipo 'int'.

    Nota:
        Se deben introducir los valores ya estando en el mismo nivel de tiempo, si un
        valor ya es anual, los demas valores también deben estar anualizados.
    """

    def __new__(cls, vn, r, rc, t):
        if not isinstance(vn, (int, float)):
            raise ValueError("El Valor Nominal del bono debe ser 'int' o 'float'.")
        if not isinstance(t, (int, float)):
            raise ValueError("El tiempo debe ser un valor de tipo 'int' o 'float'.")
        if not isinstance(r, (int, float)):
            raise ValueError("La tasa de interés debe ser 'int' o 'float'.")
        if not isinstance(rc, (int, float)):
            raise ValueError("La tasa cupón debe ser 'int' o 'float'.")

        return object.__new__(cls)

    def __init__(self, vn, r, rc, t):

        self.__vn = vn
        self.__r = r
        self.__rc = rc
        self.__t = t

    def get_val_nom(self):
        """Retorna el Valor Nominal del bono"""
        return self.__vn

    def get_int_rate(self):
        """Retorna la tasa de interés del bono"""
        return self.__r

    def get_cupon_rate(self):
        """Retorna la tasa cupón del bono"""
        return self.__rc

    def get_time(self):
        """Retorna el tiempo por el cual estará vigente el bono"""
        return self.__t

    def price(self):
        """Retorna el precio del bono"""
        _va = 0
        cupon = self.__rc * self.__vn

        for i in range(1, self.__t+1):
            _va += cupon/(1+self.__r)**i

        _va += self.__vn * (1+self.__r)**(-self.__t)
        return _va

    def duration(self):
        """Retorna la duración de un bono"""
        dur = 0
        cupon = self.__rc * self.__vn

        for i in range(1, self.__t+1):
            dur += i*(cupon/(1+self.__r)**i)

        dur += (self.__t * self.__vn)/(1+self.__r)**self.__t
        dur *= 1/self.price()
        return dur

    def dur_mod(self):
        """Retorna la duración modificada del bono"""
        duration = self.duration()
        dmod = duration/(1+self.__r)
        return dmod

    def convexidad(self):
        """Retorna la convexidad del bono"""
        cupon = self.__rc * self.__vn
        deriv2 = 0

        for time in range(1, self.__t+1):
            deriv2 += time*(time+1)*cupon/(1+self.__r)**(time+2)

        deriv2 += self.__vn * self.__t * (self.__t+1)/(1+self.__r)**(self.__t+2)
        deriv2 *= 1/self.price()
        return deriv2

    def var_price(self, new_rate, method=None):
        """Obtención de la variación del precio del bono ante una cambio en la variable
        tasa de interés

        Keywrod arguments:

        new_rate: Nueva tasa de interés en puntos decimales.

        method: Se determina de qué manera se quiere obtener la variación del precio, ya sea por
        el método convencional, por medio de la duración del bono o usando la convexidad del bono

            method puede tomar lo siguientes valores:
            - No tomarlo en cuenta y se da el método convencional de variación de precios.
            - method = 'dur_mod', que usa la duración del bono.
            - method = 'Dm-Conv', que usa la convexidad del bono.
        """
        new_bond = Bond(self.__vn, new_rate, self.__rc, self.__t)
        p_0 = self.price()

        if method is None:
            p_1 = new_bond.price()
            vprice = (p_1 - p_0)/p_0

        elif method == 'dur_mod':
            vrate = new_rate - self.__r
            vprice = -self.dur_mod()*vrate

        elif method == 'Dm-Conv':
            vrate = new_rate - self.__r
            conv = self.convexidad()
            vprice = -self.dur_mod()*vrate + 0.5*conv*(vrate)**2

        return vprice

class Asset:
    """Objeto que crea una acción.

    Nota:
        Está en desarrollo.
    """

    def __init__(self, rend, desv):
        self.rend = rend
        self.desv = desv

class Portfolio:
    """Objeto que crea un portafolio básico compuesto de dos intrumentos financieros
    puede ser un bono o una acción

    Keyword arguments:

    instr1: Puede ser de la clase 'Asset' o 'Bond'.

    instr2: Puede ser de la clase 'Asset' o 'Bond'.

    weights: Son los pesos en los que se invierten en cada instrumentos financieros.
    El valor debe ser solo del instrumento 1 y debe estar en decimales (no en porcentaje).

    corr: correlación entre los instrumentos.
    """

    def __new__(cls, instr1, instr2, weigths, corr):
        if not isinstance(instr1, Asset):
            raise ValueError("Los instrumentos deben ser de clase 'Asset'.")
        elif not isinstance(instr2, Asset):
            raise ValueError("Los instrumentos deben ser de clase 'Asset'.")
        elif weigths < 0 or weigths > 1:
            raise ValueError("El peso del instrumento debe estar entre 0 y 1.")
        elif corr < -1 or corr > 1:
            raise ValueError("La correlación entre los instrumentos deben estar entre 0 y 1.")

        return object.__new__(cls)

    def __init__(self, instr1, instr2, weights, corr):
        self.instr1 = instr1
        self.instr2 = instr2
        self.w_1 = weights
        self.w_2 = 1-weights
        self.corr = corr

    def get_covariance(self):
        """Retorna la covarianza del portafolio"""
        cov = self.corr * self.instr1.desv * self.instr2.desv
        return cov

    def get_yield(self):
        """Retorna el rendimiento del portafolio"""
        rend = self.w_1 * self.instr1.rend + self.w_2 * self.instr2.rend
        return rend

    def get_variance(self):
        """Retorna la varianza del portafolio"""
        cov = self.get_covariance()
        desv1 = self.w_1**2 * self.instr1.desv**2
        desv2 = self.w_2**2 * self.instr2.desv**2
        desvcorr = 2 * self.w_1 * self.w_2 * cov
        variance = desv1 + desv2 + desvcorr
        return variance

    def get_std(self):
        """Retorna la desviación estándar del portafolio"""
        return np.sqrt(self.get_variance())

    def description(self):
        """Descripción básica del portafolio, en el que se muestra la covarianza, el rendimiento,
        la varianza, y su desviación estándar.
        """
        _char = [
            ["Covarianza", str(round(self.get_covariance(), 4))],
            ["Rendimiento", str(round(self.get_yield(), 4))],
            ["Varianza", str(round(self.get_variance(), 4))],
            ["Desviación estándar", str(round(self.get_std(), 4))]
        ]
        arr = np.array(_char).transpose()
        size_1 = max(list(map(len, arr[0])))
        size_2 = max(list(map(len, arr[1])))
        sizer = [size_1, size_2]
        description = ""
        for row in _char:
            for i, val in enumerate(row):
                if i == 0:
                    description += "{:19s}".format(val) + ": "
                else:
                    description += val.rjust(sizer[i], " ") + "\n"
        return description

    def show_yields(self, corr_list, show=True):
        """
        Grafica la curva de rendimiento del portafolio para distintos pesos según
        los rendimientos y la desviación estándar de las acciones.

        Keyword arguments:

        corr_list: Inserta una lista con las respectivas correlaciones entre los
        instrumentos financieros 1 y 2.

        show: Por defecto es 'True', pero si no se desea mostrar el gráfico, se iguala
        a 'False'.
        """
        fig, axs = plt.subplots()

        for corr in corr_list:
            wgt = np.linspace(0, 1, 200)
            rends = []
            desvs = []
            for _w in wgt:
                new_port = Portfolio(self.instr1, self.instr2, _w, corr)
                rend = new_port.get_yield()
                desv = new_port.get_std()
                rends.append(rend)
                desvs.append(desv)

            axs.plot(desvs, rends, label=f"corr: {corr}")
            axs.legend()
        if show:
            plt.show()

        return fig
